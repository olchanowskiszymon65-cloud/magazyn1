import streamlit as st
import pandas as pd
import os

# --- 1. KONFIGURACJA STRONY (Musi być na samej górze!) ---
st.set_page_config(page_title="magazyn", layout="centered")

FILE_PATH = "inventory.csv"

# --- 2. FUNKCJE ZAPISU I ODCZYTU (CSV) ---
def load_data():
    if os.path.exists(FILE_PATH):
        try:
            df = pd.read_csv(FILE_PATH)
            if not df.empty:
                # Konwersja ilości na liczby całkowite
                df['Ilość'] = pd.to_numeric(df['Ilość'], errors='coerce').fillna(0).astype(int)
            return df
        except:
            return pd.DataFrame({'Nazwa': [], 'Ilość': []})
    return pd.DataFrame({'Nazwa': [], 'Ilość': []})

def save_data(df):
    df.to_csv(FILE_PATH, index=False)
    st.rerun()

# --- 3. STYLIZACJA CSS (Tło, Czcionki, Kolory) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    /* Główna czcionka Montserrat */
    html, body, [class*="css"], .stMarkdown, p, div, label {
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Tło: Europejska ciężarówka w firmie logistycznej */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
        url("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Napis magazyn na górze */
    .main-title {
        font-size: 80px !important;
        font-weight: 700 !important;
        color: white !important;
        text-align: center;
        margin-top: -50px;
        margin-bottom: 30px;
        text-transform: lowercase;
        letter-spacing: -2px;
    }

    /* Białe kontenery dla czytelności treści */
    [data-testid="stMetric"], .stForm, .stDataFrame, [data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.96) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        color: #1a1a1a !important;
    }

    /* Kolor tekstów w metrykach i etykietach */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"], label {
        color: #1a1a1a !important;
    }

    /* Zielony przycisk dodawania */
    div.stButton > button:first-child {
        background-color: #2E7D32 !important;
        color: white !important;
        width: 100%;
        font-weight: 700 !important;
        border: none !important;
        height: 3em !important;
    }

    /* Czerwony przycisk usuwania */
    [data-testid="stExpander"] button {
        background-color: #C62828 !important;
        color: white !important;
        width: 100%;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTERFEJS UŻYTKOWNIKA ---

# Wyświetlenie tytułu
st.markdown('<h1 class="main-title">magazyn</h1>', unsafe_allow_html=True)

# Wczytanie danych
df = load_data()

# Statystyki na górze
total_types = len(df)
total_qty = df['Ilość'].sum() if not df.empty else 0

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Rodzaje produktów", value=total_types)
with col2:
    st.metric(label="Suma wszystkich sztuk", value=total_qty)

st.write("")

# Formularz dodawania towaru
with st.form(key='dodaj_form', clear_on_submit=True):
    st.markdown("### 📥 Przyjęcie towaru")
    nazwa = st.text_input("Nazwa przedmiotu", placeholder="Wpisz nazwę...")
    ilosc = st.number_input("Ilość (szt)", min_value=1, step=1)
    submit = st.form_submit_button(label="ZATWIERDŹ DOSTAWĘ")

    if submit:
        if nazwa.strip():
            nowy_towar = pd.DataFrame([{'Nazwa': nazwa.strip(), 'Ilość': int(ilosc)}])
            df_updated = pd.concat([df, nowy_towar], ignore_index=True)
            save_data(df_updated)
        else:
            st.error("Błąd: Wpisz nazwę towaru!")

# Wyświetlanie tabeli i opcja usuwania
if not df.empty:
    st.markdown("### 📦 Stan ewidencji")
    
    # Przygotowanie tabeli z ID
    df_pokaz = df.copy()
    df_pokaz.insert(0, 'ID', range(1, len(df_pokaz) + 1))
    
    st.dataframe(df_pokaz, use_container_width=True, hide_index=True)

    # Panel usuwania
    with st.expander("🗑️ Zarządzanie brakami / Usuwanie"):
        wybor_id = st.selectbox("Wybierz ID do usunięcia", options=df_pokaz['ID'].tolist())
        if st.button("USUŃ TRWALE Z SYSTEMU"):
            # Indeks w pandas to ID - 1
            df_final = df.drop(df.index[wybor_id - 1]).reset_index(drop=True)
            save_data(df_final)
else:
    st.info("Magazyn jest pusty. Użyj formularza powyżej, aby dodać towary.")
