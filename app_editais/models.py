from django.db import models
import uuid


class Aluno(models.Model):
    matricula = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    nacionalidade = models.CharField(max_length=50)
    cpf = models.CharField(max_length=14)
    sexo = models.CharField(max_length=10)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    data_nasc = models.DateField()
    usuario = models.CharField(max_length=100, null=True)

class Edital(models.Model):
    numero = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    n_vagas = models.IntegerField()
    n_vagas_t = models.IntegerField(null=True)
    data_inicial = models.DateField()
    data_final = models.DateField()
    pdf_edital = models.FileField(null=True, upload_to=f'pdfs_editais/')
    ata_cons = models.FileField(null=True, upload_to=f'pdfs_editais/')
    ata_coleg = models.FileField(null=True, upload_to=f'pdfs_editais/')

class Inscricao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    edital = models.ForeignKey(Edital, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Pendente', choices=[('Pendente', 'Pendente'), ('Aprovado', 'Aprovado'), ('Reprovado', 'Reprovado')])
    justificativa = models.TextField(null=True)
    
    class Meta:
        unique_together = ('aluno', 'edital')

class Professor(models.Model):
    matricula = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    nacionalidade = models.CharField(max_length=50)
    cpf = models.CharField(max_length=14)
    sexo = models.CharField(max_length=10)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    data_nasc = models.DateField()
    graduacao = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100, null=True)

class Projeto(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    data_de_inicio = models.DateField()
    data_de_fim = models.DateField()
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Em andamento', choices=[('Em andamento', 'Em andamento'), ('Concluído', 'Concluído')])

class Relatorio(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, default='Pendente', choices=[('Pendente', 'Pendente'), ('Aprovado', 'Aprovado'), ('Reprovado', 'Reprovado')])
    data_de_envio = models.DateField(auto_now_add=True)
    projeto_id = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    pdf_edital = models.FileField(null=True, upload_to=f'relatorios/')
    just_reprov = models.TextField(null=True)
    

class Prex(models.Model):
    pis = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    nacionalidade = models.CharField(max_length=50)
    cpf = models.CharField(max_length=14)
    sexo = models.CharField(max_length=10)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    data_nasc = models.DateField()
    usuario = models.CharField(max_length=100, null=True)
