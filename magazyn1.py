
import streamlit as st
import pandas as pd

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="magazyn", layout="centered")

# --- 2. LOGIKA SESJI (TYMCZASOWA) ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Nazwa', 'Ilość'])

# --- 3. STYLIZACJA CSS (MAKSYMALNA CZYTELNOŚĆ) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    /* Wymuszenie czcionki i czarnego koloru tekstu dla formularzy i tabel */
    html, body, [class*="css"], .stMarkdown, p, div, label, .stMetric, .stSelectbox {
        font-family: 'Montserrat', sans-serif !important;
        color: #000000 !important;
    }

    /* Tło z europejską ciężarówką */
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
        color: #ffffff !important;
        text-align: center;
        margin-top: -50px;
        margin-bottom: 30px;
        text-transform: lowercase;
        letter-spacing: -2px;
    }

    /* Białe kontenery bez przezroczystości dla tekstu */
    [data-testid="stMetric"], .stForm, .stDataFrame, [data-testid="stExpander"], div[data-testid="stTextInput"] {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    }

    /* Ukrycie komunikatów o błędach i ostrzeżeń na dole strony */
    #MainMenu, footer, header {visibility: hidden;}
    .stAlert { background-color: #ffffff !important; color: #000000 !important; border: none !important; }

    /* Stylizacja przycisków */
    div.stButton > button {
        background-color: #2E7D32 !important;
        color: white !important;
        font-weight: 700 !important;
        width: 100%;
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

# Dane z pamięci sesji
df = st.session_state.inventory

# Statystyki
col_m1, col_m2 = st.columns(2)
col_m1.metric("Rodzaje towarów", len(df))
col_m2.metric("Łączna liczba sztuk", int(df['Ilość'].sum() if not df.empty else 0))

st.write("")

# Wyszukiwarka
search_q = st.text_input("🔍 Wyszukaj towar...", "").strip().lower()
f_df = df[df['Nazwa'].str.contains(search_q, case=False, na=False)] if search_q else df

# Formularz dodawania
with st.form(key='add_p', clear_on_submit=True):
    st.markdown("### 📥 Nowa dostawa")
    c1, c2 = st.columns([3, 1])
    n_in = c1.text_input("Nazwa przedmiotu")
    q_in = c2.number_input("Ilość", min_value=1, step=1)
    if st.form_submit_button("ZATWIERDŹ"):
        if n_in.strip():
            new_r = pd.DataFrame([{'Nazwa': n_in.strip(), 'Ilość': int(q_in)}])
            st.session_state.inventory = pd.concat([st.session_state.inventory, new_r], ignore_index=True)
            st.rerun()

# Tabela i edycja
if not f_df.empty:
    st.markdown("### 📦 Stan ewidencji")
    d_df = f_df.copy()
    d_df.insert(0, 'ID', range(1, len(d_df) + 1))
    st.dataframe(d_df, use_container_width=True, hide_index=True)

    with st.expander("⚙️ Zarządzaj towarem"):
        # Użycie try/except zapobiega błędom przy nagłym usunięciu wiersza
        try:
            v_id = st.selectbox("Wybierz ID", d_df['ID'].tolist())
            sel_name = d_df[d_df['ID'] == v_id]['Nazwa'].values[0]
            r_idx = st.session_state.inventory[st.session_state.inventory['Nazwa'] == sel_name].index[0]

            b1, b2, b3 = st.columns(3)
            if b1.button("➕ Dodaj 1"):
                st.session_state.inventory.at[real_idx, 'Ilość'] += 1
                st.rerun()
            if b2.button("➖ Odejmij 1"):
                if st.session_state.inventory.at[r_idx, 'Ilość'] > 0:
                    st.session_state.inventory.at[r_idx, 'Ilość'] -= 1
                    st.rerun()
            if b3.button("🗑️ USUŃ", kind="secondary"):
                st.session_state.inventory = st.session_state.inventory.drop(r_idx).reset_index(drop=True)
                st.rerun()
        except:
            st.write("Wybierz poprawny element z listy.")
        
