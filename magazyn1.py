import streamlit as st
import pandas as pd
import os

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="magazyn", layout="centered")

FILE_PATH = "inventory.csv"

# --- 2. FUNKCJE ZAPISU I ODCZYTU ---
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

# --- 3. STYLIZACJA CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    html, body, [class*="css"], .stMarkdown, p, div, label {
        font-family: 'Montserrat', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
        url("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

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

    [data-testid="stMetric"], .stForm, .stDataFrame, [data-testid="stExpander"], div[data-testid="stTextInput"] {
        background-color: rgba(255, 255, 255, 0.96) !important;
        padding: 15px !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        color: #1a1a1a !important;
    }

    [data-testid="stMetricValue"], [data-testid="stMetricLabel"], label {
        color: #1a1a1a !important;
    }

    /* Przycisk dodawania (zielony) */
    div.stButton > button:first-child {
        background-color: #2E7D32 !important;
        color: white !important;
        width: 100%;
        font-weight: 700 !important;
        border: none !important;
    }

    /* Przycisk usuwania (czerwony) */
    .stButton button[kind="secondary"] {
        color: #C62828 !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTERFEJS UŻYTKOWNIKA ---

st.markdown('<h1 class="main-title">magazyn</h1>', unsafe_allow_html=True)

df = load_data()

# Statystyki
total_types = len(df)
total_qty = df['Ilość'].sum() if not df.empty else 0

col_m1, col_m2 = st.columns(2)
col_m1.metric("Rodzaje towarów", total_types)
col_m2.metric("Łączna liczba sztuk", total_qty)

st.write("")

# --- WYSZUKIWARKA ---
search_query = st.text_input("🔍 Wyszukaj towar po nazwie...", "").strip().lower()

# Filtracja danych na potrzeby widoku
if search_query:
    filtered_df = df[df['Nazwa'].str.contains(search_query, case=False, na=False)]
else:
    filtered_df = df

# --- FORMULARZ DODAWANIA ---
with st.form(key='dodaj_form', clear_on_submit=True):
    st.markdown("### 📥 Nowa dostawa")
    c1, c2 = st.columns([3, 1])
    nazwa_input = c1.text_input("Nazwa przedmiotu")
    ilosc_input = c2.number_input("Ilość", min_value=1, step=1)
    if st.form_submit_button("ZATWIERDŹ DOSTAWĘ"):
        if nazwa_input.strip():
            nowy_towar = pd.DataFrame([{'Nazwa': nazwa_input.strip(), 'Ilość': int(ilosc_input)}])
            df_updated = pd.concat([df, nowy_towar], ignore_index=True)
            save_data(df_updated)
        else:
            st.error("Podaj nazwę towaru!")

# --- WYŚWIETLANIE TABELI I ZARZĄDZANIE ---
if not filtered_df.empty:
    st.markdown("### 📦 Stan ewidencji")
    
    # Przygotowanie tabeli do wyświetlenia
    display_df = filtered_df.copy()
    display_df.insert(0, 'ID', range(1, len(display_df) + 1))
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # --- PANEL ZARZĄDZANIA ---
    with st.expander("⚙️ Szybka edycja wybranego towaru"):
        id_list = display_df['ID'].tolist()
        wybor_id = st.selectbox("Wybierz ID towaru z tabeli powyżej", id_list)
        
        # Znalezienie towaru w oryginalnym DF
        nazwa_wybrana = display_df[display_df['ID'] == wybor_id]['Nazwa'].values[0]
        real_idx = df[df['Nazwa'] == nazwa_wybrana].index[0]

        st.write(f"Zarządzasz: **{nazwa_wybrana}** (Stan: {df.at[real_idx, 'Ilość']} szt.)")
        
        btn1, btn2, btn3 = st.columns(3)
        if btn1.button("➕ Dodaj 1"):
            df.at[real_idx, 'Ilość'] += 1
            save_data(df)
            
        if btn2.button("➖ Odejmij 1"):
            if df.at[real_idx, 'Ilość'] > 0:
                df.at[real_idx, 'Ilość'] -= 1
                save_data(df)

        if btn3.button("🗑️ USUŃ TOWAR", type="secondary"):
            df = df.drop(real_idx).reset_index(drop=True)
            save_data(df)
else:
    if search_query:
        st.warning("Nie znaleziono towaru o takiej nazwie.")
    else:
        st.info("Magazyn jest pusty.")
