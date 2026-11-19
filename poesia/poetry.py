from pyscript import document, when
import html
import re

# REMOVER ECRA DE CARREGAMENTO
loading = document.getElementById("loading")
if loading:
    loading.remove()


# Dicionário de sinónimos para substituição
SINONIMOS = {
    "feliz": "contente",
    "triste": "melancólico",
    "belo": "lindo",
    "belos": "lindos",
    "bela": "linda",
    "belas": "lindas",
    "bom": "ótimo",
    "grande": "vasto",
    "pequeno": "reduzido",
    "noite": "negrume",
    "dia": "claridade",
    "sol": "astro",
    "mar": "oceano",
    "vento": "brisa",
    "frio": "gelado",
    "calor": "quentura",
    "amor": "afeto",
    "vida": "existência",
    "tempo": "espaço"
}

PONTUACAO = ".,!?;:()[]\"'«»"


# =====================================
# WIDGET 1 - ANALISADOR DE POESIA
# =====================================

@when("click", "#analyze-button")
def analisar_texto(event):

    texto = document.getElementById("poem-input").value
    resultado = document.getElementById("analysis-result")
    rewrite_section = document.getElementById("rewrite-section")

    if texto.strip() == "":
        resultado.innerText = "Por favor, escreve algum texto."
        if rewrite_section:
            rewrite_section.style.display = "none"

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

        # Mostrar a secção de substituição de sinónimos após a análise
        if rewrite_section:
            rewrite_section.style.display = "block"
            document.getElementById("rewrite-result").innerHTML = ""


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
