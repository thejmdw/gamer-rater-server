from gamer_rater_server_api.models import category
from django.db import models
from django.db.models.deletion import CASCADE

class GameCategory(models.Model):
    game = models.ForeignKey("Game", on_delete=CASCADE)
    category = models.ForeignKey("Category", on_delete=CASCADE)