from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

#extend from standard Django User Model

class CustomUser(AbstractUser):
    KILOGRAM = 'kg'
    POUND = 'lbs'
    UNITS = [
        (KILOGRAM, 'kg'),
        (POUND, 'lb')
    ]

    fav_color = models.CharField(blank=True, max_length=120)
    birth_year = models.IntegerField(blank=True, default='1970')
    body_weight = models.DecimalField(blank=True, decimal_places=2, max_digits=4, default='0')
    preferred_unit = models.CharField(max_length=3, choices=UNITS, default = KILOGRAM)
    barbell_weight = models.DecimalField(blank=True, decimal_places=2, max_digits=4, default='0')

    def __str__(self) -> str:
        return self.username

class Workout(models.Model):
    start = models.DateTimeField(auto_now=False)
    end = models.DateTimeField(auto_now=False)
    weights_lifted = models.IntegerField(blank=True, default='0')
    duration = models.IntegerField(blank=True, default='0')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user} {self.start}"

class WorkExercise(models.Model):
    name = models.CharField(blank=True, max_length=256)
    workset_weight = models.IntegerField(blank=True, default='0')
    notes = models.TextField(blank=True, default='0')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.id} {self.name}"

class WorkExerciseDetails(models.Model):
    WORKSET = 'work_set'
    WARMUPSET = 'warmup_set'
    TYPE = [
        (WORKSET, 'work_set'),
        (WARMUPSET, 'warmup_set')
    ]
    rep = models.IntegerField(blank=True, default='0')
    weight = models.IntegerField(blank=True, default='0')
    type = models.CharField(max_length=11, choices=TYPE, default = None)
    w_exercise = models.ForeignKey(WorkExercise, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.id