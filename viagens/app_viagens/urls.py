from django.urls import path
from . import views

urlpatterns = [
    # Página Inicial
    path('', views.tela_inicial, name='tela_inicial'),
    
    # ========== DESTINOS ==========
    path('destinos/', views.listar_destinos, name='listar_destinos'),
    path('destinos/inserir/', views.inserir_destino, name='inserir_destino'),
    path('destinos/editar/<int:id>/', views.editar_destino, name='editar_destino'),
    path('destinos/excluir/<int:id>/', views.excluir_destino, name='excluir_destino'),
    path('destinos/detalhes/<int:id>/', views.detalhes_destino, name='detalhes_destino'),
    
    # ========== VIAJANTES ==========
    path('viajantes/', views.listar_viajantes, name='listar_viajantes'),
    path('viajantes/inserir/', views.inserir_viajante, name='inserir_viajante'),
    path('viajantes/editar/<int:id>/', views.editar_viajante, name='editar_viajante'),
    path('viajantes/excluir/<int:id>/', views.excluir_viajante, name='excluir_viajante'),
    
    # ========== ROTEIROS ==========
    path('roteiros/', views.listar_roteiros, name='listar_roteiros'),
    path('roteiros/inserir/', views.inserir_roteiro, name='inserir_roteiro'),
    path('roteiros/editar/<int:id>/', views.editar_roteiro, name='editar_roteiro'),
    path('roteiros/excluir/<int:id>/', views.excluir_roteiro, name='excluir_roteiro'),
    
    # ========== ITENS ROTEIRO ==========
    path('itens-roteiro/', views.listar_itens_roteiro, name='listar_itens_roteiro'),
    path('itens-roteiro/inserir/', views.inserir_item_roteiro, name='inserir_item_roteiro'),
    path('itens-roteiro/excluir/<int:roteiro_id>/<int:destino_id>/', 
         views.excluir_item_roteiro, name='excluir_item_roteiro'),
    
    # ========== GUIAS LOCAIS ==========
    path('guias/', views.listar_guias, name='listar_guias'),
    path('guias/inserir/', views.inserir_guia, name='inserir_guia'),
    path('guias/editar/<int:id>/', views.editar_guia, name='editar_guia'),
    path('guias/excluir/<int:id>/', views.excluir_guia, name='excluir_guia'),
    
    # ========== HISTÓRICOS ==========
    path('historicos/', views.listar_historicos, name='listar_historicos'),
    path('historicos/inserir/', views.inserir_historico, name='inserir_historico'),
    path('historicos/editar/<int:id>/', views.editar_historico, name='editar_historico'),
    path('historicos/excluir/<int:id>/', views.excluir_historico, name='excluir_historico'),
    
   # Consultas Avançadas
    path('consultas/', views.consultas_avancadas, name='consultas_avancadas'),
    
]