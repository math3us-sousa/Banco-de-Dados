from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse

def tela_inicial(request):
    return render(request, 'app_viagens/tela_inicial.html')
    
# ========== DESTINOS ==========
def listar_destinos(request):
    if request.method == 'POST':
        nome = request.POST.get('nome') #UNIQUE
        localizacao = request.POST.get('localizacao')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO destinos (nome, localizacao)
                VALUES (%s, %s)
            """, [nome, localizacao])
        return redirect('listar_destinos')

    id_busca = request.GET.get('id_busca')
    if id_busca:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_destino, nome, localizacao
                FROM destinos
                WHERE id_destino = %s
            """, [id_busca])
            destinos = cursor.fetchall()
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_destino, nome, localizacao
                FROM destinos
                ORDER BY nome
            """)
            destinos = cursor.fetchall()

    return render(request, 'app_viagens/destinos.html', {'destinos': destinos})

from django.contrib import messages

def inserir_destino(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        localizacao = request.POST.get('localizacao')

        try:
            with connection.cursor() as cursor:
                # Verifica duplicidade
                cursor.execute("SELECT 1 FROM destinos WHERE name = %s", [name])
                if cursor.fetchone():
                    messages.error(request, 'Já existe um destino com esse nome.')
                    return redirect('listar_destinos')

                cursor.execute(
                    "INSERT INTO destinos (name, localizacao) VALUES (%s, %s)",
                    [name, localizacao]
                )
            return redirect('listar_destinos')

        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')
            return redirect('listar_destinos')

def editar_destino(request, id):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        localizacao = request.POST.get('localizacao')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE destinos
                SET nome = %s, localizacao = %s
                WHERE id_destino = %s
            """, [nome, localizacao, id])
        return redirect('listar_destinos')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_destino, nome, localizacao
            FROM destinos
            WHERE id_destino = %s
        """, [id])
        destino = cursor.fetchone()

    return render(request, 'app_viagens/editar_destino.html', {'destino': destino})

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
    if request.method == 'POST':
        id_destino = request.POST.get('id_destino')
        nome = request.POST.get('nome')
        especialidade = request.POST.get('especialidade')
        contato = request.POST.get('contato')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO guias_locais (id_destino, nome, especialidade, contato)
                VALUES (%s, %s, %s, %s)
            """, [id_destino, nome, especialidade, contato])
        return redirect('listar_guias')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT g.id_guia, g.nome, g.especialidade, g.contato, d.nome
            FROM guias_locais g
            JOIN destinos d ON g.id_destino = d.id_destino
            ORDER BY g.nome
        """)
        guias = cursor.fetchall()

        cursor.execute("SELECT id_destino, nome FROM destinos ORDER BY nome")
        destinos = cursor.fetchall()

    return render(request, 'app_viagens/guias.html', {
        'guias': guias,
        'destinos': destinos
    })


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
        id_destino = request.POST.get('id_destino')
        nome = request.POST.get('nome')
        especialidade = request.POST.get('especialidade')
        contato = request.POST.get('contato')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE guias_locais
                SET id_destino = %s, nome = %s, especialidade = %s, contato = %s
                WHERE id_guia = %s
            """, [id_destino, nome, especialidade, contato, id])
        return redirect('listar_guias')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_guia, id_destino, nome, especialidade, contato
            FROM guias_locais
            WHERE id_guia = %s
        """, [id])
        guia = cursor.fetchone()

    return render(request, 'app_viagens/editar_guia.html', {'guia': guia})


def excluir_guia(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM guias_locais WHERE id_guia = %s", [id])
    return redirect('listar_guias')


# ========== ROTEIROS DE VIAGENS ==========
def listar_roteiros(request):
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

    id_busca = request.GET.get('id_busca')

    with connection.cursor() as cursor:
        # Listagem
        if id_busca:
            cursor.execute("""
                SELECT r.id_roteiro, v.nome, r.data, r.descricao
                FROM roteiros_de_viagens r
                JOIN viajantes v ON r.id_usuario = v.id_viajante
                WHERE r.id_roteiro = %s
                ORDER BY r.data DESC
            """, [id_busca])
            roteiros = cursor.fetchall()
        else:
            cursor.execute("""
                SELECT r.id_roteiro, v.nome, r.data, r.descricao
                FROM roteiros_de_viagens r
                JOIN viajantes v ON r.id_usuario = v.id_viajante
                ORDER BY r.data DESC
            """)
            roteiros = cursor.fetchall()

        cursor.execute("SELECT id_viajante, nome FROM viajantes ORDER BY nome")
        viajantes = cursor.fetchall()

    return render(request, 'app_viagens/roteiros.html', {
        'roteiros': roteiros,
        'viajantes': viajantes
    })

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
        cursor.execute("""
            SELECT id_roteiro, id_usuario, data, descricao
            FROM roteiros_de_viagens
            WHERE id_roteiro = %s
        """, [id])
        roteiro = cursor.fetchone()

    return render(request, 'app_viagens/editar_roteiro.html', {'roteiro': roteiro})

def excluir_roteiro(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM roteiros_de_viagens WHERE id_roteiro = %s", [id])
    return redirect('listar_roteiros')


# ========== ITEM ROTEIRO ==========
def listar_itens_roteiro(request):
    if request.method == 'POST':
        id_roteiro = request.POST.get('id_roteiro')
        id_destino = request.POST.get('id_destino')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO item_roteiro (id_roteiro, id_destino)
                VALUES (%s, %s)
            """, [id_roteiro, id_destino])
        return redirect('listar_itens_roteiro')

    id_busca = request.GET.get('id_busca')

    with connection.cursor() as cursor:
        # Itens listados
        if id_busca:
            cursor.execute("""
                SELECT ir.id_roteiro, r.descricao, ir.id_destino, d.nome
                FROM item_roteiro ir
                JOIN roteiros_de_viagens r ON ir.id_roteiro = r.id_roteiro
                JOIN destinos d ON ir.id_destino = d.id_destino
                WHERE ir.id_roteiro = %s
            """, [id_busca])
            itens = cursor.fetchall()
        else:
            cursor.execute("""
                SELECT ir.id_roteiro, r.descricao, ir.id_destino, d.nome
                FROM item_roteiro ir
                JOIN roteiros_de_viagens r ON ir.id_roteiro = r.id_roteiro
                JOIN destinos d ON ir.id_destino = d.id_destino
                ORDER BY ir.id_roteiro
            """)
            itens = cursor.fetchall()

        # Dropdowns
        cursor.execute("SELECT id_roteiro, descricao FROM roteiros_de_viagens ORDER BY descricao")
        roteiros = cursor.fetchall()

        cursor.execute("SELECT id_destino, nome FROM destinos ORDER BY nome")
        destinos = cursor.fetchall()

    return render(request, 'app_viagens/item_roteiro.html', {
        'itens': itens,
        'roteiros': roteiros,
        'destinos': destinos,
    })



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
    if request.method == 'POST':
        id_roteiro = request.POST.get('id_roteiro')
        id_usuario = request.POST.get('id_usuario')
        data_da_viagem = request.POST.get('data_da_viagem')
        avaliacao = request.POST.get('avaliacao_da_viagem')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO historico_de_viagens (id_roteiro, id_usuario, data_da_viagem, avaliacao_da_viagem)
                VALUES (%s, %s, %s, %s)
            """, [id_roteiro, id_usuario, data_da_viagem, avaliacao])
        return redirect('listar_historicos')

    id_busca = request.GET.get('id_busca')

    with connection.cursor() as cursor:
        # Listagem
        if id_busca:
            cursor.execute("""
                SELECT h.id_historico, r.descricao, v.nome, h.data_da_viagem, h.avaliacao_da_viagem
                FROM historico_de_viagens h
                JOIN roteiros_de_viagens r ON h.id_roteiro = r.id_roteiro
                JOIN viajantes v ON h.id_usuario = v.id_viajante
                WHERE h.id_historico = %s
            """, [id_busca])
            historicos = cursor.fetchall()
        else:
            cursor.execute("""
                SELECT h.id_historico, r.descricao, v.nome, h.data_da_viagem, h.avaliacao_da_viagem
                FROM historico_de_viagens h
                JOIN roteiros_de_viagens r ON h.id_roteiro = r.id_roteiro
                JOIN viajantes v ON h.id_usuario = v.id_viajante
                ORDER BY h.data_da_viagem DESC
            """)
            historicos = cursor.fetchall()

        # Dropdowns
        cursor.execute("SELECT id_roteiro, descricao FROM roteiros_de_viagens ORDER BY descricao")
        roteiros = cursor.fetchall()

        cursor.execute("SELECT id_viajante, nome FROM viajantes ORDER BY nome")
        viajantes = cursor.fetchall()

    return render(request, 'app_viagens/historicos.html', {
        'historicos': historicos,
        'roteiros': roteiros,
        'viajantes': viajantes
    })
    avaliacao = int(request.POST.get('avaliacao_da_viagem'))
    if not (0 <= avaliacao <= 10):
        return JsonResponse({'erro': 'A avaliação deve ser entre 0 e 10.'}, status=400)


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
        id_roteiro = request.POST.get('id_roteiro')
        id_usuario = request.POST.get('id_usuario')
        data = request.POST.get('data_da_viagem')
        avaliacao = request.POST.get('avaliacao_da_viagem')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE historico_de_viagens
                SET id_roteiro = %s, id_usuario = %s, data_da_viagem = %s, avaliacao_da_viagem = %s
                WHERE id_historico = %s
            """, [id_roteiro, id_usuario, data, avaliacao, id])
        return redirect('listar_historicos')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_historico, id_roteiro, id_usuario, data_da_viagem, avaliacao_da_viagem
            FROM historico_de_viagens
            WHERE id_historico = %s
        """, [id])
        historico = cursor.fetchone()

    return render(request, 'app_viagens/editar_historico.html', {'historico': historico})


def excluir_historico(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM historico_de_viagens WHERE id_historico = %s", [id])
    return redirect('listar_historicos')

# ========== VIAJANTES ==========

def listar_viajantes(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        destino_favorito = request.POST.get('destino_favorito')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO viajantes (nome, destino_favorito)
                VALUES (%s, %s)
            """, [nome, destino_favorito])
        return redirect('listar_viajantes')

    id_busca = request.GET.get('id_busca')
    if id_busca:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_viajante, nome, destino_favorito
                FROM viajantes
                WHERE id_viajante = %s
            """, [id_busca])
            viajantes = cursor.fetchall()
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_viajante, nome, destino_favorito
                FROM viajantes
                ORDER BY nome
            """)
            viajantes = cursor.fetchall()

    return render(request, 'app_viagens/viajantes.html', {'viajantes': viajantes})
def inserir_viajante(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        destino_favorito = request.POST.get('destino_favorito')
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO viajantes (nome, destino_favorito)
                VALUES (%s, %s, %s)
            """, [nome, destino_favorito])
        return redirect('listar_viajantes')
    return render(request, 'app_viagens/inserir_viajante.html')
def editar_viajante(request, id):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        destino_favorito = request.POST.get('destino_favorito')
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE viajantes
                SET nome = %s, destino_favorito = %s
                WHERE id_viajante = %s
            """, [nome, destino_favorito, id])
        return redirect('listar_viajantes')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_viajante, nome, destino_favorito
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
    letra = request.GET.get('letra', '').strip()
    id_min = request.GET.get('id_min')
    id_max = request.GET.get('id_max')

    with connection.cursor() as cursor:

        # 1. Média de avaliações por destino
        cursor.execute("""
            SELECT d.nome, AVG(h.avaliacao_da_viagem::numeric) AS media_avaliacao
            FROM historico_de_viagens h
            JOIN roteiros_de_viagens r ON h.id_roteiro = r.id_roteiro
            JOIN item_roteiro ir ON r.id_roteiro = ir.id_roteiro
            JOIN destinos d ON ir.id_destino = d.id_destino
            GROUP BY d.nome
            HAVING AVG(h.avaliacao_da_viagem::numeric) > 3
            ORDER BY media_avaliacao DESC
        """)
        media_avaliacoes = cursor.fetchall()

        # 2. Viajantes com mais viagens este ano
        cursor.execute("""
            SELECT v.nome, COUNT(h.id_historico) AS total_viagens
            FROM viajantes v
            JOIN historico_de_viagens h ON v.id_viajante = h.id_usuario
            WHERE v.id_viajante IN (
                SELECT id_usuario
                FROM historico_de_viagens
                WHERE EXTRACT(YEAR FROM data_da_viagem) = EXTRACT(YEAR FROM CURRENT_DATE)
                GROUP BY id_usuario
            )
            GROUP BY v.nome
            ORDER BY total_viagens DESC
        """)
        viajantes_ativos = cursor.fetchall()

        # 3. Destinos não visitados
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

        # 4. Consulta dinâmica com LIKE + BETWEEN
        if letra and id_min and id_max:
            cursor.execute("""
                SELECT nome, localizacao
                FROM destinos
                WHERE nome ILIKE %s AND id_destino BETWEEN %s AND %s
            """, [letra + '%', id_min, id_max])
            destinos_b_between = cursor.fetchall()
        else:
            destinos_b_between = []

        # 5. União de destinos
        cursor.execute("""
            SELECT nome FROM destinos WHERE id_destino <= 5
            UNION
            SELECT nome FROM destinos WHERE id_destino > 5
        """)
        destinos_union = cursor.fetchall()

        # 6. Destinos em qualquer roteiro
        cursor.execute("""
            SELECT nome
            FROM destinos
            WHERE id_destino = ANY (
                SELECT id_destino FROM item_roteiro
            )
        """)
        destinos_any = cursor.fetchall()

        # 7. Destinos em todos os roteiros
        cursor.execute("SELECT COUNT(*) FROM roteiros_de_viagens")
        total_roteiros = cursor.fetchone()[0]

        cursor.execute("""
            SELECT d.nome
            FROM destinos d
            WHERE d.id_destino IN (
                SELECT ir.id_destino
                FROM item_roteiro ir
                GROUP BY ir.id_destino
                HAVING COUNT(DISTINCT ir.id_roteiro) = %s
            )
        """, [total_roteiros])
        destinos_all = cursor.fetchall()

        # 8. Estatísticas das avaliações
        cursor.execute("""
            SELECT 
                MIN(avaliacao_da_viagem::integer),
                MAX(avaliacao_da_viagem::integer),
                COUNT(*),
                SUM(avaliacao_da_viagem::integer)
            FROM historico_de_viagens
        """)
        min_val, max_val, total_count, sum_val = cursor.fetchone()
        agregacoes = {
            'min': min_val,
            'max': max_val,
            'total': total_count,
            'sum': sum_val
        }
        # 9. Viajantes com destino favorito preenchido (IS NOT NULL)
        cursor.execute("""
            SELECT id_viajante, nome, destino_favorito
            FROM viajantes
            WHERE destino_favorito IS NOT NULL
            ORDER BY nome;
        """)
        viajantes_com_destino = cursor.fetchall()
        # 10. Destinos com ID maior que todos os destinos que começam com Z
        cursor.execute("""
            SELECT nome
            FROM destinos
            WHERE id_destino > ALL (
                SELECT id_destino
                FROM destinos
                WHERE nome LIKE 'Z%'
            )
        """)
        destinos_maior_que_z = cursor.fetchall()



    return render(request, 'app_viagens/consultas_avancadas.html', {
        'media_avaliacoes': media_avaliacoes,
        'viajantes_ativos': viajantes_ativos,
        'destinos_nao_visitados': destinos_nao_visitados,
        'destinos_b_between': destinos_b_between,
        'destinos_union': destinos_union,
        'destinos_any': destinos_any,
        'destinos_all': destinos_all,
        'agregacoes': agregacoes,
        'viajantes_com_destino': viajantes_com_destino,
        'destinos_maior_que_z': destinos_maior_que_z,
    })
