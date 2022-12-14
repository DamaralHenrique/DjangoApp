# Generated by Django 4.1.2 on 2022-10-06 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rota',
            fields=[
                ('id_rota', models.IntegerField(primary_key=True, serialize=False)),
                ('aeroporto_partida', models.CharField(max_length=200)),
                ('aeroporto_chegada', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'rotas',
            },
        ),
        migrations.CreateModel(
            name='StatusVoo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'status_voo',
            },
        ),
        migrations.CreateModel(
            name='Voo',
            fields=[
                ('id_voo', models.IntegerField(primary_key=True, serialize=False)),
                ('chegada_prevista', models.DateTimeField()),
                ('partida_prevista', models.DateTimeField()),
                ('companhia_aerea', models.CharField(max_length=200)),
                ('id_rota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.rota')),
            ],
            options={
                'db_table': 'voos',
            },
        ),
        migrations.CreateModel(
            name='VooDinamico',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('partida_real', models.DateTimeField()),
                ('chegada_real', models.DateTimeField()),
                ('id_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.statusvoo')),
                ('id_voo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.voo')),
            ],
            options={
                'db_table': 'voo_dinamico',
            },
        ),
        migrations.CreateModel(
            name='Conexao',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=200)),
                ('id_rota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.rota')),
            ],
            options={
                'db_table': 'conexoes',
            },
        ),
    ]
