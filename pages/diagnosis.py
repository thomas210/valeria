import streamlit as st
from models.patient import Patient

def highlight_values(val): 
    color = 'green' if val > 0 else 'red' 
    return 'color: %s' % color

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

        st.write("Informe as condições prévias:")

        patient.setDiabetes(st.checkbox("Diabetes", help=""))

        patient.setHypertension(st.checkbox("Hipertensão", help=""))

        if (st.form_submit_button("Realizar Diagnóstico")):

            with st.spinner('Realizando diagnóstico...'):
                result, probability_df = patient.diagnosis()
                e0, e1, e2 = patient.explainer()

            st.write(f'## O resultado do diagnóstico foi **{result}**')

            st.write("Abaixo é possível observar o resultado detalhado do diagnóstico, informado a probabilidade de cada doença:")
            st.dataframe(probability_df)

            st.write("### Resultado detalhado")
            st.write(f"Os valores abaixo buscam explicar melhor como o sistema de _machine learning_ chegou no resultado {result}. Para cada atributo foi aplicado um valor que representa o quão influente o mesmo foi para esta classificação, quanto maior o valor, mais forte foi a sua influência nesta classificação. Valores positivos estão coloridos em verde e indicam influência a favor da classificação {result}, enquanto que valores negativos estão coloridos em vermelho e indicam uma influência contrária a classificação {result}.")

            st.write("Abaixo é possível analisar quais atributos influenciaram positivamente")
            st.write
            # st.bar_chart(explainer)
            st.dataframe(e0.style.applymap(highlight_values))
            st.write(e1.style.background_gradient(cmap='Greens'))
            st.write(e2.style.background_gradient(cmap='Reds'))

            st.write("---")
            st.warning("**AVISO IMPORTANTE: este resultado é proveniente de um modelo de _machine learning_, não é definitivo. Analise também a situação epidemiológica da sua região.**")
