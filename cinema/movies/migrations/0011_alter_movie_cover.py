# Generated by Django 5.0.6 on 2024-07-03 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_movie_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='cover',
            field=models.ImageField(upload_to='media/movies/covers'),
        ),
    ]
