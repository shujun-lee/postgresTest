from email import message_from_string
from rest_framework import serializers
from .models import CustomUser, Workout, WorkExercise, WorkExerciseDetails
from datetime import date
from rest_framework.validators import UniqueValidator

#do i need to store gender?
class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all(), message='A user with that email address already exists.')
            ],
    )
    username = serializers.CharField(
         validators=[
            UniqueValidator(queryset=CustomUser.objects.all(), message='A user with this username already exists.')
            ],
    )
    password = serializers.CharField(min_length=8, write_only=True)
    age = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'password', 'birth_year', 'body_weight', 'preferred_unit', 'barbell_weight', 'age')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def get_age(self, obj):
        delta = int(date.today().year) - obj.birth_year
        return int(delta)


class WorkExerciseDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = WorkExerciseDetails
        fields = ("rep_complete", "weight", "set_type")

class WorkExerciseSerializers(serializers.ModelSerializer):
    workout_exercise_details = WorkExerciseDetailsSerializers(many=True, read_only=True)

    class Meta:
        model = WorkExercise
        fields = ("exercise_name", "workset_weight", "notes", "workout", "workout_exercise_details")

class WorkoutSerializers(serializers.ModelSerializer):
    #have a standalone serializer for CRUD?

    #calculate workout duration
    # user = CustomUserSerializer()
    duration = serializers.SerializerMethodField()
    #accept username value in user field
    user = serializers.SlugRelatedField(slug_field="username", queryset=CustomUser.objects.all())
    workout_exercises = WorkExerciseSerializers(many=True, read_only=True)
    workout_exercise_details = WorkExerciseDetailsSerializers(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = ( "id", "start", "end", "weights_lift" , "duration", "user", 'workout_exercises', 'workout_exercise_details' )
        extra_kwargs = {'workout_exercises': {'read_only': True}}

    def get_duration(self, obj):
        print('obj printout from work seralizer' + str(self))
        return None

#create need password, update no need password [different fields same methods]
class UserUpdateSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    username = serializers.CharField(
        required=False,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all(), message='A user with this username already exists.')
            ],)
    workouts = WorkoutSerializers(many=True, read_only=True)
 
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'birth_year', 'body_weight', 'preferred_unit', 'barbell_weight', 'age', 'workouts')
        extra_kwargs = {'workouts': {'read_only': True}}

    def get_age(self, obj):
        delta = int(date.today().year) - obj.birth_year
        return int(delta)

class WriteWorkoutSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    class Meta:
        model = Workout
        fields = ( "id", "start", "end", "weights_lift" , "duration", "user", 'workout_exercises', 'workout_exercise_details' )
        extra_kwargs = {'workout_exercises': {'read_only': True}}

    def get_duration (self, obj):
        print('obj printout ' + str(self.rep_complete))
