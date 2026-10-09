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

`fgv/formulario-fgv.pdf` — PDF de 53 páginas com as fórmulas que mais caem no vestibular da
FGV, **em ordem de importância**: 18 temas de Matemática, 13 de Física e 11 de Química. Cada
tema traz uma explicação do que é, cada fórmula vem com o significado de cada letra e de quando
usar, e os exercícios são **68 questões reais da FGV**, com gabarito oficial e resolução comentada.

- **Como o ranking foi feito**: classificamos por tema as 165 questões objetivas de Matemática
  de 9 provas (Vestibular Unificado 2026.1 e 2024, FGV 2026.2 e FGV‑SP de 2020 a 2024.2) e as
  75 de Física e 75 de Química das 5 provas de Economia (FGV‑SP 2020, 2022, 2023, 2024 e
  Unificado 2026.1). Questões que misturam dois temas contam para os dois.
- **Mais cobrados em Matemática**: problemas aritméticos (razão, proporção, regra de três, MMC)
  com 27 questões, geometria plana (19), probabilidade (17), geometria analítica (14) e
  geometria espacial (13).
- **Mais cobrados em Física**: óptica e termologia (9 cada), ondas (8). **Em Química**:
  orgânica (15), estequiometria (10), oxirredução e eletroquímica (9).
- **Questões**: transcritas das provas; os gabaritos foram conferidos com os oficiais. Provas e
  gabaritos consultados no arquivo de resoluções comentadas do Curso Objetivo.

O PDF é gerado a partir de `fgv/fonte/partes/*.html` (fórmulas em LaTeX, renderizadas com
KaTeX e impressas pelo Chromium). O sumário é paginado automaticamente:

```sh
cd fgv/fonte
npm install
npm run build   # requer Python 3 com pypdf
```
