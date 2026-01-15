import streamlit as st
from datetime import date, datetime

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
h1 { color: #2ecc71 !important; text-align:center; }
h2, h3, label, p {
    color: orange !important;
}
button {
    background-color: #2ecc71 !important;
    color: black !important;
    font-weight: bold !important;
    border-radius: 10px !important;
}
.big-btn button {
    width: 260px !important;
    height: 90px !important;
    font-size: 22px !important;
    border-radius: 50% !important;
}
.center {
    display:flex;
    justify-content:center;
    align-items:center;
    flex-direction:column;
}
.success-msg {
    color:#2ecc71;
    font-size:28px;
    font-weight:bold;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# SESSION STATE
# ==================================================
if "step" not in st.session_state:
    st.session_state.step = "welcome"

if "nom" not in st.session_state:
    st.session_state.nom = ""

if "heure" not in st.session_state:
    st.session_state.heure = {}

# ==================================================
# BASE DE DONNÉES
# ==================================================
bdd = {
    "Respo": ["Gricha", "Rodrigue", "Yeni"],
    "Soprano": ["Chariette", "Ruth", "Rebeca", "Emmanuella", "Irssa", "Maman Angèle"],
    "Altos": ["Radegonde", "Emy-Grâce", "Nell", "Tessa", "Andréa", "Lydia", "Amandine", "Stessy", "Nady-Grâce", "Dalie Clara", "Alice"],
    "Tenors": ["Jaurès", "Christ", "Gloire", "Jadel", "Harold", "Christian Joël", "Jordan"],
    "Musiciens": ["Jaifry", "Lionnel", "Laure-Naïké", "Thierry", "Joyce"],
    "Son": ["Emmanuel"]
}

sexe = {
    "Gricha":"H","Rodrigue":"H","Yeni":"H","Jaurès":"H","Christ":"H","Gloire":"H",
    "Jaden":"H","Harold":"H","Christian Joël":"H","Jordan":"H",
    "Jaifry":"H","Lionnel":"H","Esdras":"H","Thierry":"H","Joyce":"F","Emmanuel":"H"
}

# ==================================================
# ÉCRAN 1 – BIENVENUE
# ==================================================
if st.session_state.step == "welcome":
    st.markdown("""
    <div class="center" style="height:80vh;">
        <h1>Bienvenue au ROC 🎹</h1>
        <p style="color:white;">Application officielle de liste de présence</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Entrer"):
        st.session_state.step = "nom"
    st.stop()

# ==================================================
# ÉCRAN 2 – SAISIE NOM
# ==================================================
if st.session_state.step == "nom":
    st.markdown("<h2>Veuillez entrer votre nom</h2>", unsafe_allow_html=True)
    nom = st.text_input("Nom")

    if st.button("Valider mon nom"):
        nom_clean = nom.strip().title()
        tous = [n for groupe in bdd.values() for n in groupe]
        if nom_clean in tous:
            st.session_state.nom = nom_clean
            st.session_state.step = "heure"
        else:
            st.error("Nom non reconnu")

    st.stop()

# ==================================================
# ÉCRAN 3 – HEURE D’ARRIVÉE
# ==================================================
if st.session_state.step == "heure":
    st.markdown("<h2>Bonjour 👋</h2>", unsafe_allow_html=True)
    st.markdown("<p>Clique sur le bouton pour enregistrer ton heure</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("### Bonjour")
    with col2:
        if st.button("🟢 Heure d’arrivée", key="heure_btn"):
            st.session_state.heure[st.session_state.nom] = datetime.now().strftime("%H:%M")
            if st.session_state.nom == "Dalie Clara":
                st.session_state.step = "liste"
            else:
                st.session_state.step = "fin"

    st.stop()

# ==================================================
# ÉCRAN 4 – MESSAGE FINAL (NON DALIE)
# ==================================================
if st.session_state.step == "fin":
    prefix = "Bonne répétition"
    if st.session_state.nom in bdd["Respo"]:
        prefix = "Bonne répétition Respo"

    st.markdown(f"""
    <div class="center" style="height:70vh;">
        <div class="success-msg">{prefix} {st.session_state.nom}</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ==================================================
# ÉCRAN 5 – LISTE DE PRÉSENCE (DALIE CLARA)
# ==================================================
st.markdown("<h1>Liste de présence – ROC</h1>", unsafe_allow_html=True)
st.markdown(f"<p>Date : {date.today().strftime('%d/%m/%Y')}</p>", unsafe_allow_html=True)

selection = {}
for pupitre, noms in bdd.items():
    st.subheader(pupitre)
    selection[pupitre] = st.multiselect("", noms, key=pupitre)

if st.button("Valider la liste"):
    presents = set()
    for noms in selection.values():
        presents.update(noms)

    tous = set(n for g in bdd.values() for n in g)
    absents = sorted(tous - presents)

    hommes = sum(1 for n in presents if sexe.get(n) == "H")
    femmes = len(presents) - hommes

    texte = f"Liste de présence – ROC\nDate : {date.today().strftime('%d/%m/%Y')}\n\n"

    for pupitre, noms in selection.items():
        if noms:
            texte += f"{pupitre}\n"
            for n in noms:
                heure = st.session_state.heure.get(n, "--:--")
                texte += f"🟢 {n} ({heure})\n"
            texte += "\n"

    texte += "Absents\n"
    for n in absents:
        texte += f"🔴 {n}\n"

    texte += f"\nTotaux des présents\nFemmes : {femmes}\nHommes : {hommes}\nTotal : {len(presents)}"

    st.text_area("📋 Liste finale (copiable)", texte, height=420)

