# Generated by Django 3.2.6 on 2022-02-02 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_dot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dot',
            name='rating',
            field=models.FloatField(),
        ),
    ]
