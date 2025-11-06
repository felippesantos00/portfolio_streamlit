# 📊 Consulta FIPE de Veículos

Aplicação interativa em **Streamlit** para consultar e visualizar a variação dos valores da **Tabela FIPE** ao longo do tempo.  
O app consome a **API oficial da FIPE**, permitindo selecionar **marca, modelo, ano e combustível** e gerar gráficos com a evolução dos preços.

---

## 🚀 Funcionalidades

- Consulta automática da **tabela FIPE mais recente**.
- Seleção de **marca, modelo e ano** diretamente no app.
- Escolha do **tipo de combustível**.
- Definição do número de meses a consultar.
- **Validação automática**: o app verifica se a API da FIPE está online antes de prosseguir.
- Geração de **gráfico interativo** com o histórico de valores usando **Plotly**.

---

## 🛠 Tecnologias Utilizadas

- [Streamlit](https://streamlit.io/) → Interface interativa
- [Requests](https://docs.python-requests.org/) → Consumo da API FIPE
- [Pandas](https://pandas.pydata.org/) → Manipulação de dados
- [Plotly Express](https://plotly.com/python/plotly-express/) → Visualização de dados
- API pública da [Tabela FIPE](https://veiculos.fipe.org.br/)

---

## 📦 Instalação

Clone este repositório:

```bash
git clone https://github.com/seu-usuario/consulta-fipe.git
cd consulta-fipe
```

Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## ▶️ Como Executar

Na raiz do projeto, execute:

```bash
streamlit run app.py
```

O navegador abrirá automaticamente em:  
👉 [http://localhost:8501](http://localhost:8501)

---

## 📊 Exemplo de Uso

1. Escolha a **marca** (ex: Honda).
2. Selecione o **modelo** (ex: HR-V).
3. Escolha o **ano** (ex: 2022).
4. Defina o **tipo de combustível**.
5. Escolha quantos meses deseja analisar.
6. Clique em **"Buscar valores FIPE"**.

O sistema exibirá:
- A quantidade de registros obtidos.
- Um gráfico interativo mostrando a evolução dos valores.

---

## ⚠️ Observações Importantes

- A API da FIPE pode ficar temporariamente indisponível; o app exibirá um aviso nesses casos.
- Alguns modelos/anos podem não ter dados para todos os meses ou tipos de combustível.
- Há pequenas pausas (`sleep`) entre as requisições para evitar bloqueios.

---

## 📜 Licença

Este projeto é de uso livre para estudos e fins não comerciais.  
Sinta-se à vontade para contribuir ou adaptar conforme necessário.
