# Generated by Django 3.2.25 on 2024-03-20 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_notification_item_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.CharField(default='title one', max_length=255),
            preserve_default=False,
        ),
    ]
