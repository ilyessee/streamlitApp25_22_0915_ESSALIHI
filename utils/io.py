import pandas as pd
import streamlit as st

@st.cache_data
def load_conso(path="data/consommation-quotidienne-brute.csv"):
    """
    Charger et nettoyer les données de consommation quotidienne.
    Combine Date + Heure en Datetime et supprime les lignes avec des NaN importantes.
    """
    df = pd.read_csv(path, sep=";")

    # Supprimer colonne inutile
    df = df.drop(columns=['Date - Heure'])

    # Combiner Date + Heure en Datetime
    df['Datetime'] = pd.to_datetime(
        df['Date'].astype(str).str.strip() + ' ' + df['Heure'].astype(str).str.strip(),
        dayfirst=True,
        errors='coerce'
    )
    df = df.drop(columns=['Date', 'Heure'])

    # Supprimer les lignes avec NaN dans les colonnes critiques
    df = df.dropna(subset=[
        'Consommation brute gaz totale (MW PCS 0°C)',
        'Consommation brute électricité (MW) - RTE',
        'Consommation brute totale (MW)'
    ])

    # Trier par Datetime
    df = df.sort_values('Datetime').reset_index(drop=True)

    return df

@st.cache_data
def load_prod(path="data/parc-national-annuel-prod-eolien-solaire.csv"):
    """
    Charger et nettoyer les données du parc éolien et solaire.
    """
    df = pd.read_csv(path, sep=";")
    
    # Nettoyer les noms de colonnes
    df.columns = [c.strip() for c in df.columns]
    
    # Colonnes numériques
    numeric_cols = ['Parc installé éolien (MW)', 'Parc installé solaire (MW)']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Trier par année
    df = df.sort_values('Annee').reset_index(drop=True)
    
    return df
