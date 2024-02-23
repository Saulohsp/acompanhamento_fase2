import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pygsheets
import os

# Autenticação e leitura da planilha
credenciais = pygsheets.authorize(service_file=os.getcwd() + "/cred.json")
link_google_sheets = "https://docs.google.com/spreadsheets/d/1WOXcj67pbfOoKxij4BDPWzQee7zt2r5LKiFhe67lOEk/edit#gid=0"
arquivo = credenciais.open_by_url(link_google_sheets)

# Aba_insumos_ppq1
aba_insumos_ppq1 = arquivo.worksheet_by_title("insumosPPQ1")
data_ppq1 = aba_insumos_ppq1.get_all_values()
header_ppq1 = data_ppq1[0]  
df_ppq1 = pd.DataFrame(data_ppq1[1:], columns=header_ppq1)  

# Aba_insumos_ppq2
aba_insumos_ppq2 = arquivo.worksheet_by_title("insumosPPQ2")
data_ppq2 = aba_insumos_ppq2.get_all_values()
header_ppq2 = data_ppq2[0] 
df_ppq2 = pd.DataFrame(data_ppq2[1:], columns=header_ppq2)  

st.set_page_config(
    page_title="Cronograma",
    page_icon="📦",
    layout="wide"
    )

st.title('Insumos Fase 2A - Embalagem')

# Criação das duas colunas principais
col_ppq1, col_ppq2 = st.columns(2)

# PPQ-1
with col_ppq1:
    st.header("PPQ-1")
    for index, row in df_ppq1.iterrows():
        if row['StatusPPQ1'] == 'ok':
            st.success(f'{row["InsumoPPQ1"]}')
        else:
            st.warning(f'{row["InsumoPPQ1"]}')

# PPQ-2
with col_ppq2:
    st.header("PPQ-2")
    for index, row in df_ppq2.iterrows():
        if row['StatusPPQ2'] == 'ok':
            st.success(f'{row["InsumoPPQ2"]}')
        else:
            st.warning(f'{row["InsumoPPQ2"]}')
