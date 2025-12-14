import streamlit as st
import pandas as pd
import os

# Nazwa pliku do przechowywania danych
FILE_PATH = "inventory.csv"

def initialize_inventory():
    """Tworzy plik CSV, jeśli nie istnieje, lub wczytuje istniejące dane."""
    if os.path.exists(FILE_PATH):
        try:
            df = pd.read_csv(FILE_PATH)
            if not df.empty:
                # Upewnienie się, że kolumna 'Ilość' ma typ liczby całkowitej
                df['Ilość'] = df['Ilość'].astype(int)
            return df
        except pd.errors.EmptyDataError:
            # Plik istnieje, ale jest pusty
            return pd.DataFrame({'Nazwa': [], 'Ilość': []})
        except Exception as e:
            st.error(f"Błąd podczas wczytywania CSV: {e}")
            return pd.DataFrame({'Nazwa': [], 'Ilość': []})
    else:
        # Utworzenie pustego DataFrame
        return pd.DataFrame({'Nazwa': [], 'Ilość': []})

def save_inventory(df):
    """Zapisuje DataFrame do pliku CSV i wymusza ponowne uruchomienie aplikacji."""
    df.to_csv(FILE_PATH, index=False)
    # st.rerun() jest kluczowe, ponieważ ponowne uruchomienie skryptu wymusza 
    # ponowne wczytanie zaktualizowanego pliku CSV.
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
    st.markdown("Aplikacja do zarządzania stanem magazynowym. Stan jest zapisywany w pliku **`inventory.csv`**.")

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
            
            st.success(f"Dodano: **{new_item.strip()}** (Ilo

