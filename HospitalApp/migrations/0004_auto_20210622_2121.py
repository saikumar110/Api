# Generated by Django 2.2 on 2021-06-22 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalApp', '0003_auto_20210619_2003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='first_name',
            new_name='Full_name',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='DateJoined',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='Updated_On',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='email',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='password',
        ),
        migrations.AlterField(
            model_name='patient',
            name='LastOtp',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
