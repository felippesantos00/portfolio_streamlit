from twelvedata import TDClient
import pandas as pd
import streamlit as st
import dotenv as env
import plotly.graph_objects as go


def projection_investiments_app():
    # Carregar variável de ambiente
    env.load_dotenv("conf/.env")
    API_TOKEN_TWELVE = env.dotenv_values("conf/.env")["API_TOKEN_TWELVE"]

    td = TDClient(apikey=API_TOKEN_TWELVE)

    st.title("📈 Projeção de Investimentos")

    # Lista de ações
    list_of_investments = ["PETR4", "VALE3", "ITUB4", "ABEV3", "BBDC3"]
    option = st.selectbox("Selecione uma ação", list_of_investments)
    st.write("Você selecionou:", option)

    # Quantidade de ações
    quantidade_acoes = st.slider("Quantidade de ações", 1, 100, 10)

    # Intervalo
    intervalo = st.selectbox(
        "Selecione o intervalo",
        ["1min", "5min", "15min", "30min", "45min", "1h",
            "2h", "4h", "8h", "1day", "1week", "1month"]
    )

    # Define limites máximos de pontos de dados dependendo do intervalo
    interval_max_points = {
        "1min": 1440,     # 1 dia de minuto a minuto
        "5min": 288,      # 1 dia dividido em blocos de 5min
        "15min": 96,
        "30min": 48,
        "45min": 32,
        "1h": 24,
        "2h": 12,
        "4h": 6,
        "8h": 3,
        "1day": 365,
        "1week": 52,
        "1month": 36
    }

    max_dias = interval_max_points.get(intervalo, 30)
    dias = st.slider("Quantidade de dias/pontos de dados",
                     1, max_dias, min(30, max_dias))

    # Buscar dados históricos
    try:
        ts = td.time_series(
            symbol=option,
            interval=intervalo,
            outputsize=dias
        ).as_pandas()

        if ts.empty:
            st.error("Não há dados disponíveis para esta ação.")
        else:
            ts["close"] = ts["close"].astype(float)
            ts = ts.reset_index()
            ts["datetime"] = pd.to_datetime(
                ts["datetime"]).dt.strftime("%Y-%m-%d %H:%M:%S")

            fig_plotly = go.Figure()
            fig_plotly.add_trace(go.Scatter(
                x=ts["datetime"],
                y=ts["close"],
                mode='lines',
                name=option
            ))
            fig_plotly.update_layout(
                title=f"Preço da Ação: {option}",
                xaxis_title="",
                yaxis_title="Preço (R$)",
                template="plotly_dark"
            )
            st.write(f"### Dados históricos ({dias} pontos de dados)")
            st.plotly_chart(fig_plotly, use_container_width=True)

            # st.line_chart(ts.set_index("datetime")["close"])
            # st.dataframe(ts)

    except Exception as e:
        st.error(f"Erro ao buscar dados da ação: {e}")
