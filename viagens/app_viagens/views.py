from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse

def tela_inicial(request):
    return render(request, 'app_viagens/tela_inicial.html')
    
# ========== DESTINOS ==========
def listar_destinos(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_destino, nome, localizacao 
            FROM destinos 
            ORDER BY nome
        """)
        destinos = cursor.fetchall()
    return render(request, 'app_viagens/destinos.html', {'destinos': destinos})

def inserir_destino(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        localizacao = request.POST.get('localizacao')
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO destinos (nome, localizacao) VALUES (%s, %s)",
                    [nome, localizacao]
                )
            return redirect('listar_destinos')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return render(request, 'app_viagens/inserir_destino.html')

def editar_destino(request, id):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        localizacao = request.POST.get('localizacao')
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE destinos
                    SET nome = %s, localizacao = %s
                    WHERE id_destino = %s
                """, [nome, localizacao, id])
            return redirect('listar_destinos')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT nome, localizacao FROM destinos WHERE id_destino = %s", [id])
        destino = cursor.fetchone()
    return render(request, 'app_viagens/editar_destino.html', {'destino': destino, 'id': id})

def excluir_destino(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM destinos WHERE id_destino = %s", [id])
    return redirect('listar_destinos')

def detalhes_destino(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT nome, localizacao FROM destinos WHERE id_destino = %s", [id])
        destino = cursor.fetchone()
    return render(request, 'app_viagens/detalhes_destino.html', {'destino': destino})


# ========== GUIAS LOCAIS ==========
def listar_guias(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT g.id_guia, g.nome, g.especialidade, g.contato, d.nome 
            FROM guias_locais g
            JOIN destinos d ON g.id_destino = d.id_destino
        """)
        guias = cursor.fetchall()
    return render(request, 'app_viagens/guias.html', {'guias': guias})

def inserir_guia(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        especialidade = request.POST.get('especialidade')
        contato = request.POST.get('contato')
        id_destino = request.POST.get('id_destino')
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO guias_locais (nome, especialidade, contato, id_destino)
                VALUES (%s, %s, %s, %s)
            """, [nome, especialidade, contato, id_destino])
        return redirect('listar_guias')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_destino, name FROM destinos")
        destinos = cursor.fetchall()
    return render(request, 'app_viagens/inserir_guia.html', {'destinos': destinos})

def editar_guia(request, id):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        especialidade = request.POST.get('especialidade')
        contato = request.POST.get('contato')
        id_destino = request.POST.get('id_destino')
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE guias_locais
                SET nome = %s, especialidade = %s, contato = %s, id_destino = %s
                WHERE id_guia = %s
            """, [nome, especialidade, contato, id_destino, id])
        return redirect('listar_guias')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT nome, especialidade, contato, id_destino FROM guias_locais WHERE id_guia = %s", [id])
        guia = cursor.fetchone()
        cursor.execute("SELECT id_destino, name FROM destinos")
        destinos = cursor.fetchall()
    return render(request, 'app_viagens/editar_guia.html', {'guia': guia, 'destinos': destinos, 'id': id})

def excluir_guia(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM guias_locais WHERE id_guia = %s", [id])
    return redirect('listar_guias')


# ========== ROTEIROS DE VIAGENS ==========
def listar_roteiros(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.id_roteiro, v.nome, r.data, r.descricao 
            FROM roteiros_de_viagens r
            JOIN viajantes v ON r.id_usuario = v.id_viajante
            ORDER BY r.data DESC
        """)
        roteiros = cursor.fetchall()
    return render(request, 'app_viagens/roteiros.html', {'roteiros': roteiros})

def inserir_roteiro(request):
    if request.method == 'POST':
        id_usuario = request.POST.get('id_usuario')
        data = request.POST.get('data')
        descricao = request.POST.get('descricao')
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO roteiros_de_viagens (id_usuario, data, descricao)
                VALUES (%s, %s, %s)
            """, [id_usuario, data, descricao])
        return redirect('listar_roteiros')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_viajante, nome FROM viajantes")
        viajantes = cursor.fetchall()
    return render(request, 'app_viagens/inserir_roteiro.html', {'viajantes': viajantes})

def editar_roteiro(request, id):
    if request.method == 'POST':
        id_usuario = request.POST.get('id_usuario')
        data = request.POST.get('data')
        descricao = request.POST.get('descricao')
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE roteiros_de_viagens
                SET id_usuario = %s, data = %s, descricao = %s
                WHERE id_roteiro = %s
            """, [id_usuario, data, descricao, id])
        return redirect('listar_roteiros')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_usuario, data, descricao FROM roteiros_de_viagens WHERE id_roteiro = %s", [id])
        roteiro = cursor.fetchone()
        cursor.execute("SELECT id_viajante, nome FROM viajantes")
        viajantes = cursor.fetchall()
    return render(request, 'app_viagens/editar_roteiro.html', {'roteiro': roteiro, 'id': id, 'viajantes': viajantes})

def excluir_roteiro(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM roteiros_de_viagens WHERE id_roteiro = %s", [id])
    return redirect('listar_roteiros')

# ========== ITEM ROTEIRO ==========
def listar_itens_roteiro(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ir.id_roteiro, r.descricao, ir.id_destino, d.nome
            FROM item_roteiro ir
            JOIN roteiros_de_viagens r ON ir.id_roteiro = r.id_roteiro
            JOIN destinos d ON ir.id_destino = d.id_destino
        """)
        itens = cursor.fetchall()
    return render(request, 'app_viagens/item_roteiro.html', {'itens': itens})

def inserir_item_roteiro(request):
    if request.method == 'POST':
        id_roteiro = request.POST.get('id_roteiro')
        id_destino = request.POST.get('id_destino')
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO item_roteiro (id_roteiro, id_destino)
                VALUES (%s, %s)
            """, [id_roteiro, id_destino])
        return redirect('listar_itens_roteiro')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_roteiro, descricao FROM roteiros_de_viagens")
        roteiros = cursor.fetchall()
        cursor.execute("SELECT id_destino, name FROM destinos")
        destinos = cursor.fetchall()
    return render(request, 'app_viagens/inserir_item_roteiro.html', {'roteiros': roteiros, 'destinos': destinos})

def excluir_item_roteiro(request, roteiro_id, destino_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM item_roteiro
            WHERE id_roteiro = %s AND id_destino = %s
        """, [roteiro_id, destino_id])
    return redirect('listar_itens_roteiro')


# ========== HISTÓRICO DE VIAGENS ==========
def listar_historicos(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT h.id_historico, r.descricao, v.nome, h.data_da_viagem, 
                   h.avaliacao_da_viagem
            FROM historico_de_viagens h
            JOIN roteiros_de_viagens r ON h.id_roteiro = r.id_roteiro
            JOIN viajantes v ON h.id_usuario = v.id_viajante
            WHERE h.data_da_viagem IS NOT NULL
            ORDER BY h.data_da_viagem DESC
        """)
        historicos = cursor.fetchall()
    return render(request, 'app_viagens/historicos.html', {'historicos': historicos})

def inserir_historico(request):
    if request.method == 'POST':
        id_usuario = request.POST.get('id_usuario')
        id_roteiro = request.POST.get('id_roteiro')
        data_viagem = request.POST.get('data_viagem')
        comentario = request.POST.get('comentario')
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO historico_de_viagens (id_usuario, id_roteiro, data_viagem, comentario)
                VALUES (%s, %s, %s, %s)
            """, [id_usuario, id_roteiro, data_viagem, comentario])
        return redirect('listar_historico')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_viajante, nome FROM viajantes")
        viajantes = cursor.fetchall()
        cursor.execute("SELECT id_roteiro, descricao FROM roteiros_de_viagens")
        roteiros = cursor.fetchall()
    return render(request, 'app_viagens/inserir_historico.html', {
        'viajantes': viajantes,
        'roteiros': roteiros
    })

def editar_historico(request, id):
    if request.method == 'POST':
        id_usuario = request.POST.get('id_usuario')
        id_roteiro = request.POST.get('id_roteiro')
        data_viagem = request.POST.get('data_viagem')
        comentario = request.POST.get('comentario')
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE historico_de_viagens
                SET id_usuario = %s, id_roteiro = %s, data_viagem = %s, comentario = %s
                WHERE id_historico = %s
            """, [id_usuario, id_roteiro, data_viagem, comentario, id])
        return redirect('listar_historico')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_usuario, id_roteiro, data_viagem, comentario FROM historico_de_viagens WHERE id_historico = %s", [id])
        historico = cursor.fetchone()
        cursor.execute("SELECT id_viajante, nome FROM viajantes")
        viajantes = cursor.fetchall()
        cursor.execute("SELECT id_roteiro, descricao FROM roteiros_de_viagens")
        roteiros = cursor.fetchall()
    return render(request, 'app_viagens/editar_historico.html', {
        'historico': historico,
        'id': id,
        'viajantes': viajantes,
        'roteiros': roteiros
    })

def excluir_historico(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM historico_de_viagens WHERE id_historico = %s", [id])
    return redirect('listar_historico')



# ========== VIAJANTES ==========

def listar_viajantes(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        destino_favorito = request.POST.get('destino_favorito')
        data_cadastro = request.POST.get('data_cadastro')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO viajantes (nome, destino_favorito, data_de_cadastro)
                VALUES (%s, %s, %s)
            """, [nome, destino_favorito, data_cadastro])
        return redirect('listar_viajantes')

    id_busca = request.GET.get('id_busca')
    if id_busca:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_viajante, nome, destino_favorito, data_de_cadastro
                FROM viajantes
                WHERE id_viajante = %s
            """, [id_busca])
            viajantes = cursor.fetchall()
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_viajante, nome, destino_favorito, data_de_cadastro
                FROM viajantes
                ORDER BY nome
            """)
            viajantes = cursor.fetchall()

    return render(request, 'app_viagens/viajantes.html', {'viajantes': viajantes})
def inserir_viajante(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        destino_favorito = request.POST.get('destino_favorito')
        data_cadastro = request.POST.get('data_cadastro')
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO viajantes (nome, destino_favorito, data_de_cadastro)
                VALUES (%s, %s, %s)
            """, [nome, destino_favorito, data_cadastro])
        return redirect('listar_viajantes')
    return render(request, 'app_viagens/inserir_viajante.html')
def editar_viajante(request, id):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        destino_favorito = request.POST.get('destino_favorito')
        data_cadastro = request.POST.get('data_cadastro')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE viajantes
                SET nome = %s, destino_favorito = %s, data_de_cadastro = %s
                WHERE id_viajante = %s
            """, [nome, destino_favorito, data_cadastro, id])
        return redirect('listar_viajantes')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_viajante, nome, destino_favorito, data_de_cadastro
            FROM viajantes
            WHERE id_viajante = %s
        """, [id])
        viajante = cursor.fetchone()

    return render(request, 'app_viagens/editar_viajante.html', {'viajante': viajante})

def excluir_viajante(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM viajantes WHERE id_viajante = %s", [id])
    return redirect('listar_viajantes')

   # ========== CONSULTAS COMPLEXAS ==========
def consultas_avancadas(request):
    # Consulta 1: Média de avaliações por destino (GROUP BY)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT d.nome, AVG(h.avaliacao_da_viagem::numeric) as media_avaliacao
            FROM historico_de_viagens h
            JOIN roteiros_de_viagens r ON h.id_roteiro = r.id_roteiro
            JOIN item_roteiro ir ON r.id_roteiro = ir.id_roteiro
            JOIN destinos d ON ir.id_destino = d.id_destino
            GROUP BY d.nome
            HAVING AVG(h.avaliacao_da_viagem::numeric) > 3
            ORDER BY media_avaliacao DESC
        """)
        media_avaliacoes = cursor.fetchall()

    # Consulta 2: Viajantes com mais viagens (Subconsulta com IN)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT v.nome, COUNT(h.id_historico) as total_viagens
            FROM viajantes v
            JOIN historico_de_viagens h ON v.id_viajante = h.id_usuario
            WHERE v.id_viajante IN (
                SELECT id_usuario 
                FROM historico_de_viagens 
                WHERE EXTRACT(YEAR FROM data_da_viagem) = EXTRACT(YEAR FROM CURRENT_DATE)
            GROUP BY v.nome
            ORDER BY total_viagens DESC
        """)
        viajantes_ativos = cursor.fetchall()

    # Consulta 3: Destinos não visitados (EXISTS/NOT EXISTS)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT d.nome
            FROM destinos d
            WHERE NOT EXISTS (
                SELECT 1 FROM item_roteiro ir
                JOIN roteiros_de_viagens r ON ir.id_roteiro = r.id_roteiro
                JOIN historico_de_viagens h ON r.id_roteiro = h.id_roteiro
                WHERE ir.id_destino = d.id_destino
            )
        """)
        destinos_nao_visitados = cursor.fetchall()

    return render(request, 'app_viagens/consultas.html', {
        'media_avaliacoes': media_avaliacoes,
        'viajantes_ativos': viajantes_ativos,
        'destinos_nao_visitados': destinos_nao_visitados
    })
 