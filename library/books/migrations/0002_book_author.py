# Generated by Django 4.1.13 on 2024-05-27 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
