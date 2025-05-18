from django.db import models

class Destinos(models.Model):
    id_destino = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)  # Chave candidata (UNIQUE)
    localizacao = models.CharField(max_length=100)

    class Meta:
        app_label = 'app_viagens'
        managed = False  # Tabela já existe no banco
        db_table = 'destinos'

    def __str__(self):
        return f"{self.nome} ({self.localizacao})"


class GuiasLocais(models.Model):
    id_guia = models.AutoField(primary_key=True)
    id_destino = models.ForeignKey(Destinos, on_delete=models.DO_NOTHING, db_column='id_destino')
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100)
    contato = models.CharField(max_length=50)

    class Meta:
        app_label = 'app_viagens'
        managed = False
        db_table = 'guias_locais'

    def __str__(self):
        return f"{self.nome} - {self.especialidade}"


class RoteirosViagens(models.Model):
    id_roteiro = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Viajantes', on_delete=models.CASCADE, db_column='id_usuario')  # Novo campo
    data = models.DateField()
    descricao = models.TextField()

    class Meta:
        app_label = 'app_viagens'
        managed = False
        db_table = 'roteiros_de_viagens'

class ItemRoteiro(models.Model):
    id_roteiro = models.ForeignKey(
        'RoteirosViagens', 
        on_delete=models.CASCADE,
        db_column='id_roteiro',
        primary_key=False  # Parte 1 da chave composta
    )
    id_destino = models.ForeignKey(
        'Destinos', 
        on_delete=models.DO_NOTHING,
        db_column='id_destino',
        primary_key=False  # Não pode ter dois primary_key=True
    )

    class Meta:
        app_label = 'app_viagens'
        managed = False
        db_table = 'item_roteiro'
        unique_together = (('id_roteiro', 'id_destino'),)  # Chave composta real
        # Removido id_item pois agora a chave é composta

    def __str__(self):
        return f"Roteiro {self.id_roteiro_id} - Destino {self.id_destino_id}"


class Viajantes(models.Model):
    id_viajante = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    destino_favorito = models.CharField(max_length=100, blank=True, null=True)
    data_de_cadastro = models.DateField()  # Nome corrigido (era data_de_cadastr)

    class Meta:
        app_label = 'app_viagens'
        managed = False
        db_table = 'viajantes'


class HistoricoViagens(models.Model):
    id_historico = models.AutoField(primary_key=True)
    id_roteiro = models.ForeignKey(RoteirosViagens, on_delete=models.DO_NOTHING, db_column='id_roteiro')
    id_usuario = models.ForeignKey('Viajantes', on_delete=models.DO_NOTHING, db_column='id_usuario')
    data_da_viagem = models.DateField()
    avaliacao_da_viagem = models.TextField(blank=True, null=True)  # Tipo text, não integer

    class Meta:
        app_label = 'app_viagens'
        managed = False
        db_table = 'historico_de_viagens'