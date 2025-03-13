from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserOption(models.Model):
    OPTIONS = [
        ('nintendo_switch', 'Nintendo Switch'),
        ('xbox', 'Xbox'),
        ('pc', 'PC'),
        ('playstation', 'Playstation'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    option = models.CharField(max_length=20, choices=OPTIONS)

    def __str__(self):
        return f"{self.user.username} - {self.option}"