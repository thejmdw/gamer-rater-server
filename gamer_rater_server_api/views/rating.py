"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gamer_rater_server_api.models import Rating, Game
from django.contrib.auth.models import User


class RatingView(ViewSet):
    """Level up games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        # gamer = Gamer.objects.get(user=request.auth.user)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        rating = Rating()
        rating.rating = request.data["rating"]

        rating.game = Game.objects.get(pk=request.data["gameId"])
        rating.user = request.auth.user
        # game.description = request.data["description"]
        # game.designer = request.data["designer"]
        # game.number_of_player = request.data["numberOfPlayers"]
        # game.release_year = request.data["releaseYear"]
        # game.game_duration = request.data["gameDuration"]
        # game.age_range = request.data["ageRange"]
        # game.categories = request.data["categories"]

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `gameTypeId` in the body of the request.
        # game_type = GameType.objects.get(pk=request.data["gameTypeId"])
        # game.game_type = game_type

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            rating.save()
            #  game.categories.set(request.data["categories"])
            #  game.categories.add(request.data["categories"])
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        # gamer = Gamer.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        rating = Rating()
        rating.rating = request.data["rating"]

        rating.game = Game.objects.get(pk=request.data["gameId"])
        rating.user = request.auth.user
        # game = Game.objects.get(pk=pk)
        # game.title = request.data["title"]
        # game.description = request.data["description"]
        # game.designer = request.data["designer"]
        # game.number_of_player = request.data["numberOfPlayers"]
        # game.release_year = request.data["releaseYear"]
        # game.game_duration = request.data["gameDuration"]
        # game.age_range = request.data["ageRange"]
        # game.categories = request.data["categories"]

        # game_type = GameType.objects.get(pk=request.data["gameTypeId"])
        # game.game_type = game_type
        rating.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            rating = Rating.objects.get(pk=pk)
            rating.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except rating.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from the database
        ratings = Rating.objects.all()

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        game = self.request.query_params.get('game', None)
        if game is not None:
            ratings = ratings.filter(game__id=game)

        serializer = RatingSerializer(
            ratings, many=True, context={'request': request})
        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username' )

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    class Meta:
        model = Game
        fields = ( 'title', )
        depth = 1

class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    user = UserSerializer(many=False)
    game = GameSerializer(many=False)

    class Meta:
        model = Rating
        fields = ( 'id', 'user', 'game', 'rating' )
        depth = 1