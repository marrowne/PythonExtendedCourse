import xmlrpc.client

"""
Zadanie polega na modyfikacji programu z listy 8 tak, aby powstała aplikacja
rozproszona. Obsługa zdarzeń interfejsu użytkownika zamiast wykonywać operacje
na danych powinna wysyłać odpowiednie żądania do serwera, a zadania (np.
modyfikacja bazy danych) powinien realizować serwer
"""

from gui import *

app = Gui()
with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
    result = proxy.show_contacts()
to_main_table(app.liststore, result)
Gtk.main()
