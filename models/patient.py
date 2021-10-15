import pickle
import pandas as pd
import numpy as np
import lime.lime_tabular
import streamlit as st

class Patient:
    """Classe de Paciente, responsável por armazenar os dados do paciente e realizar o dianóstico do mesmo, com a utilização de um model de ML.
    """

    def __init__(self):
        """Construtor da classe, inicialização das labels e definição do caminho para o modelo de ML.
        """

        #Saídas formatadas do modelo para visualização no front
        self.outputs = {
            "CHIKUNGUNYA": "Chikungunya",
            "DENGUE": "Dengue",
            "OUTRAS_DOENCAS": "Inconclusivo"
        }

        # Inputs categóricos(binários) do modelo
        self.categorical_labels = [
            "FEBRE", "MIALGIA", "CEFALEIA", "EXANTEMA", "NAUSEA", "DOR_COSTAS",
            "CONJUNTVIT", "ARTRITE", "ARTRALGIA", "PETEQUIA_N", "DOR_RETRO",
            "DIABETES", "HIPERTENSA"
        ]

        # Inputs numéricos do modelo
        self.numerical_labels = [
            "DIAS"
        ]

        self.labels = self.categorical_labels + self.numerical_labels

        # caminho onde está localizado o modelo de ML
        self.path_model_ml = "ml\\gradient_model.pkl"

    def diagnosis (self):
        """Realiza o dianóstico do paciente, utilizando os dados dos atributos para realizar a classificação pelo modelo de ML

        Returns:
            string: o resultado da classificação do modelo formatado para visualização 
            pandas.Dataframe object: dataframe contendo as probablidades de cada saída do modelo com o padrão [doença | probabilidade]
        """
        
        with open(self.path_model_ml, "rb") as f:
            model = pickle.load(f)
            data = self.getRecord()
            classification = model.predict(data)[0]
            prob = model.predict_proba(data)

            prob_df = pd.DataFrame(
                ['{:.2%}'.format(i) for i in prob[0]],
                index=self.outputs.values(),
                columns=["Porcentagem"] # Necessário em português para visualização no front
            )
            return self.outputs[classification], prob_df

    def explainer(self):
        """Utiliza o LIME para explicação do predição do dianóstico

        Returns:
            pandas.Dataframe object: Dataframe contendo o valor de importância para cada atributo, seguinto o padrão [value] com cada atributo como index
        """

        path_database = st.secrets["path_database"]
        database = pd.read_csv(path_database, sep=';', usecols=self.labels)

        explainer = lime.lime_tabular.LimeTabularExplainer(
            database.to_numpy(),
            feature_names=self.labels,
            class_names=self.outputs.keys(),
            categorical_features=[count for count, value in enumerate(self.categorical_labels)],
            categorical_names=self.categorical_labels,
            kernel_width=3,
            verbose=False
        )

        exp = explainer.explain_instance(
            np.array(self.getRecord()[0]),
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

    # Setters

    # Input Febre
    def setFever (self, value):
        self.fever = value

    # Input Mialgia
    def setMyalgia (self, value):
        self.myalgia = value

    # Input Cefaleia
    def setHeadache (self, value):
        self.headache = value

    # Input Exantema
    def setRash (self, value):
        self.rash = value

    # Input Náusea
    def setNausea (self, value):
        self.nausea = value

    # Input Dor Costas
    def setBackPain (self, value):
        self.backPain = value

    # Input Conjuntvit
    def setConjunctivitis (self, value):
        self.conjunctivitis = value

    # Input Artrite
    def setArthritis (self, value):
        self.arthritis = value

    # Input Artralgia
    def setArthralgia (self, value):
        self.arthralgia = value

    # Input Petéquia
    def setPetechia (self, value):
        self.petechia = value

    # Input Dor Retroorbital
    def setEyePain (self, value):
        self.eyaPain = value

    # Input Diabetes
    def setDiabetes (self, value):
        self.diabetes = value

    # Input Hipertensão
    def setHypertension (self, value):
        self.hypertension = value

    # Input Dias
    def setDays (self, value):
        self.days = value


    
    # Getters
    
    def getLabels(self):
        """Método get para obter todas as labels utlizada no modelo de ML

        Returns:
            list: array com todas as labels do modelo de ML
        """
        return self.labels

    def getRecord(self):
        """Get para retornar a ficha médica do paciente, com todas as informações dos atributos. IMPORTANTE: É NECESSÁRIO ESTAR NA MESMA ORDEM EM QUE O MODELO DE ML FOI TREINADO

        Returns:
            list: array dos os valores dos atributos do paciente
        """
        
        return [[
            self.fever,
            self.myalgia,
            self.headache,
            self.rash,
            self.nausea,
            self.backPain,
            self.conjunctivitis,
            self.arthritis,
            self.arthralgia,
            self.petechia,
            self.eyaPain,
            self.diabetes,
            self.hypertension,
            self.days
        ]]