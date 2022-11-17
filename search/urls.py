from django.urls import path
from django.shortcuts import HttpResponse
import search.views as views

def home(request):
    return HttpResponse('hola')

urlpatterns = [
    # Home
    path('', views.Home, name=''),
    path('datasets', views.Datasets, name='datasets')
]

'''
    # BD
    path('bd/', views.QueryBd, name='bd'),
    path('bd/actividades/', views.QueryActividades, name='actividades'),
    path('bd/barrios/', views.QueryBarrios, name='barrios'),
    path('bd/conocimientos/', views.QueryConocimientos, name='conocimientos'),
    path('bd/habilidades/', views.QueryHabilidades, name='habilidades'),
    path('bd/lugares/', views.QueryLugares, name='lugares'),
    path('bd/mascotas/', views.QueryMascotas, name='mascotas'),
    path('bd/misiones/', views.QueryMisiones, name='misiones'),
    path('bd/mundos/', views.QueryMundos, name='mundos'),
    path('bd/profesiones/', views.QueryProfesiones, name='profesiones'),
    path('bd/sims/', views.QuerySims, name='sims'),
    path('bd/unidades_domesticas/', views.QueryUnidadesDomesticas, name='unidades_domesticas'),
    path('bd/viajeros', views.QueryViajeros, name='viajeros'),

    # Frontend
    # path('game/')



    #Simulaciones
    path('simulacion/', views.Simulacion, name='simulacion'),
    path('simulacion/viajeros/', views.Simular_Viajeros, name='viajar'),
    path('simulacion/misiones/', views.Simular_Misiones, name='hacer_mision'),
    path('simulacion/actividades/', views.Simular_Actividades, name='hacer_actividad'),



    #Creacion
    path('creacion/unidades_domesticas/', views.CrearUnidadDomestica, name='crear_unidad_domestica'),
    path('creacion/sim/', views.CrearSim, name='crear_sim'),
    path('creacion/mascota/', views.CrearSim, name='crear_mascota'),

    #Consultas
    path('consultas/', views.Queries, name='queries')
'''