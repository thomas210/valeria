import pickle
import pandas as pd
import numpy as np
import lime.lime_tabular
import streamlit as st

'''
Model de Paciente, dentro desta classe e armazenado os dados do paciente e
e realizado o diagnostico do mesmo, com a utilizacao de um model de ML
'''

class Paciente:

    def __init__(self):
        '''
        construtor da classe
        sao definidos de acordo com o modelo de ML
        saidas
            Correspondencia da saida do modelo ML
            com o que será visualizado no front
        categorical_labels
            inputs categoricos(binarios) do modelo
        numerical_labels
            inputs numericos do modelo
        labels
            todas os inputs do modelo
            E NECESSARIO ESTAR NA MESMA ORDEM NO MODELO
        path_model_ml
            caminho onde o modelo de ml esta no projeto
        '''

        self.saidas = {
            "CHIKUNGUNYA": "Chikungunya",
            "DENGUE": "Dengue",
            "OUTRAS_DOENCAS": "Inconclusivo"
        }

        self.categorical_labels = [
            "FEBRE", "MIALGIA", "CEFALEIA", "EXANTEMA", "NAUSEA", "DOR_COSTAS",
            "CONJUNTVIT", "ARTRITE", "ARTRALGIA", "PETEQUIA_N", "DOR_RETRO",
            "DIABETES", "HIPERTENSA"
        ]

        self.numerical_labels = [
            "DIAS"
        ]

        self.labels = self.categorical_labels + self.numerical_labels

        self.path_model_ml = "ml\\gradient_model.pkl"

    def diagnostico(self):
        """
        Realizacao do dianostico
        O modelo e carregado e a classificacao e realizada
        Return
            ->Doenca calssifcada, formatada
            ->Dataframe com a porcentagem de cada doenca para visualizacao
        """
        with open(self.path_model_ml, "rb") as f:
            self.model = pickle.load(f)
            dados = self.getFicha()
            self.classificacao = self.model.predict(dados)[0]
            prob = self.model.predict_proba(dados)

            prob_df = pd.DataFrame(
                ['{:.2%}'.format(i) for i in prob[0]],
                index=self.saidas.values(),
                columns=["Porcentagem"]
            )
            return self.saidas[self.classificacao], prob_df

    def explainer(self):

        path_database = st.secrets["path_database"]
        database = pd.read_csv(path_database, sep=';', usecols=self.labels)

        explainer = lime.lime_tabular.LimeTabularExplainer(
            database.to_numpy(),
            feature_names=self.labels,
            class_names=self.saidas.keys(),
            categorical_features=[count for count, value in enumerate(self.categorical_labels)],
            categorical_names=self.categorical_labels,
            kernel_width=3,
            verbose=False
        )

        exp = explainer.explain_instance(
            np.array(self.getFicha()[0]),
            self.model.predict_proba,
            num_features=14,
            top_labels=3
        )

        for count, value in enumerate(self.saidas.keys()):
            if value == self.classificacao:
                pos_label = count

        exp_dict = dict(exp.as_list(label=pos_label))

        return pd.DataFrame(
            exp_dict.values(),
            columns=["Value"],
            index=exp_dict.keys()
        )

    #Seters#

    def setFebre (self, value):
        self.FEBRE = value

    def setMialgia (self, value):
        self.MIALGIA = value

    def setCefaleia (self, value):
        self.CEFALEIA = value

    def setExantema (self, value):
        self.EXANTEMA = value

    def setNausea (self, value):
        self.NAUSEA = value

    def setDorCostas (self, value):
        self.DOR_COSTAS = value

    def setConjuntvit (self, value):
        self.CONJUNTVIT = value

    def setArtrite (self, value):
        self.ARTRITE = value

    def setArtralgia (self, value):
        self.ARTRALGIA = value

    def setPetequia (self, value):
        self.PETEQUIA_N = value

    def setDorRetro (self, value):
        self.DOR_RETRO = value

    def setDiabetes (self, value):
        self.DIABETES = value

    def setHipertensao (self, value):
        self.HIPERTENSA = value

    def setDias (self, value):
        self.DIAS = value


    
    #Geters#
    
    def getLabels(self):
        return self.labels

    def getFicha(self):
        """
        Get para retornar os dados do paciente
        IMPORTANTE ESTA NA MESMA ORDEM DO MODELO
        """
        return [[
            self.FEBRE,
            self.MIALGIA,
            self.CEFALEIA,
            self.EXANTEMA,
            self.NAUSEA,
            self.DOR_COSTAS,
            self.CONJUNTVIT,
            self.ARTRITE,
            self.ARTRALGIA,
            self.PETEQUIA_N,
            self.DOR_RETRO,
            self.DIABETES,
            self.HIPERTENSA,
            self.DIAS
        ]]