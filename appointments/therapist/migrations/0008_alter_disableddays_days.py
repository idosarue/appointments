# Generated by Django 3.2.7 on 2021-09-11 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('therapist', '0007_alter_disableddays_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disableddays',
            name='days',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
