# Study-mkre

Material de preparação para os vestibulares do Mackenzie e da FGV (curso de Administração), a partir da análise de provas anteriores.

## Análise de conteúdo

`analise/mapa-mackenzie.html` — análise comparativa das duas últimas provas, com os
conteúdos mais cobrados em Matemática, Português e Geografia, ordenados por prioridade.
Publicado também como página: https://claude.ai/code/artifact/18c16328-493f-4a92-b5c8-d71f0e6dc63c

### Provas analisadas

| Prova | Data | Questões |
|---|---|---|
| Processo Seletivo Mackenzie — 1º semestre 2026, Grupo 1 | 26/11/2025 | 60 + redação |
| Vestibular Higienópolis — 2º semestre 2025, Prova B | 11/06/2025 | 60 + redação |

O texto extraído de cada prova está em `analise/prova-2026-texto.txt` e
`analise/prova-2025-2-texto.txt`, para consulta e para futuras comparações quando
novas provas forem incluídas.

### Principais achados

- **A estrutura é fixa nas duas provas**: Português Q1–Q10, Inglês Q11–Q15,
  Física Q16–Q22, Química Q23–Q29, Matemática Q30–Q39, Biologia Q40–Q46,
  História Q47–Q53, Geografia Q54–Q60.
- **Matemática**: geometria (plana, analítica, espacial e trigonometria) responde por
  cerca de metade do bloco. Oito dos dez temas se repetiram nas duas provas.
- **Português**: divisão interna fixa — seis questões de interpretação de texto e
  quatro de literatura. Modernismo é o assunto literário mais cobrado.
- **Geografia**: cartografia e geopolítica atual concentram mais da metade do bloco.

## Guia FGV Administração

`fgv/guia-fgv-administracao.pdf` — PDF de 56 páginas para a prova de **Administração** da FGV,
focado em **Geografia, Atualidades e História**, com os temas **em ordem de importância**:
12 de Geografia e Atualidades, 9 de História e, no fim, 18 de Matemática. Cada tema traz uma
explicação do que é e cartões com os conceitos, datas e termos que a prova cobra. Os
exercícios são **65 questões reais da FGV** (33 de Humanas e 32 de Matemática), com gabarito
oficial e resolução comentada que aponta as pegadinhas das alternativas erradas.

- **Como o ranking foi feito**: classificamos por tema principal as 105 questões objetivas de
  Ciências Humanas de 7 provas de Administração (Vestibular Unificado 2026.1 e 2024, Vestibular
  FGV 2026.2 e FGV‑SP 2024.2, 2023.2, 2023 e 2022): 58 de Geografia e Atualidades e 47 de
  História. O ranking de Matemática usa as 165 questões objetivas de 9 provas (2020 a 2026).
- **Mais cobrados em Geografia e Atualidades**: geopolítica e conflitos atuais, economia
  brasileira e mundial e meio ambiente (9 questões cada, presentes nas 7 provas), seguidos de
  globalização e cidades globais (6) e agronegócio (5).
- **Mais cobrados em História**: século XX (guerras, fascismos e Guerra Fria, 9), Brasil
  Império (7), sociedade, cultura e direitos (7), Idade Moderna (6) e Brasil colonial (6).
- **Consulta rápida**: linhas do tempo do Brasil e do mundo, pares de conceitos que a FGV troca
  nas alternativas, economia em uma linha e tabelas de Matemática.
- **Questões**: transcritas das provas e conferidas palavra por palavra; os gabaritos são os
  oficiais. Provas e gabaritos consultados no arquivo de resoluções comentadas do Curso Objetivo.
  Física e Química, da versão anterior, foram retiradas porque não caem na prova de Administração.

## Guia Mackenzie Administração

`mackenzie/guia-mackenzie-administracao.pdf` — PDF de 39 páginas com **Geografia e História**
para o vestibular do Mackenzie, com os temas **em ordem de importância**: 11 de Geografia e 12
de História. Cada tema traz uma explicação do que é e cartões com os conceitos, datas e termos
que a prova cobra. Os exercícios são **36 questões reais do Mackenzie** (17 de Geografia e 19 de
História), com gabarito oficial e resolução comentada que aponta as pegadinhas.

- **Como o ranking foi feito**: classificamos por tema principal as 140 questões objetivas de
  História (Q47–Q53) e Geografia (Q54–Q60) de 10 provas: 1º semestre de 2023, 2024, 2025 e 2026
  (dois dias de prova em cada) e 2º semestre de 2023 e 2024. Empates são desfeitos pelo número de
  provas em que o tema apareceu e, depois, pelas questões de 2025 e 2026.
- **Mais cobrados em Geografia**: geopolítica e atualidades (14 questões, em 8 provas),
  cartografia com contas de escala e fuso (12, em 8 provas), população (9) e biomas (8).
- **Mais cobrados em História**: Idade Média (8, em 7 provas), América e Brasil coloniais (8),
  Brasil de 1945 a 1985 (7), guerras mundiais e fascismos (7), revoluções e ideologias (7) e
  Era Vargas (6, em 6 provas).
- **Consulta rápida**: tabelas de escala e de fusos, massas de ar, linhas do tempo do Brasil e
  do mundo e pares de conceitos que o Mackenzie troca nas alternativas.
- **Questões**: transcritas das provas e conferidas palavra por palavra; as imagens viraram uma
  descrição entre colchetes. Os gabaritos são os oficiais do Mackenzie. Provas e gabaritos
  consultados no arquivo de resoluções comentadas do Curso Objetivo.

## Como gerar os PDFs

Os dois guias são montados por `gerador-pdf/` a partir das partes HTML de cada um
(`fgv/partes/*.html` e `mackenzie/partes/*.html`, concatenadas em ordem alfabética), com o estilo
comum de `gerador-pdf/estilo.css`. As fórmulas em LaTeX são renderizadas com KaTeX, o Chromium
imprime o PDF e o sumário é paginado automaticamente:

```sh
cd gerador-pdf
npm install
npm run fgv         # gera fgv/guia-fgv-administracao.pdf
npm run mackenzie   # gera mackenzie/guia-mackenzie-administracao.pdf
# requer Python 3 com pypdf
```
