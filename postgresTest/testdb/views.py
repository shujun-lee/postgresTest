from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import CustomUser, Workout, WorkExercise, WorkExerciseDetails
from .serializers import CustomUserSerializer, UserUpdateSerializer, ReadWorkoutSerializers, WorkExerciseSerializers, WorkExerciseDetailsSerializers, WriteWorkoutSerializer

# Viewset vs
# Generic Views (ListCreateAPIView, RetrieveUpdateDestroyAPIView) model related vs
# APIView - similar to regular View
# x Function based views.x
class CustomUserCreate(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#test protected route
class HelloWorldView(APIView):

    def get(self, request):
        return Response(data={"hello":"world"}, status=status.HTTP_200_OK)

#list user route
class UserListAPIView(ListAPIView):

    permission_classes = (permissions.AllowAny,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UserProfileUpdateAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = (permissions.AllowAny,)
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer

# class WorkoutLatest(APIView):
#     permission_classes = (permissions.AllowAny,)
#
#     def get(self, request):
#

#Workout model
class WorkoutViewSet(ModelViewSet):

    permission_classes = (permissions.AllowAny,)

    queryset = Workout.objects.all()

    #possible to use different Serializer for Read and Write
    # serializer_class = WorkoutSerializers

    # def get_queryset(self):
    #  return Workout.objects.select_related("workout_exercises", "workout_exercise_details", "user").filter(user=1)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadWorkoutSerializers
        return WriteWorkoutSerializer

    # def perform_create(self, serializer):
    #     return serializer.save(owner = self.request.user)


#Workout Exercise model
class WorkExerciseViewSet(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = WorkExercise.objects.all()
    serializer_class = WorkExerciseSerializers

    def perform_create(self, serializer):
        print('in perform_create')
        serializer.save(workout=Workout.objects.latest('id'))

class WorkExerciseDetailsViewSet(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = WorkExerciseDetails.objects.all()
    serializer_class = WorkExerciseDetailsSerializers
