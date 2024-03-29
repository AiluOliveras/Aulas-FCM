# Generated by Django 4.1.3 on 2023-04-25 23:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aulasfcm', '0013_remove_event_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operacion', models.CharField(max_length=10)),
                ('endpoint', models.CharField(max_length=150)),
                ('fecha', models.DateTimeField()),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
