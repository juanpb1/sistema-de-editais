from django.shortcuts import render
from .models import Prex

def home(request):
    return render(request, "home/index.html")

def prex(request):
    return render(request, "prex/index.html")

def prexs(request):
    novo_Prex = Prex()
    novo_Prex.pis = request.POST.get('pis')
    novo_Prex.nome = request.POST.get('nome')
    novo_Prex.nacionalidade = request.POST.get('nacionalidade')
    novo_Prex.cpf = request.POST.get('cpf')
    novo_Prex.sexo = request.POST.get('sexo')
    novo_Prex.email = request.POST.get('email')
    novo_Prex.telefone = request.POST.get('telefone')
    novo_Prex.data_nasc = request.POST.get('data_nasc')
    novo_Prex.save()
