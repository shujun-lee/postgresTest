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
    total_rep_weight = serializers.SerializerMethodField()

    class Meta:
        model = WorkExerciseDetails
        fields = ("rep_complete", "weight", "set_type", "workout_exercise","id", "total_rep_weight")

    def get_total_rep_weight(self, obj):
        total = obj.rep_complete * obj.weight
        return total

class WorkExerciseSerializers(serializers.ModelSerializer):
    workout_exercise_details = WorkExerciseDetailsSerializers(many=True, required=False)
    total_exercise_weight = serializers.SerializerMethodField()
    exercise_name = serializers.CharField(required=False)


    class Meta:
        model = WorkExercise
        fields = ("exercise_name", "total_exercise_weight", "workset_weight", "notes", "workout", "workout_exercise_details")

    #create workout exercise first and its details if any
    def create (self, validated_data):
        details = validated_data.pop('workout_exercise_details', [])
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

        #multiple details, which one to update?
        # if details:
        #     workout_e_details.rep_complete = details.get('rep_complete', workout_e_details.rep_complete)
        #     workout_e_details.weight = details.get('weight', workout_e_details.weight)
        #     workout_e_details.set_type = details.get('set_type', workout_e_details.set_type)
        #
        # workout_e_details.save()

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

class WorkoutSerializers(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    #accept username value in user field
    user = serializers.SlugRelatedField(slug_field="username", queryset=CustomUser.objects.all())
    workout_exercises = WorkExerciseSerializers(many=True, read_only=True)
    workout_exercise_details = WorkExerciseDetailsSerializers(many=True, read_only=True)
    weights_lift = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = ( "id", "start", "end", "weights_lift" , "duration", "user", 'workout_exercises', 'workout_exercise_details' )
        extra_kwargs = {'workout_exercises': {'read_only': True}}

    def get_duration (self, validated_data):
        difference = validated_data.end - validated_data.start
        seconds_in_day = 24 * 60 * 60
        divmod(difference.days * seconds_in_day + difference.seconds, 60)
        return difference

    def get_weights_lift(self, obj):
        #get all workout exercise and exercise details under this workout pk
        # workout_id = obj.id
        # workout_exercises = WorkExercise.objects.filter(workout=workout_id)
        print(self.data)
        print(obj)
        # workout_exerises_serialize = WorkExerciseSerializers(workout_exercises)
        # print(workout_exerises_serialize.data)
        #sum total exercise weight
        # for exercise in workout_exerises_serialize:
        #     print(exercise.total_exercise_weight)
        pass
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
    workout_exercises = WorkExerciseSerializers(many=True, read_only=True)
    workout_exercise_details = WorkExerciseDetailsSerializers(many=True, read_only=True)
    user = serializers.SlugRelatedField(slug_field="username", queryset=CustomUser.objects.all())

    class Meta:
        model = Workout
        fields = ( "id", "start", "end", "weights_lift" , "duration", "user", 'workout_exercises', 'workout_exercise_details' )

    #custom method required to writed nested fields
    # def create(self, validated_data):
    #     pass
    def update(self, instance, validated_data):
        #retreive workout instance
        instance.id = validated_data.get('id', instance.id)
        workout_exercises = validated_data.get('workout_exercises')
        if workout_exercises:
            pass
        print(instance)
        instance.save()
        return instance
        # instance.name = validated_data.get('name', instance.name)
        # workout = Workout.objects.get(pk=validated_data.pop('id'))

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError("End must occur after start")
        return data

    def get_duration (self, validated_data):
        difference = validated_data.end - validated_data.start
        seconds_in_day = 24 * 60 * 60
        divmod(difference.days * seconds_in_day + difference.seconds, 60)
        return difference
