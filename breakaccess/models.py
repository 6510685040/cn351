from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username} Profile'
