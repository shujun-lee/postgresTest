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
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)

    age = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'birth_year', 'body_weight', 'preferred_unit', 'barbell_weight', 'age')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def validate_username(self, value):
        if CustomUser.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def get_age(self, obj):
        delta = int(date.today().year) - obj.birth_year
        return int(delta)

class WorkoutSerializers(serializers.ModelSerializer):
    #have a standalone serializer for CRUD?

    #calculate workout duration

    #accept username value in user field
    user = serializers.SlugRelatedField(slug_field="username", queryset=CustomUser.objects.all())
    class Meta:
        model = Workout
        fields = ( "id", "start", "end", "weights_lift" , "duration", "user")

class WorkExerciseSerializers(serializers.ModelSerializer):
    workout = WorkoutSerializers()
    class Meta:
        model = WorkExercise
        fields = ("exercise_name", "workset_weight", "notes", "workout")

class WorkExerciseDetailsSerializers(serializers.ModelSerializer):
    w_exercise = WorkExerciseSerializers()
    class Meta:
        model = WorkExerciseDetails
        fields = ("rep", "weight", "type", "w_exercise")
