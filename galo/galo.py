from pyscript import document, when
import asyncio
import random

# REMOVER ECRA DE CARREGAMENTO
loading = document.getElementById("loading")
if loading:
    loading.remove()


# =====================================
# WIDGET 2 - JOGO DO GALO COM DIFICULDADES
# =====================================

# Configuracoes e estado
modo_jogo = "cpu"          # "cpu" (vs computador) ou "pvp" (2 jogadores offline)
dificuldade = "medio"      # "facil", "medio", "dificil"
jogador_atual = "X"        # "X" comeca sempre
tabuleiro = [""] * 9
jogo_ativo = True
bloqueio_input = False     # Bloqueia cliques durante animacoes e turno do bot

# Placar
vitorias_x = 0
vitorias_o = 0
empates = 0

COMBINACOES_VITORIA = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
    [0, 4, 8], [2, 4, 6]              # Diagonais
]


def atualizar_interface():
    """Renderiza as pecas no tabuleiro e atualiza o placar."""
    for i in range(9):
        celula = document.getElementById(f"cell-{i}")
        if celula:
            valor = tabuleiro[i]
            celula.innerText = valor
            celula.className = "galo-cell"

            if valor == "X":
                celula.classList.add("cell--x")
            elif valor == "O":
                celula.classList.add("cell--o")

    # Atualizar placar
    doc_vx = document.getElementById("score-x")
    doc_vo = document.getElementById("score-o")
    doc_emp = document.getElementById("score-empates")

    if doc_vx:
        doc_vx.innerText = str(vitorias_x)
    if doc_vo:
        doc_vo.innerText = str(vitorias_o)
    if doc_emp:
        doc_emp.innerText = str(empates)


def verificar_fim_jogo(tab_param=None):
    """Verifica se ha vitoria ou empate num determinado tabuleiro."""
    tab = tab_param if tab_param is not None else tabuleiro

    for a, b, c in COMBINACOES_VITORIA:
        if tab[a] != "" and tab[a] == tab[b] == tab[c]:
            return tab[a], [a, b, c]

    if "" not in tab:
        return "empate", []

    return None, []


def destacar_vencedores(indices):
    """Realca a linha vitoriosa de 3 em linha."""
    for idx in indices:
        celula = document.getElementById(f"cell-{idx}")
        if celula:
            celula.classList.add("cell--winner")


def definir_status(texto, cor=None):
    """Atualiza o texto de estado do jogo."""
    status_el = document.getElementById("galo-status")
    if status_el:
        status_el.innerText = texto
        if cor:
            status_el.style.color = cor
        else:
            status_el.style.color = "var(--text)"


# =====================================
# INTELIGENCIA ARTIFICIAL & DIFICULDADES
# =====================================

def jogada_ganhar_ou_bloquear():
    """Tenta vencer ou bloquear imediatamente."""
    # 1. Tentar vencer
    for a, b, c in COMBINACOES_VITORIA:
        linha = [tabuleiro[a], tabuleiro[b], tabuleiro[c]]
        if linha.count("O") == 2 and linha.count("") == 1:
            for pos in [a, b, c]:
                if tabuleiro[pos] == "":
                    return pos

    # 2. Bloquear jogador X
    for a, b, c in COMBINACOES_VITORIA:
        linha = [tabuleiro[a], tabuleiro[b], tabuleiro[c]]
        if linha.count("X") == 2 and linha.count("") == 1:
            for pos in [a, b, c]:
                if tabuleiro[pos] == "":
                    return pos

    # 3. Centro se livre
    if tabuleiro[4] == "":
        return 4

    return None


def minimax(tab, profundidade, is_max):
    """Algoritmo Minimax para o modo Dificil (imbativel)."""
    resultado, _ = verificar_fim_jogo(tab)

    if resultado == "O":
        return 10 - profundidade
    elif resultado == "X":
        return profundidade - 10
    elif resultado == "empate":
        return 0

    if is_max:
        melhor = -1000
        for i in range(9):
            if tab[i] == "":
                tab[i] = "O"
                pontos = minimax(tab, profundidade + 1, False)
                tab[i] = ""
                melhor = max(melhor, pontos)
        return melhor
    else:
        melhor = 1000
        for i in range(9):
            if tab[i] == "":
                tab[i] = "X"
                pontos = minimax(tab, profundidade + 1, True)
                tab[i] = ""
                melhor = min(melhor, pontos)
        return melhor


def jogada_minimax():
    """Calcula a melhor jogada possivel usando Minimax."""
    # Otimizacao de abertura: se o centro estiver livre no 1º turno do bot
    if tabuleiro.count("") >= 7 and tabuleiro[4] == "":
        return 4

    melhor_val = -1000
    melhor_jogada = None

    espacos = [i for i, v in enumerate(tabuleiro) if v == ""]
    random.shuffle(espacos)

    for i in espacos:
        tabuleiro[i] = "O"
        val = minimax(tabuleiro, 0, False)
        tabuleiro[i] = ""
        if val > melhor_val:
            melhor_val = val
            melhor_jogada = i

    return melhor_jogada if melhor_jogada is not None else random.choice(espacos)


def calcular_jogada_computador():
    """Seleciona a jogada consoante o nivel de dificuldade."""
    espacos_livres = [i for i, v in enumerate(tabuleiro) if v == ""]
    if not espacos_livres:
        return None

    if dificuldade == "facil":
        # Nivel Facil: jogadas 100% aleatorias
        return random.choice(espacos_livres)

    elif dificuldade == "medio":
        # Nivel Medio: 50% das vezes joga inteligente, 50% joga aleatorio
        if random.random() < 0.5:
            smart = jogada_ganhar_ou_bloquear()
            if smart is not None:
                return smart
        return random.choice(espacos_livres)

    elif dificuldade == "dificil":
        # Nivel Dificil: estrategia Minimax perfeita
        return jogada_minimax()

    return random.choice(espacos_livres)


# =====================================
# ANIMACAO DE FIM DE PARTIDA (POPUP)
# =====================================

async def mostrar_animacao_resultado(tipo, vencedor=None):
    """Exibe o modal animado de celebracao de fim de jogo."""
    await asyncio.sleep(0.35)

    overlay = document.getElementById("galo-result-overlay")
    box = document.getElementById("result-modal-box")
    icon = document.getElementById("result-icon")
    title = document.getElementById("result-title")
    msg = document.getElementById("result-message")

    if not overlay or not box:
        return

    box.className = "result-modal"
    nome_dif = {"facil": "Fácil", "medio": "Médio", "dificil": "Difícil"}.get(dificuldade, "Médio")

    if tipo == "vitoria_cpu_humano":
        box.classList.add("modal--win")
        if icon: icon.innerText = "🏆"
        if title: title.innerText = "Vitória! 🎉"
        if msg: msg.innerText = f"Fantástico! Conseguiste vencer o Computador em nível {nome_dif}!"

    elif tipo == "derrota_cpu":
        box.classList.add("modal--loss")
        if icon: icon.innerText = "🤖"
        if title: title.innerText = "O Computador Venceu!"
        if msg: msg.innerText = f"O computador superou-te no nível {nome_dif}. Tenta novamente para te desforrares!"

    elif tipo == "vitoria_pvp":
        box.classList.add("modal--win")
        if icon: icon.innerText = "👑"
        if title: title.innerText = f"Vitória do Jogador {vencedor}!"
        if msg: msg.innerText = f"Parabéns ao Jogador {vencedor} por completar 3 em linha com sucesso!"

    elif tipo == "empate":
        box.classList.add("modal--draw")
        if icon: icon.innerText = "🤝"
        if title: title.innerText = "Jogo Empatado!"
        if msg: msg.innerText = "Ninguém cedeu terreno nesta partida. Um duelo renhido!"

    overlay.classList.remove("hidden")
    overlay.classList.add("active")


def fechar_modal_resultado():
    """Fecha a janela animada de resultado."""
    overlay = document.getElementById("galo-result-overlay")
    if overlay:
        overlay.classList.remove("active")
        overlay.classList.add("hidden")


@when("click", "#btn-play-again")
def ao_clicar_jogar_novamente(event):
    fechar_modal_resultado()
    reiniciar_partida()


@when("click", "#result-backdrop")
def ao_clicar_fundo_resultado(event):
    fechar_modal_resultado()


# =====================================
# FLUXO DE JOGO
# =====================================

async def executar_jogada(posicao):
    """Processa a jogada na posicao indicada."""
    global jogador_atual, jogo_ativo, vitorias_x, vitorias_o, empates, bloqueio_input

    if not jogo_ativo or tabuleiro[posicao] != "" or bloqueio_input:
        return

    # Registar peca
    tabuleiro[posicao] = jogador_atual
    atualizar_interface()

    # Verificar se terminou com esta jogada
    resultado, celulas_ganhadoras = verificar_fim_jogo()

    if resultado:
        jogo_ativo = False

        if resultado == "empate":
            empates += 1
            definir_status("Jogo empatado! Ninguém fez 3 em linha. 🤝", "#85838f")
            atualizar_interface()
            await mostrar_animacao_resultado("empate")
        else:
            destacar_vencedores(celulas_ganhadoras)
            if resultado == "X":
                vitorias_x += 1
                if modo_jogo == "cpu":
                    definir_status("Vitória! Venceste o Computador! 🎉", "#28a745")
                    atualizar_interface()
                    await mostrar_animacao_resultado("vitoria_cpu_humano")
                else:
                    definir_status("Vitória do Jogador X! 🎉", "#8064d8")
                    atualizar_interface()
                    await mostrar_animacao_resultado("vitoria_pvp", "X")
            else:
                vitorias_o += 1
                if modo_jogo == "cpu":
                    definir_status("O Computador venceu desta vez! 🤖", "#ff6b6b")
                    atualizar_interface()
                    await mostrar_animacao_resultado("derrota_cpu")
                else:
                    definir_status("Vitória do Jogador O! 🎉", "#ff6b6b")
                    atualizar_interface()
                    await mostrar_animacao_resultado("vitoria_pvp", "O")
        return

    # Alternar vez
    if modo_jogo == "pvp":
        jogador_atual = "O" if jogador_atual == "X" else "X"
        definir_status(f"Vez de jogar: Jogador {jogador_atual}")

    elif modo_jogo == "cpu":
        # Vez do computador
        jogador_atual = "O"
        definir_status("O computador está a pensar... 🤖")
        bloqueio_input = True

        # Pausa para dar sensacao natural de pensamento
        await asyncio.sleep(0.4)

        jogada_cpu = calcular_jogada_computador()
        bloqueio_input = False

        if jogada_cpu is not None and jogo_ativo:
            tabuleiro[jogada_cpu] = "O"
            atualizar_interface()

            res_cpu, celulas_cpu = verificar_fim_jogo()
            if res_cpu:
                jogo_ativo = False
                if res_cpu == "empate":
                    empates += 1
                    definir_status("Jogo empatado! 🤝", "#85838f")
                    atualizar_interface()
                    await mostrar_animacao_resultado("empate")
                else:
                    vitorias_o += 1
                    destacar_vencedores(celulas_cpu)
                    definir_status("O Computador venceu! 🤖", "#ff6b6b")
                    atualizar_interface()
                    await mostrar_animacao_resultado("derrota_cpu")
            else:
                jogador_atual = "X"
                definir_status("A tua vez (Jogador X)!")


@when("click", "#galo-board")
async def ao_clicar_tabuleiro(event):
    target = event.target
    if not target:
        return

    botao = None
    try:
        botao = target.closest(".galo-cell")
    except Exception:
        if "galo-cell" in getattr(target, "className", ""):
            botao = target

    if not botao:
        return

    idx_str = botao.getAttribute("data-index")
    if idx_str is not None:
        posicao = int(idx_str)
        await executar_jogada(posicao)


# =====================================
# MODOS & DIFICULDADES
# =====================================

@when("click", "#mode-cpu")
def mudar_modo_cpu(event):
    global modo_jogo
    modo_jogo = "cpu"

    btn_cpu = document.getElementById("mode-cpu")
    btn_pvp = document.getElementById("mode-pvp")
    label_o = document.getElementById("label-score-o")
    diff_container = document.getElementById("difficulty-container")

    if btn_cpu: btn_cpu.classList.add("active")
    if btn_pvp: btn_pvp.classList.remove("active")
    if label_o: label_o.innerText = "Computador (O)"
    if diff_container: diff_container.style.display = "flex"

    reiniciar_partida()


@when("click", "#mode-pvp")
def mudar_modo_pvp(event):
    global modo_jogo
    modo_jogo = "pvp"

    btn_cpu = document.getElementById("mode-cpu")
    btn_pvp = document.getElementById("mode-pvp")
    label_o = document.getElementById("label-score-o")
    diff_container = document.getElementById("difficulty-container")

    if btn_pvp: btn_pvp.classList.add("active")
    if btn_cpu: btn_cpu.classList.remove("active")
    if label_o: label_o.innerText = "Jogador O"
    if diff_container: diff_container.style.display = "none"

    reiniciar_partida()


@when("click", "#diff-facil")
def definir_diff_facil(event):
    atualizar_dificuldade("facil")


@when("click", "#diff-medio")
def definir_diff_medio(event):
    atualizar_dificuldade("medio")


@when("click", "#diff-dificil")
def definir_diff_dificil(event):
    atualizar_dificuldade("dificil")


def atualizar_dificuldade(nova_dif):
    global dificuldade
    dificuldade = nova_dif

    for nivel in ["facil", "medio", "dificil"]:
        btn = document.getElementById(f"diff-{nivel}")
        if btn:
            if nivel == nova_dif:
                btn.classList.add("active")
            else:
                btn.classList.remove("active")

    reiniciar_partida()


@when("click", "#btn-reset-game")
def ao_clicar_reiniciar(event):
    reiniciar_partida()


def reiniciar_partida():
    global tabuleiro, jogador_atual, jogo_ativo, bloqueio_input

    fechar_modal_resultado()

    tabuleiro = [""] * 9
    jogador_atual = "X"
    jogo_ativo = True
    bloqueio_input = False

    atualizar_interface()

    if modo_jogo == "cpu":
        nome_dif = {"facil": "Fácil", "medio": "Médio", "dificil": "Difícil"}.get(dificuldade, "Médio")
        definir_status(f"Novo jogo ({nome_dif})! A tua vez (Jogador X).")
    else:
        definir_status("Novo jogo! Vez do Jogador X.")


# Iniciar no arranque
reiniciar_partida()
