import streamlit as st

from dados import AVISO, pegar_relatos
from layout import alerta_emergencia, cabecalho, estatisticas, grade_cartoes


def tela_inicio():
    # ----- Topo -----
    cabecalho("🛡️", "ESCUDO JOVEM", "Relate casos de cyberbullying com segurança")
    st.caption(AVISO)

    # ----- Como funciona -----
    grade_cartoes(
        [
            ("📝", "1. Relate", "Conte o que aconteceu, onde e quando. Pode ser sem se identificar."),
            ("🔎", "2. Acompanhe", "Receba um protocolo e veja o andamento do seu caso."),
            ("🤝", "3. Receba apoio", "Uma autoridade responde com orientações e providências."),
        ]
    )

    # ----- Números reais (lidos do relatos.json) -----
    relatos = pegar_relatos()
    concluidos = 0
    for relato in relatos:
        if relato["status"] == "Concluído":
            concluidos += 1
    estatisticas([(len(relatos), "relatos recebidos"), (concluidos, "casos concluídos")])

    # ----- Emergência -----
    alerta_emergencia("<b>Risco imediato?</b> Ligue <b>190</b>. Apoio emocional: <b>CVV 188</b>.")

    st.write("**Entre para continuar:**")
