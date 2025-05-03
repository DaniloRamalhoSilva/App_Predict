import streamlit as st
from menu_lateral import configura_sidebar
from simulador_csv import roda_csv
from simulador_online import roda_online

st.set_page_config(
    page_title='Simulador - Case Ifood',
    page_icon='./images/logo_fiap.png',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.title('Simulador - Conversão de Vendas')
with st.expander('Descrição do App', expanded=False):
    st.write('O objetivo principal deste app .....')

# obtém escolha de fonte e, se CSV, o arquivo
database, file = configura_sidebar()

# encaminha para o simulador apropriado
if database == 'CSV':
    if file:
        roda_csv(file)
    else:
        st.warning('Arquivo CSV não foi carregado')
else:
    roda_online()
