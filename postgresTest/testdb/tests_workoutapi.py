from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *
from .serializers import *
# from .serializers import

import datetime
# Create your tests here.

class WorkoutTestCase(APITestCase):
    def setUp(self):

        self.valid_user = {
            'username': "admin1",
            'birth_year': 1988,
            'email': "efg@gmail.com",
            'password': "1234567890",
            'body_weight' : 10.01,
            'preferred_unit' : 'lbs',
            'barbell_weight': 10.10,
        }
        url = reverse('create_user')
        response = self.client.post(url, self.valid_user, format='json')

        first_time = datetime.datetime(2022, 7, 1)
        later_time = datetime.datetime.now()

        self.workout = Workout.objects.create(start = first_time , end = later_time, weights_lift = 0.00, user = CustomUser.objects.get(username = 'admin1'))

    def test_get_all_workout(self):
        #API Response
        url = '/api/workout/'
        response = self.client.get(url)
        #get data from db
        workout = Workout.objects.all()
        serializer = ReadWorkoutSerializers(workout, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_new_workout(self):

        #API
        url = '/api/workout/'
        data = {
            'start': datetime.datetime(2022, 7, 20),
            'end': datetime.datetime(2022, 7, 21),
            'weights_lift': 0.00,
            'user': 'admin1',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 2)

    def test_invalid_new_workout(self):
        #API
        url = '/api/workout/'
        data = {
            'start': datetime.datetime(2022, 7, 20),
            'end': datetime.datetime(2022, 7, 21),
            'weights_lift': 0.00,
            'user': 'user1',
        }
        response = self.client.post(url, data, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 1)

    def test_new_workout_same_start_time(self):
        #API
        url = '/api/workout/'
        data = {
            'start': datetime.datetime(2022, 7, 20),
            'end': datetime.datetime(2022, 7, 21),
            'weights_lift': 0.00,
            'user': 'admin1',
        }
        data2 = {
            'start': datetime.datetime(2022, 7, 20),
            'end': datetime.datetime.now(),
            'weights_lift': 0.00,
            'user': 'admin1',
        }
        response = self.client.post(url, data, format='json')
        response2 = self.client.post(url, data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Workout.objects.count(), 2)
