import base64
import streamlit as st


def app():
    st.write(
        "Abaixo você pode analisar a quantidade de casos de Dengue e Chikungunya no Brasil com o passar dos anos, bem como a quantidade de casos suspeitos/inconclusivos dessas doenças")

    st.write("### Quantidade de casos de Dengue entre 2013 e 2020")
    file_ = open("images/dengue.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="gif">',
        unsafe_allow_html=True,
    )

    st.write("### Quantidade de casos de Chikungunya entre 2015 e 2020")
    file_ = open("images/chika.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="gif">',
        unsafe_allow_html=True,
    )

    st.write("### Quantidade de casos suspeitos/inconclusivos entre 2013 e 2020")
    file_ = open("images/outros.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="gif">',
        unsafe_allow_html=True,
    )

    st.write("---")

    st.write("Dados coletados no Sistema de Informação de Agravos de Notificação (SINAN)")
