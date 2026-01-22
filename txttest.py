import modules.objectLib as ol



def print_menu():
    print("\n" + "="*30)
    print("      TODO LIST - TEST")
    print("="*30)
    print("1. Wyświetl zadanie")
    print("2. Wyświetl wszystkie zadania")
    print("3. Dodaj nowe zadanie")
    print("4. Edytuj zadanie")
    print("5. Usuń zadanie")
    print("6. Generuj losowe zadania (Mock)")
    print("7. Wyczyść całą bazę")
    print("0. Wyjdź")
    print("-" * 30)

def app():
    # 1. Inicjalizacja bazy danych i sesji
    print("Uruchamianie bazy danych...")
    session = ol.dbSelfHost()
    print("Baza gotowa.")

    while True:
        print_menu()
        wybor = input("Wybierz opcję: ")

        match wybor:

            case '1': # Wyświetlanie pojedynczego
                try:
                    id_task = int(input("Podaj ID zadania: "))
                    task_info = ol.getTask(id_task, session)

                    if task_info == -1:
                        print("[BŁĄD] Nie znaleziono zadania o takim ID.")
                    else:
                        print("\n--- SZCZEGÓŁY ZADANIA ---")
                        for klucz, wartosc in task_info.items():
                            print(f"{klucz}: {wartosc}")
                        print("-------------------------")
                        
                except ValueError:
                    print("[BŁĄD] ID musi być liczbą całkowitą.")

            case '2': # Wyświetlanie wszystkich
                tasks = ol.getAll(session)
                if not tasks:
                    print("\n[INFO] Lista zadań jest pusta.")
                else:
                    print(f"\nZnaleziono {len(tasks)} zadań:")
                    for t in tasks:
                        print(t)

            case '3': # Dodawanie
                tytul = input("Podaj tytuł: ")
                opis = input("Podaj opis: ")
                try:
                    prio = int(input("Podaj priorytet (1-3): "))
                    result = ol.createTask(tytul, opis, prio, session)
                    print(f"[SUKCES] Dodano zadanie. ID: {result}")
                except ValueError:
                    print("[BŁĄD] Priorytet musi być liczbą!")

            case '4': # Edycja
                try:
                    id_task = int(input("Podaj ID zadania do edycji: "))
                    if ol.getTask(id_task, session) == -1:
                        print(f"[BŁĄD] Nie znaleziono zadania o ID: {id_task}")
                        continue

                    print("Co chcesz zmienić?")
                    print("1. Tytuł")
                    print("2. Opis")
                    print("3. Priorytet")
                    print("4. Status ukończenia")
                    field_choice = input("Wybór pola: ")
                
                    
                    match field_choice:
                        case '1':
                            new_val = input("Wprowadź nową wartość: ")
                            ol.editTask(id_task, ol.EditType.TITLE, new_val, session)
                        case '2':
                            new_val = input("Wprowadź nową wartość: ")
                            ol.editTask(id_task, ol.EditType.DESC, new_val, session)
                        case '3':
                            new_val = input("Wprowadź nową wartość (1/2/3): ")
                            ol.editTask(id_task, ol.EditType.PRIOR, int(new_val), session)
                        case '4':
                            new_val = input("Wprowadź nową wartość (true/false): ")
                            if new_val.lower() not in ['true', 'false']:
                                print("[BŁĄD] Wartość musi być 'true' lub 'false'.")
                                continue
                            elif new_val.lower() == 'true':
                                val_bool = True
                            else:
                                val_bool = False
                            ol.editTask(id_task, ol.EditType.COMPL, val_bool, session)
                        case _:
                            print("Nieznane pole.")

                    print("[INFO] Próba edycji zakończona.")

                except ValueError:
                    print("[BŁĄD] Wprowadzono niepoprawne dane.")

            case '5': # Usuwanie
                try:
                    id_task = int(input("Podaj ID zadania do usunięcia: "))
                    result = ol.deleteTask(id_task, session)
                    if result == 0:
                        print("[SUKCES] Zadanie usunięte.")
                    else:
                        print("[BŁĄD] Nie znaleziono zadania o takim ID.")
                except ValueError:
                    print("[BŁĄD] ID musi być liczbą.")

            case '6': # Mock
                try:
                    ile = int(input("Ile losowych zadań wygenerować?: "))
                    ol.mock(ile, session)
                    print(f"[SUKCES] Wygenerowano {ile} zadań.")
                except ValueError:
                    print("[BŁĄD] Podaj liczbę.")
            
            case '7': # Czyszczenie
                dec = input("Czy na pewno usunąć WSZYSTKO? (t/n): ")
                if dec.lower() == 't':
                    ol.clearTasks(session)
                    print("[INFO] Baza wyczyszczona.")

            case '0': # Wyjście
                print("Zamykanie programu...")
                session.close()
                break

            case _: # Domyślny przypadek (else)
                print("Nieznana opcja, spróbuj ponownie.")

if __name__ == "__main__":
    app()