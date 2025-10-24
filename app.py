import streamlit as st
from sections import intro, overview, deep_dives, conclusions
from utils.io import load_conso, load_prod

# --- Page config ---
st.set_page_config(
    page_title="Énergie France",
    layout="wide",
    page_icon="⚡"
)

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
section = st.sidebar.radio("Aller à", ["Introduction", "Vue d'ensemble", "Analyses détaillées", "Conclusions"])

# --- Charger les données ---
@st.cache_data
def load_data():
    conso = load_conso("data/consommation-quotidienne-brute.csv")
    prod = load_prod("data/parc-national-annuel-prod-eolien-solaire.csv")

    # Renommer les colonnes pour simplifier
    conso.rename(columns={
        'Consommation brute électricité (MW) - RTE': 'Consommation élec (MW)',
        'Consommation brute gaz totale (MW PCS 0°C)': 'Consommation gaz (MW PCS)',
        'Consommation brute totale (MW)': 'Consommation totale (MW)'
    }, inplace=True)

    return conso, prod

conso_df, prod_df = load_data()

# --- Afficher la section choisie ---
if section == "Introduction":
    intro.show()
elif section == "Vue d'ensemble":
    overview.show(conso_df, prod_df)
elif section == "Analyses détaillées":
    deep_dives.show(conso_df, prod_df)
elif section == "Conclusions":
    conclusions.show()
