# Generated by Django 4.2.4 on 2023-11-14 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_editais', '0011_projeto_status_relatorio_pdf_edital_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='relatorio',
            name='data_de_envio',
            field=models.DateField(auto_now_add=True, default='2023-10-10'),
            preserve_default=False,
        ),
    ]
