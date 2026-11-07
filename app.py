import streamlit as st

from autoridade import tela_autoridade
from dados import AVISO
from layout import aplicar_estilo, aplicar_script, cabecalho
from login import tela_login
from vitima import tela_vitima

st.set_page_config(page_title="Canal Seguro (protótipo)", page_icon="🛡️")
aplicar_estilo()  # liga o estilo.css
aplicar_script()  # liga o script.js

# Memória do app: guarda quem está usando (None = ninguém entrou ainda)
if "perfil" not in st.session_state:
    st.session_state.perfil = None


def sair():
    st.session_state.clear()  # apaga tudo o que o app lembrava da pessoa


# ----- Decide qual tela mostrar -----
perfil = st.session_state.perfil

if perfil is None:
    tela_login()
else:
    cabecalho("🛡️", "Canal Seguro", "Relate casos de cyberbullying com segurança")
    st.caption(AVISO)

    with st.sidebar:
        if perfil == "vitima":
            st.write("Você está como: **" + st.session_state.nome_completo + "**")
        elif perfil == "autoridade":
            st.write("Você está como: **" + st.session_state.agente + "**")
        else:
            st.write("Você está como: **Anônimo**")
        st.button("Sair", on_click=sair)

    if perfil == "autoridade":
        tela_autoridade()
    else:
        tela_vitima()
