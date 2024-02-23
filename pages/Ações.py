import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pygsheets
import os
import datetime

#data de hoje
data_de_hoje = datetime.date.today()

# Autenticação e leitura da planilha
credenciais = pygsheets.authorize(service_file=os.getcwd() + "/cred.json")
link_google_sheets = "https://docs.google.com/spreadsheets/d/1WOXcj67pbfOoKxij4BDPWzQee7zt2r5LKiFhe67lOEk/edit#gid=0"
arquivo = credenciais.open_by_url(link_google_sheets)

# Aba da planilha
aba = arquivo.worksheet_by_title("acoes")
data = aba.get_all_values()
header = data[0]  # Extrai a primeira linha como cabeçalho
df = pd.DataFrame(data[1:], columns=header)  # Usa o resto dos dados sem a primeira linha e define o cabeçalho

st.set_page_config(
    page_title="Ações",
    page_icon="🔄",
    layout="wide"
    )

st.title('Plano de ações')

st.header("Em andamento:")
for index, row in df.iterrows():
    due_date = datetime.datetime.strptime(row["Due date"], "%d/%m/%Y").date()
    if due_date >= data_de_hoje:
        col1, col2, col3 = st.columns([5, 1, 1])
        col1.warning(f'{row["Ação"]}')
        col2.warning(f'{row["Due date"]}')
        col3.warning(f'{row["Responsavel"]}')


st.header("Em atraso:")
for index, row in df.iterrows():
    due_date = datetime.datetime.strptime(row["Due date"], "%d/%m/%Y").date()
    if due_date < data_de_hoje:
        col1, col2, col3 = st.columns([5, 1, 1])
        col1.error(f'{row["Ação"]}')
        col2.error(f'{row["Due date"]}')
        col3.error(f'{row["Responsavel"]}')



