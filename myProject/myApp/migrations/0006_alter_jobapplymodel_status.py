# Generated by Django 4.2.4 on 2024-09-26 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0005_jobapplymodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplymodel',
            name='status',
            field=models.CharField(choices=[('applied', 'Applied'), ('interview_scheduled', 'Interview Scheduled'), ('rejected', 'Rejected'), ('hired', 'Hired')], default='Pending', max_length=20),
        ),
    ]
