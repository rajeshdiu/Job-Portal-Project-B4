# Generated by Django 5.1.1 on 2024-09-26 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0003_jobapplymodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobmodel',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]