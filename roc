import streamlit as st
from datetime import date

# ==================================================
# CONFIG PAGE (DOIT ÊTRE TOUT EN HAUT)
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

/* Titre principal */
h1 {
    color: #2ecc71 !important;
}

/* Sous-titres (pupitres) */
h2, h3 {
    color: #ffd27f !important;
    font-size: 1.1rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Texte normal */
p, label {
    color: white !important;
    font-size: 1rem !important;
}

/* Boutons */
button {
    background-color: #2ecc71 !important;
    color: black !important;
    font-weight: bold !important;
    border-radius: 8px !important;
}

/* Bouton copier (bleu visuel) */
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
# ÉTAT SESSION (ACCUEIL)
# ==================================================
if "entree" not in st.session_state:
    st.session_state.entree = False

# ==================================================
# ÉCRAN DE BIENVENUE
# ==================================================
if not st.session_state.entree:
    st.markdown("""
    <div style="display:flex;
                flex-direction:column;
                justify-content:center;
                align-items:center;
                height:80vh;">
        <h1>Bienvenue au ROC 🎹</h1>
        <p style="font-size:1.2rem;">
            Application officielle de liste de présence
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Entrer"):
        st.session_state.entree = True

    # IMPORTANT : bloque le reste de l'app
    st.stop()

# ==================================================
# BASE DE DONNÉES (FIXE)
# ==================================================
bdd = {
    "Respo": ["Gricha", "Rodrigue"],
    "Soprano": [
        "Chariette", "Ruth", "Rebeca", "Emmanuella",
        "Irssa", "Maman Angèle", "Alice", "Sullyvan"
    ],
    "Altos": [
        "Radegonde", "Emy-Grâce", "Nell", "Tessa",
        "Andréa", "Lydia", "Amandine", "Stessy", "Nady-Grâce"
    ],
    "Tenors": [
        "Jaurès", "Christ", "Gloire", "Jadel",
        "Harold", "Christ Joël", "Jordan"
    ],
    "Musiciens": [
        "Jaifry", "Lionnel", "Esdras",
        "Laure-Naïké", "Thierry", "Joyce"
    ],
    "Son": ["Emmanuel"],
}

# ==================================================
# SEXE (UTILISÉ UNIQUEMENT POUR LES TOTAUX)
# ==================================================
sexe = {
    "Gricha": "H", "Rodrigue": "H", "Jordan": "H",
    "Jaifry": "H", "Lionnel": "H", "Esdras": "H",
    "Thierry": "H", "Joyce": "H", "Emmanuel": "H",
    # Tous les autres = femmes par défaut
}

# ==================================================
# TITRE + DATE AUTOMATIQUE
# ==================================================
st.markdown("<h1>Liste de présence – ROC</h1>", unsafe_allow_html=True)
st.markdown(
    f"<p>Date : {date.today().strftime('%d/%m/%Y')}</p>",
    unsafe_allow_html=True
)

st.markdown("---")

# ==================================================
# SÉLECTION DES PRÉSENTS (CLIC UNIQUEMENT)
# ==================================================
st.markdown("### Sélectionnez les présents puis cliquez sur **Valider**")

selection = {}

for pupitre, noms in bdd.items():
    st.subheader(pupitre)
    selection[pupitre] = st.multiselect(
        label="",
        options=noms,
        key=pupitre
    )

# ==================================================
# VALIDATION
# ==================================================
if st.button("Valider la liste"):

    # Présents
    presents = {nom for noms in selection.values() for nom in noms}

    # Tous les noms
    tous = {nom for noms in bdd.values() for nom in noms}

    # Absents
    absents = sorted(tous - presents)

    st.markdown("---")

    # ==============================
    # AFFICHAGE PRÉSENTS PAR PUPITRE
    # ==============================
    for pupitre, noms in selection.items():
        if noms:
            st.subheader(pupitre)
            for nom in noms:
                st.markdown(f"🟢 {nom}")

    # ==============================
    # AFFICHAGE ABSENTS (SANS PUPITRE)
    # ==============================
    st.subheader("Absents")
    for nom in absents:
        st.markdown(f"🔴 {nom}")

    # ==============================
    # TOTAUX (NUMÉRIQUES UNIQUEMENT)
    # ==============================
    hommes = 0
    femmes = 0

    for nom in presents:
        if sexe.get(nom) == "H":
            hommes += 1
        else:
            femmes += 1

    st.markdown("---")
    st.subheader("Totaux des présents")
    st.markdown(f"Femmes : {femmes}")
    st.markdown(f"Hommes : {hommes}")
    st.markdown(f"Total : {len(presents)}")

    # ==============================
    # TEXTE FINAL COPIABLE
    # ==============================
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

    st.text_area(
        "📋 Liste finale (copiable)",
        texte,
        height=420
    )

    st.markdown(
        "<div class='copy-btn'>👉 Sélectionnez le texte ci-dessus et copiez</div>",
        unsafe_allow_html=True
    )
