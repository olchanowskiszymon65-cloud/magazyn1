import streamlit as st
import pandas as pd
import random
import time

# UWAGA: W tej wersji stan (lista towarów) będzie resetowany po każdej interakcji,
# ponieważ nie używamy st.session_state, ani trwałej bazy danych/API.
# Ten kod GWARANTUJE WYŚWIETLANIE się w Streamlit Cloud, ale NIE trwałość danych.

# --- Symulacja Danych (Zastępuje Trwałą Bazę Danych) ---
def get_initial_inventory():
    """Zwraca tymczasową listę towarów."""
    return [
        {"Nazwa": "Laptop Business", "Ilość": 5},
        {"Nazwa": "Monitor 24\"", "Ilość": 12},
        {"Nazwa": "Mysz optyczna", "Ilość": 30},
    ]

# Globalna zmienna przechowująca stan (będzie resetowana!)
global_inventory_list = get_initial_inventory()


def calculate_stats(inventory_list):
    """Oblicza statystyki magazynu z podanej listy."""
    df = pd.DataFrame(inventory_list)
    total_unique_items = len(df)
    total_quantity = df['Ilość'].sum() if not df.empty else 0
    return total_unique_items, total_quantity

def main():
    st.set_page_config(page_title="Magazyn1", layout="wide")
    st.title("📦 Magazyn1 (Bez Session State - Stan Tymczasowy)")
    st.markdown("⚠️ **UWAGA:** Dane są tymczasowe. Każda interakcja z aplikacją spowoduje ponowne uruchomienie skryptu i reset stanu.")

    # Wczytanie stanu (zostaje zresetowany przy każdym uruchomieniu)
    inventory_list = get_initial_inventory() 
    
    # --- Sekcja Dodawania Towaru ---
    st.header("➕ Dodaj Nowy Towar")
    
    with st.form(key='add_item_form', clear_on_submit=True):
        new_item = st.text_input("Nazwa Towaru", placeholder="Wpisz np. Klawiatura bezprzewodowa")
        quantity = st.number_input("Ilość", min_value=1, value=1, step=1)
        add_button = st.form_submit_button("Dodaj do Magazynu")

        if add_button and new_item:
            # Tutaj normalnie byłaby funkcja do zapisu do bazy danych/API
            st.warning(f"Zapis: {new_item.strip()} (Ilość: {int(quantity)}) - W trybie 'bez sesji' zapis jest ignorowany.")
            # Nie używamy st.rerun(), bo stan i tak zostanie zresetowany.


    # --- Sekcja Statystyk i Wyświetlania Magazynu ---
    
    total_unique_items, total_quantity = calculate_stats(inventory_list)
    
    st.header("📊 Aktualny Stan Magazynu (Tymczasowy)")
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    col_stat1.metric(label="Łączna Liczba Towarów (Sztuk)", value=total_quantity)
    col_stat2.metric(label="Unikalne Pozycje", value=total_unique_items)
    col_stat3.error("Stan nie jest trwały.")

    if inventory_list:
        df_display = pd.DataFrame(inventory_list)
        df_display.insert(0, 'ID', range(1, 1 + len(df_display)))
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # --- Sekcja Usuwania Towaru ---
        st.subheader("➖ Usuń Towar po ID")
        
        available_ids = df_display['ID'].tolist()
        
        if available_ids:
            col_remove, col_filler = st.columns([1, 4])
            
            with col_remove:
                id_to_remove = st.selectbox("Wybierz ID do usunięcia:", available_ids, index=0)
                
                if st.button("Usuń Wybrany"):
                    st.warning(f"Usuwanie ID {id_to_remove} jest ignorowane w tym trybie.")
            
    else:
        st.info("Magazyn jest pusty.")


if __name__ == "__main__":
    main()
