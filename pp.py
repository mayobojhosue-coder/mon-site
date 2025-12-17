import streamlit as st

st.title("liste de presence")

texte_tous_les_noms=st.text_area("écrivez les noms des pésent")
texte_presents=st.text_area("écrivez les noms des présents")
if st.button("valider"):
    tous_les_noms=[
        nom.strip()
        for nom in texte_tous_les_noms.split("\n")
        if nom.strip() !=""
    ]
    presents=[
        nom.strip()
        for nom in texte_presents.split("\n")
        if nom.strip() !=""
    ]
    absents=[
        nom for nom in tous_les_noms
        if nom not in  presents
    ]
    st.write("présents:",presents)
    st.write("absents:",absents)
