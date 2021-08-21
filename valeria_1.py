import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import time
import base64

st.set_page_config(page_title="VALERIA", page_icon="val_temp.png")

pages = ["Início", "Diagnóstico", "Casos", "Sobre"]

st.sidebar.image("val_temp.png", use_column_width=True)

pagina = st.sidebar.selectbox(
    "Escolha uma opção",
    pages
)

if (pagina == "Início"):

    st.write("# Bem Vindo!")

    st.write("---")

    st.write("### Eu sou a Valéria, a sua assistente para o diagnóstico rápido de Dengue e Chikungunya!")

    st.write("### Sou um acrônimo para *Virtual Assistant for LEarning pRocesses In Arbovirus*!")

    st.write("Aqui, o nosso objetivo é auxiliar os profisionais de saúde para ter mais confiança no diagnóstico inicial dos pacientes. Espero que possamos trabalhar bem juntos!")

    st.write("---")

    st.write("Para realizar o seu diagnóstico inicial, acesse a barra de menu no canto esquerdo e escolha a opção **Diagnóstico**")

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

        st.write ("Informe os sintomas:")

        FEBRE = Checkbox(st.checkbox("Febre"))

        MIALGIA = Checkbox(st.checkbox("Mialgia", help="Dor muscular"))

        CEFALEIA = Checkbox(st.checkbox("Cefaleia", help="Dor de cabeça"))

        EXANTEMA = Checkbox(st.checkbox("Exantema", help="Manchas vermelhas em um região"))

        NAUSEA = Checkbox(st.checkbox("Náusea"))

        DOR_COSTAS = Checkbox(st.checkbox("Dor nas costas"))

        CONJUNTVIT = Checkbox(st.checkbox("Conjutivite"))

        ARTRITE = Checkbox(st.checkbox("Artrite", help="Inflamação das articulações"))

        ARTRALGIA = Checkbox(st.checkbox("Artralgia", help="Dor nas articulações"))

        PETEQUIA_N = Checkbox(st.checkbox("Petéquias", help="Pequenas manchas vermelhas ou marrom que surgem geralmente aglomeradas, mais frequentemente nos braços, pernas ou barriga"))

        DOR_RETRO = Checkbox(st.checkbox("Dor Retroorbital", help="Dor ao redor dos olhos"))

        DIABETES = Checkbox(st.checkbox("Diabetes", help=""))

        HIPERTENSA = Checkbox(st.checkbox("Hipertensão", help=""))

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
            doencas_texto = ["Chikungunya", "Dengue", "Inconclusivo"]

            for count, value in enumerate(doencas):
                if (value == doenca):
                    d = doencas_texto[count]
                    p = prob[0][count]
            st.write(f'O resultado do diagnóstico foi **{d}**')

            res_df = pd.DataFrame(prob, columns=doencas_texto, index=["Probabilidade"])

            df_style = res_df.style.format(
                {'Dengue':'{:.2%}',
                'Chikungunya':'{:.2%}',
                'Inconclusivo':'{:.2%}'}
            )


            st.write("Abaixo é possível obersar o resultados detalhado do diagnóstico:")
            st.dataframe(df_style)

            st.write("**AVISO: Este diagnóstico não substitui a avaliação médica, procure o postinho mais próximo!**")

elif (pagina == "Casos"):

    st.write("Abaixo você pode analisar a quantidade de casos de Dengue e Chikungunya no Brasil com o passar dos anos, bem como a quantidade de casos suspeitos/inclonclusivos dessas doenças")

    """### Quantidade de casos de Dengue entre 2013 e 2020"""
    file_ = open("dengue.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="gif">',
        unsafe_allow_html=True,
    )

    """### Quantidade de casos de Chikungunya entre 2015 e 2020"""
    file_ = open("chika.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="gif">',
        unsafe_allow_html=True,
    )

    """### Quantidade de casos suspeitos/inclonclusivos entre 2013 e 2020"""
    file_ = open("outros.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="gif">',
        unsafe_allow_html=True,
    )

    st.write("---")

    st.write("Dados coletados no Sistema de Informação de Agravos de Notificação (SINAN)")

elif (pagina == "Sobre"):

    st.write("## Realização")

    col_1, dotlab_col, col_3 = st.columns(3)

    dotlab_col.image("DotLab.png")

    st.write("## Apoio")

    upe_col, fmt_col = st.columns(2)
    upe_col.image("upe.png", use_column_width=True)
    fmt_col.image("fmt.png")

    st.write("## Financiamento")

    facepe_col, fapeam_col = st.columns(2)
    facepe_col.image("facepe.png")
    fapeam_col.image("fapeam.png")

    st.balloons()