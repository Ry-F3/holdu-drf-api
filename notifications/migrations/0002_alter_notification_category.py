# Generated by Django 3.2.25 on 2024-03-20 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='category',
            field=models.CharField(choices=[('connection', 'Connection'), ('new_job', 'New Job'), ('accepted_application', 'Accepted Application'), ('message_alert', 'Message Alert'), ('connection_request', 'Connection_Request')], max_length=50),
        ),
    ]
