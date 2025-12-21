
        
import streamlit as st
import pandas as pd

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="magazyn", layout="centered")

# Inicjalizacja danych w pamięci (znikną po F5)
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Nazwa', 'Ilość'])

# --- 2. STYLIZACJA CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

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
        color: #ffffff !important;
        text-align: center;
        margin-top: -50px;
        margin-bottom: 30px;
        text-transform: lowercase;
        letter-spacing: -2px;
    }

    [data-testid="stMetric"], .stForm, .stDataFrame, div[data-testid="stTextInput"], .inventory-item {
        background-color: #ffffff !important;
        padding: 15px !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        margin-bottom: 10px;
    }

    /* Ukrycie elementów Streamlit */
    #MainMenu, footer, header {visibility: hidden;}

    /* Przyciski */
    div.stButton > button {
        font-weight: 700 !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTERFEJS ---

st.markdown('<h1 class="main-title">magazyn</h1>', unsafe_allow_html=True)

# Statystyki
df = st.session_state.inventory
c1, c2 = st.columns(2)
c1.metric("Towary", len(df))
c2.metric("Suma sztuk", int(df['Ilość'].sum() if not df.empty else 0))

# --- SYSTEM DODAWANIA ---
with st.form("quick_add", clear_on_submit=True):
    st.markdown("### 📥 Przyjmij towar")
    col_n, col_q, col_b = st.columns([3, 1, 1])
    n = col_n.text_input("Nazwa")
    q = col_q.number_input("Ilość", min_value=1, step=1)
    if col_b.form_submit_button("DODAJ"):
        if n.strip():
            # Jeśli towar istnieje - dodaj ilość, jeśli nie - stwórz nowy
            if n.strip() in st.session_state.inventory['Nazwa'].values:
                st.session_state.inventory.loc[st.session_state.inventory['Nazwa'] == n.strip(), 'Ilość'] += q
            else:
                new_data = pd.DataFrame([{'Nazwa': n.strip(), 'Ilość': q}])
                st.session_state.inventory = pd.concat([st.session_state.inventory, new_data], ignore_index=True)
            st.rerun()

st.divider()

# --- POPRAWIONY SYSTEM ZARZĄDZANIA (LISTA) ---
if not st.session_state.inventory.empty:
    st.markdown("### 📦 Stan i szybka edycja")
    
    for index, row in st.session_state.inventory.iterrows():
        # Tworzymy wiersz dla każdego produktu z przyciskami + i -
        with st.container():
            col_name, col_qty, col_plus, col_minus, col_del = st.columns([3, 1, 1, 1, 1])
            
            col_name.write(f"**{row['Nazwa']}**")
            col_qty.write(f"{row['Ilość']} szt.")
            
            if col_plus.button("➕", key=f"plus_{index}"):
                st.session_state.inventory.at[index, 'Ilość'] += 1
                st.rerun()
                
            if col_minus.button("➖", key=f"minus_{index}"):
                if st.session_state.inventory.at[index, 'Ilość'] > 0:
                    st.session_state.inventory.at[index, 'Ilość'] -= 1
                    st.rerun()
            
            if col_del.button("🗑️", key=f"del_{index}"):
                st.session_state.inventory = st.session_state.inventory.drop(index).reset_index(drop=True)
                st.rerun()
else:
    st.write("Magazyn jest pusty.")
