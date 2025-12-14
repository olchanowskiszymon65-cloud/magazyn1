import streamlit as st
import pandas as pd
import os

# Nazwa pliku do przechowywania danych
FILE_PATH = "inventory.csv"

def initialize_inventory():
    """Tworzy plik CSV, jeśli nie istnieje, lub wczytuje istniejące dane."""
    if os.path.exists(FILE_PATH):
        try:
            # Wczytanie istniejących danych
            df = pd.read_csv(FILE_PATH)
            # Upewnienie się, że kolumny mają właściwy typ, jeśli plik nie jest pusty
            if not df.empty:
                df['Ilość'] = df['Ilość'].astype(int)
            return df
        except pd.errors.EmptyDataError:
            # Plik istnieje, ale jest pusty
            return pd.DataFrame({'Nazwa': [], 'Ilość': []})
        except Exception as e:
            # Inne błędy odczytu
            st.error(f"Błąd podczas wczytywania CSV: {e}")
            return pd.DataFrame({'Nazwa': [], 'Ilość': []})
    else:
        # Utworzenie nowego DataFrame dla pustego magazynu
        return pd.DataFrame({'Nazwa': [], 'Ilość': []})

def save_inventory(df):
    """Zapisuje DataFrame do pliku CSV i wymusza ponowne uruchomienie aplikacji."""
    df.to_csv(FILE_PATH, index=False)
    # st.rerun() jest kluczowe dla odświeżenia widoku po zapisie, 
    # ponieważ Streamlit nie wie, że plik się zmienił.
    st.rerun()

def main():
    st.set_page_config(page_title="Magazyn (CSV)", layout="wide")
    st.title("📦 Magazyn Bez Sesji (Streamlit + Plik CSV)")
    st.markdown("⚠️ Ta wersja zachowuje stan poprzez odczyt i zapis do pliku **`inventory.csv`** (bez `st.session_state`).")

    # 1. Wczytanie aktualnego stanu z pliku (wykonywane przy każdym uruchomieniu skryptu)
    current_df = initialize_inventory()

    # --- Sekcja Dodawania Towaru ---
    st.header("➕ Dodaj Nowy Towar")
    
    with st.form(key='add_item_form', clear_on_submit=True):
        new_item = st.text_input("Nazwa Towaru", placeholder="Wpisz np. Monitor 27 cali")
        quantity = st.number_input("Ilość", min_value=1, value=1, step=1)
        add_button = st.form_submit_button("Dodaj do Magazynu")

        if add_button and new_item:
            # Utworzenie nowego wiersza i dołączenie go do DataFrame
            new_row = pd.DataFrame([{'Nazwa': new_item.strip(), 'Ilość': int(quantity)}])
            # Łączymy stary i nowy DataFrame
            updated_df = pd.concat([current_df, new_row], ignore_index=True)
            
            st.success(f"Dodano: **{new_item.strip()}** (Ilość: {int(quantity)}). Zapis do pliku CSV...")
            save_inventory(updated_df) 

        elif add_button and not new_item:
            st.warning("Wpisz nazwę towaru.")

    # --- Sekcja Wyświetlania i Usuwania Towaru ---
    st.header("📊 Aktualny Stan Magazynu")
    
    if not current_df.empty:
        # Kopia DataFrame do wyświetlania i dodania kolumny 'ID'
        current_df_display = current_df.copy()
        current_df_display.insert(0, 'ID', range(1, 1 + len(current_df_display)))
        
        st.dataframe(current_df_display, use_container_width=True, hide_index=True)
        
        # Usuwanie towaru
        st.subheader("➖ Usuń Towar po ID")
        
        # Lista dostępnych ID
        available_ids = current_df_display['ID'].tolist()
        
        if available_ids:
            col_remove, col_info = st.columns([1, 4])
            
            with col_remove:
                # W Streamlit selectbox wymaga domyślnego indexu, jeśli jest puste, ale tutaj mamy IDs
                id_to_remove = st.selectbox("Wybierz ID do usunięcia:", available_ids, index=0)
                
                if st.button("Usuń Wybrany"):
                    # ID jest liczone od 1, indeks listy/DataFrame od 0
                    index_to_remove = id_to_remove - 1 
                    
                    if 0 <= index_to_remove < len(current_df):
                        removed_name = current_df.iloc[index_to_remove]['Nazwa']
                        
                        # Usunięcie wiersza i resetowanie indeksów
                        updated_df = current_df.drop(current_df.index[index_to_remove]).reset_index(drop=True)
                        
                        st.success(f"Usunięto: **{removed_name}** (ID: {id_to_remove}). Zapis do pliku CSV...")
                        save_inventory(updated_df) 
                    else:
                        st.error("Nieprawidłowy numer ID. Spróbuj ponownie.")
            
            with col_info:
                st.info("Stan jest zapisywany w pliku CSV. **Pamiętaj:** W darmowych środowiskach chmurowych dane w pliku CSV mogą być niestałe (tymczasowe).")
            
    else:
        st.info("Magazyn jest pusty. Użyj formularza powyżej, aby dodać pierwszy towar.")


if __name__ == "__main__":
    main()
