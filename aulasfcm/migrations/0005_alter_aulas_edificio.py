# Generated by Django 4.1.3 on 2022-12-21 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aulasfcm', '0004_alter_aulas_edificio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aulas',
            name='edificio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='aulasfcm.edificios'),
            preserve_default=False,
        ),
    ]
