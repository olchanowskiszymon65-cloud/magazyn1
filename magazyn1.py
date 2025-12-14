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
    st.markdown("Aplikacja do zarządzania stanem magazynowym z użyciem listy (DataFrame) zapisywanej w pliku **`inventory.csv`**.")

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
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    col_stat1.metric(label="Łączna Liczba Towarów (Sztuk)", value=total_quantity)
    col_stat2.metric(label="Unikalne Pozycje", value=total_unique_items)
    col_stat3.info("Stan jest zapisywany w pliku CSV na serwerze.")

    if not current_df.empty:
        # Kopia DataFrame do wyświetlania i dodania kolumny 'ID'
        current_df_display = current_df.copy()
        current_df_display.insert(0, 'ID', range(1, 1 + len(current_df_display)))
        
        st.dataframe(current_df_display, use_container_width=True, hide_index=True)
        
        # --- Sekcja Usuwania Towaru ---
        st.subheader("➖ Usuń Towar po ID")
        
        available_ids = current_df_display['ID'].tolist()
        
        if available_ids:
            col_remove, col_filler = st.columns([1, 4])
            
            with col_remove:
                # Domyślnie wybieramy pierwszy dostępny ID
                id_to_remove = st.selectbox("Wybierz ID do usunięcia:", available_ids, index=0)
                
                if st.button("Usuń Wybrany"):
                    # ID jest liczone od 1, indeks listy/DataFrame od 0
                    index_to_remove = id_to_remove - 1 
                    
                    if 0 <= index_to_remove < len(current_df):
                        removed_name = current_df.iloc[index_to_remove]['Nazwa']

