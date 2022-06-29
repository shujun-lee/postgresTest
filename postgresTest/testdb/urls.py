from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from .views import CustomUserCreate, HelloWorldView, UserListAPIView, WorkoutViewSet, WorkExerciseViewSet, WorkExerciseDetailsViewSet

router = routers.SimpleRouter()
router.register(r'workout', WorkoutViewSet, basename="workout")
router.register(r'workexercise', WorkExerciseViewSet, basename="workout_exercise")
router.register(r'workexercisedetails', WorkExerciseDetailsViewSet, basename="workout_exercise_details")

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', CustomUserCreate.as_view(), name="create_user"),
    path('user/list/', UserListAPIView.as_view(), name="create_user"),

    # path('workout/', WorkoutModelViewSet.as_view(), name="workout"),

    #test protected route
    path('hello/', HelloWorldView.as_view(), name='hello_world')


] + router.urls
