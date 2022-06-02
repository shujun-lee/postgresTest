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



class Teacher(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()
