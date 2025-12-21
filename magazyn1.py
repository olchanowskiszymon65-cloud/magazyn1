import streamlit as st
import pandas as pd

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="magazyn", layout="centered")

# Inicjalizacja danych (reset po F5)
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Nazwa', 'Ilość'])

# --- 2. STYLIZACJA CSS (EKSTREMALNA WIDOCZNOŚĆ ETYKIET I LISTY) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&display=swap');

    /* Globalne ustawienie czcionki - Najgrubsza 900 */
    html, body, [class*="css"], .stMarkdown, p, div, label, .stMetric, input {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 900 !important;
    }

    /* Przyciemnione tło strony */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), 
        url("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Tytuł główny */
    .main-title {
        font-size: 110px !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        text-align: center;
        margin-top: -80px;
        margin-bottom: 40px;
        text-transform: lowercase;
        letter-spacing: -5px;
        text-shadow: 10px 10px 20px rgba(0,0,0,1);
    }

    /* Kontenery statystyk i formularza (Białe) */
    [data-testid="stMetric"], .stForm {
        background-color: #ffffff !important;
        padding: 40px !important;
        border-radius: 25px !important;
        border: 6px solid #000000 !important;
        box-shadow: 0 20px 60px rgba(0,0,0,0.9) !important;
    }

    /* NAPISY "NAZWA TOWARU" i "ILE SZTUK" - MAKSYMALNIE WIDOCZNE */
    label {
        font-size: 35px !important; /* Ogromny napis */
        color: #000000 !important;
        text-transform: uppercase !important;
        margin-bottom: 15px !important;
        display: block !important;
        line-height: 1.2 !important;
    }

    /* Pola tekstowe - tekst wpisywany w środku */
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {
        font-size: 30px !important;
        height: 70px !important;
        color: #000000 !important;
        border: 4px solid #000000 !important;
        background-color: #F8F9FA !important;
    }

    /* BIAŁA CZCIONKA DLA LISTY NA DOLE (Bez tła) */
    .item-text-white {
        font-size: 45px !important;
        color: #ffffff !important;
        text-transform: uppercase;
        font-weight: 900 !important;
        text-shadow: 4px 4px 15px #000000, -4px -4px 15px #000000;
        margin: 0;
    }

    /* Przyciski edycji na dole */
    div[data-testid="stHorizontalBlock"] button {
        font-size: 30px !important;
        height: 70px !important;
        border: 3px solid #ffffff !important;
        border-radius: 15px !important;
    }

    /* Przycisk ZATWIERDŹ DOSTAWĘ */
    form .stButton > button {
        background-color: #D500F9 !important;
        color: #ffffff !important;
        font-size: 35px !important;
        height: 3.5em !important;
        border: 4px solid #000000 !important;
        margin-top: 20px !important;
    }

    /* Ukrycie elementów Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTERFEJS ---

st.markdown('<h1 class="main-title">magazyn</h1>', unsafe_allow_html=True)

# Statystyki
df = st.session_state.inventory
c1, c2 = st.columns(2)
with c1:
    st.metric("TYPY", len(df))
with c2:
    st.metric("SZTUKI", int(df['Ilość'].sum() if not df.empty else 0))

st.write("")

# --- FORMULARZ (BIAŁY) ---
with st.form("delivery_vfinal", clear_on_submit=True):
    # Nagłówek wewnątrz formularza
    st.markdown("<h2 style='text-align:center; color:black; font-size:45px; margin-bottom:20px;'>📥 NOWA DOSTAWA</h2>", unsafe_allow_html=True)
    
    col_n, col_q = st.columns([2, 1])
    # Etykiety są stylizowane przez CSS 'label' powyżej
    n = col_n.text_input("NAZWA TOWARU")
    q = col_q.number_input("ILE SZTUK", min_value=1, step=1)
    
    if st.form_submit_button("ZATWIERDŹ DOSTAWĘ"):
        if n.strip():
            if n.strip() in st.session_state.inventory['Nazwa'].values:
                st.session_state.inventory.loc[st.session_state.inventory['Nazwa'] == n.strip(), 'Ilość'] += q
            else:
                new_row = pd.DataFrame([{'Nazwa': n.strip(), 'Ilość': q}])
                st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
            st.rerun()

st.write("")

# --- LISTA (BIAŁA CZCIONKA BEZ PASKÓW) ---
if not st.session_state.inventory.empty:
    st.markdown("<h2 style='color:white; font-size:50px; text-shadow: 4px 4px 20px black;'>📋 STAN MAGAZYNU:</h2>", unsafe_allow_html=True)
    
    for index, row in st.session_state.inventory.iterrows():
        with st.container():
            col_name, col_qty, col_plus, col_minus, col_del = st.columns([3, 2, 1, 1, 1])
            
            col_name.markdown(f'<p class="item-text-white">{row["Nazwa"]}</p>', unsafe_allow_html=True)
            col_qty.markdown(f'<p class="item-text-white">{row["Ilość"]} SZT.</p>', unsafe_allow_html=True)
            
            # Przycisk PLUS (Zielony)
            if col_plus.button("➕", key=f"p_{index}"):
                st.session_state.inventory.at[index, 'Ilość'] += 1
                st.rerun()
                
            # Przycisk MINUS (Żółty)
            if col_minus.button("➖", key=f"m_{index}"):
                if st.session_state.inventory.at[index, 'Ilość'] > 0:
                    st.session_state.inventory.at[index, 'Ilość'] -= 1
                    st.rerun()
            
            # Przycisk USUŃ (Czerwony)
            if col_del.button("🗑️", key=f"d_{index}"):
                st.session_state.inventory = st.session_state.inventory.drop(index).reset_index(drop=True)
                st.rerun()
        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.4); margin: 20px 0;'>", unsafe_allow_html=True)
else:
    st.markdown("<p class='item-text-white' style='text-align:center; opacity:0.7;'>MAGAZYN PUSTY</p>", unsafe_allow_html=True)

