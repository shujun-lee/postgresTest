from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CustomUser, Workout, WorkExercise, WorkExerciseDetails
import datetime
class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse("create_user")
        data = {
            "username": "user1",
            "birth_year": 2000,
            "body_weight": "43.00",
            "preferred_unit": "kg",
            "barbell_weight": "0.00",
            "email": "hello1@gmail.com",
            "password": "123456789"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, "user1")

    def test_create_workout_same_datetime(self):
        """
        Ensure we can create a new workout object.
        """
        url_user = reverse("create_user")
        data_user = {
            "username": "user1",
            "birth_year": 2000,
            "body_weight": "43.00",
            "preferred_unit": "kg",
            "barbell_weight": "0.00",
            "email": "hello1@gmail.com",
            "password": "123456789"
        }
        response_user = self.client.post(url_user, data_user, format='json')

        url = "/api/workout/"
        data = {
            'start': datetime.datetime(2022, 7, 1),
            'end': datetime.datetime.now(),
            'weights_lift': 0.00,
            'user': 'user1',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 1)
        self.assertEqual(Workout.objects.get().weights_lift, 0.00)

        data2 = {
            'start': datetime.datetime(2022, 7, 1),
            'end': datetime.datetime(2022, 7, 14),
            'weights_lift': 10.00,
            'user': 'user1',
        }
        response2 = self.client.post(url, data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 1)
