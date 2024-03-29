from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from .views import CustomUserCreate, HelloWorldView, UserListAPIView, UserProfileUpdateAPIView, WorkoutViewSet, WorkExerciseViewSet, WorkExerciseDetailsViewSet, CustomTokenObtainPairView

router = routers.SimpleRouter()
# router.register(r'user', UserProfileViewSet, basename="user")
router.register(r'workout', WorkoutViewSet, basename="workout")
router.register(r'workexercise', WorkExerciseViewSet, basename="workout_exercise")
router.register(r'workexercisedetails', WorkExerciseDetailsViewSet, basename="workout_exercise_details")

urlpatterns = [
    path('token/obtain/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

    path('user/create/', CustomUserCreate.as_view(), name="create_user"),
    # path('user/exercise/', UserListAPIView.as_view(), name="user_exercise"),
    path('user/profile/' , UserListAPIView.as_view(), name="users"),
    path('user/profile/<int:pk>', UserProfileUpdateAPIView.as_view(), name="user_profile"),
    # path('workout/user/latest', )


    # path('workout/', WorkoutModelViewSet.as_view(), name="workout"),

    #test protected route
    path('hello/', HelloWorldView.as_view(), name='hello_world')


] + router.urls
