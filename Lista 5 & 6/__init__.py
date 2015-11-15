"""
LISTA 5
Napisz pakiet użytecznych narzędzi webowych, które pomogą pielęgnować
i ulepszać prowadzony serwis:

    1. moduł przeglądający strony WWW (pliki *.html) podanym katalogu
    i podkatalogach i sprawdzający, czy odnośniki do innych stron czy obrazków
    są aktywne;
    2. moduł przeglądający strony serwisu (również przeglądając pliki) i dla
    każdej strony (pliku) wypisujący, w których plikach są odnośniki do niej.

Zaimplementuj te moduły jako iteratory zwracające wynik odpowiednich akcji.

----------------------------------------------------------------------------
Moduł 1 został przeze mnie rozszerzony o sprawdzanie w strony w sieci.

Moduł 1 obsługuje katalogi wyłącznie z plikami w formacie UTF-8.
Dla przykładu ISO-8852-2 jest niewspierane.

Za zgodą oceniającego moduły nie zostały zaimplementowane jako iteratory.
"""

"""
LISTA 6
Zmodyfikuj zadanie z poprzedniej listy tak, aby poszczególne „podzadania”
przeglądania stron były wykonywane w wątkach lub odrębnych procesach.
W szczególności, aby operacje odczytu plików/pobierania stron znalazły się w
odrębnych wątkach bądź procesach. Sprawdź, czy wykorzystywane w programie
biblioteczne struktury danych są bezpieczne ze względu na wątki i odpowiednio
zmodyfikuj operacje na nich, jeżeli nie nadają się do programów wielowątkowych.
"""

from lists import *
from relative import *

checkFolder('/home/moohrdy/Dokumenty/WWWCourse')

print('\n')
obj = Links('/home/moohrdy/Dokumenty/WWWCourse')
print(obj.linksPrint())

obj1 = LinkChecker('http://onet.pl')
print("Poprwność wszystkich odnośników na stronie Onetu:", obj1.checkLinks() == True and obj1.checkImages() == True)