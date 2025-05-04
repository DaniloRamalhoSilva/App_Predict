import streamlit as st
import pandas as pd
from pycaret.classification import load_model, predict_model
import matplotlib.pyplot as plt

def roda_csv(file):
    # --- Lê o CSV enviado ---
    Xtest = pd.read_csv(file)

    # --- Carrega o modelo treinado ---
    mdl_rf = load_model('./pickle/pickle_rf_pycaret')

    # --- Gera predições com score bruto para a classe 1 ---
    ypred = predict_model(mdl_rf, data=Xtest, raw_score=True)

    # --- Expander: mostra CSV original ---
    with st.expander('Visualizar CSV carregado:', expanded=False):
        c1, _ = st.columns([2, 4])
        qtd = c1.slider(
            'Quantas linhas mostrar?',
            min_value=5,
            max_value=Xtest.shape[0],
            step=10,
            value=5
        )
        st.dataframe(Xtest.head(qtd))

    # --- Seção de Predições (slider + métricas) ---
    st.markdown("## Predições")
    c1, _, c2, c3 = st.columns([0.5, 0.1, 0.2, 0.2])
    threshold = c1.slider(
        'Threshold (corte para predição = 1)',
        min_value=0.0,
        max_value=1.0,
        step=0.01,
        value=st.session_state.get("threshold", 0.5)
    )
    st.session_state["threshold"] = threshold

    qtd_true = int((ypred['prediction_score_1'] >= threshold).sum())
    c2.metric('Qtd clientes = 1', qtd_true)
    c3.metric('Qtd clientes = 0', len(ypred) - qtd_true)

    # --- DataFrame com a classe final ---
    df_pred = ypred.copy()
    df_pred['pred_class'] = (df_pred['prediction_score_1'] >= threshold).astype(int)

    def highlight_score(val):
        color = 'olive' if val >= threshold else 'orangered'
        return f'background-color: {color}'

    # --- Abas de Dados e Analytics ---
    tab_dados, tab_analytics = st.tabs(['Dados', 'Analytics'])

    # Aba "Dados"
    with tab_dados:
        st.markdown(f"#### Resultados (threshold = {threshold:.2f})")
        view_type = st.radio('', ('Completo', 'Só predições'))
        if view_type == 'Completo':
            df_view = df_pred.copy()
        else:
            df_view = df_pred[['Label', 'prediction_score_1', 'pred_class']]

        st.dataframe(
            df_view.style.applymap(highlight_score, subset=['prediction_score_1'])
        )

        csv = df_view.to_csv(sep=';', decimal=',', index=True)
        st.download_button(
            'Download CSV',
            data=csv,
            file_name='Predicoes.csv',
            mime='text/csv'
        )

    # Aba "Analytics"
    with tab_analytics:
        st.markdown("### Análise de Distribuições por Grupo de Features")

        # Definição dos grupos de features
        feature_groups = {
            "Campanhas": [
                "AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3",
                "AcceptedCmp4", "AcceptedCmp5", "Complain"
            ],
            "Dados Pessoais": [
                "Age", "Kidhome", "Teenhome",
                "Income", "Time_Customer"
            ],
            "Perfil de Gastos": [
                "MntFishProducts", "MntFruits", "MntGoldProds",
                "MntMeatProducts", "MntSweetProducts", "MntWines"
            ],
            "Compras e Promoções": [
                "NumCatalogPurchases", "NumDealsPurchases",
                "NumStorePurchases", "NumWebPurchases",
                "NumWebVisitsMonth", "Recency"
            ]
        }

        # Para cada grupo, cria um expander
        for group_name, feats in feature_groups.items():
            with st.expander(group_name, expanded=False):
                # filtra apenas as features numéricas existentes
                available_feats = [
                    f for f in feats
                    if f in df_pred.select_dtypes(include='number').columns
                ]

                for feat in available_feats:
                    st.write(f"**{feat}**")
                    # Cria dois espaços lado a lado
                    col1, col2 = st.columns(2)

                    # Boxplot na coluna 1
                    with col1:
                        fig, ax = plt.subplots()
                        ax.boxplot(
                            [df_pred.loc[df_pred.pred_class == cls, feat] for cls in [0, 1]],
                            labels=['Classe 0', 'Classe 1']
                        )
                        ax.set_ylabel(feat)
                        ax.set_xlabel('Classe predita')
                        ax.set_title(f'Boxplot de {feat}')
                        st.pyplot(fig)
                        plt.close(fig)

                    # Histograma na coluna 2
                    with col2:
                        fig2, ax2 = plt.subplots()
                        ax2.hist(
                            df_pred.loc[df_pred.pred_class == 0, feat],
                            bins=30, alpha=0.6, label='Classe 0'
                        )
                        ax2.hist(
                            df_pred.loc[df_pred.pred_class == 1, feat],
                            bins=30, alpha=0.6, label='Classe 1'
                        )
                        ax2.set_xlabel(feat)
                        ax2.set_ylabel('Frequência')
                        ax2.set_title(f'Histograma de {feat}')
                        ax2.legend()
                        st.pyplot(fig2)
                        plt.close(fig2)
