// Gera ../formulario-fgv.pdf a partir de partes/*.html.
//
// 1. Renderiza as fórmulas LaTeX — \( ... \) inline e \[ ... \] em destaque — com KaTeX.
//    (Não usamos $ como delimitador porque o texto tem muitos "R$".)
// 2. Imprime o HTML com o Chromium do Playwright, gerando marcadores a partir dos títulos.
// 3. Lê nos marcadores a página de cada tópico, preenche o sumário e imprime de novo.
//
// Uso: npm install && npm run build   (requer Python 3 com pypdf, para marcadores.py)
// Variáveis opcionais: CHROMIUM_PATH (executável do Chromium), SRC e OUT.

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import katex from 'katex';
import { chromium } from 'playwright-core';

const dir = path.dirname(fileURLToPath(import.meta.url));
// O fonte fica dividido em partes/*.html (início, Matemática, Física, Química, fim),
// concatenadas em ordem alfabética. SRC permite usar um único arquivo.
const partsDir = path.join(dir, 'partes');
const readSource = () =>
  process.env.SRC
    ? fs.readFileSync(path.resolve(dir, process.env.SRC), 'utf8')
    : fs.readdirSync(partsDir).filter((f) => f.endsWith('.html')).sort()
        .map((f) => fs.readFileSync(path.join(partsDir, f), 'utf8')).join('\n');
const outPath = path.resolve(dir, process.env.OUT ?? '../formulario-fgv.pdf');
const buildDir = path.join(dir, '.build');
fs.mkdirSync(buildDir, { recursive: true });

const macros = {
  '\\sen': '\\operatorname{sen}',
  '\\tg': '\\operatorname{tg}',
};

function renderMath(html) {
  const render = (tex, displayMode) =>
    katex.renderToString(tex.trim(), { displayMode, throwOnError: true, macros, strict: 'ignore' });
  return html
    .replace(/\\\[([\s\S]+?)\\\]/g, (_, tex) => render(tex, true))
    .replace(/\\\(([\s\S]+?)\\\)/g, (_, tex) => render(tex, false));
}

// Cada tópico tem <div class="topic-head" data-toc="m01"> ... <h1|h2>Título</h1|h2>,
// e o sumário tem <td class="pg" data-pg="m01"> para receber a página.
function topics(html) {
  const re = /data-toc="([a-z]+\d*)">\s*<span class="tnum">[^<]+<\/span>[\s\S]*?<h[12][^>]*>([\s\S]*?)<\/h[12]>/g;
  return [...html.matchAll(re)].map(([, id, h]) => {
    const title = h.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
    // A palavra mais longa do título confirma, no texto extraído, em que página ele caiu
    // (o pdftotext às vezes quebra e reordena as linhas de um título).
    const probe = title.split(/[^\p{L}]+/u).reduce((a, w) => (w.length > a.length ? w : a), '');
    return { id, title, probe };
  });
}

function withPages(html, pages) {
  return html.replace(/<td class="pg" data-pg="([a-z]+\d*)">[^<]*<\/td>/g, (m, id) => {
    if (!(id in pages)) throw new Error(`Página não encontrada para ${id}`);
    return `<td class="pg" data-pg="${id}">${pages[id]}</td>`;
  });
}

const marcadores = (acao, pdf) =>
  execFileSync('python3', [path.join(dir, 'marcadores.py'), acao, pdf], { encoding: 'utf8' });

// Comparação sem acentos nem espaços: a fonte dos títulos às vezes sai do pdftotext com o
// acento como caractere separado (ex.: "A´nalise").
const simplify = (t) =>
  t.normalize('NFD').replace(/[\p{M}\u00B4\u0060\u02C6\u02DC\u00A8\s]/gu, '').toLowerCase();

function pageTexts(pdf) {
  const text = execFileSync('pdftotext', ['-enc', 'UTF-8', pdf, '-'], { encoding: 'utf8' });
  return text.split('\f').map(simplify);
}

// Os títulos dos tópicos aparecem nos marcadores na ordem do documento, depois do sumário.
// Quando um bloco é empurrado para a página seguinte, o Chromium às vezes aponta o marcador
// para a página anterior; por isso confirmamos no texto da página e, se preciso, usamos a seguinte.
function locate(pdf, list) {
  const outline = JSON.parse(marcadores('ler', pdf));
  const texts = pageTexts(pdf);
  const pages = {};
  let i = 0;
  for (const { id, title, probe } of list) {
    while (i < outline.length && outline[i][0] !== title) i++;
    if (i === outline.length) throw new Error(`Título não encontrado nos marcadores: ${title}`);
    const p = outline[i][1];
    const found = [p, p + 1].find((n) => texts[n - 1]?.includes(simplify(probe)));
    if (!found) throw new Error(`Título não encontrado no texto das páginas ${p}–${p + 1}: ${title}`);
    pages[id] = found;
  }
  return pages;
}

const chromiumPath =
  process.env.CHROMIUM_PATH ??
  ['/opt/pw-browsers/chromium-1194/chrome-linux/chrome'].find((p) => fs.existsSync(p));

const browser = await chromium.launch(chromiumPath ? { executablePath: chromiumPath } : {});

async function print(html, pdfPath) {
  const htmlPath = path.join(buildDir, 'formulario.render.html');
  fs.writeFileSync(htmlPath, html);
  const page = await browser.newPage();
  await page.goto('file://' + htmlPath, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: pdfPath,
    preferCSSPageSize: true,
    printBackground: true,
    outline: true,
    tagged: true,
  });
  await page.close();
}

// Fontes e KaTeX vêm de node_modules; o HTML final fica em .build/, então ajustamos os caminhos.
let source = readSource().replaceAll('href="node_modules/', 'href="../node_modules/');
source = renderMath(source);
const list = topics(source);

// Passada 1: descobrir as páginas.
const draft = path.join(buildDir, 'rascunho.pdf');
await print(source, draft);
const pages = locate(draft, list);

// Passada 2: PDF final, com o sumário preenchido.
await print(withPages(source, pages), outPath);
await browser.close();

// Conferência: preencher o sumário não pode ter mudado a paginação.
const check = locate(outPath, list);
const wrong = list.filter(({ id }) => check[id] !== pages[id]);
if (wrong.length) {
  console.error('Sumário divergente para:', wrong.map((t) => t.id));
  process.exit(1);
}
marcadores('corrigir', outPath);
console.log(`OK: ${outPath} (${list.length} tópicos)`);
console.log(list.map(({ id }) => `${id}:${pages[id]}`).join(' '));
