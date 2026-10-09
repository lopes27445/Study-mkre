# Study-mkre

Material de preparação para os vestibulares do Mackenzie e da FGV, a partir da análise de provas anteriores.

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

## Formulário FGV

`fgv/formulario-fgv.pdf` — PDF de 34 páginas com as fórmulas que mais caem no vestibular da
FGV, organizadas em 35 temas (20 de Matemática, 8 de Física e 7 de Química), cada um com
exercícios de cinco alternativas e resolução comentada (52 no total). Os exercícios são
inéditos, no estilo da banca, e todas as respostas foram conferidas numericamente.

- **Prioridade dos temas de Matemática**: definida pela classificação das 15 questões de
  Matemática da prova objetiva do Vestibular Unificado FGV 2026.1 (turno 2) e das 15 da
  prova da FGV-SP 2019. Alta = 2 ou mais questões; média = 1; complementar = não caiu.
- **Física e Química**: para Ciências Econômicas na FGV-SP, cuja prova objetiva inclui
  essas matérias. São temas clássicos de vestibular, sem análise de provas.
- **Mais cobrados**: probabilidade, estatística, geometria analítica e geometria espacial
  (3 questões cada nas duas provas), seguidos de porcentagem, juros, PA/PG, função
  quadrática, trigonometria e problemas de razão e proporção.

O PDF é gerado a partir de `fgv/fonte/formulario.html` (fórmulas em LaTeX, renderizadas com
KaTeX e impressas pelo Chromium):

```sh
cd fgv/fonte
npm install
npm run build   # requer Python 3 com pypdf
```
