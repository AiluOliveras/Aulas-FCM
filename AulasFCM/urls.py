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
from django.contrib.auth.views import LoginView, LogoutView
from aulasfcm.views import AulasCreate,AulasDelete,AulasDetail,AulasList,AulasUpdate, EdificiosCreate, EdificiosDelete, EdificiosDetail, EdificiosList, EdificiosUpdate
from aulasfcm.views import EntidadesCreate, EntidadesDelete, EntidadesDetail, EntidadesList, EntidadesUpdate
from aulasfcm.views import PasswordChangeView, CustomPasswordChangeView, UsuariosUpdate, CustomUsuariosUpdate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('bienvenida/', include('aulasfcm.urls')),

    path('aulas/', login_required((AulasList.as_view(template_name = "aulas/index.html"))), name='aulas'),
    path('aulas/detalle/<int:pk>', login_required(AulasDetail.as_view(template_name = "aulas/detail.html"))),
    path('aulas/crear', login_required(AulasCreate.as_view(template_name = "aulas/create.html"))),
    path('aulas/editar/<int:pk>', login_required(AulasUpdate.as_view(template_name="aulas/update.html"))),
    path('aulas/eliminar/<int:pk>',login_required(AulasDelete.as_view())),

    path('edificios/', login_required(EdificiosList.as_view(template_name = "edificios/index.html")), name='edificios'),
    path('edificios/detalle/<int:pk>', login_required(EdificiosDetail.as_view(template_name = "edificios/detail.html"))),
    path('edificios/crear', login_required(EdificiosCreate.as_view(template_name = "edificios/create.html"))),
    path('edificios/editar/<int:pk>', login_required(EdificiosUpdate.as_view(template_name="edificios/update.html"))),
    path('edificios/eliminar/<int:pk>', login_required(EdificiosDelete.as_view())),

    path('entidades/', login_required(EntidadesList.as_view(template_name = "entidades/index.html")), name='entidades'),
    path('entidades/detalle/<int:pk>', login_required(EntidadesDetail.as_view(template_name = "entidades/detail.html"))),
    path('entidades/crear', login_required(EntidadesCreate.as_view(template_name = "entidades/create.html"))),
    path('entidades/editar/<int:pk>', login_required(EntidadesUpdate.as_view(template_name="entidades/update.html"))),
    path('entidades/eliminar/<int:pk>', login_required(EntidadesDelete.as_view())),

    path('cambiar-clave/', login_required(PasswordChangeView.as_view(template_name='change-password.html',success_url="/cambiar-clave/exitoso")),name='cambiar-clave'),
    path('cambiar-clave/exitoso', login_required(CustomPasswordChangeView.as_view(template_name='change-password.html',success_url="/cambiar-clave/exitoso")), name = 'cambiar-clave/exitoso'),
    path('cambiar-email/', login_required(UsuariosUpdate.as_view(template_name="change-email.html"))),
    path('cambiar-email/exitoso',login_required(CustomUsuariosUpdate.as_view(template_name='change-email.html')), name = 'cambiar-email/exitoso'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
]
