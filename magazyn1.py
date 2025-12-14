import streamlit as st
import pandas as pd
import os

# Nazwa pliku do przechowywania danych (Magazyn bez st.session_state)
FILE_PATH = "inventory.csv"

def initialize_inventory():
    """Wczytuje lub inicjuje pusty DataFrame magazynu."""
    if os.path.exists(FILE_PATH):
        try:
            df = pd.read_csv(FILE_PATH)
            if not df.empty:
                df['Ilość'] = df['Ilość'].astype(int)
            return df
        except pd.errors.EmptyDataError:
            return pd.DataFrame({'Nazwa': [], 'Ilość': []})
        except Exception as e:
            st.error(f"Błąd podczas wczytywania CSV: {e}")
            return pd.DataFrame({'Nazwa': [], 'Ilość': []})
    else:
        return pd.DataFrame({'Nazwa': [], 'Ilość': []})

def save_inventory(df):
    """Zapisuje DataFrame do pliku CSV i wymusza ponowne uruchomienie aplikacji."""
    df.to_csv(FILE_PATH, index=False)
    # st.rerun() jest kluczowe, aby Streamlit natychmiast odświeżył widok 
    # i wczytał zaktualizowany plik CSV.
    st.rerun()

def calculate_stats(df):
    """Oblicza i zwraca statystyki magazynu."""
    total_unique_items = len(df)
    total_quantity = df['Ilość'].sum() if not df.empty else 0
    return total_unique_items, total_quantity

def main():
    # Ustawienie nazwy okna przeglądarki
    st.set_page_config(page_title="Magazyn1", layout="wide")
    
    # Główna nazwa wyświetlana na górze aplikacji
    st.title("📦 Magazyn1")
    st.markdown("Aplikacja do zarządzania stanem magazynowym z użyciem pliku **`inventory.csv`** jako trwałego magazynu danych.")

    # 1. Wczytanie aktualnego stanu z pliku
    current_df = initialize_inventory()

    # --- Sekcja Dodawania Towaru ---
    st.header("➕ Dodaj Nowy Towar")
    
    with st.form(key='add_item_form', clear_on_submit=True):
        new_item = st.text_input("Nazwa Towaru", placeholder="Wpisz np. Klawiatura bezprzewodowa")
        quantity = st.number_input("Ilość", min_value=1, value=1, step=1)
        add_button = st.form_submit_button("Dodaj do Magazynu")

        if add_button and new_item:
            new_row = pd.DataFrame([{'Nazwa': new_item.strip(), 'Ilość': int(quantity)}])
            updated_df = pd.concat([current_df, new_row], ignore_index=True)
            
            st.success(f"Dodano: **{new_item.strip()}** (Ilość: {int(quantity)}).")
            save_inventory(updated_df) 

        elif add_button and not new_item:
            st.warning("Wpisz nazwę towaru.")

    # --- Sekcja Statystyk i Wyświetlania Magazynu ---
    
    total_unique_items, total_quantity = calculate_stats(current_df)
    
    st.header("📊 Aktualny Stan Magazynu")
    
    col_stat1, col_stat2, col_stat3
