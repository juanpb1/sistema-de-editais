# Generated by Django 4.2.4 on 2023-11-15 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_editais', '0012_relatorio_data_de_envio'),
    ]

    operations = [
        migrations.AddField(
            model_name='relatorio',
            name='just_reprov',
            field=models.TextField(null=True),
        ),
    ]