# Generated by Django 4.1.7 on 2023-02-22 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_state_medical_council_doctor_medical_council_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='last_login',
            field=models.DateTimeField(auto_now=True),
        ),
    ]