#!/usr/bin/env python3
"""Lê e corrige os marcadores (outline) do PDF gerado pelo Chromium.

uso: marcadores.py ler ARQUIVO.pdf
         imprime JSON [[título, página], ...]
     marcadores.py corrigir ARQUIVO.pdf TÍTULO ASSUNTO PALAVRAS-CHAVE
         reescreve o arquivo com títulos limpos e metadados

O Chromium às vezes repete o texto de um título no marcador ("ProbabilidadeProbabilidade")
quando o bloco foi empurrado para a página seguinte; aqui isso é desfeito.
"""
import json
import sys

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject


def limpar(titulo):
    titulo = " ".join(str(titulo).split())
    meio = len(titulo) // 2
    if len(titulo) % 2 == 0 and titulo[:meio] == titulo[meio:]:
        return titulo[:meio]
    return titulo


def ler(caminho):
    leitor = PdfReader(caminho)
    saida = []

    def percorrer(itens):
        for item in itens:
            if isinstance(item, list):
                percorrer(item)
            else:
                saida.append([limpar(item.title), leitor.get_destination_page_number(item) + 1])

    percorrer(leitor.outline)
    print(json.dumps(saida, ensure_ascii=False))


def corrigir(caminho, titulo, assunto, palavras):
    escritor = PdfWriter(clone_from=caminho)
    raiz = escritor._root_object.get("/Outlines")

    def visitar(no):
        while no is not None:
            no = no.get_object()
            if "/Title" in no:
                no[NameObject("/Title")] = TextStringObject(limpar(no["/Title"]))
            if "/First" in no:
                visitar(no["/First"])
            no = no.get("/Next")

    if raiz is not None:
        visitar(raiz.get_object().get("/First"))
    escritor.add_metadata({"/Title": titulo, "/Subject": assunto, "/Keywords": palavras})
    escritor.page_mode = "/UseOutlines"
    with open(caminho, "wb") as arquivo:
        escritor.write(arquivo)


if __name__ == "__main__":
    acao, *args = sys.argv[1:]
    {"ler": ler, "corrigir": corrigir}[acao](*args)
