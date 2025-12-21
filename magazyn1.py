import streamlit as st
import pandas as pd

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="magazyn", layout="centered")

# Inicjalizacja danych w pamięci
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Nazwa', 'Ilość'])

# --- 2. STYLIZACJA CSS (MAKSYMALNA WIDOCZNOŚĆ I NOWY PRZYCISK) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&display=swap');

    /* Ekstremalnie gruba czcionka i głęboka czerń */
    html, body, [class*="css"], .stMarkdown, p, div, label, .stMetric {
        font-family: 'Montserrat', sans-serif !important;
        color: #000000 !important;
        font-weight: 900 !important;
    }

    /* Przyciemnione tło dla lepszego kontrastu */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
        url("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Wielki napis magazyn */
    .main-title {
        font-size: 100px !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        text-align: center;
        margin-top: -70px;
        margin-bottom: 40px;
        text-transform: lowercase;
        letter-spacing: -5px;
        text-shadow: 5px 5px 15px rgba(0,0,0,1);
    }

    /* Kontenery - czysta biel i grube ramki */
    [data-testid="stMetric"], .stForm, .inventory-row {
        background-color: #ffffff !important;
        padding: 30px !important;
        border-radius: 20px !important;
        border: 5px solid #000000 !important;
        box-shadow: 0 20px 60px rgba(0,0,0,0.8) !important;
        margin-bottom: 25px;
    }

    /* TEKST PRODUKTÓW - POWIĘKSZONY DO 32px */
    .item-text {
        font-size: 32px !important;
        line-height: 1.1;
        color: #000000 !important;
        text-transform: uppercase;
        margin: 0;
    }

    /* UKRYCIE MENU */
    #MainMenu, footer, header {visibility: hidden;}

    /* STYLIZACJA PRZYCISKÓW */
    .stButton > button {
        border-radius: 15px !important;
        font-weight: 900 !important;
        border: 3px solid #000000 !important;
        text-transform: uppercase;
    }

    /* NOWY PRZYCISK ZATWIERDŹ (Błękit Królewski) */
    form .stButton > button {
        background-color: #0052FF !important;
        color: #ffffff !important;
        font-size: 26px !important;
        height: 4em !important;
        box-shadow: 0 0 20px rgba(0, 82, 255, 0.5) !important;
    }
    form .stButton > button:hover {
        background-color: #003db3 !important;
        border-color: #ffffff !important;
    }

    /* Przycisk PLUS (Neonowa Zieleń) */
    div[data-testid="stHorizontalBlock"] div:nth-child(3) button {
        background-color: #39FF14 !important;
        font-size: 24px !important;
    }

    /* Przycisk MINUS (Słoneczny Żółty) */
    div[data-testid="stHorizontalBlock"] div:nth-child(4) button {
        background-color: #FFFB00 !important;
        font-size: 24px !important;
    }

    /* Przycisk USUŃ (Ognisty Czerwony) */
    div[data-testid="stHorizontalBlock"] div:nth-child(5) button {
        background-color: #FF0000 !important;
        color: #ffffff !important;
        font-size: 24px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTERFEJS ---

st.markdown('<h1 class="main-title">magazyn</h1>', unsafe_allow_html=True)

# Statystyki (Powiększone)
df = st.session_state.inventory
c1, c2 = st.columns(2)
with c1:
    st.metric("TYPY TOWARÓW", len(df))
with c2:
    st.metric("SUMA SZTUK", int(df['Ilość'].sum() if not df.empty else 0))

st.write("")

# --- FORMULARZ DODAWANIA ---
with st.form("main_add_form", clear_on_submit=True):
    st.markdown("## 📥 DOPISZ NOWY TOWAR")
    col_n, col_q = st.columns([2, 1])
    n = col_n.text_input("NAZWA PRODUKTU")
    q = col_q.number_input("ILE SZTUK", min_value=1, step=1)
    # Odświeżony przycisk zatwierdzania
    if st.form_submit_button("ZATWIERDŹ DOSTAWĘ"):
        if n.strip():
            if n.strip() in st.session_state.inventory['Nazwa'].values:
                st.session_state.inventory.loc[st.session_state.inventory['Nazwa'] == n.strip(), 'Ilość'] += q
            else:
                new_row = pd.DataFrame([{'Nazwa': n.strip(), 'Ilość': q}])
                st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
            st.rerun()

st.write("")

# --- LISTA TOWARÓW ---
if not st.session_state.inventory.empty:
    st.markdown("## 📋 AKTUALNA LISTA")
    
    for index, row in st.session_state.inventory.iterrows():
        st.markdown('<div class="inventory-row">', unsafe_allow_html=True)
        # Układ kolumn: Nazwa, Ilość, +, -, Usuń
        col_name, col_qty, col_plus, col_minus, col_del = st.columns([3, 2, 1, 1, 1])
        
        col_name.markdown(f'<p class="item-text">{row["Nazwa"]}</p>', unsafe_allow_html=True)
        col_qty.markdown(f'<p class="item-text">{row["Ilość"]} SZT.</p>', unsafe_allow_html=True)
        
        if col_plus.button("➕", key=f"add_{index}"):
            st.session_state.inventory.at[index, 'Ilość'] += 1
            st.rerun()
            
        if col_minus.button("➖", key=f"sub_{index}"):
            if st.session_state.inventory.at[index, 'Ilość'] > 0:
                st.session_state.inventory.at[index, 'Ilość'] -= 1
                st.rerun()
        
        if col_del.button("🗑️", key=f"del_{index}"):
            st.session_state.inventory = st.session_state.inventory.drop(index).reset_index(drop=True)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="inventory-row"><p class="item-text" style="text-align:center;">BRAK TOWARÓW</p></div>', unsafe_allow_html=True)
