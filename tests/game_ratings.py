import json
from rest_framework import status
from rest_framework.test import APITestCase
from gamer_rater_server_api.models import Game, Rating, Category


class RatingTests(APITestCase):
    def setUp(self):
        """
        Create a new account
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        game = Game()
        game.release_year = 1995
        game.game_duration = 60
        game.description = 'some generic description'
        game.age_range = 60
        game.title = "Clue"
        game.designer = "Milton Bradley"
        game.number_of_player = 6
        game.user_id = 1

        game.save()
        game.categories.set([1])

        category = Category()
        category.label = "Board game"
        category.save()


    def test_create_rating(self):
        """
        Ensure we can create a new game rating.
        """
        url = "/ratings"
        data = {
            "gameId": 1,
            "rating": 10,
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["game"], {'title': 'Clue'})
        self.assertEqual(json_response["rating"], 10)

    def test_change_rating(self):
        """
        Ensure we can change an existing game.
        """
        # game = Game()
        # game.release_year = 1995
        # game.game_duration = 60
        # game.description = 'some generic description'
        # game.age_range = 60
        # game.title = "Clue"
        # game.designer = "Milton Bradley"
        # game.number_of_player = 6
        # game.user_id = 1
        # game.save()
        # game.categories.set([1])

        
        

        rating = Rating()
        # rating.game =  Game.objects.get(pk=data["gameId"])
        rating.game_id = 1
        rating.user_id = 1
        rating.rating = 10
        # rating.id = 1
        rating.save()
        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "id": 1,
            "gameId": 1,
            "rating": 1,
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/ratings/{rating.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/ratings/{rating.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["game"], {'title': 'Clue'})
        self.assertEqual(json_response["rating"], 1)
