# Generated by Django 3.2.7 on 2021-09-20 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('therapist', '0009_comment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateField(null=True),
        ),
    ]