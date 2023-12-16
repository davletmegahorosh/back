from django.db import models
from django.contrib.auth.models import User

class ChatRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_message = models.TextField()
    gpt3_response = models.TextField()
    audio_url = models.URLField()

    def __str__(self):
        return f"{self.user.username} - {self.input_message}"
