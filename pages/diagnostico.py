import pickle
import re
import urllib.parse

import pandas as pd
import requests
import streamlit as st


def app():
    cep_max_size = 8
    cep_regex = "\d{8}"

    diagnostico_key = 'diagnostico'
    prob_key = 'prob'

    doencas = ["CHIKUNGUNYA", "DENGUE", "OUTRAS_DOENCAS"]
    doencas_texto = ["Chikungunya", "Dengue", "Inconclusivo"]

    class Checkbox:
        def __init__(self, value):
            self.value = value

        def get_value(self):
            if self.value:
                res = 1
            else:
                res = 2
            return res

    st.write("## Preencha os campos com as informações para realizar o diagnóstico:")

    DIAS = st.number_input("Quantos dias está sentindo os sintomas?", min_value=0, format="%d")

    st.write("Informe os sintomas:")

    FEBRE = Checkbox(st.checkbox("Febre"))

    MIALGIA = Checkbox(st.checkbox("Mialgia", help="Dor muscular"))

    CEFALEIA = Checkbox(st.checkbox("Cefaleia", help="Dor de cabeça"))

    EXANTEMA = Checkbox(st.checkbox("Exantema", help="Manchas vermelhas em um região"))

    NAUSEA = Checkbox(st.checkbox("Náusea"))

    DOR_COSTAS = Checkbox(st.checkbox("Dor nas costas"))

    CONJUNTVIT = Checkbox(st.checkbox("Conjutivite"))

    ARTRITE = Checkbox(st.checkbox("Artrite", help="Inflamação das articulações"))

    ARTRALGIA = Checkbox(st.checkbox("Artralgia", help="Dor nas articulações"))

    PETEQUIA_N = Checkbox(st.checkbox("Petéquias",
                                      help="Pequenas manchas vermelhas ou marrom que surgem geralmente aglomeradas, mais frequentemente nos braços, pernas ou barriga"))

    DOR_RETRO = Checkbox(st.checkbox("Dor Retroorbital", help="Dor ao redor dos olhos"))

    st.write("Informe as comorbidades prévias:")

    DIABETES = Checkbox(st.checkbox("Diabetes", help=""))

    HIPERTENSA = Checkbox(st.checkbox("Hipertensão", help=""))

    if st.button("Realizar Diagnóstico"):

        dados = [[
            FEBRE.get_value(), MIALGIA.get_value(), CEFALEIA.get_value(),
            EXANTEMA.get_value(), NAUSEA.get_value(), DOR_COSTAS.get_value(),
            CONJUNTVIT.get_value(), ARTRITE.get_value(), ARTRALGIA.get_value(),
            PETEQUIA_N.get_value(), DOR_RETRO.get_value(),
            DIABETES.get_value(), HIPERTENSA.get_value(), DIAS
        ]]

        with open('gradient_model.pkl', 'rb') as f:
            model = pickle.load(f)
            doenca = model.predict(dados)[0]
            st.session_state[prob_key] = model.predict_proba(dados)

        for count, value in enumerate(doencas):
            if value == doenca:
                st.session_state[diagnostico_key] = doencas_texto[count]

        st.session_state['form_submetido'] = True

    if 'form_submetido' in st.session_state:
        st.write("---")
        diagnostico = st.session_state[diagnostico_key]
        st.write(f'## O resultado do diagnóstico foi **{diagnostico}**')

        st.write("Abaixo é possível observar o resultado detalhado do diagnóstico:")
        res_df = pd.DataFrame(st.session_state[prob_key], columns=doencas_texto, index=["Probabilidade"])
        df_style = res_df.style.format(
            {'Dengue': '{:.2%}',
             'Chikungunya': '{:.2%}',
             'Inconclusivo': '{:.2%}'}
        )
        st.dataframe(df_style)

        # if diagnostico != doencas_texto[2]:
        #     st.write("---")
        #     cep = st.text_input("Informe seu CEP para buscar a Unidade de Saúde mais próxima:", max_chars=cep_max_size)
        #
        #     if st.button("Buscar"):
        #         try:
        #             cep_valido = re.search(cep_regex, cep)
        #
        #             if cep_valido:
        #                 with st.spinner('Por favor, aguarde...'):
        #                     cep_response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        #                     cep_json = cep_response.json()
        #
        #                 cidade = cep_json['localidade']
        #                 bairro = cep_json['bairro']
        #                 uf = cep_json['uf']
        #
        #                 str_to_encode = f'Unidade Básica de Saude, {bairro}, {cidade}, {uf}'
        #                 encoded = urllib.parse.quote(str_to_encode.encode("utf-8"))
        #                 st.write(
        #                     f"## Link para buscar a Unidades de Saúde: [clique aqui](https://www.google.com/maps/search/?api=1&query={encoded})")
        #             else:
        #                 raise Exception("CEP inválido")
        #         except:
        #             st.error("CEP inválido")

        st.write("---")
        st.warning("**AVISO: Este diagnóstico não é definitivo, analise também a situação epidemiológica da sua cidade.**")
