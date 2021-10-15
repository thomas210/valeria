import streamlit as st
from models.paciente import Paciente
import time

def app():

    st.write("## Preencha os campos com as informações para realizar o diagnóstico:")

    with st.form("diagnostico_form"):

        paciente = Paciente()

        paciente.setDias(st.number_input("Quantos dias está sentindo os sintomas?", min_value=0, format="%d"))

        st.write("Informe os sintomas:")

        paciente.setFebre(st.checkbox("Febre"))

        paciente.setMialgia(st.checkbox("Mialgia", help="Dor muscular"))

        paciente.setCefaleia(st.checkbox("Cefaleia", help="Dor de cabeça"))

        paciente.setExantema(st.checkbox("Exantema", help="Manchas vermelhas em um região"))

        paciente.setNausea(st.checkbox("Náusea"))

        paciente.setDorCostas(st.checkbox("Dor nas costas"))

        paciente.setConjuntvit(st.checkbox("Conjutivite"))

        paciente.setArtrite(st.checkbox("Artrite", help="Inflamação das articulações"))

        paciente.setArtralgia(st.checkbox("Artralgia", help="Dor nas articulações"))

        paciente.setPetequia(st.checkbox("Petéquias", help="Pequenas manchas vermelhas ou marrom que surgem geralmente aglomeradas, mais frequentemente nos braços, pernas ou barriga"))

        paciente.setDorRetro(st.checkbox("Dor Retroorbital", help="Dor ao redor dos olhos"))

        st.write("Informe as comorbidades prévias:")

        paciente.setDiabetes(st.checkbox("Diabetes", help=""))

        paciente.setHipertensao(st.checkbox("Hipertensão", help=""))

        if (st.form_submit_button("Realizar Diagnóstico")):

            with st.spinner('Realizando diagnóstico...'):
                # Existe um leve delay durante a classificacao do modelo, entao eu coloquei essa tela de loading
                # Foi necessario colocar um sleep de 1 sec para poder ativar a tela de loading
                # time.sleep(1)
                resultado, probabilidades_df = paciente.diagnostico()
                explainer = paciente.explainer()

            st.write(f'## O resultado do diagnóstico foi **{resultado}**')

            st.write("Abaixo é possível observar o resultado detalhado do diagnóstico:")
            st.dataframe(probabilidades_df)

            st.write("Abaixo é possível o nível de importância de cada atributo para este diagnóstico:")
            st.bar_chart(explainer)
            st.dataframe(explainer)

            st.write("---")
            st.warning("**AVISO IMPORTANTE: este resultado é proveniente de um modelo de _machine learning_, não é definitivo. Analise também a situação epidemiológica da sua região.**")