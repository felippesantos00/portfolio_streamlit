import streamlit as st
import requests
import zipfile
import io
import pandas as pd
import plotly.express as px


def consulta_dados_cvm_app():
    st.set_page_config(page_title="Análise Petrobras - CVM", layout="centered")

    st.title("📊 Análise Financeira - CVM")
    st.markdown(
        "Dados oficiais de Demonstrações Financeiras Padronizadas (DFP) extraídos da **CVM** via CSV/XBRL."
    )

    anos = st.multiselect(
        "Selecione os anos:", [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025], default=st.session_state.get("anos_selecionados"),
        key="anos_selecionados"

    )

    empresas_disponiveis = set()
    for ano in anos:
        url = f"https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_{ano}.zip"
        resp = requests.get(url)
        if resp.status_code != 200:
            continue
        z = zipfile.ZipFile(io.BytesIO(resp.content))
        arquivos = z.namelist()
        arquivo_dre = next((a for a in arquivos if "DRE_con" in a), None)
        if not arquivo_dre:
            arquivo_dre = next((a for a in arquivos if "DRE_ind" in a), None)
        if arquivo_dre:
            with z.open(arquivo_dre) as f:
                dre = pd.read_csv(f, sep=";", decimal=",", encoding="latin1")
            empresas_disponiveis.update(dre["DENOM_CIA"].dropna().unique())

    if not empresas_disponiveis:
        st.error("Não foi possível encontrar empresas nos anos selecionados.")
        return

    if "empresa_cvm" not in st.session_state:
        st.session_state.empresa_cvm = sorted(empresas_disponiveis)[0]

    empresa = st.selectbox(
        "Selecione a empresa:",
        sorted(empresas_disponiveis),
        key="empresa_cvm"
    )

    dados_todos = []

    for ano in anos:
        url = f"https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_{ano}.zip"
        resp = requests.get(url)
        if resp.status_code != 200:
            st.error(f"Erro ao baixar dados do ano {ano}")
            continue
        z = zipfile.ZipFile(io.BytesIO(resp.content))
        arquivos = z.namelist()

        arquivo_dre = next((a for a in arquivos if "DRE_con" in a), None)
        if not arquivo_dre:
            arquivo_dre = next((a for a in arquivos if "DRE_ind" in a), None)
        if arquivo_dre:
            with z.open(arquivo_dre) as f:
                dre = pd.read_csv(f, sep=";", decimal=",", encoding="latin1")
            dre_empresa = dre[dre["DENOM_CIA"].str.contains(
                empresa, case=False, na=False)]
            if not dre_empresa.empty:
                for idx, row in dre_empresa.iterrows():
                    dados_todos.append({
                        "Ano": ano,
                        "Indicador": row["DS_CONTA"],
                        "Valor": row["VL_CONTA"]
                    })

        arquivo_dmpl = next((a for a in arquivos if "DMPL_con" in a), None)
        if not arquivo_dmpl:
            arquivo_dmpl = next((a for a in arquivos if "DMPL_ind" in a), None)
        if arquivo_dmpl:
            with z.open(arquivo_dmpl) as f:
                dmpl = pd.read_csv(f, sep=";", decimal=",", encoding="latin1")
            dmpl_empresa = dmpl[dmpl["DENOM_CIA"].str.contains(
                empresa, case=False, na=False)]
            if not dmpl_empresa.empty:
                for idx, row in dmpl_empresa.iterrows():
                    dados_todos.append({
                        "Ano": ano,
                        "Indicador": row["DS_CONTA"],
                        "Valor": row["VL_CONTA"]
                    })

    if dados_todos:
        df_plot = pd.DataFrame(dados_todos)

        # Forçar valor numérico
        df_plot["Valor"] = pd.to_numeric(df_plot["Valor"], errors="coerce")

        # Agrupar por Ano e Indicador para evitar duplicatas
        df_plot_agg = df_plot.groupby(["Ano", "Indicador"], as_index=False)[
            "Valor"].sum()

        df_plot_agg["Valor"] = df_plot_agg["Valor"].fillna(0).astype(int)
        mask = (
            df_plot_agg["Indicador"].str.contains("LUCRO", case=False, na=False) |
            df_plot_agg["Indicador"].str.contains("despesas", case=False, na=False) |
            df_plot_agg["Indicador"].str.contains(
                "saldos", case=False, na=False) |
            df_plot_agg["Indicador"].str.contains(
                "dividendos", case=False, na=False)
        )

        df_plot_agg_filtrado = df_plot_agg[mask]
        st.subheader("📑 Dados Extraídos")
        st.dataframe(
            df_plot_agg.pivot(
                index="Ano", columns="Indicador", values="Valor"),
            use_container_width=True
        )

        st.subheader("📈 Evolução ao longo dos anos")
        fig = px.line(
            df_plot_agg_filtrado,
            x="Ano",
            y="Valor",
            color="Indicador",
            markers=True,
            labels={"Valor": "Valor", "Indicador": "Indicador"},
            title=f"Evolução Financeira de {empresa}",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado. Tente outros anos ou outra empresa.")
