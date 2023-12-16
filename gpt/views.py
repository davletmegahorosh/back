# views.py

import os
import uuid
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ChatRecord  # Import ChatRecord model
from .serializers import ChatRecordSerializer
from .serializers import Messages
from openai import OpenAI
from gtts import gTTS

client = OpenAI(api_key='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')

def save_audio_file(text, file_name):
    audio_directory = os.path.join(settings.MEDIA_ROOT, 'audio')

    # Check if the directory exists, and create it if it doesn't
    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)

    audio_file_path = os.path.join(audio_directory, file_name)

    # Create audio from text and save it
    tts = gTTS(text, lang='ru')
    tts.save(audio_file_path)

    return audio_file_path

class GPTResponseApiView(APIView):
    serializer_class = Messages

    def post(self, request, *args, **kwargs):
        serializer = Messages(data=request.data)

        if serializer.is_valid():
            input_text = serializer.validated_data['message']
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Summarize content you are provided with for a second-grade student."
                    },
                    {
                        "role": "user",
                        "content": input_text
                    }
                ],
                temperature=1,
                max_tokens=1000
            )

            # Generate a unique file name
            file_name = f'{uuid.uuid4()}.mp3'
            audio_file_path = save_audio_file(response.choices[0].message.content, file_name)

            # Form the URL to access the audio
            audio_url = os.path.join(settings.MEDIA_URL, 'audio', file_name)

            # Save user input, GPT-3 response, and audio URL to the database
            chat_record = ChatRecord.objects.create(
                user=request.user,  # Assuming the user is authenticated
                input_message=input_text,
                gpt3_response=response.choices[0].message.content,
                audio_url=audio_url
            )

            # Serialize the chat record for response
            chat_record_serializer = ChatRecordSerializer(chat_record)

            response_data = {
                'message': response.choices[0].message.content,
                'audio_url': audio_url,
                'chat_record': chat_record_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
