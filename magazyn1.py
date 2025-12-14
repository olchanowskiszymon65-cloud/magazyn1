import streamlit as st
import json
from urllib.parse import quote, unquote

# Klucz, pod którym będziemy przechowywać stan magazynu w URL
QUERY_KEY = "inventory_data"

def load_inventory_from_query():
    """Wczytuje stan magazynu z parametru URL i dekoduje go z JSON."""
    
    # st.query_params zwraca ImmutableDict. Używamy .get() i dekodowania.
    encoded_data = st.query_params.get(QUERY_KEY, '[]')
    
    try:
        # Dekodowanie: najpierw unquote URL, potem parsowanie JSON
        inventory_json = unquote(encoded_data)
        inventory = json.loads(inventory_json)
    except Exception:
        # W przypadku błędu parsowania lub braku danych, zwracamy pustą listę
        inventory = []
        
    return inventory

def save_inventory_to_query(inventory):
    """Koduje stan magazynu do JSON, URL i zapisuje go w parametrach URL."""
    
    # Kodowanie: najpierw JSON, potem quote URL
    inventory_json = json.dumps(inventory)
    encoded_data = quote(inventory_json)
    
    # Użycie st.query_params do aktualizacji URL i wymuszenia rerunu
    st.query_params[QUERY_KEY] = encoded_data
    # Streamlit automatycznie wywoła st.rerun() po zmianie query_params

def main():
    """Główna funkcja aplikacji Streamlit."""

    st.title("📦 Prosty Magazyn (Streamlit + Parametry URL)")
    st.markdown("⚠️ **UWAGA:** Ta wersja przechowuje stan magazynu w parametrach URL. Jest to **niezalecany** sposób zarządzania stanem, ale spełnia warunek *bez `st.session_state`*.")

    # 1. Wczytanie aktualnego stanu
    current_inventory = load_inventory_from_query()
    
    new_inventory = list(current_inventory) # Używamy kopii do modyfikacji

    # --- Sekcja Dodawania Towaru ---
    st.header("1. Dodaj Nowy Towar")
    
    with st.form(key='add_item_form', clear_on_submit=True):
        new_item = st.text_input("Nazwa Towaru (np. 'Laptop')", key='new_item_input')
        quantity = st.number_input("Ilość", min_value=1, value=1, step=1, key='quantity_input')
        add_button = st.form_submit_button("Dodaj do Magazynu")

        if add_button and new_item:
            item_data = {"name": new_item.strip(), "quantity": quantity}
            new_inventory.append(item_data)
            st.success(f"Dodano: {new_item.strip()} (Ilość: {quantity}). Stan zaktualizowany w URL.")
            save_inventory_to_query(new_inventory)
            # Nie trzeba st.rerun(), save_inventory_to_query to robi

        elif add_button and not new_item:
            st.warning("Wpisz nazwę towaru, aby go dodać.")

    # --- Sekcja Wyświetlania i Usuwania Towaru ---
    st.header("2. Aktualny Stan Magazynu")
    
    if current_inventory:
        import pandas as pd
        df = pd.DataFrame(current_inventory)
        
        # Wyświetlanie listy
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Usuwanie towaru
        st.subheader("Usuń Towar")
        
        item_names = [item['name'] for item in current_inventory]
        
        item_to_remove = st.selectbox("Wybierz towar do usunięcia:", item_names)
        
        if st.button("Usuń Wybrany Towar"):
            
            # Wyszukujemy i usuwamy element z KOPYT
            index_to_remove = -1
            for i, item in enumerate(new_inventory):
                if item['name'] == item_to_remove:
                    index_to_remove = i
                    break
            
            if index_to_remove != -1:
                del new_inventory[index_to_remove]
                st.success(f"Usunięto: {item_to_remove}. Stan zaktualizowany w URL.")
                save_inventory_to_query(new_inventory)
            else:
                st.error("Wystąpił błąd podczas usuwania.")
            
    else:
        st.info("Magazyn jest pusty. Dodaj pierwszy towar powyżej.")


if __name__ == "__main__":
    main()
