# Generated by Django 3.2.6 on 2022-02-13 19:55

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_dot_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='dot',
            name='image',
            field=models.ImageField(null=True, upload_to=core.models.dot_image_file_path),
        ),
    ]
