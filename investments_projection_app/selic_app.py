# selic_app.py
import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

def selic_app():
    url = "https://www.bcb.gov.br/api/servico/sitebcb/historicotaxasjuros"
    response = requests.get(url).json()
    df = pd.DataFrame(response['conteudo'])
    df['DataReuniaoCopom'] = pd.to_datetime(
        df['DataReuniaoCopom'], format='%Y-%m-%dT%H:%M:%S%z'
    )
    df['DataReuniaoCopom'] = df['DataReuniaoCopom'].dt.tz_localize(None)
    df['MetaSelic'] = df['MetaSelic'].astype(float)
    df = df.sort_values(by='DataReuniaoCopom').reset_index(drop=True)

    media_selic = df['MetaSelic'].mean()
    quatro_anos_atras = datetime.now() - timedelta(days=4*365)
    df_4anos = df[df['DataReuniaoCopom'] >= quatro_anos_atras]
    media_4anos = df_4anos['MetaSelic'].mean()

    st.title("📊 Simulação de Investimento - Selic")

    valor_inicial = st.number_input(
        "💰 Valor inicial do investimento (R$)", min_value=100.0, step=100.0, value=st.session_state.valor_inicial,
        format="%.2f", help="Valor inicial do investimento em reais.",
        key='valor_inicial')
    anos = st.slider("⏳ Período de simulação (anos)", 1, 20, value=st.session_state.anos,
                     key='anos', help="Selecione o período de simulação em anos.")

    if valor_inicial > 0:
        taxa_media = media_4anos / 100 
        valor_final = valor_inicial * ((1 + taxa_media) ** anos)
        lucro = valor_final - valor_inicial
        lucro_liquido = lucro * 0.85 

        st.subheader("💹 Simulação de Investimento com base na Selic")
        st.write(
            f"📊 Média SELIC últimos 4 anos: **{media_4anos:.2f}% ao ano**")
        st.write(f"⏳ Período: **{anos} anos**")
        st.write(f"💵 Valor final estimado: **R${valor_final:,.2f}**")
        st.write(f"📈 Lucro estimado: **R${lucro:,.2f}**")
        st.write(f"💰 Lucro líquido (após IR): **R${lucro_liquido:,.2f}**")

        anos_lista = list(range(anos + 1))
        valores = [valor_inicial * ((1 + taxa_media) ** t) for t in anos_lista]

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
            title="Simulação de Investimento Selic (últimos 4 anos)",
            xaxis_title="Ano",
            yaxis_title="Valor (R$)",
            template="plotly_white"
        )
        st.plotly_chart(fig_invest, use_container_width=True)


    st.number_input(
        "Média Geral da Selic (desde 1999):",
        value=media_selic,
        format="%.2f",
        disabled=True
    )
    st.number_input(
        "Média da Selic nos últimos 4 anos:",
        value=media_4anos,
        format="%.2f",
        disabled=True
    )


    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['DataReuniaoCopom'],
        y=df['MetaSelic'],
        mode='lines',
        name='Selic',
        hovertemplate="📅 Data %{x|%d/%m/%Y}<br>💰 Selic: %{y:.2f}%<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=df['DataReuniaoCopom'],
        y=[media_selic]*len(df),
        mode='lines',
        name=f'Média geral: {media_selic:.2f}%',
        line=dict(color='red', dash='dot')
    ))
    fig.add_trace(go.Scatter(
        x=df['DataReuniaoCopom'],
        y=[media_4anos]*len(df),
        mode='lines',
        name=f'Média últimos 4 anos: {media_4anos:.2f}%',
        line=dict(color='green', dash='dash')
    ))
    fig.update_layout(
        title="Evolução da Taxa Selic",
        xaxis_title="Data da Reunião do Copom",
        yaxis_title="Taxa Selic (%)",
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)
