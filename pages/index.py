import streamlit as st


def app():
    st.write("# Bem Vindo(a)!")

    st.write("---")

    st.write("### Olá, eu sou a Valéria, a sua assistente para o diagnóstico rápido de Dengue e Chikungunya!")

    st.write("### Sou um acrônimo para _*Virtual Assistant for LEarning pRocesses In Arbovirus*_!")

    st.write("Aqui, o nosso objetivo é auxiliar os profisionais de saúde para ter mais confiança no diagnóstico inicial dos pacientes. Espero que possamos trabalhar bem juntos!")

    st.info("**AVISO IMPORTANTE: O resultado que será gerado é proveniente de um modelo de _machine learning_, informado o diagnóstico mais provável para a situação do paciente. O nosso objetivo é apenas auxiliar na tomada de decisão do profissional de saúde!**")

    st.write("---")

    st.write("Para realizar o diagnóstico mais provável, acesse a barra de menu no canto esquerdo e escolha a opção **Diagnóstico**")

    st.write("Para analisar a distribuição geográfica dessas arboviroses no território nacional com o passar dos anos, acesse a barra de menu no canto esquerdo e escolha a opção **Casos**")

    st.write("Caso possua alguam dúvidsa a respeito de alguma funcionalidade, acesse a barra de menu no canto esquerdo e escolha a opção **Ajuda**")

    st.write("Para saber mais sobre a equipe que está trabalhando neste projeto, acesse a barra de menu no canto esquerdo e escolha a opção **Sobre**")
