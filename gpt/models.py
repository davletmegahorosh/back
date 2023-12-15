from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.TextField()
    response = models.TextField()


    def __str__ (self):
        return f"response for {self.user.username}"

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'чат'
        ordering = ['user']