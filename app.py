
from pyscript import document, when
import asyncio
import random

# REMOVER ECRÃ DE CARREGAMENTO
loading = document.getElementById("loading")
loading.remove()


# =====================================
# WIDGET 1 - ANALISADOR DE POESIA
# =====================================

@when("click", "#analyze-button")
def analisar_texto(event):

    texto = document.getElementById("poem-input").value
    resultado = document.getElementById("analysis-result")

    if texto.strip() == "":
        resultado.innerText = "Por favor, escreve algum texto."

    else:
        palavras = texto.lower().split()

        caracteres = len(texto)
        total_palavras = len(palavras)
        palavras_diferentes = len(set(palavras))

        # Contar frequência das palavras
        frequencia = {}

        for palavra in palavras:
            palavra = palavra.strip(".,!?;:()[]\"'")

            if palavra != "":
                if palavra in frequencia:
                    frequencia[palavra] += 1
                else:
                    frequencia[palavra] = 1

        # Encontrar a palavra mais repetida
        palavra_frequente = max(frequencia, key=frequencia.get)

        repeticoes = frequencia[palavra_frequente]

        # Sugestões simples
        if total_palavras < 10:
            sugestao = "Podes desenvolver um pouco mais o teu texto."

        elif palavras_diferentes < total_palavras / 2:
            sugestao = "Experimenta utilizar vocabulário mais variado."

        else:
            sugestao = "O teu texto apresenta alguma variedade de vocabulário!"

        resultado.innerHTML = f"""
            <h3>Resultados da análise</h3>
            <p>Caracteres: {caracteres}</p>
            <p>Palavras: {total_palavras}</p>
            <p>Palavras diferentes: {palavras_diferentes}</p>
            <p>Palavra mais utilizada: {palavra_frequente}</p>
            <p>Repetições: {repeticoes}</p>
            <h4>Sugestão inteligente</h4>
            <p>{sugestao}</p>
        """


# =====================================
# WIDGET 2 - JOGO DO GALO COM DIFICULDADES
# =====================================

modo_jogo_galo = "cpu"
dificuldade_galo = "medio"
jogador_atual_galo = "X"
tabuleiro_galo = [""] * 9
jogo_ativo_galo = True
bloqueio_input_galo = False

vitorias_x_galo = 0
vitorias_o_galo = 0
empates_galo = 0

COMBINACOES_VITORIA_GALO = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]


def atualizar_interface_galo():
    for i in range(9):
        celula = document.getElementById(f"cell-{i}")
        if celula:
            valor = tabuleiro_galo[i]
            celula.innerText = valor
            celula.className = "galo-cell"
            if valor == "X":
                celula.classList.add("cell--x")
            elif valor == "O":
                celula.classList.add("cell--o")

    doc_vx = document.getElementById("score-x")
    doc_vo = document.getElementById("score-o")
    doc_emp = document.getElementById("score-empates")

    if doc_vx:
        doc_vx.innerText = str(vitorias_x_galo)
    if doc_vo:
        doc_vo.innerText = str(vitorias_o_galo)
    if doc_emp:
        doc_emp.innerText = str(empates_galo)


def verificar_fim_jogo_galo(tab_param=None):
    tab = tab_param if tab_param is not None else tabuleiro_galo
    for a, b, c in COMBINACOES_VITORIA_GALO:
        if tab[a] != "" and tab[a] == tab[b] == tab[c]:
            return tab[a], [a, b, c]
    if "" not in tab:
        return "empate", []
    return None, []


def destacar_vencedores_galo(indices):
    for idx in indices:
        celula = document.getElementById(f"cell-{idx}")
        if celula:
            celula.classList.add("cell--winner")


def definir_status_galo(texto, cor=None):
    status_el = document.getElementById("galo-status")
    if status_el:
        status_el.innerText = texto
        status_el.style.color = cor if cor else "var(--text)"


def jogada_ganhar_ou_bloquear_galo():
    for a, b, c in COMBINACOES_VITORIA_GALO:
        linha = [tabuleiro_galo[a], tabuleiro_galo[b], tabuleiro_galo[c]]
        if linha.count("O") == 2 and linha.count("") == 1:
            for pos in [a, b, c]:
                if tabuleiro_galo[pos] == "":
                    return pos

    for a, b, c in COMBINACOES_VITORIA_GALO:
        linha = [tabuleiro_galo[a], tabuleiro_galo[b], tabuleiro_galo[c]]
        if linha.count("X") == 2 and linha.count("") == 1:
            for pos in [a, b, c]:
                if tabuleiro_galo[pos] == "":
                    return pos

    if tabuleiro_galo[4] == "":
        return 4
    return None


def minimax_galo(tab, profundidade, is_max):
    resultado, _ = verificar_fim_jogo_galo(tab)
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
                pontos = minimax_galo(tab, profundidade + 1, False)
                tab[i] = ""
                melhor = max(melhor, pontos)
        return melhor
    else:
        melhor = 1000
        for i in range(9):
            if tab[i] == "":
                tab[i] = "X"
                pontos = minimax_galo(tab, profundidade + 1, True)
                tab[i] = ""
                melhor = min(melhor, pontos)
        return melhor


def jogada_minimax_galo():
    if tabuleiro_galo.count("") >= 7 and tabuleiro_galo[4] == "":
        return 4
    melhor_val = -1000
    melhor_jogada = None
    espacos = [i for i, v in enumerate(tabuleiro_galo) if v == ""]
    random.shuffle(espacos)
    for i in espacos:
        tabuleiro_galo[i] = "O"
        val = minimax_galo(tabuleiro_galo, 0, False)
        tabuleiro_galo[i] = ""
        if val > melhor_val:
            melhor_val = val
            melhor_jogada = i
    return melhor_jogada if melhor_jogada is not None else random.choice(espacos)


def calcular_jogada_computador_galo():
    espacos_livres = [i for i, v in enumerate(tabuleiro_galo) if v == ""]
    if not espacos_livres:
        return None
    if dificuldade_galo == "facil":
        return random.choice(espacos_livres)
    elif dificuldade_galo == "medio":
        if random.random() < 0.5:
            smart = jogada_ganhar_ou_bloquear_galo()
            if smart is not None:
                return smart
        return random.choice(espacos_livres)
    elif dificuldade_galo == "dificil":
        return jogada_minimax_galo()
    return random.choice(espacos_livres)


async def mostrar_animacao_resultado_galo(tipo, vencedor=None):
    await asyncio.sleep(0.35)
    overlay = document.getElementById("galo-result-overlay")
    box = document.getElementById("result-modal-box")
    icon = document.getElementById("result-icon")
    title = document.getElementById("result-title")
    msg = document.getElementById("result-message")
    if not overlay or not box:
        return

    box.className = "result-modal"
    nome_dif = {"facil": "Fácil", "medio": "Médio", "dificil": "Difícil"}.get(dificuldade_galo, "Médio")

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


def fechar_modal_resultado_galo():
    overlay = document.getElementById("galo-result-overlay")
    if overlay:
        overlay.classList.remove("active")
        overlay.classList.add("hidden")


@when("click", "#btn-play-again")
def ao_clicar_jogar_novamente_galo(event):
    fechar_modal_resultado_galo()
    reiniciar_partida_galo()


@when("click", "#result-backdrop")
def ao_clicar_fundo_resultado_galo(event):
    fechar_modal_resultado_galo()


async def executar_jogada_galo(posicao):
    global jogador_atual_galo, jogo_ativo_galo, vitorias_x_galo, vitorias_o_galo, empates_galo, bloqueio_input_galo

    if not jogo_ativo_galo or tabuleiro_galo[posicao] != "" or bloqueio_input_galo:
        return

    tabuleiro_galo[posicao] = jogador_atual_galo
    atualizar_interface_galo()

    resultado, celulas_ganhadoras = verificar_fim_jogo_galo()

    if resultado:
        jogo_ativo_galo = False
        if resultado == "empate":
            empates_galo += 1
            definir_status_galo("Jogo empatado! Ninguém fez 3 em linha. 🤝", "#85838f")
            atualizar_interface_galo()
            await mostrar_animacao_resultado_galo("empate")
        else:
            destacar_vencedores_galo(celulas_ganhadoras)
            if resultado == "X":
                vitorias_x_galo += 1
                if modo_jogo_galo == "cpu":
                    definir_status_galo("Vitória! Venceste o Computador! 🎉", "#28a745")
                    atualizar_interface_galo()
                    await mostrar_animacao_resultado_galo("vitoria_cpu_humano")
                else:
                    definir_status_galo("Vitória do Jogador X! 🎉", "#8064d8")
                    atualizar_interface_galo()
                    await mostrar_animacao_resultado_galo("vitoria_pvp", "X")
            else:
                vitorias_o_galo += 1
                if modo_jogo_galo == "cpu":
                    definir_status_galo("O Computador venceu desta vez! 🤖", "#ff6b6b")
                    atualizar_interface_galo()
                    await mostrar_animacao_resultado_galo("derrota_cpu")
                else:
                    definir_status_galo("Vitória do Jogador O! 🎉", "#ff6b6b")
                    atualizar_interface_galo()
                    await mostrar_animacao_resultado_galo("vitoria_pvp", "O")
        return

    if modo_jogo_galo == "pvp":
        jogador_atual_galo = "O" if jogador_atual_galo == "X" else "X"
        definir_status_galo(f"Vez de jogar: Jogador {jogador_atual_galo}")
    elif modo_jogo_galo == "cpu":
        jogador_atual_galo = "O"
        definir_status_galo("O computador está a pensar... 🤖")
        bloqueio_input_galo = True
        await asyncio.sleep(0.4)
        jogada_cpu = calcular_jogada_computador_galo()
        bloqueio_input_galo = False

        if jogada_cpu is not None and jogo_ativo_galo:
            tabuleiro_galo[jogada_cpu] = "O"
            atualizar_interface_galo()
            res_cpu, celulas_cpu = verificar_fim_jogo_galo()
            if res_cpu:
                jogo_ativo_galo = False
                if res_cpu == "empate":
                    empates_galo += 1
                    definir_status_galo("Jogo empatado! 🤝", "#85838f")
                    atualizar_interface_galo()
                    await mostrar_animacao_resultado_galo("empate")
                else:
                    vitorias_o_galo += 1
                    destacar_vencedores_galo(celulas_cpu)
                    definir_status_galo("O Computador venceu! 🤖", "#ff6b6b")
                    atualizar_interface_galo()
                    await mostrar_animacao_resultado_galo("derrota_cpu")
            else:
                jogador_atual_galo = "X"
                definir_status_galo("A tua vez (Jogador X)!")


@when("click", "#galo-board")
async def ao_clicar_tabuleiro_galo(event):
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
        await executar_jogada_galo(int(idx_str))


@when("click", "#mode-cpu")
def mudar_modo_cpu_galo(event):
    global modo_jogo_galo
    modo_jogo_galo = "cpu"
    btn_cpu = document.getElementById("mode-cpu")
    btn_pvp = document.getElementById("mode-pvp")
    label_o = document.getElementById("label-score-o")
    diff_container = document.getElementById("difficulty-container")
    if btn_cpu: btn_cpu.classList.add("active")
    if btn_pvp: btn_pvp.classList.remove("active")
    if label_o: label_o.innerText = "Computador (O)"
    if diff_container: diff_container.style.display = "flex"
    reiniciar_partida_galo()


@when("click", "#mode-pvp")
def mudar_modo_pvp_galo(event):
    global modo_jogo_galo
    modo_jogo_galo = "pvp"
    btn_cpu = document.getElementById("mode-cpu")
    btn_pvp = document.getElementById("mode-pvp")
    label_o = document.getElementById("label-score-o")
    diff_container = document.getElementById("difficulty-container")
    if btn_pvp: btn_pvp.classList.add("active")
    if btn_cpu: btn_cpu.classList.remove("active")
    if label_o: label_o.innerText = "Jogador O"
    if diff_container: diff_container.style.display = "none"
    reiniciar_partida_galo()


@when("click", "#diff-facil")
def definir_diff_facil_galo(event):
    atualizar_dificuldade_galo("facil")


@when("click", "#diff-medio")
def definir_diff_medio_galo(event):
    atualizar_dificuldade_galo("medio")


@when("click", "#diff-dificil")
def definir_diff_dificil_galo(event):
    atualizar_dificuldade_galo("dificil")


def atualizar_dificuldade_galo(nova_dif):
    global dificuldade_galo
    dificuldade_galo = nova_dif
    for nivel in ["facil", "medio", "dificil"]:
        btn = document.getElementById(f"diff-{nivel}")
        if btn:
            if nivel == nova_dif:
                btn.classList.add("active")
            else:
                btn.classList.remove("active")
    reiniciar_partida_galo()


@when("click", "#btn-reset-game")
def ao_clicar_reiniciar_galo(event):
    reiniciar_partida_galo()


def reiniciar_partida_galo():
    global tabuleiro_galo, jogador_atual_galo, jogo_ativo_galo, bloqueio_input_galo
    fechar_modal_resultado_galo()
    tabuleiro_galo = [""] * 9
    jogador_atual_galo = "X"
    jogo_ativo_galo = True
    bloqueio_input_galo = False
    atualizar_interface_galo()
    if modo_jogo_galo == "cpu":
        nome_dif = {"facil": "Fácil", "medio": "Médio", "dificil": "Difícil"}.get(dificuldade_galo, "Médio")
        definir_status_galo(f"Novo jogo ({nome_dif})! A tua vez (Jogador X).")
    else:
        definir_status_galo("Novo jogo! Vez do Jogador X.")


reiniciar_partida_galo()


# =====================================
# WIDGET 3 - QUESTIONÁRIO DE MULTIMÉDIA
# =====================================

# Banco abrangente de perguntas de Multimédia
banco_perguntas = [
    {
        "pergunta": "Qual destas opções é uma linguagem de programação?",
        "opcoes": ["HTML", "Python", "JPEG"],
        "resposta": "Python",
        "dica": "É a linguagem que estamos a utilizar neste projeto.",
        "explicacao": "Python é uma linguagem de programação de alto nível."
    },
    {
        "pergunta": "O que significa a sigla JPG ou JPEG?",
        "opcoes": ["Joint Photographic Experts Group", "Java Picture Graphics", "Joint Program Graphic"],
        "resposta": "Joint Photographic Experts Group",
        "dica": "É o nome do comité de peritos que criou este formato de imagem.",
        "explicacao": "JPEG refere-se ao Joint Photographic Experts Group, formato padrão para fotografias digitais."
    },
    {
        "pergunta": "Qual é a resolução padrão de Full HD em píxeis?",
        "opcoes": ["1920 × 1080", "1280 × 720", "3840 × 2160"],
        "resposta": "1920 × 1080",
        "dica": "Tem 1920 colunas e 1080 linhas de píxeis.",
        "explicacao": "Full HD (1080p) corresponde à resolução de 1920 × 1080 píxeis."
    },
    {
        "pergunta": "Qual é a resolução de vídeo habitualmente designada por 4K UHD?",
        "opcoes": ["3840 × 2160", "2560 × 1440", "1920 × 1080"],
        "resposta": "3840 × 2160",
        "dica": "Tem o quádruplo de píxeis totais do Full HD.",
        "explicacao": "4K Ultra HD possui 3840 × 2160 píxeis, garantindo máxima definição."
    },
    {
        "pergunta": "Para que serve a linguagem CSS no desenvolvimento web?",
        "opcoes": ["Definir o estilo e apresentação visual", "Controlar bases de dados relacionais", "Criar ficheiros de áudio compactados"],
        "resposta": "Definir o estilo e apresentação visual",
        "dica": "Controla cores, fontes, espaçamentos e layouts.",
        "explicacao": "CSS (Cascading Style Sheets) controla a apresentação visual das páginas web."
    },
    {
        "pergunta": "O que significa a sigla do modelo de cor RGB?",
        "opcoes": ["Red, Green, Blue", "Resolution, Graphics, Background", "Raster, Grid, Brightness"],
        "resposta": "Red, Green, Blue",
        "dica": "São as três cores primárias de luz aditiva nos ecrãs digitais.",
        "explicacao": "RGB baseia-se na combinação de vermelho (Red), verde (Green) e azul (Blue)."
    },
    {
        "pergunta": "Para que tipo de suporte é indicado o modelo de cor CMYK?",
        "opcoes": ["Impressão gráfica em papel", "Ecrãs de smartphones e monitores", "Transmissão de rádio digital"],
        "resposta": "Impressão gráfica em papel",
        "dica": "Funciona por subtração de luz através de tintas de impressão.",
        "explicacao": "CMYK (Cyan, Magenta, Yellow, Key/Preto) é o padrão usado na indústria gráfica e impressão."
    },
    {
        "pergunta": "Qual é a principal vantagem de uma imagem vetorial (ex.: SVG)?",
        "opcoes": ["Não perde qualidade ao ser ampliada", "É sempre mais pesada que um PNG", "Só suporta imagens a preto e branco"],
        "resposta": "Não perde qualidade ao ser ampliada",
        "dica": "Baseia-se em fórmulas matemáticas e linhas, não em píxeis fixos.",
        "explicacao": "Imagens vetoriais são calculadas matematicamente e redimensionam sem qualquer perda de nitidez."
    },
    {
        "pergunta": "Qual destes formatos de áudio é sem perdas (lossless)?",
        "opcoes": ["FLAC", "MP3", "AAC"],
        "resposta": "FLAC",
        "dica": "O seu nome começa por 'Free Lossless Audio Codec'.",
        "explicacao": "FLAC preserva exatamente a qualidade original do áudio gravado em estúdio ou CD."
    },
    {
        "pergunta": "Qual destes formatos de imagem suporta canal alfa (transparência)?",
        "opcoes": ["PNG", "JPEG", "BMP tradicional"],
        "resposta": "PNG",
        "dica": "Muito usado na web para logótipos sobre fundos variáveis.",
        "explicacao": "PNG suporta canal alfa, permitindo múltiplos níveis de transparência suave."
    },
    {
        "pergunta": "Qual é a taxa de fotogramas (fps) clássica do cinema sonoro?",
        "opcoes": ["24 fps", "60 fps", "120 fps"],
        "resposta": "24 fps",
        "dica": "É o padrão adotado desde a introdução do cinema sonoro.",
        "explicacao": "A taxa clássica de 24 fotogramas por segundo cria a sensação cinematográfica tradicional."
    },
    {
        "pergunta": "Qual é a taxa de amostragem padrão de áudio com qualidade de CD?",
        "opcoes": ["44.1 kHz", "12 kHz", "96 kHz"],
        "resposta": "44.1 kHz",
        "dica": "Mais do que o dobro da frequência máxima audível pelo ouvido humano (20 kHz).",
        "explicacao": "O teorema de Nyquist-Shannon define que 44.1 kHz é suficiente para reproduzir todo o espetro audível humano."
    },
    {
        "pergunta": "Qual é o contentor de vídeo moderno mais universal na web atual?",
        "opcoes": ["MP4", "AVI", "WMV"],
        "resposta": "MP4",
        "dica": "É compatível com praticamente todos os navegadores e dispositivos móveis.",
        "explicacao": "MP4 (com codec H.264 ou H.265) é o formato de vídeo mais compatível no ecossistema digital."
    },
    {
        "pergunta": "Qual destes formatos é historicamente conhecido por suportar pequenas animações em ciclo (loop)?",
        "opcoes": ["GIF", "PDF", "TIFF"],
        "resposta": "GIF",
        "dica": "Criado pela CompuServe em 1987 e ainda muito popular na web.",
        "explicacao": "O GIF suporta múltiplos fotogramas encadeados, permitindo animações curtas sem som."
    },
    {
        "pergunta": "Qual é a proporção de ecrã (aspect ratio) panorâmica padrão em monitores e TVs?",
        "opcoes": ["16:9", "4:3", "1:1"],
        "resposta": "16:9",
        "dica": "É o formato retangular largo utilizado no YouTube e transmissões HD.",
        "explicacao": "A proporção 16:9 é o padrão global para conteúdos widescreen e alta definição."
    },
    {
        "pergunta": "O que acontece numa compressão com perdas (lossy), como no MP3 ou JPEG?",
        "opcoes": ["Elimina dados impercetíveis ao olho/ouvido para reduzir o ficheiro", "Aumenta o tamanho do ficheiro duplicando os dados", "Não altera nenhum byte do ficheiro original"],
        "resposta": "Elimina dados impercetíveis ao olho/ouvido para reduzir o ficheiro",
        "dica": "Aproveita limitações da perceção humana (psicoacústica e psicovisual).",
        "explicacao": "A compressão lossy descarta detalhes supérfluos para obter ficheiros muito menores."
    },
    {
        "pergunta": "O que representa a profundidade de cor de 24 bits (8 bits por canal RGB)?",
        "opcoes": ["Cerca de 16,7 milhões de cores possíveis", "Apenas 256 cores no total", "24 cores distintas"],
        "resposta": "Cerca de 16,7 milhões de cores possíveis",
        "dica": "Calcula-se como 256 × 256 × 256 combinações de cores.",
        "explicacao": "256 tons de vermelho × 256 de verde × 256 de azul originam 16.777.216 cores (True Color)."
    },
    {
        "pergunta": "Que padrão web eliminou a necessidade de plugins externos (como o Flash) para vídeo e áudio?",
        "opcoes": ["HTML5", "QuickTime", "Shockwave"],
        "resposta": "HTML5",
        "dica": "Introduziu as tags nativas <video> e <audio>.",
        "explicacao": "O HTML5 introduziu elementos multimédia nativos, eliminando a dependência de plugins externos."
    }
]

NUM_PERGUNTAS_POR_JOGO = 5
TEMPO_LIMITE_SEGUNDOS = 10

indice_pergunta = 0
pontuacao = 0
quiz_estado = "nao_iniciado"
ciclo_pergunta_atual = 0
perguntas_ordenadas = []


async def contagem_decrescente(ciclo_id):
    global quiz_estado

    tempo = TEMPO_LIMITE_SEGUNDOS
    elemento_timer = document.getElementById("quiz-countdown")
    barra_timer = document.getElementById("timer-bar-fill")
    icone_timer = document.getElementById("timer-icon")

    while tempo > 0:
        if quiz_estado != "a_responder" or ciclo_pergunta_atual != ciclo_id:
            return

        if elemento_timer:
            elemento_timer.innerText = f"{tempo}s"
            if tempo <= 3:
                elemento_timer.classList.add("timer-urgente")
                if icone_timer:
                    icone_timer.innerText = "💣"
            else:
                elemento_timer.classList.remove("timer-urgente")
                if icone_timer:
                    icone_timer.innerText = "⏱️"

        if barra_timer:
            porcentagem = (tempo / TEMPO_LIMITE_SEGUNDOS) * 100
            barra_timer.style.width = f"{porcentagem}%"
            if tempo <= 3:
                barra_timer.classList.add("bar-urgente")
            else:
                barra_timer.classList.remove("bar-urgente")

        await asyncio.sleep(1)

        if quiz_estado != "a_responder" or ciclo_pergunta_atual != ciclo_id:
            return

        tempo -= 1

    if quiz_estado == "a_responder" and ciclo_pergunta_atual == ciclo_id:
        await tempo_esgotado()


async def tempo_esgotado():
    global quiz_estado

    quiz_estado = "respondido"
    pergunta = perguntas_ordenadas[indice_pergunta]

    icone_timer = document.getElementById("timer-icon")
    if icone_timer:
        icone_timer.innerText = "💥"

    elemento_timer = document.getElementById("quiz-countdown")
    if elemento_timer:
        elemento_timer.innerText = "0s - BOOM!"
        elemento_timer.classList.add("timer-urgente")

    barra_timer = document.getElementById("timer-bar-fill")
    if barra_timer:
        barra_timer.style.width = "0%"

    overlay = document.getElementById("explosion-overlay")
    if overlay:
        overlay.classList.remove("hidden")
        overlay.classList.add("active")

    document.body.classList.add("shake-screen")

    resultado = document.getElementById("quiz-result")
    resultado.innerText = (
        f"Tempo esgotado! 💣💥 A resposta correta era: '{pergunta['resposta']}'. "
        f"{pergunta['explicacao']}"
    )

    botoes = document.querySelectorAll(".quiz-option")
    for b in botoes:
        b.disabled = True
        if b.getAttribute("data-answer") == pergunta["resposta"]:
            b.classList.add("correct")

    btn_acao = document.getElementById("quiz-button")
    btn_acao.disabled = False
    btn_acao.style.opacity = "1"
    btn_acao.style.cursor = "pointer"

    if indice_pergunta + 1 < len(perguntas_ordenadas):
        btn_acao.innerText = "Próxima pergunta →"
    else:
        btn_acao.innerText = "Ver pontuação final →"

    await asyncio.sleep(2.0)
    if overlay and "active" in getattr(overlay, "className", ""):
        overlay.classList.remove("active")
        overlay.classList.add("hidden")
    document.body.classList.remove("shake-screen")


@when("click", "#explosion-overlay")
def fechar_explosao(event):
    overlay = document.getElementById("explosion-overlay")
    if overlay:
        overlay.classList.remove("active")
        overlay.classList.add("hidden")
    document.body.classList.remove("shake-screen")


def mostrar_pergunta():
    global quiz_estado, ciclo_pergunta_atual

    ciclo_pergunta_atual += 1
    id_deste_ciclo = ciclo_pergunta_atual
    quiz_estado = "a_responder"

    overlay = document.getElementById("explosion-overlay")
    if overlay:
        overlay.classList.remove("active")
        overlay.classList.add("hidden")
    document.body.classList.remove("shake-screen")

    pergunta = perguntas_ordenadas[indice_pergunta]

    document.getElementById("quiz-question").innerText = (
        f"Pergunta {indice_pergunta + 1} de {len(perguntas_ordenadas)}: {pergunta['pergunta']}"
    )

    icone_timer = document.getElementById("timer-icon")
    if icone_timer:
        icone_timer.innerText = "⏱️"

    elemento_timer = document.getElementById("quiz-countdown")
    if elemento_timer:
        elemento_timer.innerText = f"{TEMPO_LIMITE_SEGUNDOS}s"
        elemento_timer.classList.remove("timer-urgente")

    barra_timer = document.getElementById("timer-bar-fill")
    if barra_timer:
        barra_timer.style.width = "100%"
        barra_timer.classList.remove("bar-urgente")

    opcoes = document.getElementById("quiz-options")
    opcoes.innerHTML = ""

    opcoes_baralhadas = pergunta["opcoes"].copy()
    random.shuffle(opcoes_baralhadas)

    for opcao in opcoes_baralhadas:
        botao = document.createElement("button")
        botao.innerText = opcao
        botao.className = "quiz-option"
        botao.setAttribute("data-answer", opcao)
        opcoes.appendChild(botao)

    document.getElementById("quiz-result").innerText = (
        f"Tens {TEMPO_LIMITE_SEGUNDOS} segundos! Escolhe uma resposta:"
    )

    btn_acao = document.getElementById("quiz-button")
    btn_acao.innerText = "Escolhe uma resposta..."
    btn_acao.disabled = True
    btn_acao.style.opacity = "0.6"
    btn_acao.style.cursor = "not-allowed"

    asyncio.create_task(contagem_decrescente(id_deste_ciclo))


def iniciar_quiz():
    global indice_pergunta, pontuacao, perguntas_ordenadas

    indice_pergunta = 0
    pontuacao = 0

    num_selecionar = min(NUM_PERGUNTAS_POR_JOGO, len(banco_perguntas))
    perguntas_ordenadas = random.sample(banco_perguntas, num_selecionar)

    mostrar_pergunta()


@when("click", "#quiz-button")
def ao_clicar_botao_quiz(event):
    global indice_pergunta, quiz_estado

    btn_acao = document.getElementById("quiz-button")

    if quiz_estado == "nao_iniciado" or quiz_estado == "terminado":
        iniciar_quiz()

    elif quiz_estado == "respondido":
        indice_pergunta += 1

        if indice_pergunta < len(perguntas_ordenadas):
            mostrar_pergunta()
        else:
            quiz_estado = "terminado"
            document.getElementById("quiz-question").innerText = "Quiz terminado!"
            document.getElementById("quiz-options").innerHTML = ""

            barra_timer = document.getElementById("timer-bar-fill")
            if barra_timer:
                barra_timer.style.width = "100%"

            elemento_timer = document.getElementById("quiz-countdown")
            if elemento_timer:
                elemento_timer.innerText = "Concluído!"
                elemento_timer.classList.remove("timer-urgente")

            resultado = document.getElementById("quiz-result")
            total = len(perguntas_ordenadas)
            msg = f"Pontuação final: {pontuacao} / {total} acertos."

            if pontuacao == total:
                msg += " Perfeito! Acertaste em todas as perguntas dentro do tempo!"
            elif pontuacao >= 3:
                msg += " Muito bem! Excelente velocidade de raciocínio e conhecimento multimédia."
            else:
                msg += " O tempo voa! Clica abaixo para tentares novamente com novas perguntas."

            resultado.innerText = msg

            btn_acao.innerText = "Jogar novamente (novas perguntas) ↺"
            btn_acao.disabled = False
            btn_acao.style.opacity = "1"
            btn_acao.style.cursor = "pointer"


@when("click", "#quiz-options")
def ao_clicar_opcao(event):
    global pontuacao, quiz_estado

    if quiz_estado != "a_responder":
        return

    target = event.target
    if not target:
        return

    botao = None
    try:
        botao = target.closest(".quiz-option")
    except Exception:
        if "quiz-option" in getattr(target, "className", ""):
            botao = target

    if not botao:
        return

    quiz_estado = "respondido"

    pergunta = perguntas_ordenadas[indice_pergunta]
    resposta = botao.getAttribute("data-answer")
    resultado = document.getElementById("quiz-result")

    elemento_timer = document.getElementById("quiz-countdown")
    if elemento_timer:
        elemento_timer.classList.remove("timer-urgente")

    if resposta == pergunta["resposta"]:
        pontuacao += 1
        botao.classList.add("correct")
        resultado.innerText = "Correto! " + pergunta["explicacao"]
    else:
        botao.classList.add("incorrect")
        resultado.innerText = (
            "Não está correto. "
            + pergunta["explicacao"]
            + " Dica: "
            + pergunta["dica"]
        )

    botoes = document.querySelectorAll(".quiz-option")
    for b in botoes:
        b.disabled = True
        if b.getAttribute("data-answer") == pergunta["resposta"]:
            b.classList.add("correct")

    btn_acao = document.getElementById("quiz-button")
    btn_acao.disabled = False
    btn_acao.style.opacity = "1"
    btn_acao.style.cursor = "pointer"

    if indice_pergunta + 1 < len(perguntas_ordenadas):
        btn_acao.innerText = "Próxima pergunta →"
    else:
        btn_acao.innerText = "Ver pontuação final →"
