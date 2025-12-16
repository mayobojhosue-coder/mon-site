import streamlit as st

st.write("tu fais quoi?")
if st.button("rien de grand"):
    st.write("t'es juste posé..ok alors.")
if st.button("je fais rien"):
    st.write("okay okay.")
reponse_perso=st.text_input("ou écris ce que tu fais:")
if reponse_perso:
    st.write("ah d'accord, tu :",reponse_pereso)
