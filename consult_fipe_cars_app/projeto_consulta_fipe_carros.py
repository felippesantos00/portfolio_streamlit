import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from time import sleep

# ----------------------------
# Configuração da página
# ----------------------------
st.set_page_config(page_title="Consulta FIPE", layout="wide")
st.title("Consulta FIPE de Veículos")

# ----------------------------
# Função para obter tabela FIPE mais recente
# ----------------------------


@st.cache_data(ttl=3600)
def get_tabelas():
    """Retorna todas as tabelas de referência disponíveis na FIPE (mais recente primeiro)."""
    url = "https://veiculos.fipe.org.br/api/veiculos/ConsultarTabelaDeReferencia"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.post(url, headers=headers)
    return pd.DataFrame(r.json())


@st.cache_data(ttl=3600)
def tabela_atual_fipe():
    """Retorna o código da tabela mais recente disponível na FIPE."""
    tabelas = get_tabelas()
    return int(tabelas.iloc[0]["Codigo"])  # mais recente

# ----------------------------
# Função para verificar se a FIPE está online
# ----------------------------


@st.cache_data(ttl=3600)
def verificar_fipe():
    """Testa se o endpoint de marcas da FIPE está respondendo."""
    try:
        payload = {"codigoTabelaReferencia": str(
            tabela_atual_fipe()), "codigoTipoVeiculo": "1"}
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                   "X-Requested-With": "XMLHttpRequest",
                   "User-Agent": "Mozilla/5.0"}
        r = requests.post("https://veiculos.fipe.org.br/api/veiculos/ConsultarMarcas",
                          data=payload, headers=headers, timeout=5)
        return r.status_code == 200 and bool(r.json())
    except:
        return False

# ----------------------------
# Funções auxiliares FIPE
# ----------------------------


@st.cache_data(ttl=3600)
def get_marcas():
    url = "https://veiculos.fipe.org.br/api/veiculos/ConsultarMarcas"
    payload = {"codigoTabelaReferencia": str(
        tabela_atual_fipe()), "codigoTipoVeiculo": "1"}
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "X-Requested-With": "XMLHttpRequest",
               "User-Agent": "Mozilla/5.0"}
    r = requests.post(url, data=payload, headers=headers)
    return pd.DataFrame(r.json())


@st.cache_data(ttl=3600)
def get_modelos(codigo_marca):
    url = "https://veiculos.fipe.org.br/api/veiculos/ConsultarModelos"
    payload = {"codigoTabelaReferencia": str(tabela_atual_fipe()),
               "codigoTipoVeiculo": "1", "codigoMarca": str(codigo_marca)}
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "X-Requested-With": "XMLHttpRequest",
               "User-Agent": "Mozilla/5.0"}
    r = requests.post(url, data=payload, headers=headers)
    modelos = r.json().get('Modelos', [])
    return pd.DataFrame(modelos)


@st.cache_data(ttl=3600)
def get_anos(codigo_marca, codigo_modelo):
    url = "https://veiculos.fipe.org.br/api/veiculos/ConsultarAnoModelo"
    payload = {"codigoTabelaReferencia": str(tabela_atual_fipe()), "codigoMarca": str(codigo_marca),
               "codigoModelo": str(codigo_modelo), "codigoTipoVeiculo": "1"}
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "X-Requested-With": "XMLHttpRequest",
               "User-Agent": "Mozilla/5.0"}
    r = requests.post(url, data=payload, headers=headers)
    return pd.DataFrame(r.json())


# ----------------------------
# Verificação inicial
# ----------------------------
if not verificar_fipe():
    st.error(
        "⚠ O sistema FIPE está fora do ar ou inacessível no momento. Tente novamente mais tarde.")
    st.stop()

# ----------------------------
# Seleção de Marca, Modelo, Ano e Combustível
# ----------------------------
marcas_df = get_marcas()
marca_dict = dict(zip(marcas_df['Label'], marcas_df['Value']))
marca_selecionada = st.selectbox("Selecione a marca", list(marca_dict.keys()))

modelos_df = get_modelos(marca_dict[marca_selecionada])
modelo_dict = dict(zip(modelos_df['Label'], modelos_df['Value']))
modelo_selecionado = st.selectbox(
    "Selecione o modelo", list(modelo_dict.keys()))

anos_df = get_anos(marca_dict[marca_selecionada],
                   modelo_dict[modelo_selecionado])
ano_dict = dict(zip(anos_df['Label'], anos_df['Value']))
ano_selecionado = st.selectbox("Selecione o ano", list(ano_dict.keys()))

combustiveis = {
    "Gasolina": 1,
    "Álcool": 2,
    "Diesel": 3,
    "Flex (Gasolina + Álcool)": 5,
    "Gás Natural": 7,
    "Elétrico": 9
}
combustivel_selecionado = st.selectbox(
    "Tipo de combustível", list(combustiveis.keys()))
tabelas_df = get_tabelas()
tabelas_referencia = tabelas_df["Codigo"].astype(
    int).tolist()  # todos os códigos disponíveis
meses_selecionados = st.number_input(
    "Escolha Quantidade de meses", 1, tabelas_referencia[0])
# ----------------------------
# Botão para buscar valores FIPE
# ----------------------------
if st.button("Buscar valores FIPE"):
    st.info("Buscando valores FIPE. Isso pode levar alguns segundos...")
    todos_dados = []
    # preferido, flex e gasolina
    combustiveis_para_tentar = [combustiveis[combustivel_selecionado], 5, 1]

    for tabela in tabelas_referencia[:meses_selecionados]:
        for combustivel in combustiveis_para_tentar:
            payload_valores = {
                "codigoTabelaReferencia": str(tabela),
                "codigoMarca": str(marca_dict[marca_selecionada]),
                "codigoModelo": str(modelo_dict[modelo_selecionado]),
                "codigoTipoVeiculo": "1",
                "anoModelo": str(ano_dict[ano_selecionado]).split("-")[0],
                "codigoTipoCombustivel": str(combustivel),
                "tipoVeiculo": "carro",
                "modeloCodigoExterno": "",
                "tipoConsulta": "tradicional"
            }
            headers_valores = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                               "X-Requested-With": "XMLHttpRequest",
                               "User-Agent": "Mozilla/5.0"}
            try:
                r = requests.post("https://veiculos.fipe.org.br/api/veiculos/ConsultarValorComTodosParametros",
                                  data=payload_valores, headers=headers_valores, timeout=10)
                if r.status_code == 200 and r.text.strip():
                    dados = r.json()
                    if dados.get('Valor') and dados.get('MesReferencia'):
                        todos_dados.append(dados)
                        sleep(0.3)
            except Exception as e:
                st.warning(
                    f"Erro ao consultar tabela {tabela} e combustível {combustivel}: {e}")
    if not todos_dados:
        st.warning("Nenhum dado FIPE disponível para os parâmetros selecionados.")
    else:
        df = pd.DataFrame(todos_dados)
        df['Valor'] = df['Valor'].str.replace(
            'R\$ ', '', regex=True).str.replace(".", "").str.replace(",", ".")
        df = df.drop_duplicates(
            subset=['MesReferencia', 'Valor', 'CodigoFipe'])

        meses = {"janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4, "maio": 5, "junho": 6,
                 "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}

        def converte_mes(x: str) -> pd.Timestamp:
            try:
                partes = x.lower().split()
                return pd.Timestamp(year=int(partes[2]), month=meses[partes[0]], day=1)
            except Exception:
                return pd.NaT

        df['Mes'] = df['MesReferencia'].map(converte_mes)
        df = df.dropna(subset=['Mes']).sort_values('Mes')

        st.write(f"Quantidade de linhas: {len(df)}")
        fig = px.line(df, x='Mes', y='Valor', markers=True,
                      title=f'Valores FIPE de {marca_selecionada} {modelo_selecionado} {ano_selecionado}',
                      labels={'Mes': 'Mês', 'Valor': 'Valor (R$)'}, hover_data={'Valor': ':,.2f'})
        st.plotly_chart(fig, use_container_width=True)
