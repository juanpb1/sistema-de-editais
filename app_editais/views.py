from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from .models import Prex, Aluno, Edital, Inscricao, Projeto, Professor, Relatorio
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rolepermissions.roles import assign_role
import datetime as dd
from datetime import datetime, timedelta
from rolepermissions.decorators import has_role_decorator
import os
from django.urls import reverse

# Create your views here.

def home(request):
    return render(request, "home/index.html")

@has_role_decorator('prex')
def prex(request):

    editais= Edital.objects.all()
    
    projetos = Projeto.objects.select_related('professor').all()

    return render(request, "prex/index.html", {'editais':editais, 'projetos':projetos})

@has_role_decorator('admin')
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
        
        data_nas = request.POST.get('data_nasc')
        formato_data = "%Y-%m-%d"
        data_nas = datetime.strptime(data_nas, formato_data)
        data = data_nas.date()
        data_hj = dd.date.today()
        data_min = data_hj - timedelta(days=16 * 365)
        
        if data > data_min:
            messages.error(request, 'Data inválida. Tente novamente.')
            return redirect("prex_cadastro")
        
        pis = Prex.objects.filter(pis= (request.POST.get('pis') )).first()
        
        if pis:
            messages.error(request, 'Matrícula Já cadastrada. Tente novamente.')
            return redirect("prex_cadastro")
        
        user = User.objects.filter(username=usuario).first()
        
        if user:
            messages.error(request, 'Usuário já Cadastrado. Tente novamente.')
            return redirect("prex_cadastro")
        else:
            user = User.objects.create_user(username=usuario, password=senha)
            user.save()
            assign_role(user, 'prex')
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

def login_professor(request):
    if request.method == "GET":
        return render(request, "professor/login.html")
    else:
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        user = authenticate(username=usuario, password=senha)
        grupos = Group.objects.filter(name="professor")
        if user:
            grupo = user.groups.all()
            if len(list(grupo)) > 0 : 
                if(grupos[0] == grupo[0]) :
                    login(request, user)
                    return redirect("professor")
                else:
                    messages.error(request, 'Cadastro não encontrado. Tente novamente.')
            else:
                login(request, user)
                return redirect("professor")
        else:
            messages.error(request, 'Usuário ou senha incorretos. Tente novamente.')
    return render(request, "professor/login.html")

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

@has_role_decorator('aluno')
def status_editais(request):
    aluno_user = request.user.username
    aluno = Aluno.objects.prefetch_related("inscricao_set").get(usuario=aluno_user)
    inscricoes = aluno.inscricao_set.all()
    
    # edital_status = {}
    # inscricoes = Inscricao.objects.filter(aluno_id=aluno_idd)
    # for inscricao in inscricoes:
    #     edital_status[inscricao.edital.numero] = inscricao.status
    #     edital_status[inscricao.edital.numero] = inscricao.justificativa

    # editais = Edital.objects.filter(numero__in=list(edital_status.keys()))

    # for edital in editais:
    #     edital.status = edital_status[edital.numero]
    
    # context = {
    #     'editais': editais
    # }
    
    return render(request, 'aluno/status_edital.html', {"inscricoes":inscricoes})

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
    return redirect("aluno_login")

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
        
        data_nas = request.POST.get('data_nasc')
        formato_data = "%Y-%m-%d"
        data_nas = datetime.strptime(data_nas, formato_data)
        data = data_nas.date()
        data_hj = dd.date.today()
        data_min = data_hj - timedelta(days=16 * 365)
        
        if data > data_min:
            messages.error(request, 'Data inválida. Tente novamente.')
            return redirect("aluno_cadastro")
        
        mat = Aluno.objects.filter(matricula= (request.POST.get('matricula') )).first()
        
        if mat:
            messages.error(request, 'Matrícula Já cadastrada. Tente novamente.')
            return redirect("aluno_cadastro")
        
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

@has_role_decorator('prex')
def create_edital(request):
    if request.method == "GET":
        return render(request, 'edital/criar.html')
    else: 
        novo_Edital = Edital()
        novo_Edital.titulo = request.POST.get('titulo')
        novo_Edital.descricao = request.POST.get('descricao')
        novo_Edital.n_vagas = request.POST.get('n_vagas')
        novo_Edital.n_vagas_t = request.POST.get('n_vagas')
        novo_Edital.data_inicial = request.POST.get('data_inicial')
        novo_Edital.data_final = request.POST.get('data_final')
         
        data_ini = request.POST.get('data_inicial')
        formato_data = "%Y-%m-%d"
        data_in = datetime.strptime(data_ini, formato_data)
        data_fin = request.POST.get('data_final')
        data_fi = datetime.strptime(data_fin, formato_data)
        
        if data_fi < data_in:
            messages.error(request, 'Data inválida. Tente novamente.')
            return render(request, 'edital/criar.html')
        
        novo_Edital.save()
        
        
        pdf_edital = request.FILES['pdf_edital']
        nome_pdf_edital = f"edital-{novo_Edital.numero}.pdf" 
        novo_Edital.pdf_edital.save(nome_pdf_edital, pdf_edital)
        
        ata_cons = request.FILES['ata_cons']
        novo_nome_ata_cons = f"ata-conselho-{novo_Edital.numero}.pdf"
        novo_Edital.ata_cons.save(novo_nome_ata_cons, ata_cons)

        ata_coleg = request.FILES['ata_coleg']
        novo_nome_ata_coleg = f"ata-colegiado-{novo_Edital.numero}.pdf" 
        novo_Edital.ata_coleg.save(novo_nome_ata_coleg, ata_coleg)

        novo_Edital.save()

        return render(request, 'edital/message.html')

@has_role_decorator('prex')    
def edit_edital(request, numero):
    edital = Edital.objects.get(numero= numero)
    if request.method == "GET":
        return render(request, 'edital/edit.html', {'edital' : edital})
    else: 
        novas_vagas = int(request.POST.get('n_vagas'))
        
        if novas_vagas >= edital.n_vagas:
            if novas_vagas == edital.n_vagas_t:
                pass
            elif novas_vagas > edital.n_vagas_t:
                edital.n_vagas_t = novas_vagas
                edital.n_vagas += abs(novas_vagas - edital.n_vagas)
            elif novas_vagas < edital.n_vagas_t:
                edital.n_vagas_t = novas_vagas
                edital.n_vagas -= abs(novas_vagas - edital.n_vagas)
            
            edital.titulo = request.POST.get('titulo')
            edital.descricao = request.POST.get('descricao')
            edital.data_final = request.POST.get('data_final')

            try:
                pdf_edital = request.FILES['pdf_edital']
                nome_pdf_edital = f"edital-{edital.numero}.pdf"
                if edital.pdf_edital:
                    caminho_arquivo = os.path.join(edital.pdf_edital)
                    os.remove(caminho_arquivo) 
                edital.pdf_edital.save(nome_pdf_edital, pdf_edital)
            except:
                pass
            try:
                ata_cons = request.FILES['ata_cons']    
                novo_nome_ata_cons = f"ata-conselho-{edital.numero}.pdf"
                if edital.ata_cons:
                    caminho_arquivo = os.path.join(edital.ata_cons)
                    os.remove(caminho_arquivo)
                edital.ata_cons.save(novo_nome_ata_cons, ata_cons)
            except:
                pass
            try:
                ata_coleg = request.FILES['ata_coleg']
                novo_nome_ata_coleg = f"ata-colegiado-{edital.numero}.pdf"
                if edital.ata_coleg:
                    caminho_arquivo = os.path.join(edital.ata_coleg)
                    os.remove(caminho_arquivo) 
                edital.ata_coleg.save(novo_nome_ata_coleg, ata_coleg)
            except:
                pass
            
            
        edital.save()
        messages.error(request, 'Alterações realizadas com sucesso.')
            
        return redirect('prex')
        
@has_role_decorator('prex')
def edital_message(request):
    return render(request, 'edital/message.html')

@has_role_decorator('professor')
def projeto_criar(request):
    return render(request, 'projeto/criar.html')

@has_role_decorator('professor')
def create_projeto(request):
    professor_user = request.user.username
    professor = Professor.objects.get(usuario=professor_user)
    professor_idd = professor.matricula
    
    novo_Projeto = Projeto()
    # novo_Projeto.id = request.POST.get('id')
    novo_Projeto.nome = request.POST.get('nome')
    novo_Projeto.data_de_inicio = request.POST.get('data_de_inicio')
    novo_Projeto.data_de_fim = request.POST.get('data_de_fim')
    novo_Projeto.professor_id = professor.matricula
    
    novo_Projeto.save()
    
    return render(request, 'projeto/message.html')

@has_role_decorator('professor')
def projeto_message(request):
    return render(request, 'projeto/message.html')

@has_role_decorator('prex') 
def visualizar_edital(request, numero):

    edital = Edital.objects.get(numero=numero)
    #alunos = Inscricao.objects.filter(edital_id=numero)
    #inscricoes_id = Inscricao.objects.filter(edital_id=numero)

    return render(request, 'prex/ver.html', {"edital": edital})

@has_role_decorator('prex')
def create_professor(request):
    if request.method == "GET":
        return render(request, 'professor/cadastro.html')
    else:   
        novo_Professor = Professor()
        novo_Professor.matricula = request.POST.get('matricula')
        novo_Professor.nome = request.POST.get('nome')
        novo_Professor.nacionalidade = request.POST.get('nacionalidade')
        novo_Professor.cpf = request.POST.get('cpf')
        novo_Professor.sexo = request.POST.get('sexo')
        novo_Professor.email = request.POST.get('email')
        novo_Professor.telefone = request.POST.get('telefone')
        novo_Professor.data_nasc = request.POST.get('data_nasc')
        novo_Professor.graduacao = request.POST.get('graduacao')
        novo_Professor.usuario = request.POST.get('usuario')
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        
        data_nas = request.POST.get('data_nasc')
        formato_data = "%Y-%m-%d"
        data_nas = datetime.strptime(data_nas, formato_data)
        data = data_nas.date()
        data_hj = dd.date.today()
        data_min = data_hj - timedelta(days=16 * 365)
        
        if data > data_min:
            messages.error(request, 'Data inválida. Tente novamente.')
            return redirect("professor_cadastro")
        
        mat = Professor.objects.filter(matricula= (request.POST.get('matricula') )).first()
        
        if mat:
            messages.error(request, 'Matrícula Já cadastrada. Tente novamente.')
            return redirect("professor_cadastro")
        
        user = User.objects.filter(username=usuario).first()
        
        if user:
            messages.error(request, 'Usuário já Cadastrado. Tente novamente.')
            return redirect("professor_cadastro")
        else:
            user = User.objects.create_user(username=usuario, password=senha)
            user.save()
            assign_role(user, 'professor')
            novo_Professor.save()

            messages.error(request, 'Cadastrado com sucesso.')
        return render(request, "professor/login.html")

@has_role_decorator('professor')
def home_professor(request):

    professor_user = request.user.username
    professor = Professor.objects.get(usuario=professor_user)
    professor_idd = professor.matricula
    
    projetos = {
        'projetos': Projeto.objects.filter(professor_id=professor_idd)
    }
    
    return render(request, "professor/index.html", projetos) 

@has_role_decorator('prex') 
def visualizar_edital(request, numero):

    edital = Edital.objects.get(numero=numero)
    alunos_pendentes = Inscricao.objects.filter(edital_id=numero, status= "Pendente")
    alunos_aprovados = Inscricao.objects.filter(edital_id=numero, status= "Aprovado")
    alunos_reprovados = Inscricao.objects.filter(edital_id=numero, status= "Reprovado")
    
    #inscricoes_id = Inscricao.objects.filter(edital_id=numero)

    return render(request, 'prex/edital.html', {"edital": edital, "alunos_pendentes": alunos_pendentes, "alunos_aprovados": alunos_aprovados, "alunos_reprovados": alunos_reprovados})

@has_role_decorator('prex') 
def visualizar_aluno(request, numero):
    aluno = Aluno.objects.get(matricula=numero)
    return render(request, 'prex/aluno.html', {"aluno": aluno} )

@has_role_decorator('prex')
def aprovar_aluno(request):
    edital_num = request.POST.get('edital_numero')
    aluno_mat = request.POST.get('aluno_mat')
    inscricao = Inscricao.objects.get(aluno_id=aluno_mat, edital_id=edital_num)
    
    edital = Edital.objects.get(numero= edital_num)
    
    if edital.n_vagas > 0:
        inscricao.status = 'Aprovado'
        inscricao.save()
        edital.n_vagas = edital.n_vagas - 1
        edital.save()
        messages.error(request, 'Aluno Aprovado')
    else:
        messages.error(request, 'Vagas indisponíveis')
        
    return redirect(f'/prex/edital/{edital_num}')

@has_role_decorator('prex')    
def reprovar_aluno(request):
    edital_num = request.POST.get('edital_numero')
    aluno_mat = request.POST.get('aluno_mat')
    inscricao = Inscricao.objects.get(aluno_id=aluno_mat, edital_id=edital_num)
    
    inscricao.status = 'Reprovado'
    inscricao.justificativa = request.POST.get('justificativa')
    inscricao.save()
    messages.error(request, 'Aluno Reprovado')
    
    return redirect(f'/prex/edital/{edital_num}')

@has_role_decorator('professor')
def ver_projeto(request, numero):
    projeto = Projeto.objects.prefetch_related('relatorio_set').select_related('professor').get(id=numero)
    return render(request, 'professor/projeto.html', {"projeto": projeto} )

@has_role_decorator('professor')
def cria_relatorio(request):
    id_projeto = request.POST.get('projeto')
    projeto = Projeto.objects.get(id=id_projeto)
    relatorio = Relatorio()
    
    print(projeto)
    
    qtd_relatorios = Relatorio.objects.filter(projeto_id_id= id_projeto).count()
    
    doc = request.FILES['documento']
    nome_documento = f"relatorio-{qtd_relatorios + 1}-{id_projeto}.pdf" 
    relatorio.projeto_id = projeto
    relatorio.pdf_edital.save(nome_documento, doc)
    relatorio.save()
    
    messages.error(request, 'Relatório enviado, aguarde o retorno da prex')
    return redirect(reverse('ver_projeto', kwargs={'numero': projeto.id}))

@has_role_decorator('professor')
def edit_projeto(request, numero):
    projeto = Projeto.objects.get(id= numero)
    if request.method == "GET":
        return render(request, 'projeto/edit.html', {'projeto' : projeto})
    else: 
        projeto.nome = request.POST.get('nome')
        projeto.data_de_fim = request.POST.get('data_de_fim')
        projeto.status = request.POST.get('status')
        projeto.save()
    
    messages.error(request, 'Alterações realizadas com sucesso.')      
    return redirect(reverse('ver_projeto', kwargs={'numero': projeto.id}))

@has_role_decorator('prex')
def ver_projeto_prex(request, numero):
    projeto = Projeto.objects.prefetch_related('relatorio_set').select_related('professor').get(id=numero)
    return render(request, 'prex/projeto.html', {"projeto": projeto} )

@has_role_decorator('prex')
def aprovar_relatorio(request, numero):
    relatorio = Relatorio.objects.select_related('projeto_id').get(id=numero)
    relatorio.status = "Aprovado"
    relatorio.save()
    
    messages.error(request, 'Relatório aprovado com sucesso!')
    return redirect(reverse('ver_projeto_prex', kwargs={'numero': relatorio.projeto_id.id}))

@has_role_decorator('prex')
def reprovar_relatorio(request, numero):
    relatorio = Relatorio.objects.select_related('projeto_id').get(id=numero)
    relatorio.status = "Reprovado"
    relatorio.just_reprov = request.POST.get('justificativa')
    relatorio.save()
    
    messages.error(request, 'Relatório reprovado com sucesso!')
    return redirect(reverse('ver_projeto_prex', kwargs={'numero': relatorio.projeto_id.id}))