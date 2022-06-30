# Generated by Django 4.0.5 on 2022-06-30 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0004_alter_workexercisedetails_set_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='barbell_weight',
            field=models.DecimalField(blank=True, decimal_places=2, default='20.00', max_digits=5),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='body_weight',
            field=models.DecimalField(blank=True, decimal_places=2, default='45.00', max_digits=5),
        ),
        migrations.AlterField(
            model_name='workexercise',
            name='exercise_name',
            field=models.CharField(choices=[('BP', 'Bench Press'), ('S', 'Squat'), ('DL', 'Deadlift'), ('BR', 'Bench Row')], max_length=2, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='workexercise',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='workexercisedetails',
            name='rep_complete',
            field=models.IntegerField(blank=True, verbose_name='rep'),
        ),
        migrations.AlterField(
            model_name='workexercisedetails',
            name='workout_exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_exercise_details', to='testdb.workexercise'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='weights_lift',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7),
        ),
    ]
