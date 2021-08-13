from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='actionimages', height_field=None,
        width_field=None, max_length=None, null=True)