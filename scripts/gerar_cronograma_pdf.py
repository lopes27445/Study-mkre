"""Gera o cronograma diário em PDF a partir do plano de 4 semanas.

Uso:  python3 scripts/gerar_cronograma_pdf.py
Saída: cronograma-diario.pdf na raiz do repositório.

Para alterar o cronograma, edite a lista SEMANAS abaixo e rode o script de novo.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "cronograma-diario.pdf"

TINTA = colors.HexColor("#1a1a1a")
CINZA = colors.HexColor("#6b6b6b")
LINHA = colors.HexColor("#d4d4d4")
FUNDO = colors.HexColor("#f2f2f2")
MAT = colors.HexColor("#1f5c8b")
POR = colors.HexColor("#8b3a1f")
DESTAQUE = colors.HexColor("#fff4e0")

# ---------------------------------------------------------------- conteúdo

# Cada dia: (dia, matemática, português)
# Cada matéria: (duração, tópico, questões da banca)
SEMANAS = [
    {
        "n": 1,
        "titulo": "Geometria analítica &middot; Teoria da linguagem",
        "porque": "Geometria analítica é o conteúdo isolado mais cobrado (6 das 40 questões). "
        "Em Português, o texto-base do bloco 01-06 é sempre um texto teórico sobre linguagem — "
        "nas 4 provas.",
        "dias": [
            (
                "Segunda",
                ("1h", "<b>DIAGNÓSTICO</b> — 10 questões cronometradas, sem consulta nenhuma.",
                 "2026/1 G2 Q30 &middot; 2026/1 G1 Q31, Q32, Q34, Q35, Q36, Q37, Q38, Q39 &middot; 2026/2 Q35"),
                ("40min", "<b>DIAGNÓSTICO</b> — interpretação e literatura.",
                 "2025/2 Q01 a Q06 &middot; 2026/1 G1 Q08, Q09, Q10"),
            ),
            (
                "Terça",
                ("40min", "Corrigir o diagnóstico e classificar cada tópico em <b>sei / inseguro / "
                 "não sei</b>. Preencher o acompanhamento.", ""),
                ("1h", "Corrigir o diagnóstico (20min). Depois: <b>as 6 funções da linguagem</b>, "
                 "cada uma com um exemplo próprio (40min).", ""),
            ),
            (
                "Quarta",
                ("1h", "<b>Circunferência: equação reduzida e geral.</b> Completar quadrados para "
                 "achar centro e raio.", "2025/2 Q37"),
                ("40min", "Funções da linguagem na prática. Cuidado: <b>fática não é o mesmo que "
                 "emotiva ou poética</b> — foi essa a pegadinha da banca.", "2026/1 G1 Q04"),
            ),
            (
                "Quinta",
                ("40min", "Distância entre pontos, ponto médio, distância de ponto a reta. "
                 "Extensão para o espaço 3D.", "2026/2 Q33"),
                ("1h", "Linguagem <b>denotativa e conotativa</b>; texto <b>literário e não "
                 "literário</b>.", "2026/1 G2 Q01, Q02, Q03"),
            ),
            (
                "Sexta",
                ("1h", "Posições relativas entre reta e circunferência; <b>condição de "
                 "tangência</b>.", "2026/1 G1 Q34"),
                ("40min", "<b>Tipo textual e gênero textual</b>; linguagem verbo-visual.",
                 "2026/1 G2 Q04, Q05, Q06"),
            ),
            (
                "Sábado",
                ("1h", "Área de figuras por coordenadas; circunferência com sistema de inequações.",
                 "2026/2 Q36 &middot; 2026/1 G2 Q34"),
                ("1h", "Tese central e inferência. Faça o bloco inteiro cronometrado em 30 min.",
                 "2026/1 G1 Q01 a Q06"),
            ),
        ],
        "checkpoint": [
            "Passo da equação geral para a reduzida sem consultar nada",
            "Identifico a função da linguagem predominante em qualquer trecho",
        ],
    },
    {
        "n": 2,
        "titulo": "Trigonometria e geometria espacial &middot; Modernismo",
        "porque": "Trigonometria são 5 das 40 questões e caiu nas 4 provas. Modernismo é o único "
        "conteúdo de literatura presente nas 4 provas.",
        "dias": [
            (
                "Segunda",
                ("1h", "Triângulo retângulo: seno, cosseno e tangente. <b>Ângulos notáveis</b> "
                 "de 30, 45 e 60 graus.", "2025/2 Q36"),
                ("40min", "Modernismo: panorama das <b>3 fases</b> e quem pertence a cada uma.", ""),
            ),
            (
                "Terça",
                ("40min", "Ângulos notáveis na prática — o de 60 graus apareceu duas vezes.",
                 "2026/1 G2 Q35"),
                ("1h", "<b>1ª fase (1922-1930)</b>: Semana de 22, Mário e Oswald de Andrade, "
                 "ruptura e primitivismo; <b>Manuel Bandeira</b>.", ""),
            ),
            (
                "Quarta",
                ("1h", "<b>LEI DOS COSSENOS.</b> Cosseno de ângulo obtuso é negativo — reduza ao "
                 "1º quadrante antes de substituir.", "2026/1 G1 Q33 &middot; 2026/2 Q35"),
                ("40min", "<b>Manuel Bandeira</b> — o autor mais cobrado. Pasárgada, temática "
                 "amorosa em camadas, coloquialidade.", "2026/1 G2 Q09"),
            ),
            (
                "Quinta",
                ("40min", "<b>LEI DOS SENOS.</b> Regra para escolher: dois lados e o ângulo entre "
                 "eles, use cossenos; lado e ângulo opostos, use senos.", "2026/1 G2 Q33"),
                ("1h", "<b>2ª fase / Geração de 30</b>: Drummond. “No meio do caminho”, de "
                 "<i>Alguma Poesia</i> (1930).", "2025/2 Q07, Q08"),
            ),
            (
                "Sexta",
                ("1h", "Cilindro: volume e <b>área lateral</b>. Cone e pirâmide: a <b>razão 1/3</b> "
                 "em relação ao cilindro ou prisma de mesma base e altura.",
                 "2025/2 Q38 &middot; 2026/1 G1 Q37"),
                ("40min", "<b>Cecília Meireles</b> — musicalidade e introspecção, mas também o "
                 "<i>Romanceiro da Inconfidência</i>, épico e de crítica social.", "2025/2 Q09"),
            ),
            (
                "Sábado",
                ("1h", "<b>Tronco de cone</b> e sua planificação em setor circular. Depois: "
                 "revisão da semana.", "2026/1 G2 Q37"),
                ("1h", "<b>3ª fase / Geração de 45</b>: Clarice Lispector, Guimarães Rosa, "
                 "João Cabral.", "2026/1 G1 Q05, Q10"),
            ),
        ],
        "checkpoint": [
            "Escolho entre lei dos senos e lei dos cossenos sem hesitar",
            "Sei de cor: cone e pirâmide valem 1/3 do cilindro ou prisma equivalente",
            "Situo Bandeira, Drummond, Cecília, Clarice e Guimarães Rosa na fase certa",
        ],
        "estendido": "Simulado de sábado (+1h): prova 2026/1 Grupo 2, questões Q30 a Q39, em 50 min.",
    },
    {
        "n": 3,
        "titulo": "Geometria plana e funções &middot; Análise linguística e poesia contemporânea",
        "porque": "Funções somam 7 questões e geometria plana mais 4. Em Português, o bloco de "
        "análise linguística (questões 04 a 06) cai sempre e quase ninguém estuda direito.",
        "dias": [
            (
                "Segunda",
                ("1h", "<b>Teorema de Tales</b> e semelhança de triângulos.", "2026/1 G1 Q35"),
                ("40min", "<b>Valor semântico das conjunções</b>: adversativa, concessiva, "
                 "conclusiva, causal e final.", ""),
            ),
            (
                "Terça",
                ("40min", "Razão de semelhança: se os lados estão na razão <i>k</i>, as áreas "
                 "estão em <i>k</i><super>2</super> e os volumes em <i>k</i><super>3</super>.",
                 "2025/2 Q32"),
                ("1h", "Conjunções na prática. Mais: <b>por que / por quê / porque / porquê</b>.",
                 "2025/2 Q06"),
            ),
            (
                "Quarta",
                ("1h", "Relações métricas na circunferência com Pitágoras; áreas de setores e "
                 "semicírculos.", "2026/1 G1 Q36 &middot; 2026/1 G2 Q36"),
                ("40min", "<b>Pontuação expressiva</b>: aspas, parênteses e travessão. Eles "
                 "explicam e nuançam — não corrigem. A banca já armou nisso.", "2026/2 Q05"),
            ),
            (
                "Quinta",
                ("40min", "<b>Função afim</b>: modelagem a partir de dois pontos, coeficiente "
                 "angular, raiz e intercepto.", "2026/1 G2 Q31 &middot; 2025/2 Q31"),
                ("1h", "Sinonímia contextual e <b>coesão referencial</b> — anáfora retoma, "
                 "catáfora antecipa.", "2026/2 Q06 &middot; 2026/1 G1 Q06"),
            ),
            (
                "Sexta",
                ("1h", "<b>Função quadrática</b>: vértice em x<sub>v</sub> = -b/2a, máximo e "
                 "mínimo. E <b>domínio</b>: raiz par, denominador e logaritmando.",
                 "2026/1 G1 Q31 &middot; 2026/2 Q31, Q32"),
                ("40min", "<b>Pressupostos e implícitos</b> no texto.", "2025/2 Q05"),
            ),
            (
                "Sábado",
                ("1h", "<b>Função composta</b> g(f(x)). <b>Logaritmos</b>: propriedades "
                 "operatórias e meia-vida.",
                 "2026/2 Q37 &middot; 2026/1 G2 Q32 &middot; 2025/2 Q34"),
                ("1h", "<b>Poesia contemporânea</b>: liberdade formal, questão feminina, relações "
                 "raciais, tom político.", "2026/1 G1 Q07 &middot; 2026/1 G2 Q07, Q10"),
            ),
        ],
        "checkpoint": [
            "Identifico o valor de qualquer conjunção dentro do texto",
            "Acho o vértice da parábola e o domínio de uma função sem consultar",
            "Sei a diferença entre razão de semelhança, de áreas e de volumes",
        ],
        "estendido": "Simulado de sábado (+1h): prova 2026/1 Grupo 2, questões Q01 a Q10, em 40 min.",
    },
    {
        "n": 4,
        "titulo": "Sequências e contagem &middot; Intertextualidade e revisão",
        "porque": "Fecha os conteúdos que faltam e reserva os dois últimos dias para revisão e "
        "simulado — que é onde o estudo das 4 semanas vira acerto.",
        "dias": [
            (
                "Segunda",
                ("1h", "<b>PA</b>: termo geral e soma dos n primeiros termos.",
                 "2025/2 Q33 &middot; 2026/1 G2 Q36"),
                ("40min", "<b>Intertextualidade</b>: paráfrase, paródia, pastiche, epígrafe, "
                 "citação e alusão.", ""),
            ),
            (
                "Terça",
                ("40min", "<b>PG infinita</b>: S = a<sub>1</sub>/(1-q) — vale só para razão entre "
                 "-1 e 1. Armadilha real: a bolinha que quica conta subida <i>e</i> descida.",
                 "2026/1 G1 Q38 &middot; 2026/1 G2 Q38"),
                ("1h", "O caso clássico da banca: <b>“Canção do Exílio”</b> e suas releituras; "
                 "Pasárgada relida por Millôr; Camões dialogando com Petrarca.",
                 "2026/2 Q07, Q08, Q09, Q10"),
            ),
            (
                "Quarta",
                ("1h", "<b>Combinatória</b>: permutação com elementos repetidos e permutação com "
                 "blocos que ficam juntos.", "2026/1 G1 Q39 &middot; 2025/2 Q35"),
                ("40min", "<b>Camões / Classicismo</b>: lírica idealizada, platonismo, "
                 "<i>Os Lusíadas</i>.", "2026/1 G2 Q08"),
            ),
            (
                "Quinta",
                ("40min", "<b>Probabilidade</b> em arranjos e em conjuntos de pontos.",
                 "2026/1 G2 Q39 &middot; 2026/2 Q39"),
                ("1h", "<b>Romantismo</b> (as 3 gerações, foco no “Mal do Século”) e "
                 "<b>Simbolismo</b> (Cruz e Sousa).", "2026/1 G1 Q09, Q08"),
            ),
            (
                "Sexta",
                ("1h", "<b>A questão 30</b> — a mais fácil da prova nas 4 edições. Regra de três, "
                 "porcentagem, aumentos sucessivos, média, moda e mediana.",
                 "2026/1 G1 Q30 &middot; 2026/1 G2 Q30 &middot; 2026/2 Q30, Q34, Q38 &middot; 2025/2 Q30"),
                ("40min", "Gêneros literários: <b>conto e romance</b> (Machado, Clarice, Guimarães "
                 "Rosa). Depois, releia o <b>caderno de erros</b> inteiro.", "2025/2 Q10"),
            ),
            (
                "Sábado",
                ("1h20", "<b>SIMULADO FINAL</b>, cronometrado e sem consulta: prova 2026/2, "
                 "questões <b>Q01 a Q10</b> e <b>Q30 a Q39</b>. São 20 questões em 1h20, que é o "
                 "tempo proporcional real da prova.", ""),
                ("40min", "Correção do simulado. Para cada erro, escreva <b>por que</b> errou. "
                 "Meta realista: 13 a 15 acertos em 20.", ""),
            ),
        ],
        "checkpoint": [
            "Faço permutação com repetição e permutação com blocos",
            "Sei a diferença entre paráfrase, paródia e pastiche",
            "Caderno de erros revisado do começo ao fim",
        ],
    },
]

# ---------------------------------------------------------------- estilos

folha = getSampleStyleSheet()


def estilo(nome, **kw):
    base = dict(fontName="Helvetica", fontSize=8.4, leading=10.6, textColor=TINTA)
    base.update(kw)
    return ParagraphStyle(nome, parent=folha["Normal"], **base)


E_TITULO = estilo("titulo", fontName="Helvetica-Bold", fontSize=19, leading=22)
E_SUB = estilo("sub", fontSize=10.5, leading=14, textColor=CINZA)
E_H2 = estilo("h2", fontName="Helvetica-Bold", fontSize=13.5, leading=16)
E_H2SUB = estilo("h2sub", fontSize=9, leading=12, textColor=CINZA)
E_CORPO = estilo("corpo")
E_NOTA = estilo("nota", fontSize=8.6, leading=11.6)
E_DIA = estilo("dia", fontName="Helvetica-Bold", fontSize=9, leading=11)
E_DUR = estilo("dur", fontName="Helvetica-Bold", fontSize=7.4, leading=9, textColor=CINZA)
E_MATLBL = estilo("matlbl", fontName="Helvetica-Bold", fontSize=7, leading=9, textColor=MAT)
E_PORLBL = estilo("porlbl", fontName="Helvetica-Bold", fontSize=7, leading=9, textColor=POR)
E_QUEST = estilo("quest", fontName="Helvetica-Oblique", fontSize=7.4, leading=9.4, textColor=CINZA)
E_CAB = estilo("cab", fontName="Helvetica-Bold", fontSize=7.6, leading=9.6, textColor=colors.white)
E_RODA = estilo("roda", fontSize=7.4, leading=9, textColor=CINZA, alignment=TA_CENTER)


def celula(rotulo_estilo, rotulo, duracao, texto, questoes):
    """Monta a célula de uma matéria: rótulo + duração, tópico e questões."""
    partes = [
        Table(
            [[Paragraph(rotulo, rotulo_estilo), Paragraph(duracao, E_DUR)]],
            colWidths=[2.4 * cm, 3.9 * cm],
            style=TableStyle([
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]),
        ),
        Paragraph(texto, E_CORPO),
    ]
    if questoes:
        partes.append(Spacer(1, 2.2))
        partes.append(Paragraph("Questões: " + questoes, E_QUEST))
    return partes


def pagina_semana(semana):
    """Uma página por semana."""
    bloco = [
        Paragraph(f"Semana {semana['n']} &nbsp;&middot;&nbsp; {semana['titulo']}", E_H2),
        Spacer(1, 3),
        Paragraph(semana["porque"], E_H2SUB),
        Spacer(1, 10),
    ]

    linhas = [[
        Paragraph("FEITO", E_CAB),
        Paragraph("DIA", E_CAB),
        Paragraph("MATEMÁTICA", E_CAB),
        Paragraph("PORTUGUÊS", E_CAB),
    ]]
    for dia, mat, por in semana["dias"]:
        linhas.append([
            "",
            Paragraph(dia, E_DIA),
            celula(E_MATLBL, "MAT", mat[0], mat[1], mat[2]),
            celula(E_PORLBL, "POR", por[0], por[1], por[2]),
        ])

    estilo_tabela = [
        ("BACKGROUND", (0, 0), (-1, 0), TINTA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, LINHA),
        ("BOX", (0, 0), (-1, -1), 0.7, TINTA),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ]
    # Quadradinho para marcar cada dia concluído.
    for i in range(1, len(linhas)):
        estilo_tabela.append(("INNERGRID", (0, i), (0, i), 0.4, LINHA))
    # Destaque para o simulado final.
    if semana["n"] == 4:
        estilo_tabela.append(("BACKGROUND", (1, 6), (-1, 6), DESTAQUE))

    bloco.append(Table(
        linhas,
        colWidths=[1.15 * cm, 1.75 * cm, 6.75 * cm, 6.75 * cm],
        style=TableStyle(estilo_tabela),
        repeatRows=1,
    ))
    bloco.append(Spacer(1, 9))

    dentro = [Paragraph(f"<b>Checkpoint da semana {semana['n']}</b>", E_NOTA), Spacer(1, 5)]
    marcas = [["", Paragraph(c, E_NOTA)] for c in semana["checkpoint"]]
    estilo_marcas = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (1, 0), (1, -1), 7),
    ]
    # Quadradinho vazio de verdade, desenhado como borda de célula.
    for i in range(len(marcas)):
        estilo_marcas.append(("BOX", (0, i), (0, i), 0.5, CINZA))
        estilo_marcas.append(("BACKGROUND", (0, i), (0, i), colors.white))
        estilo_marcas.append(("TOPPADDING", (0, i), (0, i), 1))
        estilo_marcas.append(("BOTTOMPADDING", (0, i), (0, i), 1))
    dentro.append(Table(
        marcas,
        colWidths=[0.34 * cm, 15.4 * cm],
        rowHeights=[0.42 * cm] * len(marcas),
        style=TableStyle(estilo_marcas),
        hAlign="LEFT",
    ))
    if semana.get("estendido"):
        dentro.append(Spacer(1, 6))
        dentro.append(Paragraph(
            f"<b>Faixa estendida:</b> {semana['estendido']}", E_NOTA))

    bloco.append(Table(
        [[dentro]],
        colWidths=[16.4 * cm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), FUNDO),
            ("BOX", (0, 0), (-1, -1), 0.4, LINHA),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]),
    ))

    # Espaço pautado para anotar dúvidas da semana.
    bloco.append(Spacer(1, 12))
    bloco.append(Paragraph(
        "Dúvidas e questões para revisar", E_DUR))
    bloco.append(Spacer(1, 4))
    n_linhas = 5
    bloco.append(Table(
        [[""] for _ in range(n_linhas)],
        colWidths=[16.4 * cm],
        rowHeights=[0.62 * cm] * n_linhas,
        style=TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINHA),
        ]),
        hAlign="LEFT",
    ))
    return bloco


def capa():
    grade = [
        [Paragraph(t, E_CAB) for t in ("DIA", "MATEMÁTICA", "PORTUGUÊS", "TOTAL")],
        ["Segunda", "1h00", "40min", "1h40"],
        ["Terça", "40min", "1h00", "1h40"],
        ["Quarta", "1h00", "40min", "1h40"],
        ["Quinta", "40min", "1h00", "1h40"],
        ["Sexta", "1h00", "40min", "1h40"],
        ["Sábado", "1h00", "1h00", "2h00"],
        ["Domingo", "descanso", "descanso", "-"],
        ["Total", "5h20", "5h00", "10h20"],
    ]
    linhas = [grade[0]] + [
        [Paragraph(c, E_CORPO) for c in linha] for linha in grade[1:]
    ]
    tabela_grade = Table(
        linhas,
        colWidths=[3.6 * cm, 3.2 * cm, 3.2 * cm, 2.6 * cm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), TINTA),
            ("GRID", (0, 0), (-1, -1), 0.4, LINHA),
            ("BOX", (0, 0), (-1, -1), 0.7, TINTA),
            ("BACKGROUND", (0, 8), (-1, 8), FUNDO),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]),
        hAlign="LEFT",
    )

    regras = (
        "<b>Três regras que valem mais que o cronograma</b><br/><br/>"
        "<b>1.</b>&nbsp; Questão da própria banca vale por três de qualquer outra fonte. "
        "Você tem 4 provas inteiras — prefira sempre resolver questão real a ler resumo.<br/><br/>"
        "<b>2.</b>&nbsp; Erro sem anotação é erro que vai se repetir. Toda questão errada entra no "
        "caderno de erros no mesmo dia, com o motivo real — e “errei por besteira” não é "
        "motivo.<br/><br/>"
        "<b>3.</b>&nbsp; Se atrasar, corte teoria, nunca exercício. E não tente recuperar os dias "
        "perdidos: retome de onde parou. O plano é uma ordem de prioridades, não um calendário."
    )

    return [
        Spacer(1, 12),
        Paragraph("Cronograma diário", E_TITULO),
        Spacer(1, 5),
        Paragraph(
            "Português e Matemática &nbsp;&middot;&nbsp; 4 semanas &nbsp;&middot;&nbsp; "
            "Vestibular Mackenzie",
            E_SUB,
        ),
        Spacer(1, 16),
        Paragraph(
            "Montado a partir da análise das 4 provas mais recentes (2025/2, 2026/1 Grupo 1, "
            "2026/1 Grupo 2 e 2026/2). Cada dia indica o tópico e as <b>questões reais da banca</b> "
            "para treinar. Português e Matemática somam 20 das 60 questões da prova.",
            E_CORPO,
        ),
        Spacer(1, 16),
        Paragraph("A grade da semana", E_H2),
        Spacer(1, 6),
        tabela_grade,
        Spacer(1, 8),
        Paragraph(
            "Esta é a <b>faixa núcleo</b>, de 10h20 por semana. Na <b>faixa estendida</b> (15h20), "
            "acrescente 30 min de questões de segunda a sexta, 1h de simulado no sábado e 1h30 de "
            "revisão do caderno de erros no domingo.",
            E_NOTA,
        ),
        Spacer(1, 18),
        Table(
            [[Paragraph(regras, E_NOTA)]],
            colWidths=[16.4 * cm],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), FUNDO),
                ("BOX", (0, 0), (-1, -1), 0.4, LINHA),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]),
        ),
    ]


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.2)
    canvas.setFillColor(CINZA)
    canvas.drawCentredString(
        A4[0] / 2, 1.05 * cm, f"Cronograma diário — Português e Matemática   |   {doc.page}"
    )
    canvas.restoreState()


def main():
    doc = SimpleDocTemplate(
        str(SAIDA),
        pagesize=A4,
        leftMargin=2.3 * cm,
        rightMargin=2.3 * cm,
        topMargin=1.9 * cm,
        bottomMargin=1.7 * cm,
        title="Cronograma diário - Português e Matemática",
        author="Study-mkre",
        subject="Plano de estudo de 4 semanas para o Vestibular Mackenzie",
    )

    historia = capa()
    for semana in SEMANAS:
        historia.append(PageBreak())
        historia.extend(pagina_semana(semana))

    doc.build(historia, onFirstPage=rodape, onLaterPages=rodape)
    print(f"gerado: {SAIDA}")


if __name__ == "__main__":
    main()
