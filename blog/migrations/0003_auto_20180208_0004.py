# Generated by Django 2.0.1 on 2018-02-07 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180207_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='created_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='last_logged_in',
            field=models.DateTimeField(null=True),
        ),
    ]
