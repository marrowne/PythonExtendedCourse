"""
Zaprogramuj klasę ObiektyDodawalne, która implementuje operator ’+’.
Wynikiem działania

    >>> obj1 + obj2

gdzie obj1 i obj2 są obiektami klasy (a jeszcze lepiej podklasy!)
ObiektyDodawalne a wynik obiektem klasy ObiektyDodawalne zawierający wszystkie
pola obj1 i obj2. W przypadku konfliktu, tj. gdy obj1 i obj2 zawierają pole o
tej samej nazwie program powinien wybrać dowolną wartość i wypisać ostrzeżenie.
Wykonaj to zadanie operując wprost na słowniku zmiennych obiektu. Zaimplementuj
kontrolę poprawności danych, tj. sprawdzenie, czy obj2 jest klasy
(lub podklasy) ObiektyDodawalne.
"""

class ObiektyDodawalne:
    def __add__(self, obj2):
        if (self.__class__.__name__ != 'ObiektyDodawalne' \
                and ObiektyDodawalne not in self.__class__.__bases__)\
                or \
                (obj2.__class__.__name__ != 'ObiektyDodawalne'\
                and ObiektyDodawalne not in obj2.__class__.__bases__):
            raise "Drugi element nie należy do klasy ObiektyDodawalne"

        new_obj = ObiektyDodawalne()
        new_obj.__dict__ = self.__dict__.copy()
        dict2 = obj2.__dict__.copy()

        while dict2 != {}:
            (key, value) = dict2.popitem()
            if key in new_obj.__dict__:
                print("Pole", key, "występuje w obu klasach")
            new_obj.__dict__[key] = value
        return new_obj



class Obiekt1(ObiektyDodawalne):
    def __init__(self, arg1, arg2):
        self.val1 = arg1
        self.val2 = arg2

class Obiekt2(ObiektyDodawalne):
    def __init__(self, arg1, arg2):
        self.val3 = arg1
        self.val4 = arg2

class Obiekt3(ObiektyDodawalne):
    def __init__(self, arg1, arg2):
        self.val1 = arg1
        self.val3 = arg2



obj1 = Obiekt1(1,2)
obj2 = Obiekt3(3,4)

obj = obj1 + obj2
print("obj =", obj.__dict__)
print("obj1 =", obj1.__dict__)
print("obj2 =",obj2.__dict__)