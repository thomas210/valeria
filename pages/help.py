import streamlit as st

def getName():
    return "Ajuda"

def app():
    st.write("# Ajuda")

    st.write("## Caso possua alguma dúvida a respeito da utilização da plataforma, você pode assistir ao nosso vídeo introdutório:")

    st.video("https://www.youtube.com/watch?v=3ipbYO4zJHo")
