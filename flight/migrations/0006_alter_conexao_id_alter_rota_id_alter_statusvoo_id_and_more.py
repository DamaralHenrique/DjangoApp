# Generated by Django 4.1.2 on 2022-11-06 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flight", "0005_alter_voo_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="conexao",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="rota",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="statusvoo",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="voodinamico",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
