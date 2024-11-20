

from django.urls import path
from . import views


app_name = 'epicfantasiesapp'

urlpatterns = [
    path('', views.home , name='home'),
    path('entrar', views.entrar , name='entrar'),
    path('entrar/codigodeverificacao/', views.verificacao , name='codigodeverificacao'),

    path('cadastrar', views.cadastrar , name='cadastrar'), 
    path('meuPerfil', views.perfilUsuario , name='meuPerfilU'),
    path('historias/<int:id>/', views.storyDetalhes , name='storyDetalhes'),
    path('categoria/<int:category>',views.categoria,name="categoria"),

    path('meuPerfilUpdate', views.perfilUsuarioUpdate , name='meuPerfilUpdate'),

    path('meuPerfilStory', views.meuPerfilStory , name='meuPerfilStory'),
    path('editar_historia/<int:id>/', views.editarHistoria , name='editarHistoria'),

    path('api/comentario/<int:id>/', views.comentario , name='comentario'),  
    path('api/emocao/<int:id>/', views.emocao , name='emocao'), 
    path('api/denuncia/<int:id>/', views.denuncia , name='denuncia'),  
    path('api/thumbnail/', views.thumbnail , name='thumbnail'),  
    

    path('meuPerfilAdministrador', views.perfilAdministrador , name='meuPerfilA'),
    path('feed', views.feed , name='feed'), 
    path('sair', views.sair , name='sair'),


    path('system/redirecionamento/<int:id>/', views.redirecionamento , name='redirecionamento'),


]
