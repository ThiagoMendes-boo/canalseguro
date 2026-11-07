from datetime import date

import streamlit as st

from dados import (
    LOCAIS,
    PLATAFORMAS,
    STATUS,
    TIPOS,
    achar_relato,
    criar_protocolo,
    pegar_relatos,
    salvar_relatos,
    tem_dado_pessoal,
)
from layout import protocolo_destaque, selo_status

EXEMPLO = (
    "Exemplo fictício: no grupo da turma de Lia (nome inventado), um perfil "
    "anônimo vem postando piadas e prints dela."
)


def preencher_exemplo():
    st.session_state.descricao = EXEMPLO


def tela_vitima():
    eh_vitima = st.session_state.perfil == "vitima"

    # A vítima já informou a cidade no login. O anônimo começa com o campo vazio.
    if eh_vitima:
        cidade_inicial = st.session_state.cidade
    else:
        cidade_inicial = ""

    aba_relato, aba_consulta = st.tabs(["Fazer um relato", "Consultar protocolo"])

    # ----- Fazer um relato -----
    with aba_relato:
        st.subheader("Fazer um relato")

        tipo = st.selectbox("O que aconteceu?", TIPOS)
        plataforma = st.selectbox("Em qual plataforma?", PLATAFORMAS)
        quando = st.date_input("Quando (aproximadamente)?", value=date.today())

        st.write("**Onde aconteceu?**")
        cidade = st.text_input("Cidade do acontecimento", value=cidade_inicial, max_chars=40)
        local = st.selectbox("Local do acontecimento", LOCAIS)
        local_detalhe = st.text_input(
            "Nome da escola ou endereço aproximado (opcional)", max_chars=80
        )

        risco = st.checkbox("Estou sofrendo ameaça ou me sinto em risco agora")
        if risco:
            st.error("Se há risco imediato, ligue 190 agora.")

        st.text_area(
            "Conte o que aconteceu (use apenas dados fictícios)",
            key="descricao",
            height=130,
            max_chars=600,
        )
        st.button("Preencher com exemplo fictício", on_click=preencher_exemplo)
        tem_prints = st.checkbox("Guardei prints ou outras evidências")

        if st.button("Enviar relato"):
            texto = st.session_state.descricao.strip()
            cidade = cidade.strip()

            if len(cidade) < 2:
                st.warning("Informe a cidade do acontecimento.")
            elif len(texto) < 10:
                st.warning("Descreva um pouco mais o que aconteceu.")
            elif tem_dado_pessoal(texto):
                st.error("Parece haver e-mail, telefone ou CPF. Use apenas dados fictícios.")
            else:
                protocolo = criar_protocolo()

                # Só a vítima identificada tem dados de contato guardados
                if eh_vitima:
                    nome_completo = st.session_state.nome_completo
                    telefone = st.session_state.telefone
                else:
                    nome_completo = "Anônimo"
                    telefone = "Não informado"

                relato = {
                    "protocolo": protocolo,
                    "status": "Recebido",
                    "resposta": "",
                    "providencia": "Nenhuma ainda",
                    "observacao": "",
                    "agente": "",
                    "atualizado_em": "",
                    "nome_completo": nome_completo,
                    "telefone": telefone,
                    "cidade": cidade,
                    "local": local,
                    "local_detalhe": local_detalhe.strip(),
                    "tipo": tipo,
                    "plataforma": plataforma,
                    "quando": quando.strftime("%d/%m/%Y"),
                    "risco": risco,
                    "prints": tem_prints,
                    "descricao": texto,
                }
                relatos = pegar_relatos()
                relatos.append(relato)
                salvar_relatos(relatos)

                st.success("Relato recebido! Guarde o código abaixo para acompanhar o caso:")
                protocolo_destaque(protocolo)
                st.info(
                    "Enquanto isso: não responda ao agressor, guarde os prints, "
                    "bloqueie o perfil e conte para um adulto de confiança."
                )

    # ----- Consultar protocolo -----
    with aba_consulta:
        st.subheader("Consultar protocolo")
        codigo = st.text_input("Digite o protocolo (ex.: CB-123456)", max_chars=12)

        if codigo:
            relato = achar_relato(codigo)
            if relato is None:
                st.warning("Protocolo não encontrado.")
            else:
                st.markdown("Status: " + selo_status(relato["status"]), unsafe_allow_html=True)
                st.progress((STATUS.index(relato["status"]) + 1) / len(STATUS))
                st.write("Providência: " + relato["providencia"])
                if relato["agente"]:
                    st.write("Atendido por: " + relato["agente"])
                    st.caption("Última atualização: " + relato["atualizado_em"])
                if relato["resposta"]:
                    st.info("Mensagem da autoridade: " + relato["resposta"])
                else:
                    st.caption("Ainda sem mensagem da autoridade.")