# Generated by Django 4.0.5 on 2022-06-30 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0003_remove_customuser_fav_color_remove_workexercise_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workexercisedetails',
            name='set_type',
            field=models.CharField(choices=[('work_set', 'work set'), ('warmup_set', 'warmup set')], default='warmup_set', max_length=11, verbose_name='type'),
        ),
    ]