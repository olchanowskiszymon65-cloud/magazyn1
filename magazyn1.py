import streamlit as st
import pandas as pd
import os

# Nazwa pliku do przechowywania danych
FILE_PATH = "inventory.csv"

def load_data():
    if os.path.exists(FILE_PATH):
        try:
            df = pd.read_csv(FILE_PATH)
            if not df.empty:
                df['Ilość'] = pd.to_numeric(df['Ilość'], errors='coerce').fillna(0).astype(int)
            return df
        except Exception:
            return pd.DataFrame({'Nazwa': [], 'Ilość': []})
    return pd.DataFrame({'Nazwa': [], 'Ilość': []})

def save_data(df):
    df.to_csv(FILE_PATH, index=False)
    st.rerun()

def main():
    # 1. Konfiguracja strony
    st.set_page_config(page_title="magazyn", layout="centered")

    # 2. Zaawansowana stylizacja CSS
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

        /* Ustawienie czcionki dla całej aplikacji */
        html, body, [class*="css"], .stMarkdown, p, div {
            font-family: 'Montserrat', sans-serif !important;
        }

        /* Tło z europejską ciężarówką w magazynie */
        .stApp {
            background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), 
            url("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        /* Napis magazyn na górze */
        .main-title {
            font-family: 'Montserrat', sans-serif;
            font-size: 64px !important;
            font-weight: 700 !important;
            color: #ffffff !important;
            text-align: center;
            margin-top: -50px;
            margin-bottom: 20px;
            letter-spacing: 2px;
        }

        /* Kontenery z treścią - białe, solidne dla czytelności */
        [data-testid="stMetric"], .stForm, .stDataFrame, [data-testid="stExpander"] {
            background-color: rgba(255, 255, 255, 0.95) !important;
            padding: 20px !important;
            border-radius: 12px !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
            color: #1E1E1E !important;
        }
        
        /* Poprawa widoczności etykiet w metrykach */
        [data-testid="stMetricLabel"] {
            color: #444444 !important;
            font-weight: 600 !important;
        }

        /* Przycisk dodawania */
        .stButton>button {
            width: 100%;
            background-color: #2E7D32 !important;
            color: white !important;
            border: none !important;
            padding: 10px !important;
            font-weight: 700 !important;
        }

        /* Przycisk usuwania */
        [data-testid="stExpander"] button {
            background-color: #C62828 !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Czysty napis na górze
    st.markdown('<h1 class="main-title">magazyn</h1>', unsafe_allow_html=True)

    # Wczytanie danych z pliku (bez sesji)
    inventory_df = load_data()

    # --- STATYSTYKI ---
    total_types = len(inventory_df)
    total_units = inventory_df['Ilość'].sum() if not inventory_df.empty else 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Modele produktów", total_types)
    with col2:
        st.metric("Łączna ilość sztuk", total_units)

    st.write("") 

    # --- DODAWANIE ---
    with st.form("add_form", clear_on_submit=True):
        st.markdown("### 📥 Nowa dostawa")
        name_input = st.text_input("Nazwa przedmiotu", placeholder="np. Paleta EUR")
        qty_input = st.number_input("Ilość (szt.)", min_value=1, step=1)
        
        if st.form_submit_button("DODAJ DO MAGAZYNU"):
            if name_input.strip():
                new_entry = pd.DataFrame([{'Nazwa': name_input.strip(), 'Ilość': int(qty_input)}])
                updated_df = pd.concat([inventory_df, new_entry], ignore_index=True)
                save_data(updated_df)
            else:
                st.error("Wpisz nazwę produktu!")

    # --- LISTA I USUWANIE ---
    if not inventory_df.empty:
        st.write("")
        st.markdown("### 📦 Aktualny stan")
        
        display_df = inventory_df.copy()
        display_df.insert(0, 'ID', range(1, len(display_df) + 1))
        
        # Tabela danych
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Panel usuwania
        with st.expander("🗑️ Zarządzaj brakami / Usuń towar"):
            id_to_del = st.selectbox("Wybierz ID do usunięcia", display_df['ID'].tolist())
            if st.button("USUŃ Z EWIDENCJI"):
                updated_df = inventory_df.drop(inventory_df.index[id_to_del
