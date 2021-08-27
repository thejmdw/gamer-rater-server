"""View module for handling requests about park areas"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
# from levelupapi.models import Event, Gamer, Game


class ProfileView(ViewSet):
    """Gamer can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info and events
        """
        user = request.auth.user
        # gamer = Gamer.objects.get(user=request.auth.user)
        # events = Event.objects.filter(attendees=gamer)

        # events = EventSerializer(
        #     events, many=True, context={'request': request})
        # gamer = GamerSerializer(
        #     gamer, many=False, context={'request': request})
        user = UserSerializer(user, many=False, context={'request': request})
        # Manually construct the JSON structure you want in the response
        profile = {}
        profile["user"] = user.data
        # profile["events"] = events.data

        return Response(profile)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('id',)