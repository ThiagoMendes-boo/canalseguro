import json
from datetime import datetime

import streamlit as st

from dados import (
    PROVIDENCIAS,
    STATUS,
    achar_relato,
    pegar_relatos,
    relato_em_markdown,
    salvar_relatos,
    tem_dado_pessoal,
)
from layout import cartao_relato, selo_prioridade, selo_status


def tela_autoridade():
    st.subheader("Painel da autoridade (simulação)")
    
    email_agente = st.session_state.get("email", "agentesilva.demo@gmail.com")
    tel_agente = st.session_state.get("telefone_agente", "(67) 99988-7766")
    
    st.write(
        f"Agente: **{st.session_state.agente}** | Matrícula: {st.session_state.matricula} "
        f"| Unidade: {st.session_state.unidade}\n\n"
        f"E-mail: `{email_agente}` | Telefone: `{tel_agente}`"
    )

    relatos = pegar_relatos()  # lê o arquivo relatos.json

    if len(relatos) == 0:
        st.info("Nenhum relato ainda. Peça para a vítima ou o anônimo enviar um relato.")
        return  # para aqui e não mostra o resto

    # ----- Números do topo -----
    com_risco = 0
    for relato in relatos:
        if relato["risco"]:
            com_risco += 1

    col1, col2 = st.columns(2)
    col1.metric("Relatos recebidos", len(relatos))
    col2.metric("Com risco informado", com_risco)

    # ----- Cartões com todos os relatos -----
    for relato in relatos:
        cartao_relato(relato)

    # ----- Abrir um relato -----
    protocolos = [relato["protocolo"] for relato in relatos]
    escolhido = st.selectbox("Abrir relato", protocolos)
    relato = achar_relato(escolhido, relatos)

    st.markdown(
        selo_prioridade(relato["risco"]) + selo_status(relato["status"]),
        unsafe_allow_html=True,
    )
    st.write("**Dados de contato**")
    st.write(f"Nome: {relato['nome_completo']}  |  Telefone: {relato['telefone']}")

    st.write("**Ocorrência**")
    st.write(f"Tipo: {relato['tipo']}  |  Plataforma: {relato['plataforma']}  |  Quando: {relato['quando']}")
    st.write(f"Cidade: {relato['cidade']}  |  Local: {relato['local']}")
    if relato["local_detalhe"]:
        st.write("Detalhe do local: " + relato["local_detalhe"])
    if relato["prints"]:
        evidencias = "sim"
    else:
        evidencias = "não"
    st.write("Evidências guardadas: " + evidencias)
    st.write("**Relato:**")
    st.text(relato["descricao"])

    # ----- Atualizar o caso -----
    st.write("**Atualizar o caso**")
    novo_status = st.selectbox(
        "Status",
        STATUS,
        index=STATUS.index(relato["status"]),
        key="status_" + escolhido,
    )
    nova_providencia = st.selectbox(
        "Providência tomada",
        PROVIDENCIAS,
        index=PROVIDENCIAS.index(relato["providencia"]),
        key="providencia_" + escolhido,
    )
    mensagem = st.text_area(
        "Mensagem de orientação para a vítima",
        value=relato["resposta"],
        key="mensagem_" + escolhido,
        max_chars=400,
    )
    observacao = st.text_area(
        "Observação interna (a vítima não vê)",
        value=relato["observacao"],
        key="observacao_" + escolhido,
        max_chars=400,
    )

    if st.button("Salvar atualização"):
        if tem_dado_pessoal(mensagem) or tem_dado_pessoal(observacao):
            st.error("Parece haver e-mail, telefone ou CPF nos textos. Use apenas dados fictícios.")
        else:
            relato["status"] = novo_status
            relato["providencia"] = nova_providencia
            relato["resposta"] = mensagem.strip()
            relato["observacao"] = observacao.strip()
            relato["agente"] = (
                f"{st.session_state.agente} (mat. {st.session_state.matricula}) "
                f"- {st.session_state.unidade}"
            )
            relato["atualizado_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            salvar_relatos(relatos)  # grava no arquivo relatos.json
            st.success("Atualização salva. A vítima já pode ver pelo protocolo.")

    # ----- Baixar este relato em Markdown -----
    st.download_button(
        "Baixar este relato (Markdown)",
        data=relato_em_markdown(relato),
        file_name=escolhido + ".md",
        mime="text/markdown",
    )