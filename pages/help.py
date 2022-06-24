import streamlit as st
from models.user import User
from error import errorCode

def getName():
    return "Ajuda"

def app():
    st.write("# Ajuda")

    st.write("## Dúvidas Frequentes:")

    st.write("### Como a VALERIA funciona?")

    st.write("A VALERIA utiliza um modelo de _machine learning_.O modelo recebe os dados do paciente (sintomas e doenças prévias) e realiza a classificação da doença dentre umas das três classes: Dengue, Chikungunya e Inconclusivo. Para maiores informações sobre o sistema, é possível ler o artigo sobre o nosso protótipo [aqui](https://doi.org/10.5753/webmedia_estendido.2021.17623). Atualmente, o modelo de machine learning utilizado para a classificação é o Gradient Boosting com.")

    # TODO: Quando o artigo for publicado inserir o link para o mesmo.
    st.write("Atualmente, o modelo de machine learning utilizado para a classificação é o _Gradient Boosting_, o mesmo já possui o registro expedido pelo INPI Brasil - Instituto Nacional da Propriedade Industrial, sob o número de procedimento [BR 51 2021 002710-8](http://revistas.inpi.gov.br/pdf/Programa_de_computador2655.pdf).")
    
    st.write("Para maiores informações sobre como o modelo foi configurado e avaliado, veja o artigo publicado [aqui](https://www.frontiersin.org/articles/10.3389/fitd.2021.769968/full).")

    st.write("### O que são os valores de porcentagem do resultado detalhado?")

    st.write("A saída do modelo de _machine learning_ que utilizamos é a probabilidade de cada classe ocorrer, onde a classe com maior probabilidade é considerada a saída definitiva. Então nós decidimos também inserir as probabilidades das outras classes para um melhor entendimento.") 

    st.write("Modelos de _machine learning_ não são modelos interpretavéis, tornando difícil o seu entendimento. Para minimizar esse problema, nós utilizamos o LIME (_Local Interpretable Model-Agnostic Explanations_), uma técnica que tem o objetivo de tornar o modelo mais interpretável. Para isso, a técnica gera um peso para cada atributo, levando em conta os dados de treinamento do modelo e a estrutura do modelo em si. Nós utilizamos essa técnica para definir quais foram os atributos mais importantes para o resultado do modelo e divimos em dois grupos: os atributos que favorecem a resposta do modelo e os atributos contrários a resposta do modelo.")

    st.write("O LIME é uma ferramenta de código aberto e mais detalhes podem ser lidos no seu [blog](https://www.oreilly.com/content/introduction-to-local-interpretable-model-agnostic-explanations-lime/) ou em seu [artigo](https://arxiv.org/abs/1602.04938).")

    st.write("Copyright (c) 2016, Marco Tulio Correia Ribeiro. Todos os direitos reservados.")

    st.write("Para auxiliar os profissionais de saúde com mais informações, nós também resolvemos inserir esse resultado mais detalhado. Então, o profissional de saúde pode utilizar essas informações para entender o quadro geral do paciente e observar o nível de confiança que o modelo possui em relação ao resultado informado.")

    st.write("### Alguma informação do paciente fica salva?")

    st.write("Não. Atualmente a VALERIA não armazena nenhuma informação acerca do paciente. Todos os dados são apagados no momento em que o modelo apresenta o resultado.")

    st.write("## Caso possua alguma dúvida a respeito da utilização da plataforma, você pode assistir ao nosso vídeo introdutório:")

    st.video("https://www.youtube.com/watch?v=-egcW70C7EY")

    with st.form("contact_form", clear_on_submit=True):

        st.write("## Caso ainda possua alguma outra dúvida, entre em contato conosco para que possamos lhe ajudar:")

        user = User()

        user.setName(st.text_input("Nome:"))

        user.setEmail(st.text_input("E-mail:"))

        user.setMessage(st.text_area("Mensagem:"))

        if (st.form_submit_button("Enviar")):
            cod, text = user.validate()
            if cod != errorCode.getErrors().SUCCESS.name:
                st.error(text)
            else:
                with st.spinner("Enviando..."):
                    user.sendEmail()
                st.success("Enviado com sucesso!")
