import html
import os

import streamlit as st
import streamlit.components.v1 as components

# A pasta onde estão o layout.py, o estilo.css e o script.js
PASTA = os.path.dirname(os.path.abspath(__file__))

CORES_STATUS = {
    "Recebido": "#6b7280",
    "Em análise": "#d97706",
    "Encaminhado": "#2563eb",
    "Concluído": "#16a34a",
}


def ler_arquivo(nome):
    with open(os.path.join(PASTA, nome), "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def escapar(texto):
    # Protege o layout: se alguém digitar código HTML no relato, ele vira texto comum
    return html.escape(str(texto))


# ---------- LIGAÇÃO COM O CSS E O JAVASCRIPT ----------
def aplicar_estilo():
    # Lê o estilo.css e coloca dentro de uma tag <style> na página
    css = ler_arquivo("estilo.css")
    st.markdown("<style>" + css + "</style>", unsafe_allow_html=True)


def aplicar_script():
    # Lê o script.js e roda em um iframe invisível (o st.markdown bloqueia <script>)
    js = ler_arquivo("script.js")
    components.html("<script>" + js + "</script>", height=0)


# ---------- PEÇAS DO LAYOUT ----------
def cabecalho(icone, titulo, subtitulo):
    st.markdown(
        f'<div class="hero"><div class="icone">{icone}</div>'
        f"<h1>{titulo}</h1><p>{subtitulo}</p></div>",
        unsafe_allow_html=True,
    )


def nota(texto):
    st.markdown(f'<div class="nota">{texto}</div>', unsafe_allow_html=True)


def alerta_emergencia(texto):
    st.markdown(f'<div class="alerta-emergencia">{texto}</div>', unsafe_allow_html=True)


def grade_cartoes(itens):
    # itens: lista de (emoji, titulo, texto)
    partes = []
    for emoji, titulo, texto in itens:
        partes.append(
            f'<div class="cartao-info revelar"><div class="emoji">{emoji}</div>'
            f"<b>{titulo}</b><p>{texto}</p></div>"
        )
    st.markdown('<div class="grade-cartoes">' + "".join(partes) + "</div>", unsafe_allow_html=True)


def estatisticas(itens):
    # itens: lista de (numero, rotulo). O JavaScript anima o número.
    partes = []
    for numero, rotulo in itens:
        partes.append(
            f'<div class="estatistica revelar"><b class="contador">{numero}</b>'
            f"<span>{rotulo}</span></div>"
        )
    st.markdown('<div class="estatisticas">' + "".join(partes) + "</div>", unsafe_allow_html=True)


def protocolo_destaque(protocolo):
    st.markdown(
        f'<div class="protocolo" title="Clique para copiar">{protocolo}</div>'
        '<div class="protocolo-dica">Clique no código para copiar</div>',
        unsafe_allow_html=True,
    )


def selo(texto, cor):
    return f'<span class="selo" style="background:{cor}">{texto}</span>'


def selo_status(status):
    return selo(status, CORES_STATUS[status])


def selo_prioridade(risco):
    if risco:
        return selo("ALTA", "#e5484d")
    return selo("Normal", "#6b7280")


def cartao_relato(relato):
    # Um cartão resumido para cada relato na lista da autoridade
    if relato["risco"]:
        classe = "cartao alta"
    else:
        classe = "cartao"
    st.markdown(
        f'<div class="{classe}">'
        f'<div class="cartao-topo"><b>{relato["protocolo"]}</b>'
        f'<span>{selo_prioridade(relato["risco"])}{selo_status(relato["status"])}</span></div>'
        f'<div>{escapar(relato["tipo"])}</div>'
        f'<small>{escapar(relato["cidade"])} · {escapar(relato["local"])} · '
        f'{escapar(relato["quando"])}</small></div>',
        unsafe_allow_html=True,
    )
