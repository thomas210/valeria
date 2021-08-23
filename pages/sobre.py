import streamlit as st


def app():
    st.write("## Realização")

    col_1, dotlab_col, col_3 = st.columns(3)

    dotlab_col.image("images/DotLab.png")

    st.write("## Apoio")

    upe_col, fmt_col = st.columns(2)
    upe_col.image("images/upe.png", use_column_width=True)
    fmt_col.image("images/fmt.png")

    st.write("## Financiamento")

    facepe_col, fapeam_col = st.columns(2)
    facepe_col.image("images/facepe.png")
    fapeam_col.image("images/fapeam.png")

    st.balloons()
