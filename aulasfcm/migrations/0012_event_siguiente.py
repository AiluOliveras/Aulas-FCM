# Generated by Django 4.1.3 on 2023-03-27 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aulasfcm', '0011_event_entidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='siguiente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aulasfcm.event'),
        ),
    ]
