import streamlit as st
import pandas as pd
import os

# --- KONFIGURACJA STRONY (Musi być pierwsza!) ---
st.set_page_config(page_title="magazyn", layout="centered")

FILE_PATH = "inventory.csv"

# --- FUNKCJE LOGICZNE (Bez Session State) ---
def load_data():
    if os.path.exists(FILE_PATH):
        try:
            df = pd.read_csv(FILE_PATH)
            if not df.empty:
                df['Ilość'] = pd.to_numeric(df['Ilość'], errors='coerce').fillna(0).astype(int)
            return df
        except:
            return pd.DataFrame({'Nazwa': [], 'Ilość': []})
    return pd.DataFrame({'Nazwa': [], 'Ilość': []})

def save_data(df):
    try:
        df.to_csv(FILE_PATH, index=False)
        st.rerun()
    except Exception as e:
        st.error(f"Błąd zapisu: {e}")

# --- STYLIZACJA I WYGLĄD (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    /* Czcionka dla całej strony */
    html, body, [class*="css"], .stMarkdown, p, div, label {
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Tło: Europejska ciężarówka przy magazynie */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
        url("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Główny napis magazyn na górze */
    .title-text {
        font-size: 70px !important;
        font-weight: 700 !important;
        color: white !important;
        text-align: center;
        margin-top: -60px;
        padding-bottom: 20px;
        text-transform: lowercase;
    }

    /* Solidne kontenery dla czytelności */
    [data-testid="stMetric"], .stForm, .stDataFrame, [data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4) !important;
        color: #1a1a1a !important;
    }

    /* Stylizacja metryk */
    [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
    }

    /* Przycisk dodawania (Zielony) */
    .stButton>button {
        width: 100%;
        background-color: #2E7D32 !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
    }

    /* Przycisk usuwania (Czerwony) */
    [data-testid="stExpander"] button {
        background-color: #C62828 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INTERFEJS UŻYTKOWNIKA ---

# Napis na górze
st.markdown('<p class="title-text">magazyn</p>', unsafe_allow_html=True)

# Wczytanie danych z CSV
df = load_data()

# Obliczanie statystyk
total_types = len(df)
total_qty = df['Ilość'].sum() if not df.empty else 0

# Wyświetlanie statystyk w kolumnach
c1, c2 = st.columns(2)
with c1:
    st.metric("Rodzaje towarów", total_types)
with c2:
    st.metric("Suma wszystkich sztuk", total
