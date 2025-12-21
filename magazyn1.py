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

    # 2. Stylizacja CSS (Kolory i tło z ciężarówką)
    st.markdown("""
        <style>
        /* Tło z ciężarówką */
        .stApp {
            background: linear-gradient(rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.1)), 
            url("https://images.unsplash.com/photo-1519003722824-194d4455a60c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        /* Stylizacja nagłówka głównego */
        .main-title {
            font-size: 50px !important;
            font-weight: 700 !important;
            color: #1E1E1E !important;
            text-align: center;
            margin-bottom: 30px;
            text-transform: lowercase;
        }

        /* Półprzezroczyste kontenery dla czytelności */
        div[data-testid="stVerticalBlock"] > div:has(div.stMetric), 
        .stForm, .stDataFrame {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        /* Stylizacja przycisków */
        .stButton>button {
            border-radius: 8px;
            border: none;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    # Napis na górze (bez nawiasów i ikon)
    st.markdown('<p class="main-title">magazyn</p>', unsafe_allow_html=True)

    # Wczytanie danych
    inventory_df = load_data()

    # --- STATYSTYKI ---
    total_types = len(inventory_df)
    total_units = inventory_df['Ilość'].sum() if not inventory_df.empty else 0

    col1, col2 = st.columns(2)
    col1.metric("Rodzaje towarów", total_types)
    col2.metric("Suma sztuk", total_units)

    st.write("") # Odstęp

    # --- DODAWANIE ---
    with st.form("add_form", clear_on_submit=True):
        st.subheader("Dodaj nową dostawę")
        c1, c2 = st.columns([3, 1])
        name_input = c1.text_input("Nazwa przedmiotu")
        qty_input = c2.number_input("Ilość", min_value=1, step=1)
        
        if st.form_submit_button("Zatwierdź"):
            if name_input.strip():
                new_entry = pd.DataFrame([{'Nazwa': name_input.strip(), 'Ilość': int(qty_input)}])
                updated_df = pd.concat([inventory_df, new_entry], ignore_index=True)
                save_data(updated_df)
            else:
                st.error("Wpisz nazwę!")

    # --- WYŚWIETLANIE I USUWANIE ---
    if not inventory_df.empty:
        st.write("")
        st.subheader("Aktualna lista")
        
        display_df = inventory_df.copy()
        display_df.insert(0, 'ID', range(1, len(display_df) + 1))
        
        # Tabela
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Usuwanie
        with st.expander("Panel zarządzania"):
            id_to_del = st.selectbox("Wybierz ID do usunięcia", display_df['ID'].tolist())
            if st.button("Usuń trwale", type="primary"):
                updated_df = inventory_df.drop(inventory_df.index[id_to_del - 1]).reset_index(drop=True)
                save_data(updated_df)
    else:
        st.info("Brak towarów w magazynie.")

if __name__ == "__main__":
    main()
