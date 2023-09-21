from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from .models import Prex, Aluno, Edital, Inscricao
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rolepermissions.roles import assign_role

from rolepermissions.decorators import has_role_decorator

# Create your views here.

def home(request):
    return render(request, "home/index.html")

@has_role_decorator('prex')
def prex(request):

    editais = {
        'editais': Edital.objects.all()
    }

    return render(request, "prex/index.html", editais)

@has_role_decorator('admin')
def prex_cadastro(request):
    return render(request, "prex/cadastro.html")

def create_prex(request):
    if request.method == "GET":
        return render(request, 'prex/cadastro.html')
    else:   
        novo_Prex = Prex()
        novo_Prex.pis = request.POST.get('pis')
        novo_Prex.nome = request.POST.get('nome')
        novo_Prex.nacionalidade = request.POST.get('nacionalidade')
        novo_Prex.cpf = request.POST.get('cpf')
        novo_Prex.sexo = request.POST.get('sexo')
        novo_Prex.email = request.POST.get('email')
        novo_Prex.telefone = request.POST.get('telefone')
        novo_Prex.data_nasc = request.POST.get('data_nasc')
        novo_Prex.usuario = request.POST.get('usuario')
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        
        user = User.objects.filter(username=usuario).first()
        
        if user:
            messages.error(request, 'Usuário já Cadastrado. Tente novamente.')
            return redirect("formulario_prex")
        else:
            user = User.objects.create_user(username=usuario, password=senha)
            user.save()
            assign_role(user, 'admin')
            novo_Prex.save()

            prexs = {
                'prexs': Prex.objects.all()
            }
            messages.error(request, 'Cadastrado com sucesso.')
        return render(request, "prex/login.html")

    # return render(request, 'prex/prexs.html', prexs)

def login_prex(request):
    if request.method == "GET":
        return render(request, "prex/login.html")
    else:
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        user = authenticate(username=usuario, password=senha)
        grupos = Group.objects.filter(name="prex")
        if user:
            grupo = user.groups.all()
            if len(list(grupo)) > 0 : 
                if(grupos[0] == grupo[0]) :
                    login(request, user)
                    return redirect("prex")
                else:
                    messages.error(request, 'Cadastro não encontrado. Tente novamente.')
            else:
                login(request, user)
                return redirect("prex")
        else:
            messages.error(request, 'Usuário ou senha incorretos. Tente novamente.')
    return render(request, "prex/login.html")

def logout_view(request):
    logout(request)
    return redirect("login_prex")

@has_role_decorator('prex')
def prex_message(request):
    return render(request, 'prex/message.html')

@has_role_decorator('aluno')
def aluno_home(request):
    data_atual = timezone.now()
    editais = {
        'editais': Edital.objects.filter(Q(data_final__gte=data_atual))
    }
    
    if request.method == 'GET':
        redirect('aluno_home')
    else:
        return render(request,'inscricao/aluno_incricao_form.html')

    return render(request, 'aluno/index.html', editais)

def aluno_login(request):
    if request.method == "GET":
        return render(request, "aluno/login.html")
    else:
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        user = authenticate(username=usuario, password=senha)
        grupos = Group.objects.filter(name="aluno")
        if user:
            grupo = user.groups.all()
            if len(list(grupo)) > 0 :
                if (grupos[0] == grupo[0]):
                    login(request, user)
                    return redirect("aluno_home")
                else:
                    messages.error(request, 'Cadastro não encontrado. Tente novamente.')
            else:
                login(request, user)
                return redirect("aluno_home")
        else:
            messages.error(request, 'Usuário ou senha incorretos. Tente novamente.')
    return render(request, "aluno/login.html")

@has_role_decorator('aluno')
def aluno_message(request):
    return render(request, "aluno/message.html")
         
def inscrever_aluno(request):
    if request.method == 'GET':
        redirect('aluno_home')
    else:
        aluno_user = request.user.username
        aluno = Aluno.objects.get(usuario=aluno_user)
        aluno_idd = aluno.matricula
        edital_num = request.POST.get('edital_numero')
        edital = Edital.objects.get(numero=edital_num)
        
        try:
            verif_inscricao = Inscricao.objects.get(aluno_id=aluno_idd , edital_id=edital_num)
            messages.error(request, 'Você já está Inscrito')

        except Inscricao.DoesNotExist:
            nova_insc = Inscricao()
            nova_insc.aluno = aluno
            nova_insc.edital = edital
            nova_insc.save()
            edital.save()
            messages.error(request, 'Inscrito com sucesso!')
    return redirect('aluno_home')

def aluno_cadastro(request):
       return render(request, "aluno/cadastro.html")

def create_aluno(request):
    if request.method == "GET":
        return render(request, 'aluno/cadastro.html')
    else:
        novo_Aluno = Aluno()
        novo_Aluno.matricula = request.POST.get('matricula')
        novo_Aluno.nome = request.POST.get('nome')
        novo_Aluno.nacionalidade = request.POST.get('nacionalidade')
        novo_Aluno.cpf = request.POST.get('cpf')
        novo_Aluno.sexo = request.POST.get('sexo')
        novo_Aluno.email = request.POST.get('email')
        novo_Aluno.telefone = request.POST.get('telefone')
        novo_Aluno.data_nasc = request.POST.get('data_nasc')
        novo_Aluno.usuario = request.POST.get('usuario')
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        
        user = User.objects.filter(username=usuario).first()
        
        if user:
            messages.error(request, 'Usuário já Cadastrado. Tente novamente.')
            return redirect("aluno_cadastro")
        else:
            user = User.objects.create_user(username=usuario, password=senha)
            user.save()
            assign_role(user, 'aluno')
            novo_Aluno.save()

            create_aluno = {
                'create_aluno': Aluno.objects.all()
            }
            messages.error(request, 'Cadastrado com sucesso.')
        return render(request, "aluno/login.html")
 
def permissao_negada(request, exception):
    return render(request, 'home/permissao_negada.html', status=403)

@has_role_decorator('prex')
def edital_criar(request):
    return render(request, 'edital/criar.html')

def create_edital(request):
       
    novo_Edital = Edital()
    novo_Edital.numero = request.POST.get('numero')
    novo_Edital.titulo = request.POST.get('titulo')
    novo_Edital.descricao = request.POST.get('descricao')
    novo_Edital.n_vagas = request.POST.get('n_vagas')
    novo_Edital.data_inicial = request.POST.get('data_inicial')
    novo_Edital.data_final = request.POST.get('data_final')

    novo_Edital.save()

    return render(request, 'edital/message.html')

@has_role_decorator('prex')
def edital_message(request):
    return render(request, 'edital/message.html')
