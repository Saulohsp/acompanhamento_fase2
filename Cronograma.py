# Bibliotecas GERAIS
import streamlit as st
import pandas as pd
import pygsheets
import os
import plotly.express as px

# Autenticação e leitura da planilha
credenciais = pygsheets.authorize(service_file=os.getcwd() + "/cred.json")
link_google_sheets = "https://docs.google.com/spreadsheets/d/1WOXcj67pbfOoKxij4BDPWzQee7zt2r5LKiFhe67lOEk/edit#gid=0"
arquivo = credenciais.open_by_url(link_google_sheets)

# ABA buriti
aba_buriti = arquivo.worksheet_by_title("buriti")
data_buriti = aba_buriti.get_all_values()
header_buriti = data_buriti[0]
df_buriti = pd.DataFrame(data_buriti[1:], columns=header_buriti)  

# ABA insp_ANVISA_caminho_critico
aba_insp = arquivo.worksheet_by_title("insp_ANVISA_caminho_critico")
data_insp = aba_insp.get_all_values()
header_insp = data_insp[0]
df_insp = pd.DataFrame(data_insp[1:], columns=header_insp)  


# Layout da página
st.set_page_config(
    page_title="Cronograma",
    page_icon="📅",
    layout="wide"
    )

# Título
st.title('Cronograma Fase 2A')

# Seletor de cronograma com separador de colunas
col1, col2 = st.columns([1,3])
with col1:
    opcao_cronograma = st.selectbox(
        'Selecione a versão do cronograma que deseja visualizar',
        df_buriti.columns[1:].tolist()
    )

# Limpar os dados, mantendo apenas a coluna "Workstream" e a coluna da data selecionada
df_buriti_clean = df_buriti[['Workstream', opcao_cronograma]].copy()

# Remover linhas onde a data está faltando
df_buriti_clean.dropna(subset=[opcao_cronograma], inplace=True)

# Converter a coluna de datas para o formato de data
df_buriti_clean[opcao_cronograma] = pd.to_datetime(df_buriti_clean[opcao_cronograma], format='%d/%m/%Y')

# Converter a coluna de datas para string no formato desejado
df_buriti_clean['data_formatada'] = df_buriti_clean[opcao_cronograma].dt.strftime('%d %b %Y')

# Assegurar a ordem das workstreams conforme na planilha e usar 'data_formatada' para o texto
fig = px.bar(df_buriti_clean, y='Workstream', x=opcao_cronograma, orientation='h', 
             category_orders={'Workstream': df_buriti['Workstream'].tolist()}, 
             text='data_formatada')

# Personalizar as anotações de texto
fig.update_traces(textposition='outside')

# Melhorar a formatação do gráfico
fig.update_layout(
    title=f'Cronograma Fase 2A - {opcao_cronograma}',
    uniformtext_minsize=10, 
    uniformtext_mode='hide',
    width=1150, 
    height=700   
)

# No Streamlit, use st.plotly_chart para exibir o gráfico
st.plotly_chart(fig)

# Selecionar DATA da inspeção CTO e Caminho crítico    
seleciona_data_da_inspecao = df_insp[df_insp['cronograma'] == opcao_cronograma]
data_da_inspecao = seleciona_data_da_inspecao['Data insp'].tolist()

seleciona_caminho_critico = df_insp[df_insp['cronograma'] == opcao_cronograma]
caminho_critico = seleciona_caminho_critico['Caminho crítico'].tolist()

# Data da Inspeção e CTO
st.write(f'**Previsão para Inspeção da ANVISA:** {data_da_inspecao[0]}')
st.write(f'**Caminho crítico:** {caminho_critico[0]}')

#-------------------------------#-------------------------------#------------- COMPARAÇÃO DE CRONOGRAMAS ---------------#-------------------------------#----------------------------

# Título
st.title('Comparação de cronogramas - Fase 2A')

# Seletor de cronograma com separador de colunas
col1, col2, col3 = st.columns([1,1,2])
with col1:
    opcao_comp1 = st.selectbox(
        'Selecione a **primeira** versão do cronograma para comparar',
        df_buriti.columns[1:].tolist()
    )

with col2:
    opcao_comp2 = st.selectbox(
        'Selecione a **segunda** versão do cronograma para comparar',
        df_buriti.columns[1:].tolist()
    )

# COMPARA DOIS CRONOGRAMAS

# Verificar se as opções selecionadas são iguais
if opcao_comp1 == opcao_comp2:
    col1.warning('Selecione cronogramas diferentes.')
else:
    # Preparar os dados
    df_comp1 = df_buriti[['Workstream', opcao_comp1]].copy()
    df_comp2 = df_buriti[['Workstream', opcao_comp2]].copy()
    df_comp1.dropna(subset=[opcao_comp1], inplace=True)
    df_comp2.dropna(subset=[opcao_comp2], inplace=True)
    df_comp1[opcao_comp1] = pd.to_datetime(df_comp1[opcao_comp1], format='%d/%m/%Y')
    df_comp2[opcao_comp2] = pd.to_datetime(df_comp2[opcao_comp2], format='%d/%m/%Y')

    # Calcular a diferença em dias
    df_diff = pd.merge(df_comp1, df_comp2, on='Workstream', how='inner')
    df_diff['Diferença em Dias'] = (df_diff[opcao_comp2] - df_diff[opcao_comp1]).dt.days

    # Unir os DataFrames
    df_comp1['Tipo'] = opcao_comp1
    df_comp2['Tipo'] = opcao_comp2
    df_combined = pd.concat([df_comp1.rename(columns={opcao_comp1: 'Data'}), df_comp2.rename(columns={opcao_comp2: 'Data'})])

    # Adicionar diferença em dias para opcao_comp2
    df_combined = pd.merge(df_combined, df_diff[['Workstream', 'Diferença em Dias']], on='Workstream', how='left')

    # Definir texto para as barras
    df_combined['Texto'] = df_combined.apply(lambda x: f"{x['Data'].strftime('%d/%m/%Y')} ({'+ ' if x['Diferença em Dias'] > 0 else ''}{x['Diferença em Dias']} dias)" if pd.notnull(x['Diferença em Dias']) and x['Tipo'] == opcao_comp2 else x['Data'].strftime('%d/%m/%Y'), axis=1)

    # Criar o gráfico
    fig = px.bar(df_combined, y='Workstream', x='Data', color='Tipo', orientation='h', text='Texto',
                category_orders={'Workstream': df_buriti['Workstream'].tolist()},
                barmode='group')

    # Ajustes finais no gráfico
    fig.update_layout(
        title='Comparação dos Cronogramas',
        xaxis_title='Data',
        yaxis_title='Workstream',
        legend_title='Legenda',
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        width=1200,
        height=900
    )

    fig.update_traces(textposition='outside')

    # Exibir o gráfico
    st.plotly_chart(fig)