from pyscript import document, when
import base64
import html
import io
import random
import re

# REMOVER ECRA DE CARREGAMENTO
loading = document.getElementById("loading")
if loading:
    loading.remove()


# Dicionário de sinónimos para substituição
# (cada sinónimo tem o mesmo género e número da palavra original, para o texto
# continuar a concordar: "a noite" -> "a escuridão", "os belos" -> "os lindos")
SINONIMOS = {
    # ---------- Sentimentos e emoções ----------
    "feliz": "contente",
    "felizes": "contentes",
    "triste": "infeliz",
    "tristes": "infelizes",
    "alegria": "felicidade",
    "alegre": "jovial",
    "alegres": "joviais",
    "tristeza": "melancolia",
    "dor": "mágoa",
    "dores": "mágoas",
    "medo": "receio",
    "medos": "receios",
    "raiva": "fúria",
    "ódio": "rancor",
    "paixão": "devoção",
    "paz": "serenidade",
    "esperança": "confiança",
    "sonho": "devaneio",
    "sonhos": "devaneios",
    "amor": "afeto",
    "amores": "afetos",
    "coração": "peito",
    "corações": "peitos",
    "alma": "essência",
    "almas": "essências",
    "choro": "pranto",
    "sorriso": "riso",
    "sorrisos": "risos",
    "beijo": "ósculo",
    "beijos": "ósculos",
    "desejo": "anseio",
    "desejos": "anseios",
    "silêncio": "sossego",
    "beleza": "formosura",
    "força": "energia",
    "verdade": "veracidade",
    "mentira": "falsidade",
    "destino": "fado",
    "sorte": "fortuna",

    # ---------- Natureza ----------
    "noite": "escuridão",
    "sol": "astro",
    "céu": "firmamento",
    "céus": "firmamentos",
    "mar": "oceano",
    "mares": "oceanos",
    "onda": "vaga",
    "ondas": "vagas",
    "vento": "zéfiro",
    "ventos": "zéfiros",
    "mundo": "universo",
    "mundos": "universos",
    "pedra": "rocha",
    "pedras": "rochas",
    "luz": "claridade",
    "sombra": "penumbra",
    "sombras": "penumbras",
    "fogo": "lume",
    "chamas": "labaredas",
    "floresta": "mata",
    "bosque": "arvoredo",
    "montanha": "serra",
    "montanhas": "serras",
    "campo": "prado",
    "campos": "prados",
    "manhã": "alvorada",
    "madrugada": "aurora",
    "calor": "ardor",
    "frio": "gélido",
    "fria": "gélida",
    "frios": "gélidos",
    "frias": "gélidas",
    "quente": "ardente",
    "quentes": "ardentes",

    # ---------- Adjetivos ----------
    "belo": "lindo",
    "belos": "lindos",
    "bela": "linda",
    "belas": "lindas",
    "bonito": "formoso",
    "bonita": "formosa",
    "bonitos": "formosos",
    "bonitas": "formosas",
    "lindo": "encantador",
    "linda": "encantadora",
    "lindos": "encantadores",
    "lindas": "encantadoras",
    "feio": "horrendo",
    "feia": "horrenda",
    "feios": "horrendos",
    "feias": "horrendas",
    "bom": "ótimo",
    "boa": "ótima",
    "bons": "ótimos",
    "boas": "ótimas",
    "mau": "ruim",
    "má": "ruim",
    "maus": "ruins",
    "más": "ruins",
    "grande": "enorme",
    "grandes": "enormes",
    "pequeno": "diminuto",
    "pequena": "diminuta",
    "pequenos": "diminutos",
    "pequenas": "diminutas",
    "novo": "recente",
    "novos": "recentes",
    "velho": "antigo",
    "velha": "antiga",
    "velhos": "antigos",
    "velhas": "antigas",
    "forte": "potente",
    "fortes": "potentes",
    "fraco": "débil",
    "fraca": "débil",
    "fracos": "débeis",
    "fracas": "débeis",
    "rápido": "veloz",
    "rápida": "veloz",
    "rápidos": "velozes",
    "rápidas": "velozes",
    "lento": "vagaroso",
    "lenta": "vagarosa",
    "lentos": "vagarosos",
    "lentas": "vagarosas",
    "doce": "suave",
    "doces": "suaves",
    "sozinho": "solitário",
    "sozinha": "solitária",
    "sozinhos": "solitários",
    "sozinhas": "solitárias",
    "cansado": "exausto",
    "cansada": "exausta",
    "cansados": "exaustos",
    "cansadas": "exaustas",
    "puro": "límpido",
    "pura": "límpida",
    "eterno": "perpétuo",
    "eterna": "perpétua",
    "eternos": "perpétuos",
    "eternas": "perpétuas",
    "profundo": "abissal",
    "profunda": "abissal",
    "silencioso": "calado",
    "silenciosa": "calada",
    "brilhante": "reluzente",
    "brilhantes": "reluzentes",
    "calmo": "sereno",
    "calmos": "serenos",
    "escuro": "sombrio",
    "escura": "sombria",
    "escuros": "sombrios",
    "escuras": "sombrias",
    "fácil": "simples",
    "fáceis": "simples",
    "importante": "relevante",
    "importantes": "relevantes",
    "perdido": "extraviado",
    "perdida": "extraviada",
    "juntos": "unidos",
    "juntas": "unidas",

    # ---------- Verbos ----------
    "amar": "adorar",
    "amo": "adoro",
    "ama": "adora",
    "amei": "adorei",
    "amava": "adorava",
    "olhar": "contemplar",
    "olha": "contempla",
    "ver": "avistar",
    "vejo": "avisto",
    "andar": "caminhar",
    "anda": "caminha",
    "chorar": "lacrimejar",
    "chora": "pranteia",
    "começar": "iniciar",
    "começa": "inicia",
    "acabar": "terminar",
    "acaba": "termina",
    "morrer": "falecer",
    "morre": "falece",
    "nascer": "surgir",
    "nasce": "surge",
    "viver": "existir",
    "vive": "existe",
    "pensar": "refletir",
    "penso": "reflito",
    "pensa": "reflete",
    "querer": "desejar",
    "quero": "desejo",
    "quer": "deseja",
    "voltar": "regressar",
    "esperar": "aguardar",
    "espero": "aguardo",
    "cantar": "entoar",
    "canta": "entoa",
    "sonhar": "devanear",
    "sonha": "devaneia",
    "brilhar": "reluzir",
    "brilha": "reluz",
    "procurar": "buscar",
    "procuro": "busco",
    "gritar": "bradar",
    "grita": "brada",
    "lembrar": "recordar",
    "lembro": "recordo",
    "lembra": "recorda",
    "esquecer": "olvidar",
    "esqueço": "olvido",
    "esquece": "olvida",
    "ajudar": "auxiliar",

    # ---------- Outros substantivos ----------
    "vida": "existência",
    "tempo": "momento",
    "casa": "morada",
    "casas": "moradas",
    "rosto": "semblante",
    "rostos": "semblantes",
    "palavra": "expressão",
    "palavras": "expressões",
    "história": "narrativa",
    "histórias": "narrativas",
    "fim": "final",
    "início": "princípio",
    "caminho": "trilho",
    "caminhos": "trilhos",
    "estrada": "via",
    "estradas": "vias",
    "viagem": "jornada",
    "viagens": "jornadas",
    "segredo": "mistério",
    "segredos": "mistérios",
    "memória": "lembrança",
    "memórias": "lembranças",
    "guerra": "batalha",
    "guerras": "batalhas",
    "amigo": "companheiro",
    "amiga": "companheira",
    "amigos": "companheiros",
    "amigas": "companheiras",
    "mulher": "senhora",
    "mulheres": "senhoras",
    "cidade": "urbe",
    "livro": "volume",
    "livros": "volumes",
    "música": "melodia",
    "músicas": "melodias",
    "canção": "cantiga",
    "canções": "cantigas",
    "trabalho": "labor",

    # ---------- Advérbios ----------
    "sempre": "eternamente",
    "nunca": "jamais",
    "depressa": "rapidamente",
    "devagar": "lentamente",
    "talvez": "porventura",
    "apenas": "somente",
}

PONTUACAO = ".,!?;:()[]\"'«»"

# Palavras muito comuns que não entram na nuvem de palavras
PALAVRAS_COMUNS = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas",
    "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas",
    "ao", "aos", "à", "às", "por", "pelo", "pela", "pelos", "pelas",
    "para", "com", "sem", "sob", "sobre", "entre", "até", "desde",
    "e", "ou", "mas", "nem", "que", "se", "como", "quando", "onde", "porque",
    "eu", "tu", "ele", "ela", "nós", "vós", "eles", "elas",
    "me", "te", "lhe", "lhes", "nos", "vos", "mim", "ti", "si",
    "meu", "minha", "meus", "minhas", "teu", "tua", "teus", "tuas",
    "seu", "sua", "seus", "suas", "nosso", "nossa", "este", "esta",
    "esse", "essa", "isto", "isso", "aquele", "aquela", "aquilo",
    "é", "são", "foi", "era", "ser", "estar", "está", "há", "tem",
    "não", "sim", "já", "mais", "menos", "muito", "tão", "só", "também"
}

TAMANHO_MIN_PX = 14
TAMANHO_MAX_PX = 46

# Paletas de cores para a nuvem: são os "colormap" do matplotlib usados na aula
# (colormap='Greens', 'Reds', 'viridis', ...).
# "intervalo" indica que parte do colormap se usa (da palavra menos frequente para a
# mais frequente), para as palavras serem legíveis no fundo escuro do site.
# "amostra" são as cores mostradas no botão de cada paleta.
PALETAS = {
    "viridis": {"nome": "Viridis", "intervalo": (0.30, 1.00),
                "amostra": ["#31688e", "#26828e", "#35b779", "#90d743", "#fde725"]},
    "plasma": {"nome": "Plasma", "intervalo": (0.35, 1.00),
               "amostra": ["#a62098", "#cc4778", "#ed7953", "#fdb42f", "#f0f921"]},
    "Greens": {"nome": "Greens", "intervalo": (0.80, 0.20),
               "amostra": ["#2e9e50", "#41ab5d", "#74c476", "#a1d99b", "#d4eecd"]},
    "Reds": {"nome": "Reds", "intervalo": (0.75, 0.20),
             "amostra": ["#d42a2a", "#ef3b2c", "#fb6a4a", "#fc9272", "#fdd0bd"]},
    "Blues": {"nome": "Blues", "intervalo": (0.80, 0.20),
              "amostra": ["#3182bd", "#4292c6", "#6baed6", "#9ecae1", "#d6e6f4"]},
    "Greys": {"nome": "Greys", "intervalo": (0.60, 0.00),
              "amostra": ["#6e6e7a", "#8c8c98", "#b0b0ba", "#d4d4da", "#ffffff"]},
}

# Estado da nuvem de palavras
texto_atual = ""
frequencia_atual = {}
paleta_escolhida = "viridis"
wordcloud_carregado = False


# =====================================
# WIDGET 1 - ANALISADOR DE POESIA
# =====================================

@when("click", "#analyze-button")
def analisar_texto(event):
    global frequencia_atual, texto_atual

    texto = document.getElementById("poem-input").value
    resultado = document.getElementById("analysis-result")
    rewrite_section = document.getElementById("rewrite-section")
    cloud_section = document.getElementById("cloud-section")

    # Cada nova análise volta a esconder as opções e a nuvem anterior
    document.getElementById("cloud-options").style.display = "none"
    document.getElementById("word-cloud").style.display = "none"
    document.getElementById("word-cloud").innerHTML = ""

    if texto.strip() == "":
        resultado.innerText = "Por favor, escreve algum texto."
        if rewrite_section:
            rewrite_section.style.display = "none"
        if cloud_section:
            cloud_section.style.display = "none"

    else:
        palavras = texto.lower().split()

        caracteres = len(texto)
        total_palavras = len(palavras)
        palavras_diferentes = len(set(palavras))

        # Contar frequencia das palavras
        frequencia = {}

        for palavra in palavras:
            palavra = palavra.strip(PONTUACAO)

            if palavra != "":
                if palavra in frequencia:
                    frequencia[palavra] += 1
                else:
                    frequencia[palavra] = 1

        # Encontrar a palavra mais repetida
        palavra_frequente = max(frequencia, key=frequencia.get) if frequencia else "Nenhuma"
        repeticoes = frequencia[palavra_frequente] if frequencia else 0

        # Sugestoes simples
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
            <p>Palavra mais utilizada: {html.escape(palavra_frequente)}</p>
            <p>Repetições: {repeticoes}</p>
            <h4>Sugestão inteligente</h4>
            <p>{sugestao}</p>
        """

        # Guardar o texto e as frequências e mostrar o botão da nuvem de palavras
        texto_atual = texto
        frequencia_atual = frequencia
        if cloud_section:
            cloud_section.style.display = "block"

        # Mostrar a secção de substituição de sinónimos após a análise
        if rewrite_section:
            rewrite_section.style.display = "block"
            document.getElementById("rewrite-result").innerHTML = ""


# =====================================
# NUVEM DE PALAVRAS
# =====================================

def cor_na_paleta(cores, proporcao):
    # Mistura as duas cores da paleta mais próximas da proporção (0 a 1)
    posicao = proporcao * (len(cores) - 1)
    indice = min(int(posicao), len(cores) - 2)
    mistura = posicao - indice

    inicio = cores[indice]
    fim = cores[indice + 1]
    canais = []
    for i in (1, 3, 5):
        a = int(inicio[i:i + 2], 16)
        b = int(fim[i:i + 2], 16)
        canais.append(round(a + (b - a) * mistura))
    return "#{:02x}{:02x}{:02x}".format(*canais)


async def carregar_wordcloud():
    # O WordCloud (e o matplotlib, de que depende) só são descarregados na
    # primeira nuvem, para a página do analisador abrir depressa.
    global wordcloud_carregado
    if not wordcloud_carregado:
        import pyodide_js
        await pyodide_js.loadPackage("wordcloud")
        wordcloud_carregado = True


def gerar_nuvem_wordcloud(texto, quantidade, nome_paleta):
    # Código da aula (basics.ipynb, "7. Design: Nuvem de letras"), adaptado ao site
    from wordcloud import WordCloud
    from matplotlib import colormaps

    as_minhas_stopwords = PALAVRAS_COMUNS

    # -------------------- configurar e gerar a nuvem de palavras a partir do texto --------------------
    nuvem = WordCloud(
        width=600,               # mais alta do que larga: nuvem na vertical
        height=900,
        background_color=None,   # fundo transparente, para ficar com o fundo escuro do site
        mode="RGBA",
        colormap=nome_paleta,    # Greens, Reds, viridis, ...
        max_words=quantidade,
        stopwords=as_minhas_stopwords
    ).generate(texto)

    # -------------------- cores: as palavras mais frequentes ficam no fim do colormap --------------------
    mapa = colormaps[nome_paleta]
    inicio, fim = PALETAS[nome_paleta]["intervalo"]

    def cor_por_frequencia(word, **kwargs):
        frequencia_relativa = nuvem.words_.get(word, 0.5)  # 1 = palavra mais frequente
        r, g, b, _ = mapa(inicio + (fim - inicio) * frequencia_relativa)
        return f"rgb({int(r * 255)}, {int(g * 255)}, {int(b * 255)})"

    nuvem.recolor(color_func=cor_por_frequencia)

    # -------------------- exibir a imagem na página (em vez de plt.show()) --------------------
    # Na aula a imagem era guardada com nuvem.to_file('nuvem_de_palavras.png');
    # no navegador, a imagem é convertida em texto (base64) para aparecer na página.
    imagem = io.BytesIO()
    nuvem.to_image().save(imagem, format="PNG")
    imagem_base64 = base64.b64encode(imagem.getvalue()).decode("ascii")

    return imagem_base64, len(nuvem.words_)


def html_nuvem_imagem(imagem_base64, num_palavras, quantidade, nome_paleta):
    if num_palavras < quantidade:
        legenda = (f"Pediste {quantidade} palavras, mas o texto só tem {num_palavras} palavras "
                   f"importantes diferentes. As maiores são as que mais se repetem.")
    else:
        legenda = f"As {num_palavras} palavras mais importantes. As maiores são as que mais se repetem."

    origem = f"data:image/png;base64,{imagem_base64}"
    return f"""
        <h3>☁️ Nuvem de palavras · {PALETAS[nome_paleta]["nome"]}</h3>
        <p class="cloud-legend">{legenda}</p>
        <div class="cloud-words">
            <img class="cloud-image" src="{origem}" alt="Nuvem de palavras do texto analisado">
        </div>
        <a class="cloud-download" href="{origem}" download="nuvem_de_palavras.png">⬇ Descarregar imagem (PNG)</a>
    """


def gerar_nuvem_palavras(frequencia, quantidade, nome_paleta):
    # Versão alternativa em HTML, usada só se o WordCloud não puder ser carregado
    if not frequencia:
        return "<h3>☁️ Nuvem de palavras</h3><p class=\"cloud-legend\">Não há palavras suficientes para criar a nuvem.</p>"

    cores = PALETAS[nome_paleta]["amostra"]

    # Ignorar palavras muito comuns; se só houver essas, usar todas
    importantes = {p: n for p, n in frequencia.items() if p not in PALAVRAS_COMUNS}
    if not importantes:
        importantes = frequencia

    # Escolher as palavras mais frequentes (empate: ordem alfabética)
    ordenadas = sorted(importantes.items(), key=lambda item: (-item[1], item[0]))
    escolhidas = ordenadas[:quantidade]

    maximo = escolhidas[0][1]
    minimo = escolhidas[-1][1]

    elementos = []
    for palavra, contagem in escolhidas:
        # Tamanho e cor proporcionais ao número de repetições
        if maximo == minimo:
            proporcao = 0.5
        else:
            proporcao = (contagem - minimo) / (maximo - minimo)
        tamanho = round(TAMANHO_MIN_PX + proporcao * (TAMANHO_MAX_PX - TAMANHO_MIN_PX))
        cor = cor_na_paleta(cores, proporcao)

        vezes = "vez" if contagem == 1 else "vezes"
        elementos.append(
            f'<span class="cloud-word" style="font-size: {tamanho}px; color: {cor}" '
            f'title="{html.escape(palavra)}: {contagem} {vezes}">{html.escape(palavra)}</span>'
        )

    # Baralhar para as palavras grandes não ficarem todas no início
    random.shuffle(elementos)

    if len(escolhidas) < quantidade:
        legenda = (f"Pediste {quantidade} palavras, mas o texto só tem {len(escolhidas)} palavras "
                   f"importantes diferentes. As maiores são as que mais se repetem.")
    else:
        legenda = f"As {len(escolhidas)} palavras mais importantes. As maiores são as que mais se repetem."

    return f"""
        <h3>☁️ Nuvem de palavras · {PALETAS[nome_paleta]["nome"]}</h3>
        <p class="cloud-legend">{legenda}</p>
        <div class="cloud-words">{" ".join(elementos)}</div>
    """


def criar_botoes_paletas():
    # Cria um botão para cada paleta, com uma amostra das suas cores
    contentor = document.getElementById("palette-buttons")
    if not contentor:
        return
    botoes = []
    for chave, paleta in PALETAS.items():
        ativo = " active" if chave == paleta_escolhida else ""
        gradiente = ", ".join(paleta["amostra"])
        botoes.append(
            f'<button type="button" class="palette-btn{ativo}" data-palette="{chave}">'
            f'<span class="palette-swatch" style="background: linear-gradient(90deg, {gradiente})"></span>'
            f'{paleta["nome"]}</button>'
        )
    contentor.innerHTML = "".join(botoes)


criar_botoes_paletas()


@when("click", "#cloud-ask-button")
def mostrar_opcoes_nuvem(event):
    opcoes = document.getElementById("cloud-options")
    if opcoes.style.display == "none":
        opcoes.style.display = "flex"
    else:
        opcoes.style.display = "none"


@when("click", "#palette-buttons")
def escolher_paleta(event):
    global paleta_escolhida

    target = event.target
    botao = target.closest(".palette-btn") if target else None
    if not botao:
        return

    paleta_escolhida = botao.getAttribute("data-palette")
    for b in document.querySelectorAll(".palette-btn"):
        if b.getAttribute("data-palette") == paleta_escolhida:
            b.classList.add("active")
        else:
            b.classList.remove("active")


@when("input", "#cloud-count")
def atualizar_quantidade(event):
    valor = document.getElementById("cloud-count").value
    document.getElementById("cloud-count-value").innerText = valor


@when("click", "#cloud-generate-button")
async def gerar_nuvem(event):
    quantidade = int(document.getElementById("cloud-count").value)
    nuvem = document.getElementById("word-cloud")
    botao = document.getElementById("cloud-generate-button")

    if not frequencia_atual:
        nuvem.innerHTML = gerar_nuvem_palavras(frequencia_atual, quantidade, paleta_escolhida)
        nuvem.style.display = "block"
        return

    botao.disabled = True
    nuvem.style.display = "block"
    if wordcloud_carregado:
        nuvem.innerHTML = '<p class="cloud-legend">A gerar a nuvem de palavras...</p>'
    else:
        nuvem.innerHTML = ('<p class="cloud-legend">A carregar a biblioteca WordCloud '
                           '(só demora na primeira vez)...</p>')

    try:
        await carregar_wordcloud()
        imagem_base64, num_palavras = gerar_nuvem_wordcloud(texto_atual, quantidade, paleta_escolhida)
        if num_palavras == 0:
            nuvem.innerHTML = gerar_nuvem_palavras({}, quantidade, paleta_escolhida)
        else:
            nuvem.innerHTML = html_nuvem_imagem(imagem_base64, num_palavras, quantidade, paleta_escolhida)
    except Exception as erro:
        # Sem WordCloud (por exemplo, sem internet), usa a nuvem feita em HTML
        print("Não foi possível usar o WordCloud:", erro)
        nuvem.innerHTML = gerar_nuvem_palavras(frequencia_atual, quantidade, paleta_escolhida)
    finally:
        botao.disabled = False


# =====================================
# FERRAMENTA DE SUBSTITUIÇÃO DE SINÓNIMOS
# =====================================

@when("click", "#rewrite-button")
def reescrever_com_sinonimos(event):
    texto_original = document.getElementById("poem-input").value
    rewrite_resultado = document.getElementById("rewrite-result")

    # Separar em palavras mantendo os espaços e quebras de linha originais
    partes = re.split(r"(\s+)", texto_original)
    novas_partes = []
    substituicoes_feitas = 0

    for p in partes:
        if p == "" or p.isspace():
            novas_partes.append(p)
            continue

        pontuacao_inicio = ""
        pontuacao_fim = ""

        temp = p
        while temp and temp[0] in PONTUACAO:
            pontuacao_inicio += temp[0]
            temp = temp[1:]
        while temp and temp[-1] in PONTUACAO:
            pontuacao_fim = temp[-1] + pontuacao_fim
            temp = temp[:-1]

        palavra_limpa = temp.lower()

        if palavra_limpa in SINONIMOS:
            novo_termo = SINONIMOS[palavra_limpa]
            if temp.isupper() and len(temp) > 1:
                novo_termo = novo_termo.upper()
            elif temp[0].isupper():
                novo_termo = novo_termo.capitalize()

            novas_partes.append(
                html.escape(pontuacao_inicio)
                + f'<span class="synonym-word">{novo_termo}</span>'
                + html.escape(pontuacao_fim)
            )
            substituicoes_feitas += 1
        else:
            novas_partes.append(html.escape(p))

    texto_modificado = "".join(novas_partes)

    if substituicoes_feitas == 1:
        estatistica = "Foi substituída 1 palavra (destacada no texto)."
    elif substituicoes_feitas > 1:
        estatistica = f"Foram substituídas {substituicoes_feitas} palavras (destacadas no texto)."
    else:
        estatistica = "Não foram encontradas palavras com sinónimos disponíveis."

    rewrite_resultado.innerHTML = f"""
        <div class="rewrite-box">
            <h3>✨ Poema com Sinónimos Aplicados</h3>
            <p class="rewrite-stats">{estatistica}</p>
            <div class="rewritten-poem">{texto_modificado}</div>
        </div>
    """
