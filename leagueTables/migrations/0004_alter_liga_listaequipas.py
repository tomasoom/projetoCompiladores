# Generated by Django 4.0.3 on 2022-05-23 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagueTables', '0003_clube_diferencadegolos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liga',
            name='listaEquipas',
            field=models.ManyToManyField(related_name='ligas', to='leagueTables.clube'),
        ),
    ]