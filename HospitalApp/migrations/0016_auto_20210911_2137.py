# Generated by Django 2.2 on 2021-09-11 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalApp', '0015_hospital_linkedin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hospital',
            old_name='Facebook',
            new_name='facebook',
        ),
        migrations.RenameField(
            model_name='hospital',
            old_name='Google',
            new_name='google',
        ),
        migrations.RenameField(
            model_name='hospital',
            old_name='LinkedIn',
            new_name='linkedIn',
        ),
    ]