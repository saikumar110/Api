# Generated by Django 2.2 on 2021-06-25 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalApp', '0007_auto_20210625_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='diseasedata',
            name='Age',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
