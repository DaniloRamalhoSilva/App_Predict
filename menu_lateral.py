import streamlit as st

def configura_sidebar():
    st.sidebar.write('teste sidebar')
    with st.sidebar:
        c1, c2 = st.columns([.3, .7])
        c1.image('./images/logo_fiap.png', width=100)
        c2.write('')
        c2.subheader('Auto ML - Fiap [v1]')

        db = st.radio(
            'Fonte dos dados de entrada (X):',
            ('CSV', 'Online'),
            horizontal=True
        )

        file = None
        if db == 'CSV':
            st.info('Upload do CSV')
            file = st.file_uploader('Selecione o arquivo CSV', type='csv')

    return db, file
