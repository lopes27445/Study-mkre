// Gera ../claude-vs-claude-code.pdf a partir de documento.html usando o Chromium do Playwright.
// Uso (com o Playwright instalado globalmente):
//   NODE_PATH="$(npm root -g)" node gerar-pdf.cjs
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const html = path.join(__dirname, 'documento.html');
  const pdf = path.join(__dirname, '..', 'claude-vs-claude-code.pdf');

  // Sem hinting, o Chromium não arredonda a largura dos caracteres para pixels inteiros:
  // o espaçamento do texto no PDF fica fiel às métricas das fontes.
  const browser = await chromium.launch({ args: ['--font-render-hinting=none'] });
  const page = await browser.newPage();
  await page.goto('file://' + html, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);

  await page.pdf({
    path: pdf,
    preferCSSPageSize: true, // tamanho A4 e margens vêm do @page do HTML
    printBackground: true,
    tagged: true,
    outline: true, // marcadores de navegação a partir dos títulos
  });

  await browser.close();
  console.log('PDF gerado em', pdf);
})();
