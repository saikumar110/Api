# Generated by Django 2.2 on 2021-09-10 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalApp', '0013_auto_20210909_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='Facebook',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='hospital',
            name='Google',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='hospital',
            name='twitter',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]