# Generated by Django 3.2.7 on 2021-09-20 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('therapist', '0007_auto_20210919_1332'),
        ('patient', '0005_appointmentresponse_date_t'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentresponse',
            name='week_day',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='therapist.day'),
        ),
    ]