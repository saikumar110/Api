# Generated by Django 2.2 on 2021-09-10 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalApp', '0014_auto_20210910_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='LinkedIn',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
