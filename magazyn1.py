import streamlit as st
import pandas as pd

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="magazyn", layout="centered")

# Inicjalizacja danych w pamięci (reset po F5)
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Nazwa', 'Ilość'])

# --- 2. STYLIZACJA CSS (EKSTREMALNA WIDOCZNOŚĆ I BIEL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&display=swap');

    /* Wymuszenie czcionki i czarnego koloru tekstu dla wszystkiego */
    html, body, [class*="css"], .stMarkdown, p, div, label, .stMetric, input {
        font-family: 'Montserrat', sans-serif !important;
        color: #000000 !important;
        font-weight: 900 !important;
    }

    /* Tło z ciężarówką */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
        url("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Wielki napis magazyn */
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

    /* Śnieżnobiałe kontenery z potężną czarną ramką */
    [data-testid="stMetric"], .stForm, .inventory-row {
        background-color: #ffffff !important;
        padding: 30px !important;
        border-radius: 20px !important;
        border: 5px solid #000000 !important;
        box-shadow: 0 15px 50px rgba(0,0,0,0.8) !important;
        margin-bottom: 20px;
    }

    /* Stylizacja pól wpisywania (Nowa dostawa) - BARDZO WIDOCZNE */
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {
        font-size: 28px !important;
        color: #000000 !important;
        font-weight: 900 !important;
        background-color: #f0f0f0 !important;
        border: 3px solid #000000 !important;
        height: 60px !important;
    }
    
    label {
        font-size: 24px !important;
        color: #000000 !important;
        text-transform: uppercase;
        margin-bottom: 10px !important;
    }

    /* TEKST PRODUKTÓW NA DOLE - GIGANTYCZNY */
    .item-text {
        font-size: 38px !important;
        color: #000000 !important;
        text-transform: uppercase;
        font-weight: 900 !important;
        margin: 0;
        line-height: 1;
    }

    /* UKRYCIE MENU */
    #MainMenu, footer, header {visibility: hidden;}

    /* PRZYCISKI - ŻYWE KOLORY */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 900 !important;
        border: 3px solid #000000 !important;
        transition: 0.2s;
    }

    /* Przycisk ZATWIERDŹ (Intensywny Fiolet/Magenta) */
    form .stButton > button {
        background-color: #D500F9 !important;
        color: #ffffff !important;
        font-size: 32px !important;
        height: 3.5em !important;
        box-shadow: 0 0 20px rgba(213, 0, 249, 0.4) !important;
    }

    /* Przycisk PLUS (Zieleń) */
    div[data-testid="stHorizontalBlock"] div:nth-child(3) button {
        background-color: #00E676 !important;
        font-size: 30px !important;
    }

    /* Przycisk MINUS (Żółty) */
    div[data-testid="stHorizontalBlock"] div:nth-child(4) button {
        background-color: #FFEA00 !important;
        font-size: 30px !important;
    }

    /* Przycisk USUŃ (Czerwony) */
    div[data-testid="stHorizontalBlock"] div:nth-child(5) button {
        background-color: #FF1744 !important;
        color: #ffffff !important;
        font-size: 30px !important;
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
    st.metric("SUMA WSZYSTKICH", int(df['Ilość'].sum() if not df.empty else 0))

st.write("")

# --- FORMULARZ NOWA DOSTAWA ---
with st.form("delivery_form", clear_on_submit=True):
    st.markdown("<h2 style='text-align:center; color:black; font-size:35px;'>📥 NOWA DOSTAWA</h2>", unsafe_allow_html=True)
    col_n, col_q = st.columns([2, 1])
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

# --- LISTA TOWARÓW NA DOLE (BIAŁE PASKI) ---
if not st.session_state.inventory.empty:
    st.markdown("<h2 style='color:white; font-size:45px; text-shadow: 2px 2px 10px black;'>📋 LISTA MAGAZYNOWA:</h2>", unsafe_allow_html=True)
    
    for index, row in st.session_state.inventory.iterrows():
        st.markdown('<div class="inventory-row">', unsafe_allow_html=True)
        # Nazwa, Ilość, +, -, Usuń
        col_name, col_qty, col_plus, col_minus, col_del = st.columns([3, 2, 1, 1, 1])
        
        col_name.markdown(f'<p class="item-text">{row["Nazwa"]}</p>', unsafe_allow_html=True)
        col_qty.markdown(f'<p class="item-text">{row["Ilość"]} SZT.</p>', unsafe_allow_html=True)
        
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
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="inventory-row"><p class="item-text" style="text-align:center;">MAGAZYN JEST PUSTY</p></div>', unsafe_allow_html=True)
