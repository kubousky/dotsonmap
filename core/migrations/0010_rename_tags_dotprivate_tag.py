# Generated by Django 3.2.6 on 2022-08-16 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20220816_1222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dotprivate',
            old_name='tags',
            new_name='tag',
        ),
    ]
