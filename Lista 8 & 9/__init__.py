"""
LISTA 8
Poniższe zadania polegają na implementacji aplikacji przechowujących trwale
proste dane osobiste. Każda aplikacja powinna implementować:
• trwałe przechowywanie danych;
• graficzny interfejs użytkownika (np. w GTK+);
• wyświetlenie listy danych;
• elementarne wyszukiwanie danych spełniających jakiś prosty warunek;
• podstawowe operacje dodawania, odczytu, aktualizacji i usuwania
        pojedynczych danych.
-------------------------------------------------------------------------------
Zaprogramuj własny notatnik z kontaktami do znajomych zawierający
ich numery telefonów, adresy email czy datę ostatniego wyświetlenia tego
kontaktu.
"""

"""
LISTA 9
Wybierz jeden z wcześniejszych programów wykonanych w ramach pracowni z
Pythona, ale nie starsze niż z listy 4. Wykonaj dla niego następujące zadania:

1. Przygotuj dla niego testy jednostkowe, można skorzystać z pyunit albo pydoc.
2. Sprawdź za pomocą profilowania, które fragmenty programu pochłaniają
    najwięcej czasu.
3. Poszukaj informacji o "PEP 8" (Python Enhancement Proposals). Za pomocą
    pakietu pep8 checker3 sprawdź zgodność swojego kodu źródłowego
    z zaleceniami PEP 8.
4. Poszukaj informacji o automatycznym generowaniu dokumentacji na podstawie
    kodu źródłowego oraz zawartych w nim komentarzy. Wygeneruj taką
    dokumentację w jakimś popularnym formacie (html, pdf, etc).
"""

from gui import *

app = Gui()
to_main_table(app.liststore, app.db.show_contacts())
Gtk.main()
