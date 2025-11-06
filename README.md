# 🚀 Portfolio Streamlit

Um conjunto de aplicações interativas desenvolvidas em **Python + Streamlit**, com foco em **análise de dados**, **visualização interativa** e **automação de insights**.

Cada aplicação dentro deste repositório é independente e tem seu próprio propósito, documentação e scripts de execução.  
O objetivo é demonstrar o uso de **ciência de dados aplicada** em cenários do dia a dia — desde análise de conversas do WhatsApp até projeções financeiras.

---

## 🧭 Estrutura do Repositório

```

portfolio_streamlit/
│
├── consult_fipe_cars_app/                 # Consulta interativa de preços FIPE
├── consulta_inmet_dados_historicos_app/   # Dados meteorológicos do INMET
├── investments_projection_app/            # Simulador e dashboard financeiro
└── whatsapp_metricas_app/                 # Análise de conversas do WhatsApp

````

Cada pasta contém:
- Um aplicativo principal (`.py`) desenvolvido em **Streamlit**  
- Um diretório `scripts/` com os **instaladores, dependências e inicializadores**
- Um `.streamlit/config.toml` para personalização visual
- Seu próprio `README.md` explicando uso e funcionalidades específicas

---

## 💡 Aplicações Incluídas

### 📊 **WhatsApp Métricas App**
Analisa conversas exportadas do WhatsApp e transforma em gráficos e insights.
- Contagem de mensagens por autor, horário e dia da semana  
- Nuvem de palavras e emojis mais usados  
- Exportação dos dados em CSV  

📂 Pasta: `whatsapp_metricas_app/`

---

### 🚗 **Consulta FIPE Carros**
Interface simples para buscar valores de veículos diretamente da **tabela FIPE**.
- Consulta interativa por marca, modelo e ano  
- Atualização dinâmica dos dados  
- Download em CSV  

📂 Pasta: `consult_fipe_cars_app/`

---

### 🌦️ **Consulta INMET — Dados Históricos**
Explora dados climáticos do **Instituto Nacional de Meteorologia (INMET)**.  
Permite filtrar e visualizar temperaturas, chuvas e outras variáveis por cidade e período.

📂 Pasta: `consulta_inmet_dados_historicos_app/`

---

### 💰 **Investments Projection App**
Simula e projeta investimentos com base em taxas **CDI**, **Selic** e parâmetros personalizados.  
Inclui também um **chatbot** para responder perguntas sobre finanças.

📂 Pasta: `investments_projection_app/`

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função Principal |
|-------------|------------------|
| [Python](https://www.python.org/) | Linguagem base |
| [Streamlit](https://streamlit.io/) | Criação de interfaces web |
| [Pandas](https://pandas.pydata.org/) | Manipulação e análise de dados |
| [Plotly](https://plotly.com/python/) | Visualização de dados interativa |
| [Matplotlib](https://matplotlib.org/) | Suporte a gráficos estáticos |
| [WordCloud](https://amueller.github.io/word_cloud/) | Visualização textual |
| [Requests](https://docs.python-requests.org/) | Comunicação com APIs externas |

---

## 📦 Como Executar um Projeto

Cada subpasta contém scripts para instalação e execução.  
Exemplo com o app do WhatsApp:

```bash
git clone https://github.com/felippesantos00/portfolio_streamlit.git
cd portfolio_streamlit/whatsapp_metricas_app/scripts
bash install.sh
source env_whatsapp_metricas_app/Scripts/activate
bash start.sh
````

O aplicativo abrirá automaticamente no navegador em:
👉 [http://localhost:8501](http://localhost:8501)

---

## 🚀 Objetivo do Repositório

Este repositório serve como **portfólio prático** para:

* Demonstrar aplicações reais de **análise de dados e dashboards**
* Mostrar domínio de bibliotecas populares do ecossistema Python
* Explorar **automação e visualização interativa** de forma acessível

---

## 👨‍💻 Autor

**Felippe Santos**
💡 Desenvolvedor Python | Data Enthusiast | Criador de soluções com Streamlit
📫 [GitHub](https://github.com/felippesantos00) | [LinkedIn](https://www.linkedin.com/in/felippesantos00)

---

## Licença

Distribuído sob a licença **MIT** — utilize, aprenda e contribua!