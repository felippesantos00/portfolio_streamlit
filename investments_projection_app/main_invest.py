import streamlit as st
from selic_app import selic_app
from cdi_app import cdi_app
from projection_investiments_app import projection_investiments_app
from chatbot_app import chat_bot_app
from datetime import datetime
from consulta_dados_cvm_app import consulta_dados_cvm_app

ano_atual = datetime.now().year
ano_passado = ano_atual - 1
anos_lista = [ano_passado - i for i in range(0, 4)]
default_values = {
    "percent_cdb": 115,
    "percent_cdb_input": 115,
    "valor_inicial": 1000.0,
    "anos": 5,
    "data_inicial": datetime(datetime.now().year, 1, 1).date(),
    "data_final": datetime.now().date(),
    "option_menu": "Simulação Selic",
    "empresa_cvm": "PETROLEO BRASILEIRO S.A. PETROBRAS",
    "anos_selecionados": anos_lista
}

for key, value in default_values.items():
    if key not in st.session_state or st.session_state[key] is None:
        st.session_state[key] = value

menu_options = [
    "Simulação Selic",
    "Simulação CDI/CDB",
    "Projeção de Investimentos",
    "ChatBot Local",
    "Dados Abertos CVM"
]

menu = st.sidebar.radio(
    "Escolha a opção:",
    menu_options,
    key="option_menu"
)

# ---------- Roteamento das páginas ----------
if st.session_state.option_menu == "Simulação Selic":
    selic_app()
elif st.session_state.option_menu == "Simulação CDI/CDB":
    cdi_app()
elif st.session_state.option_menu == "Projeção de Investimentos":
    projection_investiments_app()
elif st.session_state.option_menu == "ChatBot Local":
    chat_bot_app()
elif st.session_state.option_menu == "Dados Abertos CVM":
    consulta_dados_cvm_app()
