from .serializers import ChatRecordSerializer, Messages
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from catalog.models import Medicine
from .models import ChatRecord
from django.conf import settings
from openai import OpenAI
from gtts import gTTS
import os, uuid



client = OpenAI(api_key='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')

def save_audio_file(text, file_name):
    audio_directory = os.path.join(settings.MEDIA_ROOT, 'audio')

    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)

    audio_file_path = os.path.join(audio_directory, file_name)

    tts = gTTS(text, lang='ru')
    tts.save(audio_file_path)

    return audio_file_path

class GPTResponseApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Messages

    def get(self, request, *args, **kwargs):
        chat_records = ChatRecord.objects.filter(user=request.user)
        chat_records_serializer = ChatRecordSerializer(chat_records, many=True)
        return Response(chat_records_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = Messages(data=request.data)

        if serializer.is_valid():
            input_text = serializer.validated_data['message']

            medicines = Medicine.objects.all()

            suggestions = f"Возможные условия: {input_text}\n"
            suggestions += f"Лекарства из запроса:\n"

            suggestions += "\n".join([f"{med.name}: {med.recept}, {med.usage}" for med in medicines])

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Ваш личный врач готов дать вам советы о здоровье. Укажите ваши симптомы,"
                                   " и врач расскажет, какие лекарства из нашего ассортимента могут вам помочь."
                                   "советуй только те лекарства которые могут помочь с теми симптомами котрые есть у пользователя"
                    },
                    {
                        "role": "user",
                        "content": f"{input_text}\n{suggestions}"
                    }
                ],
                temperature=1,
                max_tokens=1000
            )

            file_name = f'{uuid.uuid4()}.mp3'
            audio_file_path = save_audio_file(response.choices[0].message.content, file_name)

            audio_url = os.path.join(settings.MEDIA_URL, 'audio', file_name)

            chat_record = ChatRecord.objects.create(
                user=request.user,
                input_message=input_text,
                gpt3_response=response.choices[0].message.content,
                audio_url=audio_url
            )

            chat_record_serializer = ChatRecordSerializer(chat_record)

            response_data = {
                'message': response.choices[0].message.content,
                'audio_url': audio_url,
                'chat_record': chat_record_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
