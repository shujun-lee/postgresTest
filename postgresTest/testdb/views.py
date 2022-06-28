from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from .models import CustomUser, Workout
from .serializers import CustomUserSerializer, WorkoutSerializers


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

#insert workout details
class WorkoutModelViewSet(ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializers
