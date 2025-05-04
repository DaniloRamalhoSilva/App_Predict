import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI
from pycaret.classification import load_model, predict_model


def fill_test_inputs():
    defaults = {
        "AcceptedCmp1": 1,
        "AcceptedCmp2": 0,
        "AcceptedCmp3": 0,
        "AcceptedCmp4": 1,
        "AcceptedCmp5": 0,
        "Complain": 0,
        "Age": "41",
        "Education": "Graduation",
        "Marital_Status": "Together",
        "Kidhome": "1",
        "Teenhome": "0",
        "Income": "26646.00",
        "MntFishProducts": "10",
        "MntFruits": "4",
        "MntGoldProds": "5",
        "MntMeatProducts": "20",
        "MntSweetProducts": "3",
        "MntWines": "11",
        "NumCatalogPurchases": "0",
        "NumDealsPurchases": "2",
        "NumStorePurchases": "4",
        "NumWebPurchases": "2",
        "NumWebVisitsMonth": "6",
        "Recency": "26",
        "Time_Customer": "11.13",
        # threshold default
        "threshold": 0.5
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def roda_online():
    st.header("Simulador Online — Entrada Manual")
    st.write("Preencha todos os campos antes de rodar a simulação.")

    # Preenche valores de teste somente na primeira execução
    fill_test_inputs()

    # 1) Campanhas
    with st.expander("Campanhas", expanded=True):
        AcceptedCmp1 = st.selectbox(
            "Campanha Aceita 1", [None, 0, 1],
            format_func=lambda x: "Selecione…" if x is None else ("Sim" if x == 1 else "Não"),
            key="AcceptedCmp1"
        )
        AcceptedCmp2 = st.selectbox("Campanha Aceita 2", [None, 0, 1],
                                   format_func=lambda x: "Selecione…" if x is None else ("Sim" if x == 1 else "Não"),
                                   key="AcceptedCmp2")
        AcceptedCmp3 = st.selectbox("Campanha Aceita 3", [None, 0, 1],
                                   format_func=lambda x: "Selecione…" if x is None else ("Sim" if x == 1 else "Não"),
                                   key="AcceptedCmp3")
        AcceptedCmp4 = st.selectbox("Campanha Aceita 4", [None, 0, 1],
                                   format_func=lambda x: "Selecione…" if x is None else ("Sim" if x == 1 else "Não"),
                                   key="AcceptedCmp4")
        AcceptedCmp5 = st.selectbox("Campanha Aceita 5", [None, 0, 1],
                                   format_func=lambda x: "Selecione…" if x is None else ("Sim" if x == 1 else "Não"),
                                   key="AcceptedCmp5")
        Complain = st.selectbox("Fez Reclamação", [None, 0, 1],
                                format_func=lambda x: "Selecione…" if x is None else ("Sim" if x == 1 else "Não"),
                                key="Complain")

    # 2) Dados Pessoais
    with st.expander("Dados Pessoais", expanded=False):
        age_str = st.text_input("Idade", "", key="Age")
        education_map = {"Basic": "Fundamental", "Graduation": "Graduação", "Master": "Mestrado",
                         "PhD": "Doutorado", "Master & PhD": "Mestrado e Doutorado",
                         "Absurd": "Absurdo", "YOLO": "YOLO"}
        marital_map = {"Single": "Solteiro(a)", "Together": "Juntos", "Married": "Casado(a)",
                       "Divorced": "Divorciado(a)", "Widow": "Viúvo(a)", "Alone": "Sozinho(a)",
                       "Absurd": "Absurdo", "YOLO": "YOLO"}
        education = st.selectbox("Nível de Escolaridade", [None] + list(education_map.keys()),
                                 format_func=lambda x: "Selecione…" if x is None else education_map[x],
                                 key="Education")
        marital_status = st.selectbox("Estado Civil", [None] + list(marital_map.keys()),
                                      format_func=lambda x: "Selecione…" if x is None else marital_map[x],
                                      key="Marital_Status")
        kidhome_str = st.text_input("Filhos em Casa", "", key="Kidhome")
        teenhome_str = st.text_input("Adolescentes em Casa", "", key="Teenhome")
        income_str = st.text_input("Renda (R$)", "", key="Income")

    # 3) Perfil de Gastos
    with st.expander("Perfil de Gastos", expanded=False):
        fish_str = st.text_input("Gasto em Peixes", "", key="MntFishProducts")
        fruits_str = st.text_input("Gasto em Frutas", "", key="MntFruits")
        gold_str = st.text_input("Gasto em Joias de Ouro", "", key="MntGoldProds")
        meat_str = st.text_input("Gasto em Carnes", "", key="MntMeatProducts")
        sweet_str = st.text_input("Gasto em Doces", "", key="MntSweetProducts")
        wine_str = st.text_input("Gasto em Vinhos", "", key="MntWines")

    # 4) Compras e Promoções
    with st.expander("Compras e Promoções", expanded=False):
        cat_str = st.text_input("Compras por Catálogo", "", key="NumCatalogPurchases")
        deals_str = st.text_input("Compras em Promoções", "", key="NumDealsPurchases")
        store_str = st.text_input("Compras na Loja Física", "", key="NumStorePurchases")
        web_str = st.text_input("Compras Online", "", key="NumWebPurchases")
        visits_str = st.text_input("Visitas ao Site/Mês", "", key="NumWebVisitsMonth")
        recency_str = st.text_input("Dias desde Última Compra", "", key="Recency")
        time_str = st.text_input("Tempo como Cliente (anos)", "", key="Time_Customer")

    # Botão para rodar simulação
    if st.button("Rodar Simulação"):
        inputs = {k: st.session_state[k] for k in [
            "AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5",
            "Complain", "Age", "Education", "Marital_Status", "Kidhome", "Teenhome",
            "Income", "MntFishProducts", "MntFruits", "MntGoldProds", "MntMeatProducts",
            "MntSweetProducts", "MntWines", "NumCatalogPurchases", "NumDealsPurchases",
            "NumStorePurchases", "NumWebPurchases", "NumWebVisitsMonth", "Recency", "Time_Customer"
        ]}
        if any(v in (None, "") for v in inputs.values()):
            st.error("Por favor, preencha **TODOS** os campos antes de rodar.")
            return

        # Converte tipos e prediz
        df_input = pd.DataFrame([{
            **{f: int(inputs[f]) for f in ["AcceptedCmp1","AcceptedCmp2","AcceptedCmp3","AcceptedCmp4","AcceptedCmp5","Complain"]},
            **{"Age": int(inputs["Age"]), "Kidhome": int(inputs["Kidhome"]), "Teenhome": int(inputs["Teenhome"])},
            **{"Income": float(inputs["Income"])},
            **{k: int(inputs[k]) for k in ["MntFishProducts","MntFruits","MntGoldProds","MntMeatProducts","MntSweetProducts","MntWines"]},
            **{k: int(inputs[k]) for k in ["NumCatalogPurchases","NumDealsPurchases","NumStorePurchases","NumWebPurchases","NumWebVisitsMonth","Recency"]},
            "Time_Customer": float(inputs["Time_Customer"]),
            "Education": inputs["Education"], "Marital_Status": inputs["Marital_Status"]
        }])

        mdl_rf = load_model("./pickle/pickle_rf_pycaret")
        ypred = predict_model(mdl_rf, data=df_input, raw_score=True)
        prob_true = float(ypred["prediction_score_1"][0])
        st.session_state["prob_true"] = prob_true

    # Garante valor inicial de threshold
    if "threshold" not in st.session_state:
        st.session_state["threshold"] = 0.5

    # Exibe resultado e slider de threshold se já tiver simulação
    if "prob_true" in st.session_state:
        with st.expander("Resultado da Simulação", expanded=True):
            prob_true = st.session_state["prob_true"]

            # Slider agora usa key para ler/escrever direto no session_state
            threshold = st.slider(
                "Limiar para considerar como Sim",
                min_value=0.0,
                max_value=1.0,
                step=0.05,
                value=st.session_state["threshold"]
            )

            pred_label = "Sim" if prob_true >= threshold else "Não"
            st.metric("Probabilidade de Compra", f"{prob_true:.3f}")
            st.write(f"Classificação final: **{pred_label}**")

            # Campo para o usuário digitar a instrução
            user_instr = st.text_area(
                "Ajuste o limiar por instrução (ex: 'diminua o limiar para 0.3')",
                height=100
            )

            # Botão que chama a API e atualiza o threshold
            if st.button("Processar Instrução"):

                

                # atenção: OPENAI_API_KEY deve estar setada no ambiente
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                response = client.responses.create(
                    model="gpt-4o-mini",
                    instructions=(
                        "Você é um assistente que recebe uma instrução do usuário "
                        "para ajustar o valor de threshold. "
                        "Retorne APENAS um número float entre 0 e 1, sem texto adicional."
                        f"threshold atual é {threshold}"
                        f"Probabilidade dedo cliente comprar (ser sim) é de {prob_true}"
                    ),
                    input=user_instr
                )

                text = response.output_text.strip()
                try:
                    new_thr = float(text)
                    # limita entre 0 e 1
                    new_thr = max(0.0, min(1.0, new_thr))
                    st.session_state["threshold"] = new_thr
                    st.rerun()   # substitui experimental_rerun()
                except ValueError:
                    st.error("Não foi possível interpretar o valor retornado pela API")

                


                        


