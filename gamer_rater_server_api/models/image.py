from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField()