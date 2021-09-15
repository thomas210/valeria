import streamlit as st
import pickle
import pandas as pd

cols = [
    "FEBRE", "MIALGIA", "CEFALEIA", "EXANTEMA", "NAUSEA", "DOR_COSTAS",
    "CONJUNTVIT", "ARTRITE", "ARTRALGIA", "PETEQUIA_N", "DOR_RETRO",
    "DIABETES", "HIPERTENSA", "DIAS"
]

def app():

    st.write("# Treinamento do Modelo")

    st.write("O modelo foi treinado com dados de pacientes reais das doenças listadas, durante o treinamento alguns atributos se tornaram mais relevantes que outros, abaixo é possível conferir a importância de cada atributo durante o treinamento")

    with open('gradient_model.pkl', 'rb') as f:
        model = pickle.load(f)

    chart = pd.DataFrame(model.feature_importances_, index=cols, columns=["Nível de Importância"])

    st.bar_chart(chart)