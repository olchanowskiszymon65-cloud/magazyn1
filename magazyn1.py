import streamlit as st
import pandas as pd

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="magazyn", layout="centered")

# Inicjalizacja danych w pamięci (reset po odświeżeniu)
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Nazwa', 'Ilość'])

# --- 2. STYLIZACJA CSS (EKSTREMALNA CZYTELNOŚĆ) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&display=swap');

    /* Maksymalnie gruba czcionka (900) i głęboka czerń */
    html, body, [class*="css"], .stMarkdown, p, div, label, .stMetric {
        font-family: 'Montserrat', sans-serif !important;
        color: #000000 !important;
        font-weight: 900 !important;
    }

    /* Tło z europejską ciężarówką */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
        url("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Napis główny magazyn */
    .main-title {
        font-size: 90px !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        text-align: center;
        margin-top: -60px;
        margin-bottom: 40px;
        text-transform: lowercase;
        letter-spacing: -4px;
        text-shadow: 4px 4px 10px rgba(0,0,0,0.8);
    }

    /* Kontenery - białe, solidne z grubą ramką */
    [data-testid="stMetric"], .stForm, .inventory-row {
        background-color: #ffffff !important;
        padding: 25px !important;
        border-radius: 15px !important;
        border: 4px solid #000000 !important;
        box-shadow: 0 15px 50px rgba(0,0,0,0.7) !important;
        margin-bottom: 20px;
    }

    /* Tekst na liście produktów - EKSTREMALNIE DUŻY */
    .item-text {
        font-size: 28px !important;
        line-height: 1.2;
        color: #000000 !important;
        text-transform: uppercase;
    }

    /* Ukrycie elementów Streamlit */
    #MainMenu, footer, header {visibility: hidden;}

    /* PRZYCISKI - KOLORY I ROZMIARY */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 900 !important;
        font-size: 20px !important;
        border: 2px solid #000000 !important;
        transition: 0.3s;
    }

    /* Główny przycisk ZATWIERDŹ (Granatowy zamiast czarnego) */
    form .stButton > button {
        background-color: #003366 !important;
        color: #ffffff !important;
        height: 3.5em !important;
    }

    /* Przycisk PLUS (Jasny zielony) */
    div[data-testid="stHorizontalBlock"] div:nth-child(3) button {
        background-color: #00FF00 !important;
        color: #000000 !important;
    }

    /* Przycisk MINUS (Żółty/Pomarańczowy) */
    div[data-testid="stHorizontalBlock"] div:nth-child(4) button {
        background-color: #FFCC00 !important;
        color: #000000 !important;
    }

    /* Przycisk USUŃ (Czerwony) */
    div[data-testid="stHorizontalBlock"] div:nth-child(5) button {
        background-color: #FF0000 !important;
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTERFEJS ---

st.markdown('<h1 class="main-title">magazyn</h1>', unsafe_allow_html=True)

# Statystyki
df = st.session_state.inventory
c1, c2 = st.columns(2)
with c1:
    st.metric("TYPY TOWARÓW", len(df))
with c2:
    st.metric("SUMA SZTUK", int(df['Ilość'].sum() if not df.empty else 0))

st.write("")

# --- FORMULARZ DODAWANIA ---
with st.form("add_form", clear_on_submit=True):
    st.markdown("### 📥 DOPISZ DO STANU")
    col_n, col_q = st.columns([2, 1])
    n = col_n.text_input("NAZWA TOWARU")
    q = col_q.number_input("ILE SZTUK", min_value=1, step=1)
    if st.form_submit_button("ZATWIERDŹ DOSTAWĘ"):
        if n.strip():
            if n.strip() in st.session_state.inventory['Nazwa'].values:
                st.session_state.inventory.loc[st.session_state.inventory['Nazwa'] == n.strip(), 'Ilość'] += q
            else:
                new_entry = pd.DataFrame([{'Nazwa': n.strip(), 'Ilość': q}])
                st.session_state.inventory = pd.concat([st.session_state.inventory, new_entry], ignore_index=True)
            st.rerun()

st.write("")

# --- WYŚWIETLANIE LISTY ---
if not st.session_state.inventory.empty:
    st.markdown("### 📋 AKTUALNA EWIDENCJA")
    
    for index, row in st.session_state.inventory.iterrows():
        st.markdown('<div class="inventory-row">', unsafe_allow_html=True)
        # Zwiększone kolumny dla tekstu
        col_name, col_qty, col_plus, col_minus, col_del = st.columns([3, 2, 1, 1, 1])
        
        col_name.markdown(f'<p class="item-text">{row["Nazwa"]}</p>', unsafe_allow_html=True)
        col_qty.markdown(f'<p class="item-text">{row["Ilość"]} SZT.</p>', unsafe_allow_html=True)
        
        if col_plus.button("➕", key=f"p_{index}"):
            st.session_state.inventory.at[index, 'Ilość'] += 1
            st.rerun()
            
        if col_minus.button("➖", key=f"m_{index}"):
            if st.session_state.inventory.at[index, 'Ilość'] > 0:
                st.session_state.inventory.at[index, 'Ilość'] -= 1
                st.rerun()
        
        if col_del.button("🗑️", key=f"d_{index}"):
            st.session_state.inventory = st.session_state.inventory.drop(index).reset_index(drop=True)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="inventory-row"><p class="item-text">MAGAZYN PUSTY</p></div>', unsafe_allow_html=True)
