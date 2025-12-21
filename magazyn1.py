import streamlit as st
import pandas as pd

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="magazyn", layout="centered")

# Inicjalizacja danych w pamięci (znikają po F5)
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Nazwa', 'Ilość'])

# --- 2. STYLIZACJA CSS (EKSTREMALNA WIDOCZNOŚĆ) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&display=swap');

    /* Wymuszenie najgrubszej czcionki dla całego systemu */
    * {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 900 !important;
    }

    /* Tło z ciężarówką - mocno przyciemnione dla kontrastu z białym tekstem */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), 
        url("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* GIGANTYCZNY TYTUŁ */
    .main-title {
        font-size: 120px !important;
        color: #ffffff !important;
        text-align: center;
        margin-top: -100px;
        margin-bottom: 50px;
        text-transform: lowercase;
        letter-spacing: -6px;
        text-shadow: 0 0 30px rgba(255,255,255,0.4), 10px 10px 20px #000000;
    }

    /* BIAŁY PANEL FORMULARZA */
    [data-testid="stMetric"], .stForm {
        background-color: #ffffff !important;
        padding: 50px !important;
        border-radius: 30px !important;
        border: 8px solid #000000 !important;
        box-shadow: 0 30px 80px rgba(0,0,0,1) !important;
    }

    /* ETYKIETY: NAZWA TOWARU / ILE SZTUK */
    label {
        font-size: 40px !important;
        color: #000000 !important;
        text-transform: uppercase !important;
        margin-bottom: 20px !important;
        line-height: 1 !important;
    }

    /* POLA WPISYWANIA - TEKST W ŚRODKU */
    input {
        font-size: 35px !important;
        height: 80px !important;
        color: #000000 !important;
        border: 5px solid #000000 !important;
        background-color: #ffffff !important;
    }

    /* GIGANTYCZNA BIAŁA LISTA NA TLE */
    .item-text-white {
        font-size: 50px !important;
        color: #ffffff !important;
        text-transform: uppercase;
        text-shadow: 5px 5px 20px #000000, -2px -2px 5px #000000;
        margin: 0;
        line-height: 1.1;
    }

    /* PRZYCISKI EDYCJI (+, -, 🗑️) */
    div[data-testid="stHorizontalBlock"] button {
        font-size: 40px !important;
        height: 90px !important;
        border: 4px solid #ffffff !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    }

    /* PRZYCISK ZATWIERDŹ DOSTAWĘ (NEONOWY FIOLET) */
    form .stButton > button {
        background-color: #D500F9 !important;
        color: #ffffff !important;
        font-size: 45px !important;
        height: 3.5em !important;
        border: 6px solid #000000 !important;
        margin-top: 30px !important;
    }

    /* UKRYCIE ELEMENTÓW SYSTEMOWYCH */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTERFEJS UŻYTKOWNIKA ---

st.markdown('<h1 class="main-title">magazyn</h1>', unsafe_allow_html=True)

# Sekcja Statystyk
df = st.session_state.inventory
c1, c2 = st.columns(2)
with c1:
    st.metric("TYPY", len(df))
with c2:
    st.metric("SZTUKI", int(df['Ilość'].sum() if not df.empty else 0))

st.write("")

# --- FORMULARZ DODAWANIA ---
with st.form("delivery_extreme", clear_on_submit=True):
    st.markdown("<h2 style='text-align:center; color:black; font-size:50px; margin-bottom:30px;'>📥 NOWA DOSTAWA</h2>", unsafe_allow_html=True)
    
    col_n, col_q = st.columns([2, 1])
    n = col_n.text_input("NAZWA TOWARU")
    q = col_q.number_input("ILE SZTUK", min_value=1, step=1)
    
    if st.form_submit_button("ZATWIERDŹ DOSTAWĘ"):
        if n.strip():
            # Logika aktualizacji lub dodawania
            if n.strip() in st.session_state.inventory['Nazwa'].values:
                st.session_state.inventory.loc[st.session_state.inventory['Nazwa'] == n.strip(), 'Ilość'] += q
            else:
                new_row = pd.DataFrame([{'Nazwa': n.strip(), 'Ilość': q}])
                st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
            st.rerun()

st.write("")

# --- LISTA PRODUKTÓW ---
if not st.session_state.inventory.empty:
    st.markdown("<h2 style='color:white; font-size:60px; text-shadow: 5px 5px 25px black; margin-bottom:40px;'>📋 STAN OBECNY:</h2>", unsafe_allow_html=True)
    
    for index, row in st.session_state.inventory.iterrows():
        with st.container():
            # Układ: Nazwa (3), Ilość (2), Plus (1), Minus (1), Usuń (1)
            col_name, col_qty, col_plus, col_minus, col_del = st.columns([3, 2, 1, 1, 1])
            
            col_name.markdown(f'<p class="item-text-white">{row["Nazwa"]}</p>', unsafe_allow_html=True)
            col_qty.markdown(f'<p class="item-text-white">{row["Ilość"]} SZT.</p>', unsafe_allow_html=True)
            
            # Przycisk PLUS (Neonowy Zielony)
            if col_plus.button("➕", key=f"p_{index}"):
                st.session_state.inventory.at[index, 'Ilość'] += 1
                st.rerun()
                
            # Przycisk MINUS (Neonowy Żółty)
            if col_minus.button("➖", key=f"m_{index}"):
                if st.session_state.inventory.at[index, 'Ilość'] > 0:
                    st.session_state.inventory.at[index, 'Ilość'] -= 1
                    st.rerun()
            
            # Przycisk USUŃ (Neonowa Czerwień)
            if col_del.button("🗑️", key=f"d_{index}"):
                st.session_state.inventory = st.session_state.inventory.drop(index).reset_index(drop=True)
                st.rerun()
        
        # Gruba linia rozdzielająca
        st.markdown("<hr style='border: 3px solid rgba(255,255,255,0.5); margin: 35px 0;'>", unsafe_allow_html=True)
else:
    st.markdown("<p class='item-text-white' style='text-align:center; opacity:0.5;'>MAGAZYN JEST PUSTY</p>", unsafe_allow_html=True)
