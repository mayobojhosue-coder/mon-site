import streamlit as st

# =========================
# ÉCRAN DE BIENVENUE (3s)
# =========================
st.markdown("""
<style>
#splash {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: black;
    color: white;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    font-weight: bold;
}
</style>

<div id="splash">
    Bienvenue sur BLOOM 🌸
</div>

<script>
setTimeout(function() {
    var splash = document.getElementById("splash");
    splash.style.display = "none";
}, 3000);
</script>
""", unsafe_allow_html=True)

# =========================
# STYLE (BOUTON VERT)
# =========================
st.markdown("""
<style>
div.stButton > button {
    background-color: #2ecc71;
    color: white;
    font-size: 16px;
    height: 3em;
    width: 100%;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGO
# =========================
st.image("logo.png", width=200)

# =========================
# TITRE
# =========================
st.title("Liste de présence BLOOM 🌸")

# =========================
# BASE DE DONNÉES FIXE
# =========================
garcons = [
    "andré",
    "arthur",
    "aurel",
    "darlick",
    "iknan",
    "jéremie",
    "jhosue",
    "alain emmanuel",
    "karl emmanuel",
    "stephen",
    "yvan",
    "evans",
]

filles = [
    "angèele",
    "camille",
    "helena",
    "joëlle",
