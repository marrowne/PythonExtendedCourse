"""
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

from gui import *

app = Gui()
to_main_table(app.liststore, app.db.show_contacts())
Gtk.main()