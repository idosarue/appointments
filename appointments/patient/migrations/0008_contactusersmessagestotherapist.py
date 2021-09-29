# Generated by Django 3.2.7 on 2021-09-29 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0007_appointment_week_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUsersMessagesToTherapist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('message', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
            ],
        ),
    ]