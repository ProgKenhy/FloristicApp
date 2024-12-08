from django.db import models
from users.models import User


class ChatSupportSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session for {self.user}"


class ChatSupportMessage(models.Model):
    session = models.ForeignKey(ChatSupportSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=30)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"
