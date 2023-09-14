from django.contrib import admin
from django.urls import path, include

import app_editais

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_editais.urls'))
]
