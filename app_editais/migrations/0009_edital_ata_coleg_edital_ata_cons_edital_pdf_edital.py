# Generated by Django 4.2.4 on 2023-10-26 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_editais', '0008_edital_n_vagas_t'),
    ]

    operations = [
        migrations.AddField(
            model_name='edital',
            name='ata_coleg',
            field=models.FileField(null=True, upload_to='pdfs_editais/'),
        ),
        migrations.AddField(
            model_name='edital',
            name='ata_cons',
            field=models.FileField(null=True, upload_to='pdfs_editais/'),
        ),
        migrations.AddField(
            model_name='edital',
            name='pdf_edital',
            field=models.FileField(null=True, upload_to='pdfs_editais/'),
        ),
    ]
