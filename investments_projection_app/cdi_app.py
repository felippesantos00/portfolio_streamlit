import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime


def get_cdi(data_inicial, data_final):
    """Busca CDI diário no SGS do Banco Central"""
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # garante que status_code é 200
        try:
            data = response.json()
        except ValueError:
            st.warning("A API do Banco Central retornou um conteúdo inválido.")
            return pd.DataFrame(columns=["data", "valor"])
        if not data:
            st.warning("Não há dados para o período selecionado.")
            return pd.DataFrame(columns=["data", "valor"])

        df_cdi = pd.DataFrame(data)
        df_cdi["data"] = pd.to_datetime(df_cdi["data"], format="%d/%m/%Y")
        df_cdi["valor"] = df_cdi["valor"].astype(float)
        return df_cdi
    except requests.RequestException as e:
        st.error(f"Erro de conexão com a API: {e}")
        return pd.DataFrame(columns=["data", "valor"])


def cdi_app():
    st.title("📊 Simulação de Investimento - CDI/CDB")

    # Inputs de datas
    col1, col2 = st.columns(2)
    data_inicial = col1.date_input(
        "📅 Data inicial",
        value=st.session_state.data_inicial,
        key='data_inicial_input'
    )
    data_final = col2.date_input(
        "📅 Data final",
        value=st.session_state.data_final,
        key='data_final_input'
    )

    # Atualiza session_state das datas
    st.session_state.data_inicial = data_inicial
    st.session_state.data_final = data_final

    # Buscar CDI do período
    df_cdi = get_cdi(
        data_inicial.strftime("%d/%m/%Y"),
        data_final.strftime("%d/%m/%Y")
    )

    if df_cdi.empty:
        st.warning("Não foram encontrados dados para o período selecionado.")
        return

    # Agrupar por mês (acumulado mensal)
    df_cdi["ano_mes"] = df_cdi["data"].dt.to_period("M")
    df_cdi_mensal = df_cdi.groupby("ano_mes")["valor"].sum().reset_index()
    df_cdi_mensal["ano_mes"] = df_cdi_mensal["ano_mes"].astype(str)

    # CDI médio do período
    media_cdi = df_cdi["valor"].mean()

    # Inputs de simulação
    valor_inicial = st.number_input(
        "💰 Valor inicial (R$)",
        min_value=100.0,
        step=100.0,
        value=st.session_state.valor_inicial,
        key='valor_inicial_input'
    )
    anos = st.slider(
        "⏳ Período de simulação (anos)",
        1, 20,
        value=st.session_state.anos,
        step=1,
        key='anos_input'
    )
    percent_cdb = st.slider(
        "📈 Percentual do CDI (% do CDI)",
        80, 150,
        value=st.session_state.percent_cdb,
        step=1,
        key='percent_cdb_slider'
    )

    # Sincroniza com number_input
    percent_cdb_input = st.number_input(
        "📈 Percentual do CDI (% do CDI) exato",
        min_value=80,
        max_value=150,
        value=percent_cdb,
        step=1,
        key='percent_cdb_number'
    )

    # Simulação de CDB
    if valor_inicial > 0:
        media_cdi_diario = media_cdi / 100
        taxa_cdi_anual = (1 + media_cdi_diario) ** 252 - 1
        taxa_cdb = taxa_cdi_anual * (percent_cdb / 100)

        valor_final = valor_inicial * ((1 + taxa_cdb) ** anos)
        lucro = valor_final - valor_inicial
        lucro_liquido = lucro * 0.85  # 15% IR

        st.subheader("💹 Simulação de Investimento em CDB (% do CDI)")
        st.write(f"📊 CDI médio diário: **{media_cdi:.4f}% ao dia**")
        st.write(f"📈 CDI anualizado: **{taxa_cdi_anual*100:.2f}% ao ano**")
        st.write(
            f"🏦 CDB simulado: **{percent_cdb}% do CDI → {taxa_cdb*100:.2f}% ao ano**")
        st.write(f"⏳ Período: **{anos} anos**")
        st.write(f"💵 Valor final estimado: **R${valor_final:,.2f}**")
        st.write(f"📈 Lucro estimado: **R${lucro:,.2f}**")
        st.write(f"💰 Lucro líquido (após IR): **R${lucro_liquido:,.2f}**")

        # Gráfico evolução
        anos_lista = list(range(anos + 1))
        valores = [valor_inicial * ((1 + taxa_cdb) ** t) for t in anos_lista]

        fig_invest = go.Figure()
        fig_invest.add_trace(go.Scatter(
            x=anos_lista,
            y=valores,
            mode="lines+markers",
            name="Evolução",
            hovertemplate="Ano %{x}<br>💰 R$ %{y:,.2f}<extra></extra>"
        ))
        fig_invest.add_hline(y=valor_inicial, line_dash="dot",
                             annotation_text="Valor Inicial")
        fig_invest.update_layout(
            title=f"Simulação CDB {percent_cdb}% do CDI",
            xaxis_title="Ano",
            yaxis_title="Valor (R$)",
            template="plotly_white"
        )
        st.plotly_chart(fig_invest, use_container_width=True)

    # Gráfico CDI Mensal
    fig_cdi = go.Figure()
    fig_cdi.add_trace(go.Bar(
        x=df_cdi_mensal["ano_mes"],
        y=df_cdi_mensal["valor"],
        name="CDI acumulado mensal",
        hovertemplate="Mês %{x}<br>📊 CDI %{y:.4f}<extra></extra>"
    ))
    fig_cdi.update_layout(
        title="📊 CDI acumulado por mês",
        xaxis_title="Ano-Mês",
        yaxis_title="CDI acumulado",
        template="plotly_white"
    )
    st.plotly_chart(fig_cdi, use_container_width=True)

    # Atualiza session_state dos inputs
    st.session_state.valor_inicial = valor_inicial
    st.session_state.anos = anos
    st.session_state.data_inicial = data_inicial
    st.session_state.data_final = data_final
    st.session_state.percent_cdb = percent_cdb_input
    percent_cdb = st.session_state.percent_cdb
