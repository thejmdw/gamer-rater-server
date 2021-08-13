from django.db import models
from django.contrib.auth.models import User

class Rating(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()