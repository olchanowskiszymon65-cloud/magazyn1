import streamlit as st
import pandas as pd

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="magazyn", layout="centered")

# --- 2. LOGIKA SESJI (RESET PO ODŚWIEŻENIU) ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Nazwa', 'Ilość'])

# --- 3. STYLIZACJA CSS (PRZYWRÓCENIE CZYTELNOŚCI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    /* Wymuszenie czcionki Montserrat i czarnego koloru tekstu */
    html, body, [class*="css"], .stMarkdown, p, div, label, .stMetric {
        font-family: 'Montserrat', sans-serif !important;
        color: #000000 !important;
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
        color: #ffffff !important; /* Napis główny pozostaje biały */
        text-align: center;
        margin-top: -50px;
        margin-bottom: 30px;
        text-transform: lowercase;
        letter-spacing: -2px;
    }

    /* Kontenery: Maksymalna czytelność - białe tło, czarny tekst */
    [data-testid="stMetric"], .stForm, .stDataFrame, [data-testid="stExpander"], div[data-testid="stTextInput"] {
        background-color: rgba(255, 255, 255, 1.0) !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    }

    /* Napisy w metrykach */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #333333 !important;
    }

    /* Przyciski */
    div.stButton > button {
        background-color: #2E7D32 !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
    }
    
    .stButton button[kind="secondary"] {
        background-color: #C62828 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTERFEJS UŻYTKOWNIKA ---

st.markdown('<h1 class="main-title">magazyn</h1>', unsafe_allow_html=True)

# Statystyki z Session State
df = st.session_state.inventory
total_types = len(df)
total_qty = df['Ilość'].sum() if not df.empty else 0

col_m1, col_m2 = st.columns(2)
col_m1.metric("Rodzaje towarów", total_types)
col_m2.metric("Łączna liczba sztuk", total_qty)

st.write("")

# --- WYSZUKIWARKA ---
search_query = st.text_input("🔍 Wyszukaj towar (resetuje się po F5)...", "").strip().lower()

# Filtracja widoku
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
    
    if st.form_submit_button("ZATWIERDŹ"):
        if nazwa_input.strip():
            new_row = pd.DataFrame([{'Nazwa': nazwa_input.strip(), 'Ilość': int(ilosc_input)}])
            st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
            st.rerun()
        else:
            st.error("Podaj nazwę towaru!")

# --- TABELA I EDYCJA ---
if not filtered_df.empty:
    st.markdown("### 📦 Stan ewidencji")
    
    display_df = filtered_df.copy()
    display_df.insert(0, 'ID', range(1, len(display_df) + 1))
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    with st.expander("⚙️ Zarządzaj towarem"):
        wybor_id = st.selectbox("Wybierz ID towaru", display_df['ID'].tolist())
        
        # Pobranie danych wybranego wiersza
        row_data = display_df[display_df['ID'] == wybor_id]
        nazwa_wybrana = row_data['Nazwa'].values[0]
        # Znalezienie indeksu w oryginalnym DataFrame
        real_idx = st.session_state.inventory[st.session_state.inventory['Nazwa'] == nazwa_wybrana].index[0]

        st.write(f"Produkt: **{nazwa_wybrana}**")
        
        b1, b2, b3 = st.columns(3)
        if b1.button("➕ Dodaj 1"):
            st.session_state.inventory.at[real_idx, 'Ilość'] += 1
            st.rerun()
            
        if b2.button("➖ Odejmij 1"):
            if st.session_state.inventory.at[real_idx, 'Ilość'] > 0:
                st.session_state.inventory.at[real_idx, 'Ilość'] -= 1
                st.rerun()

        if b3.button("🗑️ USUŃ", kind="secondary"):
            st.session_state.inventory = st.session_state.inventory.drop(real_idx).reset_index(drop=True)
            st.rerun()
else:
    st.info("Magazyn jest pusty. Dane zostaną wyczyszczone po odświeżeniu strony (F5).")
