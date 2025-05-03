import streamlit as st
import pandas as pd
from pycaret.classification import load_model, predict_model

def roda_csv(file):
    # carrega CSV
    Xtest = pd.read_csv(file)

    # carrega modelo
    mdl_rf = load_model('./pickle/pickle_rf_pycaret')

    # faz predição
    ypred = predict_model(mdl_rf, data=Xtest, raw_score=True)

    # mostra dados
    with st.expander('Visualizar CSV carregado:', expanded=False):
        c1, _ = st.columns([2,4])
        qtd = c1.slider(
            'Visualizar quantas linhas do CSV:',
            min_value=5,
            max_value=Xtest.shape[0],
            step=10,
            value=5
        )
        st.dataframe(Xtest.head(qtd))

    # mostra predições
    with st.expander('Visualizar Predições:', expanded=True):
        c1, _, c2, c3 = st.columns([.5,.1,.2,.2])
        threshold = c1.slider(
            'Threshold (ponto de corte para considerar predição como True)',
            min_value=0.0,
            max_value=1.0,
            step=.1,
            value=.5
        )
        qtd_true = ypred.loc[ypred['prediction_score_1'] > threshold].shape[0]
        c2.metric('Qtd clientes True', value=qtd_true)
        c3.metric('Qtd clientes False', value=len(ypred) - qtd_true)

        def color_pred(val):
            color = 'olive' if val > threshold else 'orangered'
            return f'background-color: {color}'

        view_type = st.radio('', ('Completo', 'Apenas predições'))
        if view_type == 'Completo':
            df_view = ypred.copy()
        else:
            df_view = pd.DataFrame(ypred.iloc[:, -1].copy())

        st.dataframe(df_view.style.applymap(color_pred, subset=['prediction_score_1']))

        csv = df_view.to_csv(sep=';', decimal=',', index=True)
        st.markdown(f'Shape do CSV a ser baixado: {df_view.shape}')
        st.download_button(
            label='Download CSV',
            data=csv,
            file_name='Predicoes.csv',
            mime='text/csv'
        )
