from django.contrib import admin
from django.urls import path, include
from app_editais import views
import app_editais

urlpatterns = [
    # path('', views.home,name='home'),
    path('prex', views.prex, name='prex'),
    path('professor', views.home_professor, name='professor'),
    path('prex/cadastro', views.create_prex,name='prex_cadastro'),
    path('professor/cadastro', views.create_professor,name='professor_cadastro'),
    path('prex/message', views.prex_message, name='prex_message'),
    path('aluno', views.aluno_home, name='aluno_home'),
    path('aluno/cadastro', views.aluno_cadastro, name='aluno_cadastro'),
    path('aluno/message', views.aluno_message, name='aluno_message'),
    path('aluno/status', views.status_editais, name='status_editais'),
    # path('edital/criar', views.edital_criar, name='edital_criar'),
    path('edital/message', views.edital_message, name='edital_message'),
    path('logout', views.logout_view, name='logout'),
    path('projeto/criar', views.projeto_criar, name='projeto_criar'),
    path('projeto/message', views.projeto_message, name= 'projeto_message'),
    path('prex/edital/<int:numero>', views.visualizar_edital, name='visualizar_edital'),
    path('prex/aluno/<int:numero>', views.visualizar_aluno, name='visualizar_aluno'),
    path('aprovar/', views.aprovar_aluno, name='aprovar_aluno'),
    path('reprovar/', views.reprovar_aluno, name='reprovar_aluno'),

]

