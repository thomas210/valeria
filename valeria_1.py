import streamlit as st

from pages import inicio, diagnostico, casos, ajuda, sobre
from pages.page_manager import PageManager

app = PageManager()

st.set_page_config(page_title="VALERIA", page_icon="images/val_temp.png")

app.add_page("Início", inicio.app)
app.add_page("Diagnóstico", diagnostico.app)
app.add_page("Casos", casos.app)
app.add_page("Ajuda", ajuda.app)
app.add_page("Sobre", sobre.app)

app.run()
