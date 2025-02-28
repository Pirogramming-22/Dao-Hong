# Generated by Django 5.1.4 on 2025-01-09 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_moviereview_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviereview',
            name='rating',
            field=models.FloatField(default=3.0),
        ),
        migrations.AlterField(
            model_name='moviereview',
            name='release_year',
            field=models.IntegerField(default=1990),
        ),
        migrations.AlterField(
            model_name='moviereview',
            name='review_text',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='moviereview',
            name='runtime',
            field=models.IntegerField(default=120),
        ),
    ]
