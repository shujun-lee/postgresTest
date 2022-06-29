from rest_framework import serializers
from .models import CustomUser, Workout, WorkExercise, WorkExerciseDetails

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class WorkoutSerializers(serializers.ModelSerializer):
    #have a standalone serializer for CRUD?

    #accept username value in user field
    user = serializers.SlugRelatedField(slug_field="username", queryset=CustomUser.objects.all())
    class Meta:
        model = Workout
        fields = ( "id", "start", "end", "weights_lifted" , "duration", "user")

class WorkExerciseSerializers(serializers.ModelSerializer):
    workout = WorkoutSerializers()
    class Meta:
        model = WorkExercise
        fields = ("name", "workset_weight", "notes", "workout")

class WorkExerciseDetailsSerializers(serializers.ModelSerializer):
    w_exercise = WorkExerciseSerializers()
    class Meta:
        model = WorkExerciseDetails
        fields = ("rep", "weight", "type", "w_exercise")
