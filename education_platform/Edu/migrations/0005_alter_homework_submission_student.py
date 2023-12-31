# Generated by Django 4.2.5 on 2023-10-16 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Edu', '0004_alter_lesson_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework_submission',
            name='student',
            field=models.ForeignKey(limit_choices_to={'user_type': 'Student'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
