from django.contrib.auth.models import AbstractUser
from django.db import models

#extend from standard Django User Model

class CustomUser(AbstractUser):
    KILOGRAM = 'kg'
    POUND = 'lbs'
    UNIT_CHOICES = (
        (KILOGRAM, 'kg'),
        (POUND, 'lb')
    )

    MALE = 'M'
    FEMALE = 'F'
    NON_BINARY = 'NB'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NON_BINARY, 'Non Binary')
    )

    birth_year = models.IntegerField(blank=True, default=1970)
    body_weight = models.DecimalField(blank=True, decimal_places=2, max_digits=5, default='45.00')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default = MALE, blank=True)
    preferred_unit = models.CharField(max_length=3, choices=UNIT_CHOICES, default = KILOGRAM)
    barbell_weight = models.DecimalField(blank=True, decimal_places=2, max_digits=5, default='20.00')

    def __str__(self) -> str:
        return self.username

class Workout(models.Model):
    start = models.DateTimeField(auto_now=False)
    end = models.DateTimeField(auto_now=False)
    weights_lift = models.DecimalField(blank=True, decimal_places=2, max_digits=7)
    duration = models.IntegerField(blank=True, default='0')
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='workouts',
        related_query_name='weights_lift'
    )

    #duration a calculated field base on end - start? Model Method?
    #total weights_lifted

class WorkExercise(models.Model):
    #include list of exercise here?
    BENCH_PRESS = 'Bench Press'
    SQUAT = 'Squat'
    DEADLIFT = 'Deadlift'
    BENCH_ROW = 'Bench Row'
    EXERCISE_CHOICES = (
        (BENCH_PRESS, 'Bench Press'),
        (SQUAT, 'Squat'),
        (DEADLIFT, 'Deadlift'),
        (BENCH_ROW, 'Bench Row')
    )

    exercise_name = models.CharField('name', choices=EXERCISE_CHOICES, max_length=11)
    workset_weight = models.DecimalField(blank=True, decimal_places=2, max_digits=7)
    notes = models.TextField(blank=True)
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name='workout_exercises',
        related_query_name='exercise_name'
    )


class WorkExerciseImage(models.Model):
    image = models.ImageField(upload_to='workout_exercise')
    workout_exercise = models.ForeignKey(
        WorkExercise,
        on_delete=models.CASCADE,
        related_name='workout_exercise_images'
    )

#Model name should be singular
class WorkExerciseDetails(models.Model):
    WORKSET = 'work_set'
    WARMUPSET = 'warmup_set'
    TYPE_CHOICES = (
        (WORKSET, 'work set'),
        (WARMUPSET, 'warmup set')
    )

    rep_complete = models.IntegerField('rep', blank=True)
    weight = models.DecimalField(blank=True, decimal_places=2, max_digits=5)
    set_type = models.CharField('type', max_length=11, choices=TYPE_CHOICES, default = 'warmup_set')
    workout_exercise = models.ForeignKey(
        WorkExercise,
        on_delete=models.CASCADE,
        related_name='workout_exercise_details')
