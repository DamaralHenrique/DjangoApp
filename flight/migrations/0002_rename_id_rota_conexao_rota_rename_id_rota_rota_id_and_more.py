# Generated by Django 4.1.2 on 2022-10-06 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conexao',
            old_name='id_rota',
            new_name='rota',
        ),
        migrations.RenameField(
            model_name='rota',
            old_name='id_rota',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='voo',
            old_name='id_voo',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='voo',
            old_name='id_rota',
            new_name='rota',
        ),
        migrations.RenameField(
            model_name='voodinamico',
            old_name='id_status',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='voodinamico',
            old_name='id_voo',
            new_name='voo',
        ),
    ]
