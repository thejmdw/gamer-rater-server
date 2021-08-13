from django.db import models
from django.contrib.auth.models import User
from .rating import Rating

class Game(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    designer = models.CharField(max_length=50)
    release_year = models.IntegerField()
    number_of_player = models.IntegerField()
    game_duration = models.IntegerField()
    age_range = models.IntegerField()
    categories = models.ManyToManyField("Category", through="GameCategory", related_name="Category")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def user(self):
        return self.id

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = Rating.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating
        
        return total_rating / len(ratings)

        # Calculate the averge and return it.
        # If you don't know how to calculate averge, Google it.
    @average_rating.setter
    def average_rating(self, value):
        self.__average_rating = value