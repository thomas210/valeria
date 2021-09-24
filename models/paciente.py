import pickle
import pandas as pd

class Paciente:


    def __init__(self, FEBRE, MIALGIA, CEFALEIA, EXANTEMA, NAUSEA, DOR_COSTAS, CONJUNTVIT, ARTRITE, ARTRALGIA, PETEQUIA_N, DOR_RETRO, DIABETES, HIPERTENSA, DIAS):
        """
        Inicializador da classe, e necessario passar todos os atributos na ordem para serem armazenados
        Alem disso, tambem sao setados as saidas possiveis do models e as labels(colunas do base)
        """
        self.FEBRE = FEBRE
        self.MIALGIA = MIALGIA
        self.CEFALEIA = CEFALEIA
        self.EXANTEMA = EXANTEMA
        self.NAUSEA = NAUSEA
        self.DOR_COSTAS = DOR_COSTAS
        self.CONJUNTVIT = CONJUNTVIT
        self.ARTRITE = ARTRITE
        self.ARTRALGIA = ARTRALGIA
        self.PETEQUIA_N = PETEQUIA_N
        self.DOR_RETRO = DOR_RETRO
        self.DIABETES = DIABETES
        self.HIPERTENSA = HIPERTENSA
        self.DIAS = DIAS

        self.saidas = {
            "CHIKUNGUNYA": "Chikungunya",
            "DENGUE": "Dengue",
            "OUTRAS_DOENCAS": "Inconclusivo"
        }

        self.labels = [
            "FEBRE", "MIALGIA", "CEFALEIA", "EXANTEMA", "NAUSEA", "DOR_COSTAS",
            "CONJUNTVIT", "ARTRITE", "ARTRALGIA", "PETEQUIA_N", "DOR_RETRO",
            "DIABETES", "HIPERTENSA", "DIAS"
        ]

    def diagnostico(self):
        """
        Realizacao do dianostico
        O modelo e carregado e a classificacao e realizada
        Return
            ->Doenca calssifcada, formatada
            ->Dataframe com a porcentagem de cada doenca para visualizacao
        """
        with open("D:\mestrado\\valeria_v1\gradient_model.pkl", "rb") as f:
            model = pickle.load(f)
            dados = self.getFicha()
            classificacao = model.predict(dados)[0]
            prob = model.predict_proba(dados)

            prob_df = pd.DataFrame(
                ['{:.2%}'.format(i) for i in prob[0]],
                index=self.saidas.values(),
                columns=["Porcentagem"]
            )
            return self.saidas[classificacao], prob_df

    #Sets#

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


    
    #Gets#
    
    def getLabels(self):
        return self.labels

    def getFicha(self):
        """
        Get para retornar os dados do diagnostico
        """
        dados = [[
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

        return dados