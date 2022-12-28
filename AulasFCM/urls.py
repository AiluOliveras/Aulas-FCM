"""AulasFCM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from aulasfcm.views import AulasCreate,AulasDelete,AulasDetail,AulasList,AulasUpdate, EdificiosCreate, EdificiosDelete, EdificiosDetail, EdificiosList, EdificiosUpdate

urlpatterns = [
    path('bienvenida/', include('aulasfcm.urls')),
    path('aulas/', AulasList.as_view(template_name = "aulas/index.html"), name='aulas'),
    path('aulas/detalle/<int:pk>', AulasDetail.as_view(template_name = "aulas/detail.html")),
    path('aulas/crear', AulasCreate.as_view(template_name = "aulas/create.html")),
    path('aulas/editar/<int:pk>', AulasUpdate.as_view(template_name="aulas/update.html")),
    path('aulas/eliminar/<int:pk>',AulasDelete.as_view()),

    path('edificios/', EdificiosList.as_view(template_name = "edificios/index.html"), name='edificios'),
    path('edificios/detalle/<int:pk>', EdificiosDetail.as_view(template_name = "edificios/detail.html")),
    path('edificios/crear', EdificiosCreate.as_view(template_name = "edificios/create.html")),
    path('edificios/editar/<int:pk>', EdificiosUpdate.as_view(template_name="edificios/update.html")),
    path('edificios/eliminar/<int:pk>', EdificiosDelete.as_view()),

    path('admin/', admin.site.urls),
]
