# Generated by Django 3.2.25 on 2024-03-10 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_type',
            field=models.CharField(blank=True, choices=[('employee', 'Employee'), ('employer', 'Employer')], default=None, max_length=10, null=True),
        ),
    ]