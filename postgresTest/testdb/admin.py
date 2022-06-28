from django.contrib import admin
from .models import CustomUser, Workout, WorkExercise, WorkExerciseDetails

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser

class WorkoutAdmin(admin.ModelAdmin):
    model = Workout

class WorkExerciseAdmin(admin.ModelAdmin):
    model = WorkExercise

class WorkExerciseDetailsAdmin(admin.ModelAdmin):
    model = WorkExerciseDetails

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(WorkExercise, WorkExerciseAdmin)
admin.site.register(WorkExerciseDetails, WorkExerciseDetailsAdmin)
