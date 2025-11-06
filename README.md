# 📊 WhatsApp Métricas App

Aplicação desenvolvida em **Streamlit** para análise e visualização de métricas de conversas do **WhatsApp**.  
O projeto faz parte do portfólio de aplicações desenvolvidas para demonstrar habilidades em **análise de dados**, **automação** e **visualização interativa** com **Python**.

---

## 🚀 Objetivo

O **WhatsApp Métricas App** permite importar e processar exportações de conversas do WhatsApp, extraindo métricas úteis como:

- Quantidade de mensagens por participante  
- Horários e dias mais ativos  
- Emojis e palavras mais utilizadas  
- Visualizações gráficas de engajamento  

A ideia é transformar simples históricos de conversas em **insights interativos**, úteis para estudos de comportamento, produtividade e comunicação.

---

## 🧩 Estrutura do Projeto

```

whatsapp_metricas_app/
│
├── .streamlit/
│   └── config.toml                # Configuração visual do Streamlit (tema, layout etc.)
│
├── projeto_metricas_whatsapp.py   # Código principal da aplicação
├── readme.md                      # Descrição e instruções do projeto
│
└── scripts/
├── install.sh                 # Script de instalação dos requisitos
├── requirements.txt           # Lista de dependências do Python
└── start.sh                   # Script para inicializar o aplicativo

````

---

## 🧠 Tecnologias Utilizadas

- **Python 3.9+**
- **Streamlit**
- **Pandas**
- **Matplotlib / Plotly**
- **Numpy**
- **Emoji / Regex (para análise textual)**

---

## ⚙️ Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/felippesantos00/portfolio_streamlit.git
cd portfolio_streamlit/whatsapp_metricas_app
````

### 2. Crie o ambiente virtual

```bash
python -m venv env_whatsapp_metricas_app
source env_whatsapp_metricas_app/bin/activate      # Linux / Mac
env_whatsapp_metricas_app\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install -r scripts/requirements.txt
```

ou use o script pronto:

```bash
bash scripts/install.sh
```

### 4. Execute o aplicativo

```bash
streamlit run projeto_metricas_whatsapp.py
```

ou

```bash
bash scripts/start.sh
```

O app será iniciado em:

👉 [http://localhost:8501](http://localhost:8501)

---

## 📈 Exemplos de Métricas

* Top 10 participantes mais ativos
* Frequência de mensagens por dia da semana
* Padrões de envio (horário mais comum)
* Emojis mais utilizados
* Evolução de mensagens ao longo do tempo

---

## 🧩 Próximos Passos

* Adicionar exportação de gráficos em PDF/PNG
* Criar painel de comparação entre grupos
* Implementar análise de sentimento (NLP)

---

## 👨‍💻 Autor

**Felippe Santos**
Desenvolvedor Python e entusiasta em automação e análise de dados.
📫 [LinkedIn](https://www.linkedin.com/in/felippesantos00) | [GitHub](https://github.com/felippesantos00)

---

## Licença

Este projeto está sob a licença **MIT** — sinta-se à vontade para usar e adaptar.