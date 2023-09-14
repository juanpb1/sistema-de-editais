from django.contrib import admin
from django.urls import path, include
from app_editais import views

import app_editais

urlpatterns = [
    path('', views.home,name='home'),
    path('prex/create', views.prex,name='prex'),
    path('edital/criar', views.edital_criar, name='edital_criar'),
    path('aluno', views.aluno_home, name='aluno_home'),
    path('aluno/cadastro', views.aluno_cadastro, name='aluno_cadastro'),
    path('aluno/message', views.aluno_message, name='aluno_message'),
    path('edital/message', views.edital_message, name='edital_message'),
    path('criar_edital', views.create_edital, name='edital_criar')
]
