# Study-mkre — Preparação Mackenzie

Repositório de estudos para o Processo Seletivo da Universidade Presbiteriana Mackenzie.

## 👉 Comece por aqui

**[`cronograma-diario.pdf`](cronograma-diario.pdf)** — o que estudar em **cada dia** das 4 semanas,
em 5 páginas para imprimir ou levar no celular.

**[`acompanhamento.md`](acompanhamento.md)** — o painel. É o **único arquivo que você edita**:
diagnóstico, progresso das 4 semanas, caderno de erros e simulados.

## Material de referência (não muda)

| Arquivo | O que é |
|---|---|
| [`analise-provas-mackenzie-2025-2026.md`](analise-provas-mackenzie-2025-2026.md) | Análise comparativa das 4 provas mais recentes (240 questões + 4 redações): o que cai, com que frequência e quais as prioridades por matéria |
| [`plano-4-semanas-portugues-matematica.md`](plano-4-semanas-portugues-matematica.md) | Plano de 4 semanas para Português e Matemática, em duas faixas de carga (10h ou 15h/semana), com as questões reais da banca indicadas por tópico |
| [`scripts/gerar_cronograma_pdf.py`](scripts/gerar_cronograma_pdf.py) | Gera o `cronograma-diario.pdf`. Para mudar o cronograma, edite a lista `SEMANAS` no topo do script e rode `python3 scripts/gerar_cronograma_pdf.py` |

### Provas analisadas

| Prova | Aplicação |
|---|---|
| 2026/1 — Higienópolis, Grupo 1 | 26/11/2025 |
| 2026/1 — Higienópolis, Grupo 2 | 27/11/2025 |
| 2026/2 — Prova A | 15/07/2026 |
| 2025/2 — Higienópolis, Prova B | 11/06/2025 |

## Como os três arquivos se conversam

```
analise-provas...md   →  por que estudar isso   (referência, estático)
plano-4-semanas...md  →  o que estudar hoje     (referência, estático)
cronograma-diario.pdf →  o dia a dia impresso   (gerado por script)
acompanhamento.md     →  onde eu estou          (você edita)
```

Se algum dia o plano mudar, edite o plano. O acompanhamento só guarda **estado**, nunca conteúdo —
é por isso que ele não desatualiza.
