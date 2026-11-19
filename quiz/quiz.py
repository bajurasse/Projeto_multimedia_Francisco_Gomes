from pyscript import document, when
import asyncio
import random

# REMOVER ECRA DE CARREGAMENTO
loading = document.getElementById("loading")
if loading:
    loading.remove()


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

# Configurações do jogo
NUM_PERGUNTAS_POR_JOGO = 5
TEMPO_LIMITE_SEGUNDOS = 10

indice_pergunta = 0
pontuacao = 0
quiz_estado = "nao_iniciado"  # Estados: "nao_iniciado", "a_responder", "respondido", "terminado"
ciclo_pergunta_atual = 0
perguntas_ordenadas = []


async def contagem_decrescente(ciclo_id):
    """Executa a contagem decrescente de 10 segundos para a pergunta atual."""
    global quiz_estado

    tempo = TEMPO_LIMITE_SEGUNDOS
    elemento_timer = document.getElementById("quiz-countdown")
    barra_timer = document.getElementById("timer-bar-fill")
    icone_timer = document.getElementById("timer-icon")

    while tempo > 0:
        # Se o utilizador já respondeu ou a pergunta mudou, para o timer
        if quiz_estado != "a_responder" or ciclo_pergunta_atual != ciclo_id:
            return

        # Atualizar texto do tempo e ícone (a bomba ativa quando faltam 3 segundos)
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

        # Atualizar barra gráfica do tempo
        if barra_timer:
            porcentagem = (tempo / TEMPO_LIMITE_SEGUNDOS) * 100
            barra_timer.style.width = f"{porcentagem}%"
            if tempo <= 3:
                barra_timer.classList.add("bar-urgente")
            else:
                barra_timer.classList.remove("bar-urgente")

        await asyncio.sleep(1)

        # Reavaliar após a pausa de 1 segundo
        if quiz_estado != "a_responder" or ciclo_pergunta_atual != ciclo_id:
            return

        tempo -= 1

    # Se o tempo esgotou e o utilizador ainda não respondeu: detona a bomba!
    if quiz_estado == "a_responder" and ciclo_pergunta_atual == ciclo_id:
        await tempo_esgotado()


async def tempo_esgotado():
    """Trata a explosão da bomba e o tempo esgotado."""
    global quiz_estado

    quiz_estado = "respondido"
    pergunta = perguntas_ordenadas[indice_pergunta]

    # Atualizar UI do temporizador com ícone de explosão
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

    # Ativar animação de explosão na tela e tremer o ecrã
    overlay = document.getElementById("explosion-overlay")
    if overlay:
        overlay.classList.remove("hidden")
        overlay.classList.add("active")

    document.body.classList.add("shake-screen")

    # Exibir aviso de tempo esgotado e resposta correta
    resultado = document.getElementById("quiz-result")
    resultado.innerText = (
        f"Tempo esgotado! 💣💥 A resposta correta era: '{pergunta['resposta']}'. "
        f"{pergunta['explicacao']}"
    )

    # Realçar a opção correta e desativar todas
    botoes = document.querySelectorAll(".quiz-option")
    for b in botoes:
        b.disabled = True
        if b.getAttribute("data-answer") == pergunta["resposta"]:
            b.classList.add("correct")

    # Ativar botão de avançar
    btn_acao = document.getElementById("quiz-button")
    btn_acao.disabled = False
    btn_acao.style.opacity = "1"
    btn_acao.style.cursor = "pointer"

    if indice_pergunta + 1 < len(perguntas_ordenadas):
        btn_acao.innerText = "Próxima pergunta →"
    else:
        btn_acao.innerText = "Ver pontuação final →"

    # Esperar 2 segundos de efeito da explosão antes de recolher o overlay automaticamente
    await asyncio.sleep(2.0)
    if overlay and "active" in getattr(overlay, "className", ""):
        overlay.classList.remove("active")
        overlay.classList.add("hidden")
    document.body.classList.remove("shake-screen")


@when("click", "#explosion-overlay")
def fechar_explosao(event):
    """Permite fechar o ecrã da explosão imediatamente com um clique."""
    overlay = document.getElementById("explosion-overlay")
    if overlay:
        overlay.classList.remove("active")
        overlay.classList.add("hidden")
    document.body.classList.remove("shake-screen")


def mostrar_pergunta():
    """Apresenta a pergunta atual e inicia o temporizador de 10 segundos."""
    global quiz_estado, ciclo_pergunta_atual

    ciclo_pergunta_atual += 1
    id_deste_ciclo = ciclo_pergunta_atual
    quiz_estado = "a_responder"

    # Garantir que overlays anteriores e tremores estão limpos
    overlay = document.getElementById("explosion-overlay")
    if overlay:
        overlay.classList.remove("active")
        overlay.classList.add("hidden")
    document.body.classList.remove("shake-screen")

    pergunta = perguntas_ordenadas[indice_pergunta]

    # Atualizar texto da pergunta
    document.getElementById("quiz-question").innerText = (
        f"Pergunta {indice_pergunta + 1} de {len(perguntas_ordenadas)}: {pergunta['pergunta']}"
    )

    # Reiniciar UI do temporizador para 10s
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

    # Limpar e criar opções de resposta baralhadas
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

    # Bloquear botão de avançar enquanto responde
    btn_acao = document.getElementById("quiz-button")
    btn_acao.innerText = "Escolhe uma resposta..."
    btn_acao.disabled = True
    btn_acao.style.opacity = "0.6"
    btn_acao.style.cursor = "not-allowed"

    # Iniciar temporizador assíncrono
    asyncio.create_task(contagem_decrescente(id_deste_ciclo))


def iniciar_quiz():
    """Seleciona aleatoriamente um subconjunto de perguntas e inicia o jogo."""
    global indice_pergunta, pontuacao, perguntas_ordenadas

    indice_pergunta = 0
    pontuacao = 0

    # Escolher aleatoriamente 5 perguntas do banco para que cada jogo seja diferente
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
            # Questionário finalizado
            quiz_estado = "terminado"
            document.getElementById("quiz-question").innerText = "Questionário terminado!"
            document.getElementById("quiz-options").innerHTML = ""

            # Parar barra de tempo
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

    # Só processa se o utilizador estiver na fase de responder
    if quiz_estado != "a_responder":
        return

    target = event.target
    if not target:
        return

    # Delegação de eventos: localiza o botão .quiz-option clicado
    botao = None
    try:
        botao = target.closest(".quiz-option")
    except Exception:
        if "quiz-option" in getattr(target, "className", ""):
            botao = target

    if not botao:
        return

    # Ao responder, para imediatamente a contagem decrescente
    quiz_estado = "respondido"

    pergunta = perguntas_ordenadas[indice_pergunta]
    resposta = botao.getAttribute("data-answer")
    resultado = document.getElementById("quiz-result")

    # Congelar o temporizador
    elemento_timer = document.getElementById("quiz-countdown")
    if elemento_timer:
        elemento_timer.classList.remove("timer-urgente")

    # Verificar se a resposta está correta
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

    # Realçar a resposta correta em verde e desativar todos os botões de opção
    botoes = document.querySelectorAll(".quiz-option")
    for b in botoes:
        b.disabled = True
        if b.getAttribute("data-answer") == pergunta["resposta"]:
            b.classList.add("correct")

    # Ativar o botão principal para avançar
    btn_acao = document.getElementById("quiz-button")
    btn_acao.disabled = False
    btn_acao.style.opacity = "1"
    btn_acao.style.cursor = "pointer"

    if indice_pergunta + 1 < len(perguntas_ordenadas):
        btn_acao.innerText = "Próxima pergunta →"
    else:
        btn_acao.innerText = "Ver pontuação final →"
