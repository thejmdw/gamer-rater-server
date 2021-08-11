from django.contrib import admin
from gamer_rater_server_api.models import Category, Game, Review, Rating

# Register your models here.
admin.site.register(Category)
admin.site.register(Game)
admin.site.register(Review)
admin.site.register(Rating)