from django.test import TestCase
from .models import *
from .serializers import *
# from .serializers import

import datetime
# Create your tests here.
class SerializerTestCase(TestCase):
    def setUp(self):
        self.user_attributes = {
            "username": "user1",
            "birth_year": 2000,
            "body_weight": "43.00",
            "preferred_unit": "kg",
            "barbell_weight": "0.00",
            "email": "hello1@gmail.com",
            "password": "123456789"
        }

        self.serializer_data = {

        }

        self.user = CustomUser.objects.create(**self.user_attributes)
        self.user_serializer = CustomUserSerializer(instance=self.user)

        user1 = CustomUser.objects.get(username='user1')
        self.workout_attributes = {
            'start': datetime.datetime(2022, 7, 1),
            'end': datetime.datetime.now(),
            'weights_lift': 0.00,
            'user': user1,
        }
        self.workout2_attributes = {
            'start': datetime.datetime(2022, 7, 1),
            'end': datetime.datetime(2022, 7, 14),
            'weights_lift': 10.00,
            'user': user1,
        }
        # self.workout = Workout.objects.create(**self.workout_attributes)
        self.serializer = WriteWorkoutSerializer(instance=self.workout_attributes)

    def test_user_contains_expected_fields(self):
        data = self.user_serializer.data
        self.assertEqual(set(data.keys()), set(['username', 'birth_year', 'body_weight', 'preferred_unit', 'barbell_weight', 'email', 'id', 'age']))

    def test_workout_contains_expected_fields(self):
        # self.workout = Workout.objects.create(**self.workout_attributes)
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["start", "end", "weights_lift" , "duration", "user"]))

    # def test_workout_updated_or_create(self):
    #     self.serializer = WriteWorkoutSerializer(instance=self.workout_attributes)
    #     self.serializer2 = WriteWorkoutSerializer(instance=self.workout2_attributes)
    #     data2 = self.serializer2.data
    #     records_count = Workout.objects.all().count()
    #     self.assertEqual(records_count,1)
