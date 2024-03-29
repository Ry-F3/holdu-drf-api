# Generated by Django 3.2.25 on 2024-03-14 20:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0002_rename_owner_rating_owner_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='owner_id',
            new_name='created_by',
        ),
        migrations.AlterField(
            model_name='rating',
            name='rate_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings_received', to=settings.AUTH_USER_MODEL),
        ),
    ]
