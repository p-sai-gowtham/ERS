# Generated by Django 5.0.1 on 2024-02-16 22:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Elective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dept', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100)),
                ('seats', models.IntegerField()),
                ('offering_courses', models.ManyToManyField(related_name='offering_courses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
