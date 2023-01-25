# from flask_sqlalchemy import SQLAlchemy
from email import message
from sqlalchemy import create_engine
from datetime import datetime
import pickle
import pandas as pd
import numpy as np
import lime.lime_tabular
import streamlit as st
import requests

class Patient:
    """Classe de Paciente, responsável por armazenar os dados do paciente e realizar o dianóstico do mesmo, com a utilização de um model de ML.
    """

    def __init__(self):
        """Construtor da classe, inicialização das labels e definição do caminho para o modelo de ML.
        """
        
        # self.engine = create_engine('mysql://upecaruaru01:l3g3nd4ry@mysql.upecaruaru.com.br:3306/upecaruaru01') # connect to server
        password = st.secrets["password"]
        link = st.secrets["link"]
        username = st.secrets["username"]
        self.engine = create_engine(f'mysql://{username}:{password}@{link}:3306/{username}') # connect to server

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
            "DIAS": "Período dos sintomas"
        }

        self.labels = dict(self.categorical_labels, **self.numerical_labels)

        # caminho onde está localizado o modelo de ML.
        self.path_model_ml = "ml/gradient_model.pkl"

    def diagnosis (self):
        """Realiza o dianóstico do paciente, utilizando os dados dos atributos para realizar a classificação pelo modelo de ML. Basicamente, a função carrega o modelo e faz o model.predict() com os dados do paciente. Também é executado o model.predict_proba() para obter as probabilidades de cada saída do modelo.
        Returns:
            *string: o resultado da classificação do modelo formatado para visualização;
            *pandas.Dataframe object: dataframe contendo as probablidades de cada saída do modelo com o padrão [doença | probabilidade];
        """
        
        with open(self.path_model_ml, "rb") as f:
            self.model = pickle.load(f)
            data = self.getRecord()
            self.classification = self.model.predict(data)[0]
            prob = self.model.predict_proba(data)
            
            message = "📋 Mais um diagnóstico realizado com sucesso! ✅"
            bot_token = st.secrets["telegram_token"]
            bot_chatID = st.secrets["chat_id"]
            send_text = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&text={message}"
            requests.get(send_text)
            
            try:
                self.saveData()
                
            except Exception as error:
                message = "💀 Ocorreu um erro ao enviar a mensagem para o servidor! 💥"
                bot_token = st.secrets["telegram_token"]
                bot_chatID = st.secrets["chat_id"]
                send_text = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&text={message}"
                requests.get(send_text)
                
                send_text = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&text={error}"
                requests.get(send_text)

            prob_df = pd.DataFrame(
                ['{:.2%}'.format(i) for i in prob[0]],
                index=self.outputs.values(),
                columns=["Porcentagem"] # Necessário em português para visualização no front.
            )
            return self.outputs[self.classification], prob_df

    def explainer(self):
        """Utiliza o LIME para explicação do predição do dianóstico. A base de dados de treinamento é usado para preparar o LIME, então os dados do paciente são inseridos para obtenção dos pesos para cada atributo. Por fim, os dados são anexados em um dataframe contendo o resutlado do paciente para cada atributo e o seu respectivo peso.
        Returns:
            * pandas.Dataframe object: Dataframe contendo o valor do peso de cada atributo positivo, index=Atributo header = [Resultado, Valor].
            * pandas.Dataframe object: Dataframe contendo o valor do peso de cada atributo negativo, index=Atributo header = [Resultado, Valor].
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

        # For para saber a posição da saída, infelizmente não consegui fazer isso de uma forma mais elegante.
        for count, value in enumerate(self.outputs.keys()):
            if value == self.classification:
                pos_label = count
                break

        # As saídas do explainer são inseridas em um dict para que possam ser convertidas em um dataframe posteriormente.
        exp_dict = sorted(dict(exp.as_map()[pos_label]).items())

        exp_df = pd.DataFrame(
            exp_dict,
            columns=["key", "Valor"],
            index=self.labels.values()
        )

        # A coluna de resultado contém as informações do paciente, a saída do as_map() do explainer está na mesma ordem da entrada dos atributos, e consequentemente o método getRecord() da classe também esta na mesma ordem, não sendo necessário ordenar antes de unificar.
        exp_df["Resposta do Paciente"] = np.array(self.getRecord()[0])

        # Necessário converter o tipo da coluna para poder modificar o valor livremente. Para uma melhor visualização, as colunas boolenasa foram convertidas para um resultado de "Sim" ou "Não".
        exp_df["Resposta do Paciente"] = exp_df["Resposta do Paciente"].astype(str)
        for attribute in self.categorical_labels.values():
            exp_df.loc[(exp_df.index == attribute) & (exp_df["Resposta do Paciente"] == "0"), "Resposta do Paciente"] = "Não"
            exp_df.loc[(exp_df.index == attribute) & (exp_df["Resposta do Paciente"] == "1"), "Resposta do Paciente"] = "Sim"

        # Para uma melhor visualização, o valor do peso foi multiplicado por 100.
        exp_df["Valor"] = exp_df["Valor"].apply(lambda x: x * 100)

        exp_pos = exp_df[exp_df["Valor"] > 0].sort_values(by=["Valor"], ascending=False)
        exp_neg = exp_df[exp_df["Valor"] < 0].sort_values(by=["Valor"], ascending=True)

        # Pegar apenas o resutlado do paciente
        exp_pos = exp_pos[["Resposta do Paciente"]]
        exp_neg = exp_neg[["Resposta do Paciente"]]

        return exp_pos, exp_neg

    def saveData(self):
        """
        > It takes the data from the form, adds the classification and timestamp, and saves it to the
        database
        TODO: ERROR WITH DB, SO JUST RETURN
        """
        
        return 0
        
        data = self.getRecord()
        
        # Getting the current date and time
        dt = datetime.now()

        # getting the timestamp
        ts = datetime.timestamp(dt)
        
        data_df = pd.DataFrame(data=data, columns=self.labels)
        data_df["CLASSI_FIN"] = self.classification
        data_df["timestamp"] = pd.to_datetime(ts, unit='s')
        data_df.to_sql("consultas", self.engine, index=False, if_exists="append")


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
