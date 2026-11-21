# Dashboard Multimédia

| | |
|---|---|
| **Nome da Aplicação / Dashboard Web** | Dashboard Multimédia |
| **Disciplina** | Oficina de Multimédia – 12.º Ano – CRSI |
| **Ano Letivo** | 2026/2027 |
| **Autor** | Francisco gomes |
| **Turma** |12ºA3|
| **Link da Aplicação Web** | _[Link do GitHub Pages]_ |

---

## 1. Visão Geral do Projeto

**Descrição:** O Dashboard Multimédia é uma aplicação web estática que reúne, numa página principal, três ferramentas interativas escritas em **Python que corre diretamente no navegador** através do **PyScript**. O objetivo é mostrar como a programação em Python pode ser combinada com HTML e CSS para criar experiências multimédia: analisar textos e poemas (com nuvem de palavras), jogar ao Jogo do Galo contra o computador ou contra um amigo e testar conhecimentos num questionário de multimédia com tempo limite.

**Proposta Escolhida:** Proposta 1

**Tecnologias:** HTML5 · CSS3 · Python (PyScript `2025.11.1`) · biblioteca `wordcloud` / `matplotlib` (carregada no navegador via Pyodide) · fonte Inter (Google Fonts).


## 2. Estrutura do Código e Funcionalidades Integradas

O projeto **parte dos exercícios das fichas da aula**  e **amplia-os com novos exercícios desenvolvidos com apoio de IA**.

### 2.1 Página principal (`index.html`)
Página em HTML puro (sem PyScript), organizada em "tiles" no estilo *bento grid*, com um cartão para cada ferramenta.

### 2.2 Analisador de Poesia (`poesia/`) — **adaptado das fichas**
- **Contagem de palavras e frequências** — adaptado do exercício *6.1 Contagem de palavras de um texto* (uso de `split()`, `lower()`, `strip()` e dicionários).
- **Estatísticas:** número de caracteres, palavras, palavras diferentes (`set`), palavra mais utilizada e número de repetições.
- **Sugestão inteligente** sobre a variedade do vocabulário (estruturas `if/elif/else`).
- **Nuvem de palavras** — adaptada do exercício *7. Design: Nuvem de letras* (biblioteca `WordCloud` com `colormap` e `stopwords`). No site:
  - a biblioteca só é descarregada na primeira utilização, para a página abrir depressa;
  - o utilizador escolhe a **quantidade de palavras** e a **paleta de cores** (Viridis, Plasma, Greens, Reds, Blues, Greys);
  - a imagem é convertida para base64 para aparecer na página (em vez de `plt.show()`/`to_file()`) e pode ser **descarregada em PNG**;
  - se a biblioteca não carregar (ex.: sem internet), é gerada uma nuvem alternativa em HTML.
- **Reescrita com sinónimos**  — dicionário com mais de 200 sinónimos organizados por categorias, que respeitam o género e o número da palavra original; mantém a pontuação, as maiúsculas e as quebras de linha, e destaca as palavras substituídas.

### 2.3 Jogo do Galo (`galo/`) — **novo exercício com IA**
- Tabuleiro 3×3 com listas e verificação das 8 combinações de vitória.
- **Modo vs Computador** com três níveis de dificuldade:
  - **Fácil** — jogadas aleatórias (`random.choice`);
  - **Médio** — 50% das vezes tenta ganhar/bloquear, 50% joga ao acaso;
  - **Difícil** — algoritmo **Minimax** (imbatível).
- **Modo 2 jogadores** no mesmo computador.
- Placar de vitórias/empates, destaque da linha vencedora e janela animada de fim de partida.
- Pausa assíncrona (`asyncio.sleep`) para simular o computador "a pensar".

### 2.4 Questionário de Multimédia (`quiz/`) — 
- Banco de 18 perguntas sobre formatos de imagem/áudio/vídeo, cor (RGB/CMYK), resoluções, HTML/CSS, etc. (lista de dicionários).
- Cada jogo escolhe **5 perguntas aleatórias** (`random.sample`) e baralha as opções.
- **Temporizador de 10 segundos** por pergunta com barra de progresso; nos últimos 3 segundos aparece uma bomba 💣 e, se o tempo acabar, há uma **animação de explosão** com o ecrã a tremer.
- Feedback imediato com explicação e dica, e pontuação final com mensagem personalizada.

### 2.5 Conceitos de Python utilizados
Variáveis, listas, tuplos, sets, dicionários, f-strings, métodos de strings, ciclos `for`/`while`, condições, funções, módulos (`random`, `re`, `html`, `base64`, `io`, `asyncio`), eventos com `@when` e manipulação do DOM com `document.getElementById(...)`.

---

## 3. Registo de Utilização da IA

Ao longo do projeto trabalhei em parceria com assistentes de IA (Google antigravity / Claude / Mistral — ). Seguem-se os prompts mais relevantes.

### 3.1 Prompt para conversão Web/HTML

> "Tenho este código Python de um caderno Jupyter que conta as palavras de um texto e gera uma nuvem de palavras com a biblioteca WordCloud. Converte-o numa página web usando PyScript, de forma a que o utilizador escreva o texto numa caixa, carregue num botão 'Analisar' e veja os resultados na página. Mantém o código em Python e os nomes das variáveis em português."

> "Em vez de guardar a nuvem de palavras com `to_file()` e mostrá-la com `plt.show()`, como posso mostrar a imagem diretamente na página HTML com PyScript?"

> "Cria uma página principal `index.html` em estilo dashboard com cartões que liguem a três ferramentas: um analisador de poesia, um jogo do galo e um questionário de multimédia."

### 3.2 Prompt para ampliação e construção de funcionalidades

> "Acrescenta ao analisador de poesia uma ferramenta que reescreva o poema substituindo palavras por sinónimos. Os sinónimos devem ter o mesmo género e número da palavra original e as palavras substituídas devem ficar destacadas."

> "Permite ao utilizador escolher quantas palavras aparecem na nuvem e escolher a paleta de cores entre vários colormaps do matplotlib (viridis, plasma, Greens, Reds, Blues, Greys), com um botão para descarregar a imagem."

> "Cria um Jogo do Galo em PyScript com modo contra o computador e modo de 2 jogadores. O computador deve ter três dificuldades: fácil (aleatório), médio (às vezes ganha ou bloqueia) e difícil (usa o algoritmo minimax). Mostra um placar e uma janela animada no fim de cada partida."

> "Cria um questionário de multimédia com um banco de perguntas sobre formatos de ficheiros, cores, resoluções e web. Em cada jogo devem aparecer 5 perguntas aleatórias, com 10 segundos para responder a cada uma. Se o tempo acabar, mostra uma bomba a explodir e o ecrã a tremer."

### 3.3 Dificuldades e erros corrigidos com a IA

| Problema | Solução encontrada com a IA |
|---|---|
| A página ficava em branco ao abrir o ficheiro diretamente (`file://`). | O PyScript precisa de um servidor HTTP; passei a usar `python -m http.server` / Live Preview. |
| A página demorava muito a carregar e parecia não funcionar. | Foi criado um ecrã de carregamento (`#loading`) que o Python remove quando termina de carregar. |
| A biblioteca WordCloud tornava a abertura do analisador muito lenta. | A biblioteca passou a ser carregada só quando se gera a primeira nuvem , com uma nuvem em HTML como alternativa caso falhe. |
| As palavras da nuvem eram ilegíveis no fundo escuro. | Fundo transparente (`mode="RGBA"`) e uso apenas da parte mais clara de cada colormap. |
| No questionário, ao avançar de pergunta, o temporizador antigo continuava a contar e "explodia" na pergunta seguinte. | Uso de um contador `ciclo_pergunta_atual`: cada temporizador verifica se ainda pertence à pergunta atual e termina se não pertencer. |
| No Jogo do Galo era possível clicar no tabuleiro enquanto o computador jogava. | Variável `bloqueio_input` que bloqueia os cliques durante a vez do computador. |
| Os sinónimos estragavam a concordância ("a noite" → "a escuro"). | O dicionário foi revisto para cada sinónimo ter o mesmo género e número da palavra original. |
| Pontuação e maiúsculas perdiam-se ao trocar palavras por sinónimos. | Separação da pontuação no início/fim de cada palavra e reposição das maiúsculas depois da troca. |

### 3.4 Otimização de Layout

Sugestões feitas à IA para melhorar o design:

> "Muda o design para um tema escuro moderno, em estilo *bento grid*, com cartões de cantos arredondados e um destaque em roxo."

> "Usa a fonte Inter do Google Fonts e aumenta o tamanho e o peso do título principal."

> "Aumenta as margens e o espaçamento entre os cartões e faz com que o layout se adapte ao telemóvel."

> "Os botões devem ter cantos arredondados, um efeito ao passar o rato (hover) e um estado 'ativo' para a dificuldade e a paleta escolhidas."

> "No jogo do galo, as cruzes (X) e as bolas (O) devem ter cores diferentes e a linha vencedora deve ficar destacada com uma animação."

> "No questionário, a barra do tempo deve ficar vermelha e a piscar quando faltarem 3 segundos; as respostas certas a verde e as erradas a vermelho."

---

## 4. Estrutura de Ficheiros do Repositório

```
dashboard_multimédia/
├── index.html            – página principal do Dashboard (hub com os cartões)
├── style.css             – folha de estilos partilhada por todas as páginas
├── README.md             – relatório do projeto
├── basics.ipynb          – caderno com os exercícios das fichas da aula
├── poesia/
│   ├── poetry.html       – página do Analisador de Poesia
│   └── poetry.py         – análise de texto, nuvem de palavras e sinónimos
├── galo/
│   ├── galo.html         – página do Jogo do Galo
│   └── galo.py           – lógica do jogo e IA do computador (minimax)
└── quiz/
    ├── quiz.html         – página do Questionário de Multimédia
    └── quiz.py           – banco de perguntas, temporizador e pontuação
```

1. **index.html** – página principal do Dashboard / Web App.
2. **poesia/poetry.py, galo/galo.py, quiz/quiz.py** – ficheiros Python de cada aplicação (executados no navegador pelo PyScript).
3. **style.css** – folha de estilos para o layout web.
4. **README.md** – relatório do projeto.
5. **Assets** – as nuvens de palavras são geradas dinamicamente e podem ser descarregadas em PNG; a fonte Inter e o PyScript são carregados a partir da internet.
