import streamlit as st
import pandas as pd

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="magazyn", layout="centered")

# Inicjalizacja danych (reset po F5)
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Nazwa', 'Ilość'])

# --- 2. STYLIZACJA CSS (BIEL NA TLE + MAX WIDOCZNOŚĆ) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&display=swap');

    /* Globalne ustawienie czcionki */
    html, body, [class*="css"], .stMarkdown, p, div, label, .stMetric {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 900 !important;
    }

    /* Przyciemnione tło strony */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
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

    /* Kontenery statystyk i formularza (Białe dla czytelności wpisywania) */
    [data-testid="stMetric"], .stForm {
        background-color: #ffffff !important;
        padding: 30px !important;
        border-radius: 20px !important;
        border: 5px solid #000000 !important;
        box-shadow: 0 15px 50px rgba(0,0,0,0.8) !important;
    }

    /* Stylizacja metryk (czarne na białym) */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #000000 !important;
        font-size: 35px !important;
    }

    /* BIAŁY TEKST DLA LISTY (Bez pasków) */
    .item-text-white {
        font-size: 42px !important; /* Bardzo duża czcionka */
        color: #ffffff !important;
        text-transform: uppercase;
        font-weight: 900 !important;
        text-shadow: 3px 3px 10px #000000, -3px -3px 10px #000000; /* Mocny cień dla widoczności */
        margin: 0;
        line-height: 1.2;
    }

    /* PRZYCISKI NA TLE - Z RAMKAMI */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 900 !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5) !important;
    }

    /* Przycisk ZATWIERDŹ (Dostawa) */
    form .stButton > button {
        background-color: #D500F9 !important;
        color: #ffffff !important;
        font-size: 30px !important;
        height: 3em !important;
        border: 3px solid #000000 !important;
    }

    /* Przyciski edycji (+, -, kosz) */
    div[data-testid="stHorizontalBlock"] button {
        font-size: 28px !important;
        height: 60px !important;
    }

    /* UKRYCIE MENU */
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
    st.metric("SUMA SZTUK", int(df['Ilość'].sum() if not df.empty else 0))

st.write("")

# --- FORMULARZ (BIAŁY DLA WYGODY WPISYWANIA) ---
with st.form("delivery_final", clear_on_submit=True):
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

# --- LISTA MAGAZYNOWA (BIAŁA CZCIONKA NA TLE) ---
if not st.session_state.inventory.empty:
    st.markdown("<h2 style='color:white; font-size:45px; text-shadow: 3px 3px 15px black;'>📋 LISTA MAGAZYNOWA:</h2>", unsafe_allow_html=True)
    
    for index, row in st.session_state.inventory.iterrows():
        # Kontener bez tła (background-color: transparent)
        with st.container():
            col_name, col_qty, col_plus, col_minus, col_del = st.columns([3, 2, 1, 1, 1])
            
            col_name.markdown(f'<p class="item-text-white">{row["Nazwa"]}</p>', unsafe_allow_html=True)
            col_qty.markdown(f'<p class="item-text-white">{row["Ilość"]} SZT.</p>', unsafe_allow_html=True)
            
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
        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3);'>", unsafe_allow_html=True)
else:
    st.markdown("<p class='item-text-white' style='text-align:center;'>MAGAZYN PUSTY</p>", unsafe_allow_html=True)
