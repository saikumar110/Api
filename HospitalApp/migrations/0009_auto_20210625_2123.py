# Generated by Django 2.2 on 2021-06-25 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalApp', '0008_diseasedata_age'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diseasedata',
            old_name='HospitalName',
            new_name='Hospital_Name',
        ),
        migrations.RenameField(
            model_name='diseasedata',
            old_name='MedicinePrescribed',
            new_name='Medicine_Prescribed',
        ),
    ]
