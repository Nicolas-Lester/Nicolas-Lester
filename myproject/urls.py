"""
URL configuration for myproject project.

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
from django.urls import path
from myapp import views
from django.views.generic.base import RedirectView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),  #
    path('identificador', views.Identificador, name='identificador'),
    path('', views.home_infosu, name='home_infosu'),
    path('phpmyadmin/', RedirectView.as_view(url='http://localhost/phpmyadmin/'), name='phpmyadmin'),
    path('empleador_register/', views.empleador_register_view, name='empleador_register'),
    path('empleador_login/', views.empleador_login_view, name='empleador_login'),
    path('empleador_logout/', views.empleador_logout_view, name='empleador_logout'),
    path('empleador_dashboard/', views.empleador_dashboard_view, name='empleador_dashboard'),
    path('mostrarcandidato/', views.mostrar_candidatos, name='mostrarcandidato'),
    path('empleador/descargar-archivo-candidato/<int:candidato_perfil_id>/<str:archivo>/', views.descargar_archivo_candidato, name='descargar_archivo_candidato'),
    path('asignar_puesto/', views.empleador_dashboard_view, name='empleador_dashboard_view'),
    path('asignarpuesto/', views.asignarpuesto, name='asignarpuesto'),
    path('reset_password/', views.reset_password, name='reset_password'),
    
   

    
   
]

