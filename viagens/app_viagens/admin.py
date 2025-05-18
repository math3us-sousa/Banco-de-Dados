from django.contrib import admin
from .models import Destinos, GuiasLocais, HistoricoViagens, ItemRoteiro, RoteirosViagens, Viajantes

@admin.register(Destinos)
class DestinosAdmin(admin.ModelAdmin):
    list_display = ('id_destino', 'nome', 'localizacao')
    search_fields = ('nome',)

@admin.register(GuiasLocais)
class GuiasLocaisAdmin(admin.ModelAdmin):
    list_display = ('id_guia', 'nome', 'especialidade', 'contato', 'id_destino')
    list_filter = ('id_destino',)

@admin.register(HistoricoViagens)
class HistoricoViagensAdmin(admin.ModelAdmin):
    list_display = ('id_historico', 'id_roteiro', 'id_usuario', 'data_da_viagem', 'avaliacao_da_viagem')
    date_hierarchy = 'data_da_viagem'

@admin.register(ItemRoteiro)
class ItemRoteiroAdmin(admin.ModelAdmin):
    list_display = ('id_roteiro', 'id_destino')
    list_filter = ('id_roteiro', 'id_destino')

@admin.register(RoteirosViagens)
class RoteirosViagensAdmin(admin.ModelAdmin):
    list_display = ('id_roteiro', 'data', 'descricao')
    search_fields = ('descricao',)

@admin.register(Viajantes)
class ViajantesAdmin(admin.ModelAdmin):
    list_display = ('id_viajante', 'nome', 'destino_favorito', 'data_de_cadastro')
    search_fields = ('nome',)