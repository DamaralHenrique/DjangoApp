# Generated by Django 4.1.2 on 2022-10-06 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0002_rename_id_rota_conexao_rota_rename_id_rota_rota_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conexao',
            name='num_conexao',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
