import streamlit as st

from dados import nome_completo_valido, telefone_valido
from inicio import tela_inicio
from layout import nota

# Acesso de demonstração da autoridade (aceita com ou sem acento)
USUARIOS_DEMO = ["policia", "polícia"]
SENHA_DEMO = "demo123"


def tela_login():
    tela_inicio()

    aba_vitima, aba_anonimo, aba_autoridade = st.tabs(["Vítima", "Anônimo", "Autoridade"])

    # ----- Vítima -----
    with aba_vitima:
        nota("Preencha seus dados. A autoridade usará para entrar em contato com você.")
        nome_completo = st.text_input("Nome completo", max_chars=60)
        telefone = st.text_input("Telefone com DDD (ex.: (67) 91234-5678)", max_chars=20)
        cidade = st.text_input("Cidade", max_chars=40)
        aceito = st.checkbox("Concordo que a autoridade veja esses dados para falar comigo")

        if st.button("Entrar como vítima"):
            nome_completo = nome_completo.strip()
            cidade = cidade.strip()

            if not nome_completo_valido(nome_completo):
                st.warning("Digite o nome completo (nome e sobrenome).")
            elif not telefone_valido(telefone):
                st.warning("Digite um telefone com DDD, com 10 ou 11 números.")
            elif len(cidade) < 2:
                st.warning("Digite sua cidade.")
            elif not aceito:
                st.warning("Marque a caixa de concordância para continuar.")
            else:
                st.session_state.perfil = "vitima"
                st.session_state.nome_completo = nome_completo
                st.session_state.telefone = telefone.strip()
                st.session_state.cidade = cidade
                st.rerun()

    # ----- Anônimo -----
    with aba_anonimo:
        nota("Nenhum dado pessoal é guardado. Você receberá um <b>protocolo</b> para acompanhar o caso.")

        if st.button("Entrar sem me identificar"):
            st.session_state.perfil = "anonimo"
            st.rerun()

    # ----- Autoridade (Apenas Usuário e Senha) -----
    with aba_autoridade:
        nota("Área restrita. Acesso de demonstração: usuário <b>policia</b> (ou <b>polícia</b>), senha <b>demo123</b>.")

        usuario = st.text_input("Usuário", key="login_usuario")
        senha = st.text_input("Senha", type="password", key="login_senha")

        if st.button("Entrar como autoridade"):
            usuario_limpo = usuario.strip().lower()

            if usuario_limpo not in USUARIOS_DEMO or senha != SENHA_DEMO:
                st.error("Usuário ou senha incorretos.")
            else:
                # Preenche automaticamente todos os dados fictícios do agente
                st.session_state.perfil = "autoridade"
                st.session_state.agente = "Agente Carlos Silva"
                st.session_state.matricula = "4829-PC"
                st.session_state.unidade = "Delegacia de Repressão aos Crimes Cibernéticos"
                st.session_state.email = "agentesilva.demo@gmail.com"
                st.session_state.telefone_agente = "(67) 99988-7766"
                st.rerun()
                import streamlit as st

from dados import (
    buscar_usuario,
    nome_completo_valido,
    salvar_usuario,
    telefone_valido,
)
from inicio import tela_inicio
from layout import nota

# Acesso de demonstração padrão da autoridade
USUARIOS_DEMO = ["policia", "polícia"]
SENHA_DEMO = "demo123"

DADOS_AGENTE_PADRAO = {
    "agente": "Agente Carlos Silva",
    "matricula": "4829-PC",
    "unidade": "Delegacia de Repressão aos Crimes Cibernéticos",
    "email": "agentesilva.demo@gmail.com",
    "telefone": "(67) 99988-7766",
}


def tela_login():
    tela_inicio()

    aba_vitima, aba_anonimo, aba_autoridade, aba_cadastro = st.tabs(
        ["Vítima", "Anônimo", "Autoridade", "📝 Criar Conta"]
    )

    # ----- Aba 1: Vítima -----
    with aba_vitima:
        nota("Preencha os seus dados para iniciar o atendimento.")
        nome_completo = st.text_input("Nome completo", max_chars=60)
        telefone = st.text_input("Telefone com DDD (ex.: (67) 91234-5678)", max_chars=20)
        cidade = st.text_input("Cidade", max_chars=40)
        aceito = st.checkbox("Concordo que a autoridade veja esses dados para falar comigo")

        if st.button("Entrar como vítima"):
            nome_completo = nome_completo.strip()
            cidade = cidade.strip()

            if not nome_completo_valido(nome_completo):
                st.warning("Digite o nome completo (nome e sobrenome).")
            elif not telefone_valido(telefone):
                st.warning("Digite um telefone com DDD, com 10 ou 11 números.")
            elif len(cidade) < 2:
                st.warning("Digite sua cidade.")
            elif not aceito:
                st.warning("Marque a caixa de concordância para continuar.")
            else:
                st.session_state.perfil = "vitima"
                st.session_state.nome_completo = nome_completo
                st.session_state.telefone = telefone.strip()
                st.session_state.cidade = cidade
                st.rerun()

    # ----- Aba 2: Anônimo -----
    with aba_anonimo:
        nota("Nenhum dado pessoal é guardado. Você receberá um <b>protocolo</b> para acompanhar o caso.")

        if st.button("Entrar sem me identificar"):
            st.session_state.perfil = "anonimo"
            st.rerun()

    # ----- Aba 3: Autoridade -----
    with aba_autoridade:
        nota("Área restrita. Acesso de demonstração: usuário <b>policia</b>, senha <b>demo123</b>.")

        usuario = st.text_input("Usuário / E-mail", key="login_usuario")
        senha = st.text_input("Senha", type="password", key="login_senha")

        if st.button("Entrar como autoridade"):
            usuario_limpo = usuario.strip().lower()

            # 1. Verifica se é o utilizador de demonstração padrão
            if usuario_limpo in USUARIOS_DEMO and senha == SENHA_DEMO:
                st.session_state.perfil = "autoridade"
                st.session_state.agente = DADOS_AGENTE_PADRAO["agente"]
                st.session_state.matricula = DADOS_AGENTE_PADRAO["matricula"]
                st.session_state.unidade = DADOS_AGENTE_PADRAO["unidade"]
                st.session_state.email = DADOS_AGENTE_PADRAO["email"]
                st.session_state.telefone_agente = DADOS_AGENTE_PADRAO["telefone"]
                st.rerun()
            else:
                # 2. Verifica se é um utilizador registado na base de dados
                usr = buscar_usuario(usuario_limpo)
                if usr and usr.get("senha") == senha and usr.get("perfil") == "autoridade":
                    st.session_state.perfil = "autoridade"
                    st.session_state.agente = usr.get("agente", "Agente")
                    st.session_state.matricula = usr.get("matricula", "0000")
                    st.session_state.unidade = usr.get("unidade", "Delegacia")
                    st.session_state.email = usr.get("email", "")
                    st.session_state.telefone_agente = usr.get("telefone", "")
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")

    # ----- Aba 4: Criar Conta (Cadastro) -----
    with aba_cadastro:
        nota("Cadastre uma nova conta para aceder ao sistema.")

        tipo_perfil = st.radio(
            "Tipo de cadastro:",
            ["Vítima / Cidadão", "Autoridade / Policial"],
            horizontal=True,
        )

        if tipo_perfil == "Vítima / Cidadão":
            with st.form("form_cad_vitima", clear_on_submit=True):
                nome_cad = st.text_input("Nome completo", max_chars=60)
                tel_cad = st.text_input("Telefone com DDD", max_chars=20)
                cidade_cad = st.text_input("Cidade", max_chars=40)
                email_cad = st.text_input("E-mail fictício", max_chars=60)
                senha_cad = st.text_input("Senha", type="password", max_chars=30)

                if st.form_submit_button("Cadastrar Vítima"):
                    nome_cad = nome_cad.strip()
                    cidade_cad = cidade_cad.strip()
                    email_cad = email_cad.strip().lower()

                    if not nome_completo_valido(nome_cad):
                        st.warning("Introduza o nome completo (nome e sobrenome).")
                    elif not telefone_valido(tel_cad):
                        st.warning("Introduza um telefone válido com DDD.")
                    elif len(cidade_cad) < 2:
                        st.warning("Informe a sua cidade.")
                    elif "@" not in email_cad:
                        st.warning("Informe um e-mail válido.")
                    elif buscar_usuario(email_cad):
                        st.error("Este e-mail já está cadastrado.")
                    elif len(senha_cad) < 4:
                        st.warning("A senha deve ter pelo menos 4 caracteres.")
                    else:
                        salvar_usuario({
                            "perfil": "vitima",
                            "nome_completo": nome_cad,
                            "telefone": tel_cad.strip(),
                            "cidade": cidade_cad,
                            "email": email_cad,
                            "senha": senha_cad,
                        })
                        st.success("Cadastro realizado com sucesso! Utilize a aba 'Vítima' para entrar.")

        else:
            with st.form("form_cad_autoridade", clear_on_submit=True):
                agente_cad = st.text_input("Nome do Agente", max_chars=60)
                mat_cad = st.text_input("Matrícula", max_chars=15)
                unidade_cad = st.text_input("Delegacia / Unidade", max_chars=60)
                email_cad = st.text_input("E-mail / Usuário de login", max_chars=60)
                senha_cad = st.text_input("Senha", type="password", max_chars=30)

                if st.form_submit_button("Cadastrar Agente"):
                    agente_cad = agente_cad.strip()
                    mat_cad = mat_cad.strip()
                    unidade_cad = unidade_cad.strip()
                    email_cad = email_cad.strip().lower()

                    if not nome_completo_valido(agente_cad):
                        st.warning("Introduza o nome completo do agente.")
                    elif len(mat_cad) < 3:
                        st.warning("A matrícula precisa de pelo menos 3 caracteres.")
                    elif len(unidade_cad) < 3:
                        st.warning("Informe a delegacia ou unidade.")
                    elif "@" not in email_cad and len(email_cad) < 3:
                        st.warning("Informe um usuário/e-mail válido.")
                    elif buscar_usuario(email_cad):
                        st.error("Este usuário/e-mail já está cadastrado.")
                    elif len(senha_cad) < 4:
                        st.warning("A senha deve ter pelo menos 4 caracteres.")
                    else:
                        salvar_usuario({
                            "perfil": "autoridade",
                            "agente": agente_cad,
                            "matricula": mat_cad,
                            "unidade": unidade_cad,
                            "email": email_cad,
                            "senha": senha_cad,
                            "telefone": "(67) 99988-7766",
                        })
                        st.success("Agente cadastrado com sucesso! Já pode fazer login na aba 'Autoridade'.")