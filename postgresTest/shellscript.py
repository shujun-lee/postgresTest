from testdb.models import *
from testdb.serializers import *

#does not store data to database
from unittest.mock import Mock

#create a mock user instance didnt work
user = Mock(email = "test@gmail.com", username = "admin", password = "12345678")

#create a customUser model instance
user = CustomUser(email = "test@gmail.com", username = "admin", password = "12345678")

user2 = CustomUser(email = "test@gmail.com", username = "admin2", password = "12345678", birth_year = "1988", body_weight = 10.01, preferred_unit = 'lbs', barbell_weight = 10.10)

user3 = CustomUser(email = "test@gmail.com", username = "admin2", password = "12345678", birth_year = "1988", body_weight = 10.01, preferred_unit = 'lbs', barbell_weight = 10.10)

#pass user instance into user serializer (validate fiels?)
serializer = CustomUserSerializer(instance=user2)
serializer3 = CustomUserSerializer(instance=user3)

#return what is being serialize.
serializer.data
serializer3.data

details = WorkExerciseDetails.objects.filter(workout_exercise='2')

total_exercise = []
for d in WorkExerciseDetails.objects.filter(workout_exercise='2'):
    total = d.rep_complete * d.weight
    total_exercise.append(int(total))
    print(total_exercise)

def sum_list(l):
    sum = 0
    for x in l:
        sum += x
    return sum
sum(total_exercise)
