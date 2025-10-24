# sections/deep_dives.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px

def show(conso_df, prod_df):
    st.title("Detailed Analyses & Storytelling")

    # -------------------------------
    # Sidebar controls
    # -------------------------------
    st.sidebar.header("Filters")
    min_date = conso_df['Datetime'].min().date()
    max_date = conso_df['Datetime'].max().date()
    
    # Date range filter
    start_date, end_date = st.sidebar.slider(
        "Select date range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="DD/MM/YYYY"
    )
    
    # Variable selection
    variables = st.sidebar.multiselect(
        "Select variables to display",
        options=['Consommation élec (MW)', 'Consommation gaz (MW PCS)', 'Consommation totale (MW)'],
        default=['Consommation élec (MW)', 'Consommation gaz (MW PCS)', 'Consommation totale (MW)']
    )
    
    # Filtered data
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    conso_filtered = conso_df[(conso_df['Datetime'] >= start_date) & (conso_df['Datetime'] <= end_date)]

    # -------------------------------
    # Data quality section
    # -------------------------------
    st.subheader("Data Quality Check")
    st.markdown("Missing values, duplicates, and basic validation:")
    
    missing = conso_filtered.isna().sum()
    st.write("**Missing values per column:**")
    st.dataframe(missing)
    
    duplicates = conso_filtered.duplicated().sum()
    st.write(f"**Number of duplicate rows:** {duplicates}")
    
    # Simple validation example: consumption should be ≥0
    invalid_values = (conso_filtered[variables] < 0).sum()
    st.write("**Invalid negative values:**")
    st.dataframe(invalid_values)
    
    # -------------------------------
    # KPI metrics
    # -------------------------------
    st.subheader("Key Metrics (based on filters)")
    total_elec = conso_filtered['Consommation élec (MW)'].sum()
    total_gas = conso_filtered['Consommation gaz (MW PCS)'].sum()
    total_consumption = conso_filtered['Consommation totale (MW)'].sum()
    
    # Estimate renewable %: total installed capacity vs peak electricity
    prod_df['Production verte (MW)'] = prod_df['Parc installé éolien (MW)'] + prod_df['Parc installé solaire (MW)']
    max_renewable_capacity = prod_df['Production verte (MW)'].max()
    pct_renewable = min(max_renewable_capacity / total_elec * 100, 100) if total_elec > 0 else 0
    
    st.metric("Total Electricity (MW)", f"{total_elec:,.0f}")
    st.metric("Total Gas (MW PCS)", f"{total_gas:,.0f}")
    st.metric("Total Consumption (MW)", f"{total_consumption:,.0f}")
    st.metric("Approx. % Renewable Capacity", f"{pct_renewable:.1f}%")

    # -------------------------------
    # Interactive line chart for selected variables
    # -------------------------------
    st.subheader("Consumption over selected period")
    if variables:
        fig = px.line(
            conso_filtered,
            x='Datetime',
            y=variables,
            title="Consumption over time",
            labels={'value': 'MW', 'variable': 'Energy Type'},
            markers=True
        )
        fig.update_layout(template='plotly_white', hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Hourly consumption bar chart
    # -------------------------------
    st.subheader("Average Hourly Consumption")
    conso_filtered['Hour'] = conso_filtered['Datetime'].dt.hour
    hourly_group = conso_filtered.groupby('Hour')[variables].mean().reset_index()
    fig = px.bar(
        hourly_group,
        x='Hour',
        y=variables,
        title="Average consumption by hour",
        labels={'value': 'MW', 'variable': 'Energy Type'},
        barmode='group'
    )
    fig.update_layout(template='plotly_white', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Peak electricity vs installed renewable (from 2012)
    # -------------------------------
    st.subheader("Annual Peak Electricity vs Installed Renewable Capacity")
    conso_2012 = conso_df[conso_df['Datetime'].dt.year >= 2012].copy()
    prod_2012 = prod_df[prod_df['Annee'] >= 2012].copy()
    
    conso_2012['Year'] = conso_2012['Datetime'].dt.year
    peak_yearly = conso_2012.groupby('Year')['Consommation élec (MW)'].max().reset_index()
    prod_2012['Production verte (MW)'] = prod_2012['Parc installé éolien (MW)'] + prod_2012['Parc installé solaire (MW)']
    prod_yearly = prod_2012[['Annee', 'Production verte (MW)']].rename(columns={'Annee':'Year'})
    
    merged_yearly = pd.merge(peak_yearly, prod_yearly, on='Year', how='inner')
    
    fig = px.line(
        merged_yearly,
        x='Year',
        y=['Consommation élec (MW)', 'Production verte (MW)'],
        title="Peak Annual Electricity vs Installed Renewable",
        labels={'value': 'MW', 'variable': 'Energy Type'},
        markers=True
    )
    fig.update_layout(template='plotly_white', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Small multiples 
    # -------------------------------
    st.subheader("Small Multiples by Variable")
    if len(variables) > 1:
        fig = px.line(
            conso_filtered.melt(id_vars='Datetime', value_vars=variables),
            x='Datetime',
            y='value',
            facet_col='variable',
            title="Consumption small multiples",
            labels={'value': 'MW', 'Datetime': 'Date'}
        )
        fig.update_layout(template='plotly_white', hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
