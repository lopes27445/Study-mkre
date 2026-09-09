const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, BorderStyle, Tab,
  TabStopType, LeaderType, Header, PageNumber, VerticalAlign,
  convertMillimetersToTwip,
} = require("docx");

const FONT = "Arial";

// A4 = 11906 dxa de largura; margens ABNT: esq. 30 mm, dir. 20 mm
const LARGURA_TEXTO = 11906 - convertMillimetersToTwip(30) - convertMillimetersToTwip(20);

const ANOS = [
  { ano: "2021", integrante: "Lucas Suikuni", pagina: 3 },
  { ano: "2022", integrante: "Luiz Lopes", pagina: 4 },
  { ano: "2023", integrante: "Pedro Mendietta", pagina: 5 },
  { ano: "2024", integrante: "Lucas Argolo", pagina: 6 },
  { ano: "2025", integrante: "Laura Oliveira", pagina: 7 },
];

// ---------- helpers ----------
const centro = (texto, { size = 24, bold = false, italico = false, depois = 0, antes = 0 } = {}) =>
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: antes, after: depois },
    children: [new TextRun({ text: texto, font: FONT, size, bold, italics: italico })],
  });

// linha do sumário: texto ....................... nº da página
const linhaSumario = (texto, pagina) =>
  new Paragraph({
    spacing: { after: 300 },
    tabStops: [{ type: TabStopType.RIGHT, position: LARGURA_TEXTO, leader: LeaderType.DOT }],
    children: [
      new TextRun({ text: texto, font: FONT, size: 24, bold: true }),
      new TextRun({ children: [new Tab()], font: FONT, size: 24, bold: true }),
      new TextRun({ text: String(pagina), font: FONT, size: 24, bold: true }),
    ],
  });

// espaço no topo da página: "space before" é ignorado no 1º parágrafo da página,
// então usamos um parágrafo vazio com espaçamento depois
const espacoTopo = (dxa) =>
  new Paragraph({
    spacing: { after: dxa },
    children: [new TextRun({ text: "", font: FONT, size: 24 })],
  });

const regua = () =>
  new Paragraph({
    spacing: { before: 200, after: 320 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "000000", space: 1 } },
    children: [new TextRun({ text: "", font: FONT, size: 24 })],
  });

const cabecalho = () =>
  new Header({
    children: [
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 20 })],
      }),
    ],
  });

const propriedadesPagina = () => ({
  page: {
    margin: {
      top: convertMillimetersToTwip(30),
      left: convertMillimetersToTwip(30),
      bottom: convertMillimetersToTwip(20),
      right: convertMillimetersToTwip(20),
    },
  },
});

const secao = (children) => ({
  properties: propriedadesPagina(),
  headers: { default: cabecalho() },
  children,
});

// ---------- FOLHA 1 — INTEGRANTES ----------
const folhaIntegrantes = secao(
  [
    centro("TRABALHO DE MATEMÁTICA", { size: 34, bold: true, depois: 100 }),
    centro("Provas do ENEM — 2021 a 2025", { size: 26, depois: 140 }),
    centro("Matemática e suas Tecnologias — 2º dia | Caderno 7 — Azul", { size: 22, italico: true }),
    centro("INTEGRANTES", { size: 28, bold: true, antes: 2600, depois: 560 }),
    ...ANOS.flatMap(({ ano, integrante }) => [
      centro(integrante, { size: 26, depois: 60 }),
      centro(`ENEM ${ano}`, { size: 22, italico: true, depois: 460 }),
    ]),
  ],
);

// ---------- FOLHA 2 — SUMÁRIO ----------
const folhaSumario = secao([
  centro("SUMÁRIO", { size: 28, bold: true, antes: 400, depois: 800 }),
  ...ANOS.map(({ ano, integrante, pagina }) => linhaSumario(`ENEM ${ano} — ${integrante}`, pagina)),
]);

// ---------- FOLHAS DIVISÓRIAS — UMA POR ANO ----------
const folhaAno = ({ ano, integrante }) =>
  secao(
    [
      espacoTopo(4000),
      centro("ENEM", { size: 48, bold: true, depois: 120 }),
      centro(ano, { size: 160, bold: true }),
      regua(),
      centro("Matemática e suas Tecnologias", { size: 26, depois: 60 }),
      centro("2º dia | Caderno 7 — Azul | Questões 136 a 180", { size: 24, depois: 800 }),
      centro(integrante, { size: 28, bold: true }),
    ],
  );

// ---------- MONTAGEM ----------
const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 24 } } } },
  sections: [folhaIntegrantes, folhaSumario, ...ANOS.map(folhaAno)],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("Trabalho_ENEM_2021-2025.docx", buf);
  console.log("ok");
});
