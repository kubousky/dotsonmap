# Generated by Django 3.2.6 on 2022-02-02 21:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=350)),
                ('lon', models.CharField(max_length=20)),
                ('lat', models.CharField(max_length=20)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=1)),
                ('link', models.CharField(blank=True, max_length=255)),
                ('tags', models.ManyToManyField(to='core.Tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
