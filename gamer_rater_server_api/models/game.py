from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    designer = models.CharField(max_length=50)
    release_year = models.IntegerField()
    number_of_player = models.IntegerField()
    game_duration = models.IntegerField()
    age_range = models.IntegerField()
    categories = models.ManyToManyField("Category", through="GameCategory", related_name="Category")


    def __str__(self):
        return self.title