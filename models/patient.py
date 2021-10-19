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

        #Saídas formatadas do modelo para visualização no front.
        self.outputs = {
            "CHIKUNGUNYA": "Chikungunya",
            "DENGUE": "Dengue",
            "OUTRAS_DOENCAS": "Inconclusivo"
        }

        # Inputs categóricos(binários) do modelo.
        self.categorical_labels = {
            "FEBRE": "Febre", "MIALGIA": "Mialgia", "CEFALEIA": "Cefaleia", "EXANTEMA": "Exantema", "NAUSEA": "Náusea", "DOR_COSTAS": "Dor nas costas",
            "CONJUNTVIT": "Conjuntivite", "ARTRITE": "Artrite", "ARTRALGIA": "Artralgia", "PETEQUIA_N": "Petéquias", "DOR_RETRO": "Dor Retroorbital",
            "DIABETES": "Diabetes", "HIPERTENSA": "Hipertensão"
        }

        # Inputs numéricos do modelo
        self.numerical_labels = {
            "DIAS": "Dias"
        }

        self.labels = dict(self.categorical_labels, **self.numerical_labels)

        # caminho onde está localizado o modelo de ML.
        self.path_model_ml = "ml\\gradient_model.pkl"

    def diagnosis (self):
        """Realiza o dianóstico do paciente, utilizando os dados dos atributos para realizar a classificação pelo modelo de ML.

        Returns:
            string: o resultado da classificação do modelo formatado para visualização;
            pandas.Dataframe object: dataframe contendo as probablidades de cada saída do modelo com o padrão [doença | probabilidade];
        """
        
        with open(self.path_model_ml, "rb") as f:
            self.model = pickle.load(f)
            data = self.getRecord()
            self.classification = self.model.predict(data)[0]
            prob = self.model.predict_proba(data)

            prob_df = pd.DataFrame(
                ['{:.2%}'.format(i) for i in prob[0]],
                index=self.outputs.values(),
                columns=["Porcentagem"] # Necessário em português para visualização no front.
            )
            return self.outputs[self.classification], prob_df

    def explainer(self):
        """Utiliza o LIME para explicação do predição do dianóstico.

        Returns:
            pandas.Dataframe object: Dataframe contendo o valor de importância para cada atributo, seguinto o padrão [value] com cada atributo como index.
        """

        # O Explainer necessita da base de dados de treinamento para conseguir calcular os pesos, para se ter um certo nível de segurança, eu coloquei o caminho da base de dados no secrets do streamlit para que funciona como um ".env" no nosso projeto.
        path_database = st.secrets["path_database"]
        database = pd.read_csv(path_database, sep=';', usecols=self.labels.keys())

        explainer = lime.lime_tabular.LimeTabularExplainer(
            database.to_numpy(),
            feature_names=self.labels.keys(),
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

        for count, value in enumerate(self.outputs.keys()):
            if value == self.classification:
                pos_label = count
                break

        exp_dict = dict(sorted(exp.as_list(label=pos_label)))

        # TODO: ver com o pessoal se é melhor deixar "Peso" ou "Influência" mesmo.
        # TODO: SE POSSÍVEL, analisar depois uma foram simples para pegar o valor de intervalo do atributo "Dias", no explainer é usado um intervalo, tipo "DIAS >= 2", na conversão essa informação se perde, e ela pode ser bem interessante.
        exp_df = pd.DataFrame(
            exp_dict.values(),
            columns=["Peso"],
            # index=[value for key, value in sorted(self.labels.items())]
            index=dict(sorted(self.labels.items())).values()
        ).sort_values(by=["Peso"], ascending=False)

        exp_pos = exp_df[exp_df["Peso"] > 0]
        exp_neg = exp_df[exp_df["Peso"] < 0]

        # return exp_df
        return exp_pos, exp_neg

    # TODO: Ver com o pessoal se isso aqui é realmente necessário.
    def eraseData(self):
        """Método para limpeza dos dados do paciente, com isso todas as informações da ficha clínica do paciente são apagadas do sistema
        """

        self.fever = None
        self.myalgia = None
        self.headache = None
        self.rash = None
        self.nausea = None
        self.backPain = None
        self.conjunctivitis = None
        self.arthritis = None
        self.arthralgia = None
        self.petechia = None
        self.eyaPain = None
        self.diabetes = None
        self.hypertension = None
        self.days = None


    # Setters.

    # Input Febre.
    def setFever (self, value):
        self.fever = value

    # Input Mialgia.
    def setMyalgia (self, value):
        self.myalgia = value

    # Input Cefaleia.
    def setHeadache (self, value):
        self.headache = value

    # Input Exantema.
    def setRash (self, value):
        self.rash = value

    # Input Náusea.
    def setNausea (self, value):
        self.nausea = value

    # Input Dor Costas.
    def setBackPain (self, value):
        self.backPain = value

    # Input Conjuntvit.
    def setConjunctivitis (self, value):
        self.conjunctivitis = value

    # Input Artrite.
    def setArthritis (self, value):
        self.arthritis = value

    # Input Artralgia.
    def setArthralgia (self, value):
        self.arthralgia = value

    # Input Petéquia.
    def setPetechia (self, value):
        self.petechia = value

    # Input Dor Retroorbital.
    def setEyePain (self, value):
        self.eyaPain = value

    # Input Diabetes.
    def setDiabetes (self, value):
        self.diabetes = value

    # Input Hipertensão.
    def setHypertension (self, value):
        self.hypertension = value

    # Input Dias.
    def setDays (self, value):
        self.days = value


    
    # Getters.
    
    def getLabels(self):
        """Método get para obter todas as labels utlizada no modelo de ML.

        Returns:
            list: array com todas as labels do modelo de ML.
        """
        return self.labels.keys()

    def getRecord(self):
        """Get para retornar a ficha médica do paciente, com todas as informações dos atributos. IMPORTANTE: É NECESSÁRIO ESTAR NA MESMA ORDEM EM QUE O MODELO DE ML FOI TREINADO.

        Returns:
            list: array dos os valores dos atributos do paciente.
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