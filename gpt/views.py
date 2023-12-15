from django.http import HttpResponse
from openai import OpenAI
import requests
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import Messages, Chat
from .models import Message
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from decouple import config
from catalog.models import Medicine

key = config('KEY')

client = OpenAI(
    api_key=key
)
from catalog.serializers import MedicineSerializer

class Respone(APIView):
    serializer_class = Messages
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            input_text = serializer.validated_data['text']

            # Serialize the Medicine objects to JSON
            medicines_data = MedicineSerializer(Medicine.objects.all(), many=True).data

            chat_completion = client.chat.completions.create(
                model='gpt-3.5-turbo-1106',
                messages=[
                    {
                        'medicines': medicines_data,
                        'role': 'system',
                        'content': "what kind of disease it could be depending on the symptoms that the user entered and recommend medications from medicines",
                    },
                    {
                        'role': 'user',
                        'content': input_text,
                    },
                ],
                temperature=1,
                max_tokens=1000
            )

            response_data = {'text': chat_completion.choices[0].message.content}

            response_message = Message(user=request.user, text=response_data['text'])
            response_message.save()

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
