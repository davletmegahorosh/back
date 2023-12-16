from rest_framework import serializers
from .models import ChatRecord

class Messages(serializers.Serializer):
    message = serializers.CharField(write_only=True)


class ChatRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRecord
        fields = ('user', 'input_message', 'gpt3_response', 'audio_url')
