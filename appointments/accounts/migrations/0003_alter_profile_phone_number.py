# Generated by Django 3.2.7 on 2021-09-05 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_birth_date_profile_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=10),
        ),
    ]
