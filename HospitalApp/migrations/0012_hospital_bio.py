# Generated by Django 2.2 on 2021-09-09 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalApp', '0011_hospital_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]