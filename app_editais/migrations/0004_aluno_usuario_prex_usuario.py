# Generated by Django 4.2.4 on 2023-09-12 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_editais', '0003_inscricao'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='usuario',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='prex',
            name='usuario',
            field=models.CharField(max_length=100, null=True),
        ),
    ]