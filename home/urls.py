"""prescolapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib.auth.views import logout_then_login
from alumnos.views import Index ,AlumnoReporte, Update_Alumno, Detail_Alumno, busquedaAlumno, busquedaTutores, CreateAlumno,  EvaDiario, DiarioReporte
from maestros.views import CreateMaestro, actualizarMaestro, MaestroReporte, buscarMaestros,DetalleMaestro, CreateGrupo, buscarSinGrupo, buscarGrupo, GrupoReporte, infoGrupo, actualizaGrupo,buscarEnelGrupo
from padres.views import login, CreateTutor, tutorAsign,updateTutores, TutoresReporte, Detail_Tutor, ActualizarTutores
#para las fotos
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),#YES...Duh
    path('login/', login, name='login'),#YES#YES
    path('',Index, name='index'), #YES
    
    #url para alumnos 
    path('alumnos/detalles',AlumnoReporte.as_view(),name='alumnos_reporte'),#YES
    path('alumnos/agregar',CreateAlumno.as_view(),name='alumnos_agregarxd'),#YES
    path('updateAlumno/<slug:slug>', Update_Alumno.as_view(), name="UpdateAlumno"),#YES
    path('detalles/<slug:slug>', Detail_Alumno.as_view()),#YES
    path('diario/<slug:slug>', EvaDiario.as_view()),#YES
    path('alumnos/Buscar', busquedaAlumno, name='filtroAlumno'),
    path('reporte/diario', DiarioReporte.as_view(),name="reporteDiario"),#YES

    #url para padres
    path('detalles/tutor/<slug:slug>', Detail_Tutor),#YES
    path('padres/agregar', CreateTutor.as_view(), name="AddTutor"),#YES
    path('actualiza/tutor/<slug:slug>', ActualizarTutores),#YES
    path('addtutor/<slug:slug>', tutorAsign),#YES
    path('tutores/busqueda/',busquedaTutores,name='filtroTutores'),
    
    #url para Maestros
    path('tutor/buscar', TutoresReporte.as_view(), name='reporteTutor'),#YES
    path('maestro/buscar', MaestroReporte.as_view(), name='reporteMaestro'),#YES
    path('maestros/nuevo', CreateMaestro.as_view(), name="add_teacher"),#YES
    path('actualiza/maestro/<slug:slug>',actualizarMaestro),#YES
    path('detalles/maestro/<slug:slug>', DetalleMaestro),#YES
    path('maestros/busqueda/', buscarMaestros),#YES
    path('Actualizar/Tutores', updateTutores),

    #url para Grupos
    path('detalles/grupos/<slug:slug>',infoGrupo),
    path('grupo/buscar', GrupoReporte.as_view(), name='reporteGrupo'),#YES
    path('actualiza/grupo/<slug:slug>', actualizaGrupo ),#YES
    path('grupo/crear', CreateGrupo, name='CreateGrupo'),#Yes
    path('alumnosNG/busqueda/', buscarSinGrupo),
    path('grupos/busqueda/', buscarGrupo),
    path('buscar/alumnosSG/<slug:slug>/', buscarEnelGrupo),
    #LOGOUT
    path('cerrar', logout_then_login, name='logout' ),#YES
          
    ]
#DEBUG TOOLBAR + media
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
