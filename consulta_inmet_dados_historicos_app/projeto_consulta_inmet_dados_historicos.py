import requests
import pandas as pd
import os
from datetime import datetime
import streamlit as st


@st.cache_data
def get_dados():
    baseurl = "https://portal.inmet.gov.br/uploads/dadoshistoricos"
    urls = [
        f"{baseurl}/{x}.zip" for x in range(2000, int(datetime.now().strftime("%Y"))+1)]
    print(urls)
    if not os.path.exists("inputs"):
        os.makedirs("inputs")
        print(f"Diretorio criado: inputs")
    for url in urls:
        filename = url.split("/")[-1]
        file_path = os.path.join("inputs", filename)
        if os.path.isfile(file_path):
            print(f"Arquivo já existe")
            continue
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Download completo")
        except requests.exceptions.RequestException as e:
            print(f"Erro no download: {e}")
        except IOError as e:
            print(f"Erro ao salvar arquivo: {e}")


# get_dados()
year_start, year_end = st.select_slider("Ano", options=list(
    [x for x in range(2000, 2026)]), value=(2000, 2025))
st.write(f"year_start: {year_start}, year_end: {year_end}")
files=[f"{file}.zip" for file in range(2000, 2026)
         if file >= year_start and file <= year_end]

# , 2000, int(datetime.now().strftime("%Y")))
