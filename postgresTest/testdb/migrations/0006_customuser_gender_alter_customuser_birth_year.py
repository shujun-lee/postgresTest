# Generated by Django 4.0.5 on 2022-07-04 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0005_alter_customuser_barbell_weight_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('NB', 'Non Binary')], default='M', max_length=2),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='birth_year',
            field=models.IntegerField(blank=True, default=1970),
        ),
    ]