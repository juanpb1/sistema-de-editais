from django.contrib import admin
from django.urls import path, include
from app_editais import views
from django.conf.urls import handler403

import app_editais

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_editais.urls')),
    path('login/aluno', views.aluno_login, name='aluno_login'),
    path('cadastro_aluno', views.create_aluno, name= 'aluno_cadastro'),
]
