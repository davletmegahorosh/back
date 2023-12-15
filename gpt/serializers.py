from rest_framework import serializers

from .models import Message

class Messages(serializers.Serializer):
    class Meta:
        fields = ['text']
        extra_kwargs = {
            "text" : {'write_only' :  True}
        }

class Chat(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'