import json
from rest_framework import status
from rest_framework.test import APITestCase
from gamer_rater_server_api.models import Game
from gamer_rater_server_api.models import Category


class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
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
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /Categorys
        # endpoint for creating game types
        category = Category()
        category.label = "Board game"
        category.save()


    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "categories": [1],
            "releaseYear": 1995,
            "gameDuration": 60,
            "ageRange": 60,
            "description": 'some generic description',
            "title": "Clue",
            "designer": "Milton Bradley",
            "numberOfPlayers": 6, 
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], "Clue")
        self.assertEqual(json_response["designer"], "Milton Bradley")
        self.assertEqual(json_response["game_duration"], 60)
        self.assertEqual(json_response["age_range"], 60)
        self.assertEqual(json_response["description"], 'some generic description')
        self.assertEqual(json_response["release_year"], 1995)
        self.assertEqual(json_response["number_of_player"], 6)
        self.assertEqual(json_response["categories"], [{'id': 1, 'label': 'Board game'}])
        # self.assertEqual(json_response["user_id"], self.token.user_id)

    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        game = Game()
        game.release_year = 1995
        game.game_duration = 60
        game.description = 'some generic description'
        game.age_range = 60
        game.title = "Monopoly"
        game.designer = "Milton Bradley"
        game.number_of_player = 6
        game.user_id = 1

        game.save()
        game.categories.set([1])

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/games/{game.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        # self.assertEqual(json_response["user"], 1)
        self.assertEqual(json_response["title"], "Monopoly")
        self.assertEqual(json_response["designer"], "Milton Bradley")
        self.assertEqual(json_response["game_duration"], 60)
        self.assertEqual(json_response["age_range"], 60)
        self.assertEqual(json_response["description"], 'some generic description')
        self.assertEqual(json_response["release_year"], 1995)
        self.assertEqual(json_response["number_of_player"], 6)
        self.assertEqual(json_response["categories"], [{'id': 1, 'label': 'Board game'}])

    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """
        game = Game()
        game.release_year = 1995
        game.game_duration = 60
        game.description = 'some generic description'
        game.age_range = 60
        game.title = "Monopoly"
        game.designer = "Milton Bradley"
        game.number_of_player = 6
        game.user_id = 1
        game.save()
        game.categories.set([1])

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "id": 1,
            "categories": [1],
            "releaseYear": 1990,
            "gameDuration": 60,
            "ageRange": 60,
            "description": 'some generic Monopoly description',
            "title": "Monopoly",
            "designer": "Milton Bradley",
            "numberOfPlayers": 6, 
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["title"], "Monopoly")
        self.assertEqual(json_response["designer"], "Milton Bradley")
        self.assertEqual(json_response["game_duration"], 60)
        self.assertEqual(json_response["age_range"], 60)
        self.assertEqual(json_response["description"], 'some generic Monopoly description')
        self.assertEqual(json_response["release_year"], 1990)
        self.assertEqual(json_response["number_of_player"], 6)
        self.assertEqual(json_response["categories"], [{'id': 1, 'label': 'Board game'}])

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.release_year = 1995
        game.game_duration = 60
        game.description = 'some generic description'
        game.age_range = 60
        game.title = "Monopoly"
        game.designer = "Milton Bradley"
        game.number_of_player = 6
        game.user_id = 1
        game.save()
        game.categories.set([1])

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_games(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        game = Game()
        game.release_year = 1995
        game.game_duration = 60
        game.description = 'some generic description'
        game.age_range = 60
        game.title = "Monopoly"
        game.designer = "Milton Bradley"
        game.number_of_player = 6
        game.user_id = 1

        game.save()
        game.categories.set([1])

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

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/games")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)
