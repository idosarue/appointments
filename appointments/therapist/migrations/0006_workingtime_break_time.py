# Generated by Django 3.2.7 on 2021-09-19 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('therapist', '0005_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='workingtime',
            name='break_time',
            field=models.IntegerField(default=15),
        ),
    ]