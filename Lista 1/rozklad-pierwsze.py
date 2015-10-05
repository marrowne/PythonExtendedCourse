#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Lista 1
Zadanie 4 

Napisz jednoargumentową funkcję rozklad(n) która oblicza rozkład
liczby n na czynniki pierwsze i zwraca jako wynik listę par 
[(p1, w1),(p2, w2), . . . ,(pk, wk)] taką, że

	n = p^w1 ∗ p^w2 ∗ . . . ∗p^wk

oraz p1, . . . , pk są różnymi liczbami pierwszymi. Na przykład

>>> rozklad(756)
[(2, 2), (3, 3), (7, 1)]
"""

from math import *

def factr(x):
    """    
    Funkcja przyjmująca liczbę tworząca
    listę par postaci (liczba pierwsza, wykładnik)
    """
    if x <= 0:
        return [(0,1)]
    i = 2
    p = 0 # zmienne przechowujące aktualną
    w = 0 # podstawę oraz wykładnik
    
    list = [] # używana jest tablica (lista), nie bepośrednie wypisywanie

    while i <= floor( sqrt(x) ):
        if x % i == 0:
            list, p, w = pair(i, list, p, w)
            x //= i
        else:
            i += 1
            
    if x != p:    # jeżeli nie trzeba dodać jeszcze jednej potęgi
        list.append( (p,w) )
    else:       # wpp. powiększ wykładnik liczby pierszej i zakończ
                # działanie funkcji ( tak, żeby znowu nie nie dodać (x,1) )
        list.append( (p,w+1) )
        return list
    if x > 1:
        list.append( (x,1) )

    return list
    
def pair(i, list, p, w):
    """ 
    Funkcja tworząca pary oraz powiększająca wykładniki.
    
    Funkcja przyjmuje aktualną podstawę (liczbę pierwszą),
    dotychczasową listę, ostatnią podstawę, oraz wykładnik
    """ 

    if i == p:
        w += 1
    else:
        if p != 0: list.append( (p,w) )
        p = i
        w = 1
    
    return list, p, w


print("Podaj liczbę: ")
number = int( input() )
list = factr(number)
print(list)
