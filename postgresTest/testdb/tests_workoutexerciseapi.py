from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *
from .serializers import *
# from .serializers import

import datetime
# Create your tests here.

class WorkoutExerciseTestCase(APITestCase):
    def setUp(self):

        self.admin1 = CustomUser.objects.create(email = "test@gmail.com", username = "admin1", password = "12345678", birth_year = 1988, body_weight = 10.01, preferred_unit = 'lbs', barbell_weight = 10.10)
        first_time = datetime.datetime(2022, 7, 1)
        later_time = datetime.datetime.now()

        self.workout = Workout.objects.create(start = first_time , end = later_time, weights_lift = 0.00, user = CustomUser.objects.get(username = 'admin1'))


        self.workoutExercise = WorkExercise.objects.create(exercise_name = "Bench Row" , workset_weight = 40.0, notes = 'This is my note', workout = Workout.objects.latest('id'))
        self.workoutExerciseDetails = WorkExerciseDetails.objects.create(rep_complete = 5, weight = 30, set_type = "work_set", workout_exercise=WorkExercise.objects.latest('id'))

    def test_get_all_workout(self):
        #API Response
        url = '/api/workexercise/'
        response = self.client.get(url)
        #get data from db
        workExercise = WorkExercise.objects.all()
        workoutExerciseDetails = WorkExerciseDetails.objects.all()
        serializer = WorkExerciseSerializers(workExercise, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_new_workoutExercise(self):

        #API
        url = '/api/workexercise/'
        data = {
            "exercise_name": "Bench Row",
            "workset_weight": "40",
            "notes": "2",
            "workout_exercise_details": [
            {
                "rep_complete": 5,
                "weight":"30",
                "set_type":"work_set"
            },
            {
                "rep_complete": 5,
                "weight":"30",
                "set_type":"work_set"
            }
         ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkExercise.objects.count(), 2)
        self.assertEqual(WorkExerciseDetails.objects.count(), 3)

    def test_invalid_new_workout(self):
        #API
        url = '/api/workexercise/'
        data = {
            "exercise_name": "Bench Row",

            "notes": "2",
            "workout_exercise_details": [
            {
                "rep_complete": 5,
                "weight":"30",
                "set_type":"work_set"
            },
            {
                "rep_complete": 5,
                "weight":"30",
                "set_type":"work_set"
            }
         ]
        }
        data2 = {"exercise_name":"Bench Press","workset_weight":"50.0","workout_exercise_details":[{"rep_complete":5,"weight":50,"set_type":"work_set"},{"rep_complete":5,"weight":50,"set_type":"work_set"},{"rep_complete":5,"weight":50,"set_type":"work_set"},{"rep_complete":5,"weight":50,"set_type":"work_set"},{"rep_complete":5,"weight":50,"set_type":"work_set"}]}
        response = self.client.post(url, data2, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkExerciseDetails.objects.count(), 6)

    # def test_new_workout_same_start_time(self):
    #     #API
    #     url = '/api/workout/'
    #     data = {
    #         'start': datetime.datetime(2022, 7, 20),
    #         'end': datetime.datetime(2022, 7, 21),
    #         'weights_lift': 0.00,
    #         'user': 'admin1',
    #     }
    #     data2 = {
    #         'start': datetime.datetime(2022, 7, 20),
    #         'end': datetime.datetime.now(),
    #         'weights_lift': 0.00,
    #         'user': 'admin1',
    #     }
    #     response = self.client.post(url, data, format='json')
    #     response2 = self.client.post(url, data2, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    #     self.assertEqual(Workout.objects.count(), 2)
