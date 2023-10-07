from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(max_length=500, blank=True)
    profile_img = models.ImageField(upload_to='profile_imges', blank=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username