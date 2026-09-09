// Gera o documento do trabalho em conformidade com a ABNT NBR 14724
// (fonte Arial 12, margens 3/3/2/2 cm, entrelinhas 1,5, paginação a partir
// da folha de rosto com o número impresso a partir da 1ª folha textual).
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, BorderStyle, Tab,
  TabStopType, LeaderType, Header, PageNumber, convertMillimetersToTwip,
} = require("docx");

const FONT = "Arial";
const CORPO = 24;        // 12 pt (ABNT: texto em 12)
const MENOR = 20;        // 10 pt (ABNT: paginação e citações longas)
const LINHA_1_5 = 360;   // entrelinhas 1,5
const LINHA_SIMPLES = 240;

const DISCIPLINA = "Matemática";
const PROFESSOR = "Prof. Gabriel Garcia";
const CIDADE = "[CIDADE]";
const ANO_TRABALHO = "2026";
const TITULO = "PROVAS DO ENEM DE 2021 A 2025";
const SUBTITULO = "análise das questões de Matemática e suas Tecnologias";

// A4 = 11906 dxa de largura; margens ABNT: esquerda 30 mm, direita 20 mm
const LARGURA_TEXTO = 11906 - convertMillimetersToTwip(30) - convertMillimetersToTwip(20);

// Autores em ordem alfabética (ABNT), com o ano sob responsabilidade de cada um
const AUTORES = [
  "Laura Oliveira",
  "Lucas Argolo",
  "Lucas Suikuni",
  "Luiz Lopes",
  "Pedro Mendietta",
];

const ANOS = [
  { n: 1, ano: "2021", integrante: "Lucas Suikuni", pagina: 3 },
  { n: 2, ano: "2022", integrante: "Luiz Lopes", pagina: 4 },
  { n: 3, ano: "2023", integrante: "Pedro Mendietta", pagina: 5 },
  { n: 4, ano: "2024", integrante: "Lucas Argolo", pagina: 6 },
  { n: 5, ano: "2025", integrante: "Laura Oliveira", pagina: 7 },
];
const PAGINA_REFERENCIAS = 8;

// ---------- helpers ----------
const par = (texto, opcoes = {}) => {
  const {
    size = CORPO, bold = false, italico = false, caps = false,
    alinhamento = AlignmentType.CENTER, linha = LINHA_1_5,
    antes = 0, depois = 0, recuoEsq = 0,
  } = opcoes;
  return new Paragraph({
    alignment: alinhamento,
    spacing: { before: antes, after: depois, line: linha },
    indent: recuoEsq ? { left: recuoEsq } : undefined,
    children: [new TextRun({ text: texto, font: FONT, size, bold, italics: italico, allCaps: caps })],
  });
};

const vazio = (depois = 0) => par("", { depois });

// espaço no topo: "space before" é ignorado no 1º parágrafo da página
const espacoTopo = (dxa) => par("", { depois: dxa, linha: LINHA_SIMPLES });

// entrada de sumário: título ......................... nº da folha
const linhaSumario = (indicativo, titulo, pagina) =>
  new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { after: 0, line: LINHA_1_5 },
    tabStops: [{ type: TabStopType.RIGHT, position: LARGURA_TEXTO, leader: LeaderType.DOT }],
    children: [
      new TextRun({ text: indicativo ? `${indicativo} ` : "", font: FONT, size: CORPO, bold: true }),
      new TextRun({ text: titulo, font: FONT, size: CORPO, bold: true }),
      new TextRun({ children: [new Tab()], font: FONT, size: CORPO }),
      new TextRun({ text: String(pagina), font: FONT, size: CORPO }),
    ],
  });

const regua = () =>
  new Paragraph({
    spacing: { before: 200, after: 320, line: LINHA_SIMPLES },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "000000", space: 1 } },
    children: [new TextRun({ text: "", font: FONT, size: CORPO })],
  });

// paginação ABNT: canto superior direito, a 2 cm da borda, fonte menor
const cabecalho = () =>
  new Header({
    children: [
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        spacing: { line: LINHA_SIMPLES },
        children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: MENOR })],
      }),
    ],
  });

const propriedadesPagina = (extra = {}) => ({
  page: {
    margin: {
      top: convertMillimetersToTwip(30),
      left: convertMillimetersToTwip(30),
      bottom: convertMillimetersToTwip(20),
      right: convertMillimetersToTwip(20),
      header: convertMillimetersToTwip(20),
      footer: convertMillimetersToTwip(20),
    },
    ...extra,
  },
});

const secao = (children, { numerada = false, iniciaPaginacao = false } = {}) => ({
  properties: propriedadesPagina(iniciaPaginacao ? { pageNumbers: { start: 1 } } : {}),
  ...(numerada ? { headers: { default: cabecalho() } } : {}),
  children,
});

// ---------- CAPA (não recebe número; não é contada) ----------
const capa = secao([
  ...AUTORES.map((a) => par(a, { depois: 60 })),
  espacoTopo(0),
  par(TITULO, { bold: true, antes: 2600, depois: 120 }),
  par(SUBTITULO, { depois: 2600 }),
  vazio(4400),
  par(CIDADE, { depois: 60 }),
  par(ANO_TRABALHO),
]);

// ---------- FOLHA DE ROSTO (folha 1, sem número impresso) ----------
const folhaDeRosto = secao(
  [
    ...AUTORES.map((a) => par(a, { depois: 60 })),
    par(TITULO, { bold: true, antes: 2600, depois: 120 }),
    par(SUBTITULO, { depois: 1400 }),
    new Paragraph({
      alignment: AlignmentType.JUSTIFIED,
      spacing: { line: LINHA_SIMPLES, after: 4200 },
      indent: { left: convertMillimetersToTwip(80) },
      children: [
        new TextRun({
          text:
            `Trabalho apresentado à disciplina de ${DISCIPLINA} como requisito ` +
            `parcial para avaliação, sob orientação do ${PROFESSOR}.`,
          font: FONT,
          size: CORPO,
        }),
      ],
    }),
    par(CIDADE, { depois: 60 }),
    par(ANO_TRABALHO),
  ],
  { iniciaPaginacao: true }
);

// ---------- SUMÁRIO (folha 2, sem número impresso) ----------
const sumario = secao([
  par("SUMÁRIO", { bold: true, depois: 720 }),
  ...ANOS.map(({ n, ano, integrante, pagina }) =>
    linhaSumario(String(n), `ENEM ${ano} — ${integrante}`, pagina)
  ),
  linhaSumario("", "REFERÊNCIAS", PAGINA_REFERENCIAS),
]);

// ---------- FOLHAS DE ABERTURA DE CADA ANO (seções primárias) ----------
const folhaAno = ({ n, ano, integrante }) =>
  secao(
    [
      // título de seção primária: alinhado à esquerda, caixa alta, negrito
      par(`${n} ENEM ${ano}`, {
        alinhamento: AlignmentType.LEFT,
        bold: true,
        caps: true,
        depois: 4200,
      }),
      par(ano, { bold: true, size: 96 }),
      regua(),
      par("Matemática e suas Tecnologias", { depois: 0 }),
      par("2º dia | Caderno 7 — Azul | Questões 136 a 180", { depois: 720 }),
      par(`Responsável: ${integrante}`, { bold: true }),
    ],
    { numerada: true }
  );

// ---------- REFERÊNCIAS (elemento pós-textual, sem indicativo numérico) ----------
const referencia = (ano) =>
  new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { line: LINHA_SIMPLES, after: 240 },
    children: [
      new TextRun({
        text:
          "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA. ",
        font: FONT,
        size: CORPO,
      }),
      new TextRun({
        text: `Exame Nacional do Ensino Médio ${ano}`,
        font: FONT,
        size: CORPO,
        bold: true,
      }),
      new TextRun({
        text: `: 2º dia, caderno 7, azul: matemática e suas tecnologias. Brasília, DF: Inep, ${ano}.`,
        font: FONT,
        size: CORPO,
      }),
    ],
  });

const referencias = secao(
  [
    par("REFERÊNCIAS", { bold: true, depois: 720 }),
    ...ANOS.map(({ ano }) => referencia(ano)),
  ],
  { numerada: true }
);

// ---------- MONTAGEM ----------
const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: CORPO } } } },
  sections: [capa, folhaDeRosto, sumario, ...ANOS.map(folhaAno), referencias],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("Trabalho_ENEM_2021-2025.docx", buf);
  console.log("ok");
});
