import streamlit as st
from datetime import date
import unicodedata
import time

# ======================
# 🎨 DESIGN GLOBAL
# ======================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

h1, h2, h3 {
    color: #f1c40f;
    text-align: center;
}

textarea {
    border-radius: 10px !important;
    border: 2px solid #f1c40f !important;
}

div.stButton > button {
    background-color: #2ecc71;
    color: black;
    font-weight: bold;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ======================
# 👋 MESSAGE DE BIENVENUE
# ======================
if "welcome_done" not in st.session_state:
    st.session_state.welcome_done = False

if not st.session_state.welcome_done:
    st.markdown("""
    <div style="
        position: fixed;
        top: 0; left: 0;
        width: 100%;
        height: 100%;
        background-color: black;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    ">
        <h1 style="color:white; font-size:40px;">
            Bienvenue sur BLOOM 🌸
        </h1>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(3)
    st.session_state.welcome_done = True
    st.rerun()

# ======================
# 🧠 FONCTIONS
# ======================
def nettoyer(nom):
    nom = nom.lower().strip()
    nom = unicodedata.normalize("NFD", nom)
    return "".join(c for c in nom if unicodedata.category(c) != "Mn")

# ======================
# 📅 DATE
# ======================
date_choisie = st.date_input("📅 Choisis la date", value=date.today())
jour = date_choisie.weekday()
date_affichage = date_choisie.strftime("%d/%m/%Y")

if jour == 2:
    titre = "Liste de présence BLOOM au MDP"
elif jour == 5:
    titre = "Liste de présence BLOOM – Réunion des jeunes"
elif jour == 6:
    titre = "Liste de présence BLOOM – Culte du dimanche"
else:
    titre = "Liste de présence BLOOM"

st.title(titre)

# ======================
# 📦 BASE DE DONNÉES FIXE
# ======================
garcons = [
    "André","Arthur","Aurel","Darlick","Iknan","Jéremie",
    "Jhosue","Alain Emmanuel","Karl Emmanuel",
    "Stephen","Yvan","Evans"
]

filles = [
    "Angèle","Camille","Helena","Joëlle","Josée",
    "Julyahana","Ketlyn","Maïva","Mariska","Romaine",
    "Kenza","Ketsia","Chrismaëlla","Jade","Daliah","Méléa"
]

coachs = ["Noelvine", "Jean Junior", "Valerie"]

# ======================
# ✍️ SAISIE UTILISATEUR
# ======================
if "texte_presents" not in st.session_state:
    st.session_state.texte_presents = ""

st.session_state.texte_presents = st.text_area(
    "✍️ Écris les noms des présents (un par ligne)",
    st.session_state.texte_presents
)

# ======================
# 🔘 BOUTONS
# ======================
col1, col2 = st.columns(2)

with col1:
    valider = st.button("Valider")

with col2:
    if st.button("Réinitialiser"):
        st.session_state.texte_presents = ""
        st.rerun()

# ======================
# 📋 TRAITEMENT
# ======================
if valider:
    saisis = [nettoyer(n) for n in st.session_state.texte_presents.split("\n") if n.strip()]

    def traiter(liste):
        presents = [n for n in liste if nettoyer(n) in saisis]
        absents = [n for n in liste if nettoyer(n) not in saisis]
        return presents, absents

    pg, ag = traiter(garcons)
    pf, af = traiter(filles)
    pc, ac = traiter(coachs)

    liste_finale = (
        titre.upper() + "\n"
        + "=" * len(titre) + "\n"
        + f"Date : {date_affichage}\n\n"

        + "GARÇONS PRÉSENTS\n"
        + "\n".join("✅ " + nom for nom in pg)
        + "\n\nGARÇONS ABSENTS\n"
        + "\n".join("❌ " + nom for nom in ag)

        + "\n\nFILLES PRÉSENTES\n"
        + "\n".join("✅ " + nom for nom in pf)
        + "\n\nFILLES ABSENTES\n"
        + "\n".join("❌ " + nom for nom in af)

        + "\n\nCOACHS PRÉSENTS\n"
        + "\n".join("✅ Coach " + nom for nom in pc)
        + "\n\nCOACHS ABSENTS\n"
        + "\n".join("❌ Coach " + nom for nom in ac)
    )

    st.subheader("Liste finale")
    st.text_area("", liste_finale, height=500)
