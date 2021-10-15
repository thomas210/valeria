import streamlit as st
from models.patient import Patient
import time

def app():

    st.write("## Preencha os campos com as informações para realizar o diagnóstico:")

    with st.form("diagnostico_form"):

        patient = Patient()

        patient.setDays(st.number_input("Quantos dias está sentindo os sintomas?", min_value=0, format="%d"))

        st.write("Informe os sintomas:")

        patient.setFever(st.checkbox("Febre"))

        patient.setMyalgia(st.checkbox("Mialgia", help="Dor muscular"))

        patient.setHeadache(st.checkbox("Cefaleia", help="Dor de cabeça"))

        patient.setRash(st.checkbox("Exantema", help="Manchas vermelhas em um região"))

        patient.setNausea(st.checkbox("Náusea"))

        patient.setBackPain(st.checkbox("Dor nas costas"))

        patient.setConjunctivitis(st.checkbox("Conjutivite"))

        patient.setArthritis(st.checkbox("Artrite", help="Inflamação das articulações"))

        patient.setArthralgia(st.checkbox("Artralgia", help="Dor nas articulações"))

        patient.setPetechia(st.checkbox("Petéquias", help="Pequenas manchas vermelhas ou marrom que surgem geralmente aglomeradas, mais frequentemente nos braços, pernas ou barriga"))

        patient.setEyePain(st.checkbox("Dor Retroorbital", help="Dor ao redor dos olhos"))

        st.write("Informe as comorbidades prévias:")

        patient.setDiabetes(st.checkbox("Diabetes", help=""))

        patient.setHypertension(st.checkbox("Hipertensão", help=""))

        if (st.form_submit_button("Realizar Diagnóstico")):

            with st.spinner('Realizando diagnóstico...'):
                # Existe um leve delay durante a classificacao do modelo, entao eu coloquei essa tela de loading
                # Foi necessario colocar um sleep de 1 sec para poder ativar a tela de loading
                time.sleep(1)
                result, probability_df = patient.diagnosis()

            st.write(f'## O resultado do diagnóstico foi **{result}**')

            st.write("Abaixo é possível observar o resultado detalhado do diagnóstico:")
            st.dataframe(probability_df)

            st.write("---")
            st.warning("**AVISO IMPORTANTE: este resultado é proveniente de um modelo de _machine learning_, não é definitivo. Analise também a situação epidemiológica da sua região.**")
