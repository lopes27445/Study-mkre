#!/usr/bin/env python3
"""
Gera analise/investment-banking.pdf a partir de analise/investment-banking.html.

O HTML da página é a fonte única de verdade: este script apenas o adapta para
impressão (A4), acrescenta capa e sumário, numera as páginas e grava os
marcadores de navegação do PDF.

Requisitos:
    pip install pypdf
    npm install playwright        (o Chromium do ambiente é reaproveitado)

Uso:
    python3 analise/gerar-pdf.py
    PLAYWRIGHT_DIR=/caminho/com/node_modules python3 analise/gerar-pdf.py
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter

RAIZ = Path(__file__).resolve().parent
FONTE = RAIZ / "investment-banking.html"
SAIDA = RAIZ / "investment-banking.pdf"
DATA = "20 de setembro de 2026"

SECOES = [
    ("01", "O que é um banco de investimento"),
    ("02", "As áreas de um banco por dentro"),
    ("03", "Quanto custa contratar um banco"),
    ("04", "O ciclo de um deal, passo a passo"),
    ("05", "A caixa de ferramentas: valuation"),
    ("06", "Quem são os players"),
    ("07", "O mercado agora"),
    ("08", "A escada de carreira"),
    ("09", "Como se entra, no Brasil"),
    ("10", "O lado duro, sem maquiagem"),
    ("11", "Glossário para não travar na conversa"),
    ("12", "Por onde começar agora"),
]

CSS_IMPRESSAO = """
@page{size:A4}
*{-webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{background:#fff}
body{font-size:10.4pt;line-height:1.55}
.wrap{max-width:none;margin:0;padding:0}
.indice,.busca-linha,#glossario-contador,#glossario-vazio,.leitura,#check-progresso{display:none}
.topo{display:none}
section{padding-top:0;break-before:page}
h2{font-size:16.5pt;margin-bottom:5pt;break-after:avoid}
h2 .num{font-size:9.5pt}
h3{font-size:12.5pt;margin:17pt 0 6pt;break-after:avoid}
.sub{font-size:10.4pt;margin-bottom:14pt;break-after:avoid}
p,.item p,.passo p,.duro-item p{max-width:none}
.painel,.item,.passo,.duro-item,.termo,.stat,.grafico,.destaque,.check-item,tr,figure{break-inside:avoid}
.tomb-bloco{break-inside:auto}
.painel,.tomb{box-shadow:none}
.painel{padding:16pt 18pt}
.tabela-wrap{overflow:visible}
table{min-width:0;font-size:9.3pt}
th{font-size:8pt}
td{padding:7pt 10pt 7pt 0}
td .miudo{font-size:8.6pt}
.num-col{font-size:8.8pt}
.stats{grid-template-columns:repeat(2,minmax(0,1fr))}
.stat{padding:11pt 13pt}
.stat .n{font-size:18pt}
.stat .r{font-size:9.6pt}
.grade{gap:0 26px}
.item p{font-size:9.8pt;max-width:none}
.passo p{font-size:9.8pt}
.termo dd{font-size:9.8pt}
.destaque{padding:12pt 15pt;margin-top:16pt}
.destaque p{font-size:10pt}
.nota{font-size:8.6pt}
.grafico{margin-top:16pt}
.barra .rot{font-size:9.8pt}
.tomb-val{font-size:26pt}
.anatomia li{font-size:9.8pt}
.tomb-bloco{display:block}
.tomb{max-width:104mm;margin:0 auto;padding:13pt 14pt}
.tomb-mini{margin-bottom:10pt}
.tomb-emp{font-size:16pt}
.tomb-val{font-size:21pt;margin:8pt 0 4pt}
.tomb-desc{font-size:10pt}
.tomb-rule{margin:12pt 0 10pt}
.tomb-rol{font-size:8.5pt}
.tomb-bancos{font-size:11pt;margin-bottom:9pt}
.tomb-bancos.lider{font-size:13pt}
.tomb-data{margin-top:2pt}
.anatomia{margin-top:14pt}
.anatomia li{padding:8pt 0;font-size:9.6pt}
.check-item{cursor:default}
.check-item span{font-size:10pt}
footer{break-before:page;margin-top:0;padding-top:0;border-top:0;font-size:9pt}
footer::before{content:"Fontes e notas";display:block;font-family:var(--display);font-weight:700;
  font-size:16.5pt;letter-spacing:-.015em;color:var(--ink);margin-bottom:10pt}
"""

CSS_CAPA = """
*{-webkit-print-color-adjust:exact;print-color-adjust:exact;box-sizing:border-box}
html,body{margin:0;background:var(--paper);height:100%}
.capa{height:100%;display:flex;flex-direction:column;padding:26mm 22mm 20mm}
.capa-topo{border-top:3px solid var(--ink);padding-top:14px}
.capa .eyebrow{margin-bottom:10px}
.capa h1{font-size:44pt;margin:0;line-height:1.05}
.capa .dek{font-size:13.5pt;margin-top:14px;max-width:34em}
.capa-meio{margin-top:26px;border-top:1px solid var(--linha-forte);padding-top:14px}
.capa-meio p{font-size:11pt;color:var(--grafite);max-width:40em;margin:0}
.capa-meio p b{color:var(--ink)}
.capa .rotulo{font-family:var(--mono);font-size:8.5pt;letter-spacing:.14em;text-transform:uppercase;
  color:var(--grafite-soft);margin:auto 0 8px}
.capa .stats{grid-template-columns:repeat(2,minmax(0,1fr))}
.capa .stat .n{font-size:17pt}
.capa .stat .r{font-size:9.4pt}
.capa-rodape{margin-top:22px;border-top:1px solid var(--linha-forte);padding-top:12px;
  font-family:var(--mono);font-size:9pt;color:var(--grafite);display:flex;
  justify-content:space-between;gap:12px;flex-wrap:wrap}
.capa .fontes{margin-top:18px}
.capa .fontes b{font-size:9pt}
"""

RENDER_JS = r"""
import { chromium } from 'playwright';
const [,, htmlPath, pdfPath, modo] = process.argv;
const exe = process.env.CHROME_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ colorScheme: 'light' });
await page.goto('file://' + htmlPath, { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(600);
const rodape = `<div style="width:100%;padding:0 18mm;font-family:monospace;font-size:7.5pt;
  color:#828B9E;display:flex;justify-content:space-between;">
  <span>Mapa do Investment Banking &middot; material de estudo</span>
  <span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`;
const comum = { path: pdfPath, format: 'A4', printBackground: true };
if (modo === 'capa') {
  await page.pdf({ ...comum, margin: { top: '0', bottom: '0', left: '0', right: '0' } });
} else {
  await page.pdf({ ...comum, displayHeaderFooter: true,
    headerTemplate: '<span></span>', footerTemplate: rodape,
    margin: { top: '16mm', bottom: '15mm', left: '18mm', right: '18mm' } });
}
await browser.close();
"""


def partes_fonte():
    html = FONTE.read_text(encoding="utf-8")
    estilo = re.search(r"<style>.*?</style>", html, re.S).group(0)
    fontes = "\n".join(re.findall(r'<link [^>]*>', html))
    corpo = re.search(r'<div class="wrap">.*</div>', html, re.S).group(0)
    corpo = re.sub(r'<nav class="indice".*?</nav>', "", corpo, flags=re.S)
    corpo = re.sub(r"<script>.*?</script>", "", corpo, flags=re.S)
    corpo = corpo.replace(
        "Passe o cursor ou navegue pelo teclado nas barras para ver a participação no total.",
        "Participação no total: debêntures 59%, demais de renda fixa 29%, renda variável e demais 12%.",
    ).replace('<p class="leitura" id="leitura-grafico">', '<p class="nota">')
    cabecalho = re.search(r'<header class="topo">.*?</header>', html, re.S).group(0)
    return estilo, fontes, corpo, cabecalho


def html_capa(estilo, fontes, cabecalho):
    meio = """
    <div class="capa-meio"><p><b>Doze seções.</b> O que a área faz e como cobra do cliente, as
    divisões de um banco por dentro, o ciclo completo de um deal de M&amp;A e de um IPO, os métodos
    de valuation, os players globais e brasileiros, o retrato do mercado, a escada de carreira e
    as saídas, como se entra no Brasil, o lado duro do setor, um glossário de 41 termos e um
    checklist para começar.</p></div>"""
    stats = """
    <div class="rotulo">O mercado no momento desta edição</div>
    <div class="stats">
      <div class="stat"><span class="n">13,75%</span><span class="r">Selic ao ano</span></div>
      <div class="stat"><span class="n">R$ 838,8 bi</span><span class="r">Ofertas no mercado de capitais brasileiro em 2025</span></div>
      <div class="stat"><span class="n">US$ 4,5 tri</span><span class="r">M&amp;A global em 2025</span></div>
      <div class="stat"><span class="n">1</span><span class="r">IPO na B3 desde 2021</span></div>
    </div>"""
    cab = cabecalho.replace('<header class="topo">', "").replace("</header>", "")
    cab = cab.replace('<div class="eyebrow">', '<div class="eyebrow">')
    return f"""<!doctype html><html lang="pt-BR" data-theme="light"><head><meta charset="utf-8">
{fontes}{estilo}<style>{CSS_CAPA}</style></head><body><div class="capa">
<div class="capa-topo">{cab}</div>{meio}{stats}
<div class="capa-rodape"><span>Study-mkre &middot; material de estudo</span><span>{DATA}</span></div>
</div></body></html>"""


def html_corpo(estilo, fontes, corpo, sumario_html):
    return f"""<!doctype html><html lang="pt-BR" data-theme="light"><head><meta charset="utf-8">
{fontes}{estilo}<style>{CSS_IMPRESSAO}
.sumario h2{{margin-bottom:14pt}}
.toc{{margin-top:10pt}}
.toc-item{{display:flex;align-items:baseline;gap:12px;padding:8.5pt 0;border-bottom:1px solid var(--linha)}}
.toc-item:first-child{{border-top:1px solid var(--linha-forte)}}
.toc-num{{font-family:var(--mono);font-size:9pt;font-weight:600;color:var(--azul);width:22px;flex:none}}
.toc-tit{{flex:1;font-size:11pt;font-weight:600}}
.toc-sub{{display:block;font-weight:400;font-size:9.2pt;color:var(--grafite);margin-top:1px}}
.toc-pag{{font-family:var(--mono);font-size:9.5pt;font-variant-numeric:tabular-nums;color:var(--grafite)}}
</style></head><body><div class="wrap">
<section class="sumario" style="break-before:auto">
<h2><span class="num">&nbsp;</span>Sumário</h2>
<div class="toc">{sumario_html}</div>
</section>
{corpo.replace('<div class="wrap">', '').replace('</div>', '', 0)}
</body></html>"""


RESUMOS = {
    "01": "Banco comercial x banco de investimento e as três formas de ganhar dinheiro",
    "02": "IBD, mesas, research, asset e wealth, capital próprio, middle e back office",
    "03": "Quanto cada produto cobra do cliente e por que o success fee molda a cultura",
    "04": "As oito etapas de uma venda de empresa, com os documentos de cada uma",
    "05": "DCF, múltiplos, transações precedentes, LBO — e a matemática por trás",
    "06": "Bulge bracket, boutiques, os bancos brasileiros e a anatomia de um tombstone",
    "07": "Selic, mercado de capitais, M&A global e a reabertura da janela de IPOs",
    "08": "Da vaga de estágio a sócio: o que se faz, quanto se ganha, para onde se vai",
    "09": "O caminho real no Brasil, o funil do processo seletivo e o que pesa",
    "10": "Carga horária, ciclicidade e a pergunta honesta antes de escolher a área",
    "11": "41 termos que aparecem em qualquer reunião, entrevista ou notícia do setor",
    "12": "Checklist inicial e o que ler para ir mais fundo",
}


def sumario(paginas):
    linhas = []
    for num, titulo in SECOES:
        pag = paginas.get(num, "")
        linhas.append(
            f'<div class="toc-item"><span class="toc-num">{num}</span>'
            f'<span class="toc-tit">{titulo}<span class="toc-sub">{RESUMOS[num]}</span></span>'
            f'<span class="toc-pag">{pag}</span></div>'
        )
    pag_fontes = paginas.get("fontes", "")
    linhas.append(
        '<div class="toc-item"><span class="toc-num">&mdash;</span>'
        '<span class="toc-tit">Fontes e notas<span class="toc-sub">'
        "Origem de cada número citado e o alcance das faixas de remuneração</span></span>"
        f'<span class="toc-pag">{pag_fontes}</span></div>'
    )
    return "\n".join(linhas)


def render(tmp, html, nome, modo):
    caminho = tmp / f"{nome}.html"
    caminho.write_text(html, encoding="utf-8")
    pdf = tmp / f"{nome}.pdf"
    # o script de render precisa morar ao lado do node_modules que tem o playwright
    cwd = Path(os.environ.get("PLAYWRIGHT_DIR", os.getcwd()))
    js = cwd / ".render-pdf.mjs"
    js.write_text(RENDER_JS, encoding="utf-8")
    try:
        subprocess.run(
            ["node", str(js), str(caminho), str(pdf), modo],
            check=True, cwd=str(cwd),
        )
    finally:
        js.unlink(missing_ok=True)
    return pdf


def chave(texto):
    """Texto sem espaço nenhum — imune às quebras que a extração de PDF inventa."""
    return re.sub(r"\s+", "", texto)


def mapear_paginas(pdf):
    leitor = PdfReader(str(pdf))
    textos = [chave(p.extract_text() or "") for p in leitor.pages]
    paginas = {}
    inicio = 1  # a página 1 do miolo é o sumário, que repete todos os títulos
    for num, titulo in SECOES:
        alvo = chave(titulo)
        for i in range(inicio, len(textos)):
            if alvo in textos[i]:
                paginas[num] = i + 1
                inicio = i
                break
    alvo = chave("Fontes dos números citados")
    for i in range(inicio, len(textos)):
        if alvo in textos[i]:
            paginas["fontes"] = i + 1
            break
    return paginas, len(textos)


def main():
    if shutil.which("node") is None:
        sys.exit("node não encontrado — instale o Node e o pacote playwright.")
    estilo, fontes, corpo, cabecalho = partes_fonte()

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        capa_pdf = render(tmp, html_capa(estilo, fontes, cabecalho), "capa", "capa")

        # 1ª passagem: descobre em que página cai cada seção.
        primeiro = render(tmp, html_corpo(estilo, fontes, corpo, sumario({})), "corpo1", "corpo")
        paginas, total = mapear_paginas(primeiro)
        faltando = [n for n, _ in SECOES if n not in paginas]
        if faltando:
            sys.exit(f"não localizei as seções {faltando} no PDF gerado.")
        print(f"páginas do miolo: {total}; seções: {json.dumps(paginas, ensure_ascii=False)}")

        # 2ª passagem: sumário já com os números de página.
        final = render(tmp, html_corpo(estilo, fontes, corpo, sumario(paginas)), "corpo2", "corpo")
        paginas, total = mapear_paginas(final)

        escritor = PdfWriter()
        for pagina in PdfReader(str(capa_pdf)).pages:
            escritor.add_page(pagina)
        for pagina in PdfReader(str(final)).pages:
            escritor.add_page(pagina)

        escritor.add_outline_item("Capa", 0)
        escritor.add_outline_item("Sumário", 1)
        for num, titulo in SECOES:
            escritor.add_outline_item(f"{num} · {titulo}", paginas[num])
        if "fontes" in paginas:
            escritor.add_outline_item("Fontes e notas", paginas["fontes"])

        escritor.add_metadata({
            "/Title": "Mapa do Investment Banking",
            "/Subject": "Panorama da área de investment banking — mercado, deals, valuation e carreira",
            "/Creator": "Study-mkre",
        })
        with open(SAIDA, "wb") as saida:
            escritor.write(saida)

    tamanho = SAIDA.stat().st_size / 1024
    print(f"{SAIDA} · {total + 1} páginas · {tamanho:.0f} KB")


if __name__ == "__main__":
    main()
