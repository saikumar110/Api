# Generated by Django 2.2 on 2021-06-25 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalApp', '0006_auto_20210625_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diseasedata',
            name='weight',
            field=models.IntegerField(blank=True),
        ),
    ]