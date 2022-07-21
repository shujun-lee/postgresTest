from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *
from .serializers import *
# from .serializers import

import datetime
# Create your tests here.

class GetUserTestCase(APITestCase):
    def setUp(self):
        
        self.admin = CustomUser.objects.create(email = "test@gmail.com", username = "admin", password = "12345678")
        self.user2 = CustomUser.objects.create(email = "test@gmail.com", username = "user2", password = "12345678", birth_year = 1988, body_weight = 10.01, preferred_unit = 'lbs', barbell_weight = 10.10)
        self.user3 = CustomUser.objects.create(email = "test@gmail.com", username = "user3", password = "12345678", birth_year = 1988, body_weight = 10.01, preferred_unit = 'lbs', barbell_weight = 10.10)
        self.user4 = CustomUser.objects.create(email = "test@gmail.com", username = "user4", password = "12345678", birth_year = 1988, body_weight = 10.01, preferred_unit = 'lbs', barbell_weight = 10.10)

        self.valid_user = {
            'username': "admin1", 
            'birth_year': 1988,
            'email': "efg@gmail.com", 
            'password': "1234567890", 
            'body_weight' : 10.01,
            'preferred_unit' : 'lbs', 
            'barbell_weight': 10.10,
        }
        self.invalid_user = {
            'username': "admin1", 
            'password': "1234567890", 
            'body_weight' : 10.01,
            'preferred_unit' : 'lbs', 
            'barbell_weight': 10.10,
        }
    def test_get_all_user(self):
        #API Response
        url = reverse('users')
        response = self.client.get(url)
        #get data from db
        user_profile = CustomUser.objects.all()
        serializer = CustomUserSerializer(user_profile, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_valid_single_user(self):
        #API Response
        id = {'pk':self.admin.pk}
        url = reverse('user_profile', kwargs=id)
        
        response = self.client.get(url)
        #get data from db
        user = CustomUser.objects.get(pk=self.admin.pk)
        serializer = CustomUserSerializer(user)
        # print(response.data)
        print(serializer.data)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_invalid_single_user(self):
        id = {'pk':30}
        url = reverse('user_profile', kwargs=id)

        response = self.client.get(url)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
    
    def test_post_valid_user(self):
        url = reverse('create_user')


        response = self.client.post(url, self.valid_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 5)
    
    def test_post_invalid_user(self):
        url = reverse('create_user')

        response = self.client.post(url, self.invalid_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        #API Response
        id = {'pk':self.admin.pk}
        url = reverse('user_profile', kwargs=id)
        
        self.update_data = {
            'username': 'admin100'
        }
        response = self.client.put(url, self.update_data, content_type='application/json')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

        #get data from db

    #     self.user_attributes = {
    #         "username": "user1",
    #         "birth_year": 2000,
    #         "body_weight": "43.00",
    #         "preferred_unit": "kg",
    #         "barbell_weight": "0.00",
    #         "email": "hello1@gmail.com",
    #         "password": "123456789"
    #     }

    #     self.user = CustomUser.objects.create(**self.user_attributes)
    #     self.user_serializer = CustomUserSerializer(instance=self.user)

    #     user1 = CustomUser.objects.get(username='user1')
    #     self.workout_attributes = {
    #         'start': datetime.datetime(2022, 7, 1),
    #         'end': datetime.datetime.now(),
    #         'weights_lift': 0.00,
    #         'user': user1,
    #     }
    #     self.workout2_attributes = {
    #         'start': datetime.datetime(2022, 7, 1),
    #         'end': datetime.datetime(2022, 7, 14),
    #         'weights_lift': 10.00,
    #         'user': user1,
    #     }
    #     # self.workout = Workout.objects.create(**self.workout_attributes)
    #     self.serializer = WriteWorkoutSerializer(instance=self.workout_attributes)

    # def test_user_contains_expected_fields(self):
    #     data = self.user_serializer.data
    #     self.assertEqual(set(data.keys()), set(['username', 'birth_year', 'body_weight', 'preferred_unit', 'barbell_weight', 'email', 'id', 'age']))

    # def test_workout_contains_expected_fields(self):
    #     # self.workout = Workout.objects.create(**self.workout_attributes)
    #     data = self.serializer.data
    #     self.assertEqual(set(data.keys()), set(["start", "end", "weights_lift" , "duration", "user"]))

    # def test_workout_updated_or_create(self):
    #     self.serializer = WriteWorkoutSerializer(instance=self.workout_attributes)
    #     self.serializer2 = WriteWorkoutSerializer(instance=self.workout2_attributes)
    #     data2 = self.serializer2.data
    #     records_count = Workout.objects.all().count()
    #     self.assertEqual(records_count,1)
