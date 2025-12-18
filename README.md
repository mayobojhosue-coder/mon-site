
   import streamlit as st
from datetime import date, datetime
import os

# ==================================================
# CONFIG PAGE
# ==================================================
st.set_page_config(
    page_title="ROC – Liste de présence",
    layout="wide"
)

# ==================================================
# STYLE GLOBAL
# ==================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}
h1 { color: #2ecc71 !important; }
h2, h3 {
    color: #ffd27f !important;
    font-size: 1.1rem !important;
    text-transform: uppercase;
}
p, label { color: white !important; }
button {
    background-color: #2ecc71 !important;
    color: black !important;
    font-weight: bold !important;
    border-radius: 8px !important;
}
.copy-btn {
    background-color: #3498db !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 8px !important;
    padding: 8px 16px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# SESSION STATES
# ==================================================
if "entree" not in st.session_state:
    st.session_state.entree = False

if "admin" not in st.session_state:
    st.session_state.admin = False

# ==================================================
# ÉCRAN DE BIENVENUE
# ==================================================
if not st.session_state.entree:
    st.markdown("""
    <div style="display:flex;flex-direction:column;
                justify-content:center;align-items:center;
                height:80vh;">
        <h1>Bienvenue au ROC 🎹</h1>
        <p>Application officielle de liste de présence</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Entrer"):
        st.session_state.entree = True

    st.stop()

# ==================================================
# 🔐 ACCÈS ADMIN
# ==================================================
with st.expander("🔐 Zone administrateur (modifications)"):
    code = st.text_input("Code admin", type="password")
    if code == "ROC2025":
        st.session_state.admin = True
        st.success("Mode administrateur activé")
    elif code:
        st.error("Code incorrect")

# ==================================================
# BASE DE DONNÉES
# ==================================================
bdd = {
    "Respo": ["Gricha", "Rodrigue", "Yeni"],
    "Soprano": [
        "Chariette", "Ruth", "Rebeca", "Emmanuella",
        "Irssa", "Maman Angèle"
    ],
    "Altos": [
        "Radegonde", "Emy-Grâce", "Nell", "Tessa",
        "Andréa", "Lydia", "Amandine", "Stessy",
        "Nady-Grâce", "Alice", "Dalie", "Clara"
    ],
    "Tenors": [
        "Jaurès", "Christ", "Gloire", "Jadel",
        "Harold", "Christian Joël", "Jordan"
    ],
    "Musiciens": [
        "Jaifry", "Lionnel", "Esdras",
        "Laure-Naïké", "Thierry", "Joyce"
    ],
    "Son": ["Emmanuel", "Sullyvan"],
}

# ==================================================
# SEXE
# ==================================================
sexe = {
    "Gricha": "H", "Rodrigue": "H", "Jordan": "H",
    "Jaifry": "H", "Lionnel": "H", "Esdras": "H",
    "Thierry": "H", "Joyce": "H", "Emmanuel": "H",
    "Jadel": "H", "Christian Joël": "H"
}

# ==================================================
# TITRE
# ==================================================
st.markdown("<h1>Liste de présence – ROC</h1>", unsafe_allow_html=True)
st.markdown(f"<p>Date : {date.today().strftime('%d/%m/%Y')}</p>", unsafe_allow_html=True)
st.markdown("---")

# ==================================================
# SÉLECTION DES PRÉSENTS
# ==================================================
selection = {}

for pupitre, noms in bdd.items():
    st.subheader(pupitre)
    selection[pupitre] = st.multiselect("", noms, key=pupitre)

# ==================================================
# VALIDATION + SAUVEGARDE
# ==================================================
if st.button("Valider la liste"):

    presents = {n for noms in selection.values() for n in noms}
    tous = {n for noms in bdd.values() for n in noms}
    absents = sorted(tous - presents)

    hommes = sum(1 for n in presents if sexe.get(n) == "H")
    femmes = len(presents) - hommes

    st.markdown("---")

    for pupitre, noms in selection.items():
        if noms:
            st.subheader(pupitre)
            for nom in noms:
                st.markdown(f"🟢 {nom}")

    st.subheader("Absents")
    for nom in absents:
        st.markdown(f"🔴 {nom}")

    st.subheader("Totaux des présents")
    st.markdown(f"Femmes : {femmes}")
    st.markdown(f"Hommes : {hommes}")
    st.markdown(f"Total : {len(presents)}")

    texte = (
        f"Liste de présence – ROC\n"
        f"Date : {date.today().strftime('%d/%m/%Y')}\n\n"
    )

    for pupitre, noms in selection.items():
        if noms:
            texte += f"{pupitre}\n"
            for nom in noms:
                texte += f"🟢 {nom}\n"
            texte += "\n"

    texte += "Absents\n"
    for nom in absents:
        texte += f"🔴 {nom}\n"

    texte += (
        f"\nTotaux des présents\n"
        f"Femmes : {femmes}\n"
        f"Hommes : {hommes}\n"
        f"Total : {len(presents)}"
    )

    os.makedirs("sauvegardes", exist_ok=True)
    fichier = f"sauvegardes/ROC_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(texte)

    st.text_area("📋 Liste finale (copiable)", texte, height=420)


   
