
import streamlit as st
import pandas as pd

def show(conso_df, prod_df):
    st.title("Vue d'ensemble des données énergétiques")

    # --- Nettoyage consommation ---
    st.subheader("Consommation quotidienne")
    
    # Supprimer les lignes avec NaN sur les colonnes essentielles
    cols_keep = ['Consommation gaz (MW PCS)',
                 'Consommation élec (MW)',
                 'Consommation totale (MW)',
                 'Datetime']
    conso_clean = conso_df[cols_keep].dropna()
    
    st.write("Aperçu des données de consommation (quelques lignes) :")
    st.dataframe(conso_clean.head(10))

    # Graphique ligne par demi-heure / heure
    st.subheader("Graphique de la consommation quotidienne")
    conso_indexed = conso_clean.set_index('Datetime')
    
    # Optionnel : resample journalier pour lisibilité
    conso_daily = conso_indexed.resample('D').mean()

    st.line_chart(conso_daily[[
        'Consommation gaz (MW PCS)',
        'Consommation élec (MW)',
        'Consommation totale (MW)'
    ]])

    # --- Parc éolien et solaire ---
    st.subheader("Aperçu du parc éolien et solaire")
    st.write("Aperçu des données du parc installé :")
    st.dataframe(prod_df.head(10))

    st.subheader("Évolution du parc installé")
    st.line_chart(prod_df.set_index('Annee')[['Parc installé éolien (MW)', 'Parc installé solaire (MW)']])
