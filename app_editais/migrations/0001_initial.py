# Generated by Django 4.2.4 on 2023-08-26 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('matricula', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('nacionalidade', models.CharField(max_length=50)),
                ('cpf', models.CharField(max_length=14)),
                ('sexo', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=15)),
                ('data_nasc', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Edital',
            fields=[
                ('numero', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('n_vagas', models.IntegerField()),
                ('data_inicial', models.DateField()),
                ('data_final', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('matricula', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('nacionalidade', models.CharField(max_length=50)),
                ('cpf', models.CharField(max_length=14)),
                ('sexo', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=15)),
                ('data_nasc', models.DateField()),
                ('graduacao', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('data_de_inicio', models.DateField()),
                ('data_de_fim', models.DateField()),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_editais.professor')),
            ],
        ),
        migrations.CreateModel(
            name='Relatorio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('Em andamento', 'Em andamento'), ('Concluído', 'Concluído')], max_length=20)),
                ('projeto_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_editais.projeto')),
            ],
        ),
        migrations.CreateModel(
            name='EditalAluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pendente', 'Pendente'), ('Aprovado', 'Aprovado'), ('Reprovado', 'Reprovado')], default='Pendente', max_length=20)),
                ('aluno_mat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_editais.aluno')),
                ('edital_num', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_editais.edital')),
            ],
        ),
    ]
