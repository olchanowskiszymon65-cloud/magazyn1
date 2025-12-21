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
    df.to_csv(FILE_PATH, index=False)
    st.rerun()

# --- STYLIZACJA I WYGLĄD ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    /* Czcionka dla całej strony */
    html, body, [class*="css"], .stMarkdown, p, div, label {
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Tło: Europejska ciężarówka w firmie */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
        url("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Główny napis magazyn */
    .title-text {
        font-size: 70px !important;
        font-weight: 700 !important;
        color: white !important;
        text-align: center;
        margin-top: -60px;
        padding-bottom: 20px;
        text-transform: lowercase;
    }

    /* Białe kontenery dla kontrastu */
    [data-testid="stMetric"], .stForm, .stDataFrame, [data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4) !important;
    }

    /* Napisy w tabelach i formularzach */
    h1, h2, h3, p, label {
        color: #1a1a1a !important;
    }

    /* Przyciski */
    .stButton>button {
        width: 100%;
        font-weight: 700 !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INTERFEJS UŻYTKOWNIKA ---

# Napis na górze
st.markdown('<p class="title-text">magazyn</p>', unsafe_allow_html=True)

# Wczytanie danych
df = load_data()

# Statystyki
total_types = len(df)
total_qty = df['Ilość'].sum() if not df.empty else 0

c1, c2 = st.columns(2)
with c1:
    st.metric("Rodzaje towarów", total_types)
with c2:
    st.metric("Suma sztuk", total_qty)

st.write("")

# Formularz dodawania
with st.form("dodaj_towar", clear_on_submit=True):
    st.markdown("### 📥 Nowa dostawa")
    nazwa = st.text_input("Nazwa przedmiotu", placeholder="np. Opony ciężarowe")
    ilosc = st.number_input("Ilość (szt)", min_value=1, step=1)
    przycisk = st.form_submit_button("DODAJ DO MAGAZYNU")

    if przycisk and nazwa:
        nowy_wiersz = pd.DataFrame([{'Nazwa': nazwa.strip(), 'Ilość': int(ilosc)}])
        df_updated = pd.concat([df, nowy_wiersz], ignore_index=True)
        save_data(df_updated)
    elif przycisk:
        st.error("Wpisz nazwę produktu!")

# Tabela i Usuwanie
if not df.empty:
    st.markdown("### 📦 Aktualna ewidencja")
    
    # Przygotowanie tabeli
    df_pokaz = df.copy()
    df_pokaz.insert(0, 'ID', range(1,
