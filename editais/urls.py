"""
URL configuration for editais project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app_editais import views
from django.conf.urls import handler403
from django.conf import settings
from django.conf.urls.static import static

import app_editais

handler403 = 'app_editais.views.permissao_negada'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_editais.urls')),
    path('', views.home, name='home'),
    path('login/prex', views.login_prex, name='login_prex'),
    path('login/aluno', views.aluno_login, name='aluno_login'),
    path('login/professor', views.login_professor, name='login_professor'),
    path('inscricao/', views.inscrever_aluno, name='inscrever_aluno'),
    path('cadastro_aluno', views.create_aluno, name= 'aluno_cadastro'),
    path('criar_projeto', views.create_projeto, name= 'projeto_criar'),
    path('edital/criar', views.create_edital, name='edital_criar'),
    path('edital/<int:numero>/editar', views.edit_edital, name='edital_editar')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
