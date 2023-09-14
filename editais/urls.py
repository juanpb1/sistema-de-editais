from django.contrib import admin
from django.urls import path, include
from app_editais import views
from django.conf.urls import handler403

import app_editais

handler403 = 'app_editais.views.permissao_negada'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_editais.urls')),
    path('', views.home, name='home'),
    path('login/prex', views.login_prex, name='login_prex'),
    path('login/aluno', views.aluno_login, name='aluno_login'),
    path('inscricao/', views.inscrever_aluno, name='inscrever_aluno'),
    path('cadastro_prex', views.create_prex, name='formulario_prex'),
    path('cadastro_aluno', views.create_aluno, name= 'aluno_cadastro'),
    path('criar_edital', views.create_edital, name='edital_criar')
]


