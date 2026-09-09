// Monta o trabalho completo em um único documento, conforme a ABNT NBR 14724:
// capa, folha de rosto, sumário, e — para cada ano — a folha de abertura
// seguida de todas as folhas da prova do ENEM daquele ano, mais as referências.
//
// Formatação: A4, Arial 12, margens 3/3/2/2 cm, entrelinhas 1,5, paginação
// contada a partir da folha de rosto e impressa a partir da 1ª folha textual.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, PageBreak, AlignmentType,
  BorderStyle, Tab, TabStopType, LeaderType, Header, PageNumber,
  convertMillimetersToTwip,
} = require("docx");

const FONT = "Arial";
const CORPO = 24;        // 12 pt
const MENOR = 20;        // 10 pt (paginação)
const LINHA_1_5 = 360;
const LINHA_SIMPLES = 240;

const DISCIPLINA = "Matemática";
const PROFESSOR = "Prof. Gabriel Garcia";
const CIDADE = "[CIDADE]";
const ANO_TRABALHO = "2026";
const TITULO = "PROVAS DO ENEM DE 2021 A 2025";
const SUBTITULO = "análise das questões de Matemática e suas Tecnologias";

// As folhas das provas são extraídas dos PDFs originais com:
//   pdftoppm -jpeg -jpegopt quality=78 -r 120 <prova>.pdf paginas/<ano>
const PASTA_PAGINAS = path.join(__dirname, "..", "paginas");

// A4 = 11906 dxa de largura; margens: esquerda 30 mm, direita 20 mm
const LARGURA_TEXTO = 11906 - convertMillimetersToTwip(30) - convertMillimetersToTwip(20);

// imagem das folhas da prova: 16 cm de largura (a área útil do texto)
const IMG_LARGURA_PX = Math.round((160 / 25.4) * 96);

const AUTORES = [
  "Laura Oliveira",
  "Lucas Argolo",
  "Lucas Suikuni",
  "Luiz Lopes",
  "Pedro Mendietta",
];

const ANOS = [
  { n: 1, ano: "2021", integrante: "Lucas Suikuni" },
  { n: 2, ano: "2022", integrante: "Luiz Lopes" },
  { n: 3, ano: "2023", integrante: "Pedro Mendietta" },
  { n: 4, ano: "2024", integrante: "Lucas Argolo" },
  { n: 5, ano: "2025", integrante: "Laura Oliveira" },
];

// ---------- folhas de cada prova (imagens já extraídas dos PDFs) ----------
const folhasDaProva = (ano) =>
  fs
    .readdirSync(PASTA_PAGINAS)
    .filter((f) => f.startsWith(`${ano}-`) && f.endsWith(".jpg"))
    .sort()
    .map((f) => path.join(PASTA_PAGINAS, f));

ANOS.forEach((a) => {
  a.folhas = folhasDaProva(a.ano);
});

// ---------- paginação ABNT: folha de rosto = 1, sumário = 2, texto a partir de 3 ----------
let folhaAtual = 3;
ANOS.forEach((a) => {
  a.pagina = folhaAtual;                 // folha de abertura do ano
  folhaAtual += 1 + a.folhas.length;     // abertura + folhas da prova
});
const PAGINA_REFERENCIAS = folhaAtual;

// ---------- helpers ----------
const par = (texto, opcoes = {}) => {
  const {
    size = CORPO, bold = false, italico = false, caps = false,
    alinhamento = AlignmentType.CENTER, linha = LINHA_1_5,
    antes = 0, depois = 0,
  } = opcoes;
  return new Paragraph({
    alignment: alinhamento,
    spacing: { before: antes, after: depois, line: linha },
    children: [new TextRun({ text: texto, font: FONT, size, bold, italics: italico, allCaps: caps })],
  });
};

const vazio = (depois = 0) => par("", { depois });

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

// lê largura/altura direto do cabeçalho SOF do JPEG
function dimensoesJpeg(buf) {
  let i = 2;
  while (i < buf.length) {
    if (buf[i] !== 0xff) { i++; continue; }
    const marcador = buf[i + 1];
    if (marcador >= 0xc0 && marcador <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(marcador)) {
      return { altura: buf.readUInt16BE(i + 5), largura: buf.readUInt16BE(i + 7) };
    }
    i += 2 + buf.readUInt16BE(i + 2);
  }
  throw new Error("não foi possível ler as dimensões do JPEG");
}

// uma folha da prova: quebra de página + imagem ocupando a área útil
const folhaDeProva = (arquivo) => {
  const dados = fs.readFileSync(arquivo);
  const { largura, altura } = dimensoesJpeg(dados);
  const alturaPx = Math.round((IMG_LARGURA_PX * altura) / largura);
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    // sem w:line: a altura da linha acompanha a imagem (com espaçamento fixo
    // o LibreOffice recorta a figura numa faixa fina)
    spacing: { before: 0, after: 0 },
    children: [
      new PageBreak(),
      new ImageRun({
        type: "jpg",
        data: dados,
        transformation: { width: IMG_LARGURA_PX, height: alturaPx },
      }),
    ],
  });
};

// ---------- CAPA ----------
const capa = secao([
  ...AUTORES.map((a) => par(a, { depois: 60 })),
  par(TITULO, { bold: true, antes: 2600, depois: 120 }),
  par(SUBTITULO, { depois: 2600 }),
  vazio(4400),
  par(CIDADE, { depois: 60 }),
  par(ANO_TRABALHO),
]);

// ---------- FOLHA DE ROSTO (folha 1) ----------
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

// ---------- SUMÁRIO (folha 2) ----------
const sumario = secao([
  par("SUMÁRIO", { bold: true, depois: 720 }),
  ...ANOS.map(({ n, ano, integrante, pagina }) =>
    linhaSumario(String(n), `ENEM ${ano} — ${integrante}`, pagina)
  ),
  linhaSumario("", "REFERÊNCIAS", PAGINA_REFERENCIAS),
]);

// ---------- SEÇÃO DE CADA ANO: abertura + folhas da prova ----------
const secaoDoAno = ({ n, ano, integrante, folhas }) =>
  secao(
    [
      par(`${n} ENEM ${ano}`, {
        alinhamento: AlignmentType.LEFT,
        bold: true,
        caps: true,
        depois: 4200,
      }),
      par(ano, { bold: true, size: 96 }),
      regua(),
      par("Matemática e suas Tecnologias", { depois: 0 }),
      par(`2º dia | Caderno 7 — Azul | Questões 136 a 180 | ${folhas.length} folhas`, { depois: 720 }),
      par(`Responsável: ${integrante}`, { bold: true }),
      ...folhas.map(folhaDeProva),
    ],
    { numerada: true }
  );

// ---------- REFERÊNCIAS ----------
const referencia = (ano) =>
  new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { line: LINHA_SIMPLES, after: 240 },
    children: [
      new TextRun({
        text: "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA. ",
        font: FONT, size: CORPO,
      }),
      new TextRun({
        text: `Exame Nacional do Ensino Médio ${ano}`,
        font: FONT, size: CORPO, bold: true,
      }),
      new TextRun({
        text: `: 2º dia, caderno 7, azul: matemática e suas tecnologias. Brasília, DF: Inep, ${ano}.`,
        font: FONT, size: CORPO,
      }),
    ],
  });

const referencias = secao(
  [par("REFERÊNCIAS", { bold: true, depois: 720 }), ...ANOS.map(({ ano }) => referencia(ano))],
  { numerada: true }
);

// ---------- MONTAGEM ----------
const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: CORPO } } } },
  sections: [capa, folhaDeRosto, sumario, ...ANOS.map(secaoDoAno), referencias],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("Trabalho_ENEM_2021-2025.docx", buf);
  const total = 3 + ANOS.reduce((s, a) => s + 1 + a.folhas.length, 0) + 1;
  console.log(
    `ok — ${total} folhas | ` +
      ANOS.map((a) => `${a.ano}: abertura na folha ${a.pagina} (+${a.folhas.length})`).join(" | ") +
      ` | referências na folha ${PAGINA_REFERENCIAS}`
  );
});
