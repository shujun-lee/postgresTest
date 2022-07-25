from email import message_from_string
from wsgiref import validate
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

#create no need to reference to workout exercise, but edit need - workout_exercise?
class WorkExerciseDetailsSerializers(serializers.ModelSerializer):
    total_rep_weight = serializers.SerializerMethodField()

    class Meta:
        model = WorkExerciseDetails
        fields = ("rep_complete", "weight", "set_type", "id", "total_rep_weight")

    def get_total_rep_weight(self, obj):
        total = obj.rep_complete * obj.weight
        return total

#create no need to reference to workout, but edit need - workout?

class WorkExerciseSerializers(serializers.ModelSerializer):
    workout_exercise_details = WorkExerciseDetailsSerializers(many=True, required=False)
    workset_weight = serializers.IntegerField(required=True)
    total_exercise_weight = serializers.SerializerMethodField()
    exercise_name = serializers.CharField(required=False)
    workout = serializers.PrimaryKeyRelatedField(read_only=True)


    class Meta:
        model = WorkExercise
        fields = ("id","workout", "exercise_name", "workset_weight","total_exercise_weight", "notes", "workout_exercise_details")

    #create workout exercise first and its details if any
    def create (self, validated_data):
        details = validated_data.pop('workout_exercise_details', [])
        workout_id = Workout.objects.latest('id')
        workout_exercise = WorkExercise.objects.create(**validated_data)
        #if there is details, create the details as WorkExerciseDetailsSerializers
        if details:
            WorkExerciseDetails.objects.bulk_create(
                [
                    WorkExerciseDetails(workout_exercise=workout_exercise, **workout_exercise_details)
                    for workout_exercise_details in details
                ],
            )
        
        return workout_exercise


    #update only the specific model, not the nested data
    def update(self, instance, validated_data):

        #input
        details = validated_data.pop('workout_exercise_details', [])

        #existing
        workout_e_details = instance.workout_exercise_details

        #set input to existing instance
        instance.exercise_name = validated_data.get('exercise_name', instance.exercise_name)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()


        return instance

    def get_total_exercise_weight (self, obj):
        #get all workout exercise details under this workout exercise details pk
        workout_id = obj.id
        details = WorkExerciseDetails.objects.filter(workout_exercise=workout_id)
    
        #compute
        total_exercise = 0
        for d in details:
            total = d.rep_complete * d.weight
            total_exercise += total
        return total_exercise

class ReadWorkoutSerializers(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    #accept username value in user field
    user = serializers.SlugRelatedField(slug_field="username", queryset=CustomUser.objects.all())
    workout_exercises = WorkExerciseSerializers(many=True, read_only=True)
    workout_exercise_details = WorkExerciseDetailsSerializers(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = ( "id", "start", "end", "weights_lift" , "duration", "user", 'workout_exercises', 'workout_exercise_details' )
        extra_kwargs = {'workout_exercises': {'read_only': True}}

    def get_duration (self, validated_data):
        difference = validated_data.end - validated_data.start
        seconds_in_day = 24 * 60 * 60
        divmod(difference.days * seconds_in_day + difference.seconds, 60)
        return difference

#create need password compulsory , update no need password [different fields same methods]
#need ReadWorkoutSerializers during update?
class UserUpdateSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    username = serializers.CharField(
        required=False,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all(), message='A user with this username already exists.')
            ],)
    workouts = ReadWorkoutSerializers(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'birth_year', 'body_weight', 'preferred_unit', 'barbell_weight', 'age', 'workouts')
        extra_kwargs = {'workouts': {'read_only': True}}

    def get_age(self, obj):
        delta = int(date.today().year) - obj.birth_year
        return int(delta)

#workout is created without exercise and exercise details
class WriteWorkoutSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(slug_field="username", queryset=CustomUser.objects.all())
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()

    # workout_exercises = WorkExerciseSerializers(many=True, allow_null=True)
    # workout_exercise_details = WorkExerciseDetailsSerializers(many=True, allow_null=True)

    class Meta:
        model = Workout
        fields = ("start", "end", "weights_lift" , "duration", "user")

    def validate(self, data):
        """
        Check that start is before end.
        """
        if data['start'] > data['end']:
            raise serializers.ValidationError("End must occur after start")
        return data

    def create(self, validated_data):
        """ Update workout end time if existing record with start time exist"""
        workout,created = Workout.objects.update_or_create(
            start = validated_data.get('start', None),
            user = validated_data['user'],
            weights_lift = validated_data['weights_lift'],
            defaults = {'end': validated_data.get('end', None)})
        # print(created)
        return workout

        # if workout_exercises:
        #     workout_id = Workout.objects.latest('id')
        #     WorkExercise.objects.bulk_create(
        #         [
        #             #map input to Object relational model
        #             WorkoutExercise(workout=workout_id , **workout_exercise)
        #             for workout_exercise in workout_exercises
        #         ]
        #     )

        # #if there is details, create the details as WorkExerciseDetailsSerializers
        # if details:
        #     WorkExerciseDetails.objects.bulk_create(
        #         [
        #             WorkExerciseDetails(workout_exercise=workout_exercise, **workout_exercise_details)
        #             for workout_exercise_details in details
        #         ],
        #     )

    def get_duration (self, validated_data):
        difference = validated_data.end - validated_data.start
        seconds_in_day = 24 * 60 * 60
        divmod(difference.days * seconds_in_day + difference.seconds, 60)
        return difference
