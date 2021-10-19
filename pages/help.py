import streamlit as st

def getName():
    return "Ajuda"

def app():
    st.write("# Ajuda")

    st.write("## Dúvidas Frenquentes:")

    st.write("### Como funciona o diagnóstico da VALERIA?")

    st.write("Para realizar o diagnóstico mais provável do paciente, a VALERIA utliza um modelo de _machine learning_ para classificação. O modelo recebe os dados do paciente (sintomas e doenças prévias) e realiza a classificação da doença do paciente. A saída do modelo é a classificação do paciente entre umas das três classes, Dengue, Chikungunya e Inconclusivo")

    st.write("Atualmente o modelo de _machine learning_ utilizado para a classificação é o _Gradient Boosting_. Para maiores informações sobre como foi realizado o experimento para desenvolvimento deste modelo, é possível analisar o artigo publicado [aqui](https://www.overleaf.com/project)*ATUALIZAR O LINK AINDA!*")

    st.write("### O que são os valores de porocentagem do resultado detalhado?")

    st.write("O saída do modelo de _machine learning_ que utilizamos na verdade é probabilidade de cada classe disponível, onde a classe com maior probabilidade é considerada a saída definitiva. Para auxiliar os profissionais de saúde com mais informações nós também resolvemos inserir esse resultado mais detalhado. Então o profissional de saúde pode utilizar essas informações para entender o quadro geral do paciente e observar o nível de confiança que o modelo possui em relação ao resultado informado.")

    st.write("### O que são os valores de \"influência\" de cada atributo?")

    st.write("Modelos de _machine learning_ não são modelos interpretavéis, tornando difícil o seu entendimento. Para minimizar esse problema, nós utilizamos o LIME (_Local Interpretable Model-Agnostic Explanations_) uma técnica que tem o objetivo de tornar o modelo mais interpretável. Para isso, a técnica gerar um peso para cada atributo, levando em conta os dados de treinamento do modelo e a estrutura do modelo em si. Quanto maior o peso de cada atributo, maior foi a sua relevância para a classificação final. Valores positivos indicam que o atributo contribuiu para a classificação final do modelo, enquanto que valores negativos indicam que o atributo contribuiu para uma classificação diferente da final.")

    st.write("O LIME é uma ferramenta de código aberto e mais detalhes podem ser lidos no seu [blog](https://www.oreilly.com/content/introduction-to-local-interpretable-model-agnostic-explanations-lime/) ou em seu [artigo](https://arxiv.org/abs/1602.04938)")

    st.write("Copyright (c) 2016, Marco Tulio Correia Ribeiro. Todos os direitos reservados.")

    st.write("Esperamos que essas informações ajudem aos médicos a entender o porquê do modelo ter feito a classificação final, e, junto com a experiência do prórpio profissional de saúde, poder oferecer um diagnóstico clínicos mais acurado.")

    st.write("### Alguma informação do paciente fica salva?")

    st.write("Não, atualmente a VALERIA não registra nenhuma informação acerca do paciente, todos os dados do paciente são apagados no momento em que o diagnóstico é realizado.")

    st.write("## Caso possua alguma dúvida a respeito da utilização da plataforma, você pode assistir ao nosso vídeo introdutório:")

    st.video("https://www.youtube.com/watch?v=3ipbYO4zJHo")