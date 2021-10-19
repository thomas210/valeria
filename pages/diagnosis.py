import streamlit as st
from models.patient import Patient
# from pages import help

# def highlight_values(val): 
#     color = 'green' if val > 0 else 'red' 
#     return 'color: %s' % color

def app():

    st.write("## Preencha os campos com as informações do paciente para realizar o diagnóstico:")

    with st.form("diagnostico_form"):

        patient = Patient()

        patient.setDays(st.number_input("Quantos dias o paciente está sentindo os sintomas?", min_value=0, format="%d"))

        st.write("Informe os sintomas do paciente:")

        col_symptoms_1, col_symptoms_2 = st.columns(2)

        patient.setFever(col_symptoms_1.checkbox("Febre"))

        patient.setMyalgia(col_symptoms_1.checkbox("Mialgia", help="Dor muscular"))

        patient.setHeadache(col_symptoms_1.checkbox("Cefaleia", help="Dor de cabeça"))

        patient.setRash(col_symptoms_1.checkbox("Exantema", help="Manchas vermelhas em um região"))

        patient.setNausea(col_symptoms_1.checkbox("Náusea"))

        patient.setBackPain(col_symptoms_1.checkbox("Dor nas costas"))

        patient.setConjunctivitis(col_symptoms_2.checkbox("Conjutivite"))

        patient.setArthritis(col_symptoms_2.checkbox("Artrite", help="Inflamação das articulações"))

        patient.setArthralgia(col_symptoms_2.checkbox("Artralgia", help="Dor nas articulações"))

        patient.setPetechia(col_symptoms_2.checkbox("Petéquias", help="Pequenas manchas vermelhas ou marrom que surgem geralmente aglomeradas, mais frequentemente nos braços, pernas ou barriga"))

        patient.setEyePain(col_symptoms_2.checkbox("Dor Retroorbital", help="Dor ao redor dos olhos"))

        st.write("Informe as condições prévias do paciente:")

        col_comorbidities_1, col_comorbidities_2 = st.columns(2)

        patient.setDiabetes(col_comorbidities_1.checkbox("Diabetes", help=""))

        patient.setHypertension(col_comorbidities_2.checkbox("Hipertensão", help=""))

        if (st.form_submit_button("Realizar Diagnóstico")):

            with st.spinner('Realizando diagnóstico...'):
                result, probability_df = patient.diagnosis()
                exp_pos, exp_neg = patient.explainer()
                patient.eraseData()

            st.write(f'## O resultado do diagnóstico foi **{result}**')

            st.write("### Resultado detalhado")

            st.write(f"Abaixo é possível observar o resultado detalhado do diagnóstico. Caso haja alguma dúvida sobre como esses valores foram gerados, você pode consultar a tela de Ajuda no canto esquerdo.")

            st.write("#### Probabilidade de cada doença")
            st.dataframe(probability_df)

            # Eu tirei essa explicação daqui pq coloquei na tela de ajuda, com a ideia de ficar mais clean essa tela

            # st.write(f"Os valores abaixo buscam explicar melhor como o sistema de _machine learning_ chegou no resultado {result}. Para cada atributo foi aplicado um valor que representa o quão influente o mesmo foi para esta classificação, quanto maior o valor, mais forte foi a sua influência nesta classificação. Valores positivos estão coloridos em verde e indicam influência a favor da classificação {result}, enquanto que valores negativos estão coloridos em vermelho e indicam uma influência contrária a classificação {result}. Para mais informações sobre como esse número é gerado, você pode consultar a tela de {help.getName()} no canto esquerdo.")

            st.write("#### Peso de cada atributo para este diagnóstico provável")

            # st.dataframe(e0.style.applymap(highlight_values))

            col_pos, col_neg = st.columns(2)

            col_pos.write(f"Atributos que contribuíram para o resutlado {result}")
            col_pos.dataframe((exp_pos.style.background_gradient(cmap='Greens')))

            col_neg.write(f"Atributos que não contribuíram para o resultado {result}")
            col_neg.dataframe((exp_neg.style.background_gradient(cmap='Reds')))

            st.write("---")
            st.warning("**AVISO IMPORTANTE: este resultado é proveniente de um modelo de _machine learning_, não é definitivo. Analise também a situação epidemiológica da sua região.**")
