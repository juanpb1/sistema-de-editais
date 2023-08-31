from django.contrib import admin
from django.urls import path, include
from app_editais import views

import app_editais

urlpatterns = [
    path('', views.home,name='home'),
]
