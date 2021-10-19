import streamlit as st

from pages import index, diagnosis, cases, help, about
from pages.page_manager import PageManager

app = PageManager()

st.set_page_config(page_title="VALERIA", page_icon="images/val_temp.png")

app.add_page("Início", index.app)
app.add_page("Diagnóstico", diagnosis.app)
app.add_page("Casos", cases.app)
app.add_page(help.getName(), help.app)
app.add_page("Sobre", about.app)

app.run()
