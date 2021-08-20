import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import time

st.write("# V.A.L.E.R.I.A")

st.write("Vamos lá")

pages = ["Home", "Diagnóstico", "Sobre"]

st.sidebar.image("val_temp.png", use_column_width=True)

pagina = st.sidebar.selectbox(
    "Escolha uma opção",
    pages
)

if (pagina == "Home"):

    st.write("# Bem Vindo!")

    st.write("---")

    st.write("### Eu sou a Valéria, a sua assistente para o diagnóstico rápido de Dengue e Chikungunya! Sou um acrônimo para *Virtual Assistant for LEarning pRocesses In Arbovirus*!")

    st.write("Aqui, o nosso objetivo é auxiliar os profisionais de saúde para ter mais confiança na execução inicial das atividades. Espero que possamos trabalhar bem juntos!")

    labels = ["Suspeitos", "Confirmados"]
    dengue_casos = [1317746, 1008013]
    chika_casos = [63368, 39634]

    fig_dengue, ax_dengue = plt.subplots()
    ax_dengue.pie(dengue_casos, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title("Casos de Dengue nas Américas em 2020")
    ax_dengue.axis('equal')

    fig_chika, ax_chika = plt.subplots()
    ax_chika.pie(chika_casos, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title("Casos de Chikungunya nas Américas em 2020")
    ax_chika.axis('equal')

    st.write("A confirmação de casos das arboviroses é um problema presente em todas as Américas. Como é possível observar nos gráficos abaixo, a taxa de confirmação dos casos está abaixo de 50%.")

    st.pyplot(fig_dengue, clear_figure=True)

    st.pyplot(fig_chika)

elif (pagina == "Diagnóstico"):

    class Checkbox:
        def __init__(self, value):
            self.value = value
        def getValue(self):
            if (self.value):
                res = 1
            else:
                res = 2
            return res

    st.write("## Preencha os campos com as informações para realizar o diagnóstico:")

    with st.form("diagnostico"):

        DIAS = st.number_input("Quantos dias está sentindo os sintomas?", min_value=0, format="%d")

        FEBRE = Checkbox(st.checkbox("Febre?"))

        MIALGIA = Checkbox(st.checkbox("Mialgia?"))

        CEFALEIA = Checkbox(st.checkbox("Cefaleia?"))

        EXANTEMA = Checkbox(st.checkbox("Exantema?"))

        NAUSEA = Checkbox(st.checkbox("Náusea?"))

        DOR_COSTAS = Checkbox(st.checkbox("Dor nas costas?"))

        CONJUNTVIT = Checkbox(st.checkbox("Conjutivite?"))

        ARTRITE = Checkbox(st.checkbox("Artrite?"))

        ARTRALGIA = Checkbox(st.checkbox("Artralgia?"))

        PETEQUIA_N = Checkbox(st.checkbox("Petéquias?"))

        DOR_RETRO = Checkbox(st.checkbox("Dor ao redor dos olhos?"))

        DIABETES = Checkbox(st.checkbox("Diabetes?"))

        HIPERTENSA = Checkbox(st.checkbox("Hipertensão?"))

        if (st.form_submit_button("Realizar Diagnóstico")):

            header = [
                "FEBRE", "MIALGIA", "CEFALEIA", "EXANTEMA", "NAUSEA", "DOR_COSTAS",
                "CONJUNTVIT", "ARTRITE", "ARTRALGIA", "PETEQUIA_N", "DOR_RETRO",
                "DIABETES", "HIPERTENSA", "DIAS"
            ]

            dados = []

            dados.append([
                FEBRE.getValue(), MIALGIA.getValue(), CEFALEIA.getValue(),
                EXANTEMA.getValue(), NAUSEA.getValue(), DOR_COSTAS.getValue(),
                CONJUNTVIT.getValue(), ARTRITE.getValue(), ARTRALGIA.getValue(),
                PETEQUIA_N.getValue(), DOR_RETRO.getValue(),
                DIABETES.getValue(), HIPERTENSA.getValue(), DIAS
            ]) 

            with open('gradient_model.pkl', 'rb') as f:
                model = pickle.load(f)
                doenca = model.predict(dados)[0]
                prob = model.predict_proba(dados)

            doencas = ["CHIKUNGUNYA", "DENGUE", "OUTRAS_DOENCAS"]
            doencas_texto = ["Chikungunya", "Dengue", "Negativo"]

            for count, value in enumerate(doencas):
                if (value == doenca):
                    d = doencas_texto[count]
                    p = prob[0][count]
            st.write(f'O resultado do diagnóstico foi {d} com uma taxa de confiança de {p:.2%}')

elif (pagina == "Sobre"):

    st.write("Este Sistema foi desenvolvido pelo grupo de Pesquisa DotLAB Brasil!")

    st.image("DotLab.png")