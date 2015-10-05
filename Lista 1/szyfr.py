#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Lista 1
Zadanie 2

Napisz program który szyfruje tekst za pomocą następującego algorytmu
opartego na algorytmie XOR: do zaszyfrowania jest potrzebny klucz k, tj. liczba
z przedziału [0 . . . 255]. Kolejne litery tekstu zamieniamy na odpowiedni
kod ASCII, obliczamy wynik operacji XOR z k i do szyfrogramu wstawiamy wynik
operacji zamieniony na odpowiedni znak ASCII. Na przykład tekst Python za
pomocą klucza 7 (binarnie: 0000 0111) szyfrujemy tak:

###################################################################################
# litery  |     P     |     y     |     t     |     h     |     o     |     n     #
#---------+-----------+-----------+-----------+-----------+-----------+-----------#
# ASCII   | 0101 0000 | 0111 1001 | 0111 0100 | 0110 1000 | 0110 1111 | 0110 1110 #
#---------+-----------+-----------+-----------+-----------+-----------+-----------#
# XOR     | 0101 0111 | 0111 1110 | 0111 0011 | 0110 1111 | 0110 1000 | 0110 1001 #
#---------+-----------+-----------+-----------+-----------+-----------+-----------#
# szyfr   |     W     |     ~     |     s     |     o     |     h     |     i     #
###################################################################################

Program ma mieć postać funkcji zaszyfruj(tekst, klucz), która dla podanego
tekstu i klucza zwraca zaszyfrowany tekst. Zaprogramuj również funkcję
odszyfruj(szyfr, klucz).
"""

def encryption(text, key):
    """
    Funkcja przyjmująca tekst i klucz
    oraz zwracająca zaszyfrowany tekst.
    """
    array = [chr( ord(x) ^ key ) for x in text]
    return ''.join(array)

def decryption(cipher, key):
    """    
    Funkcja przyjmująca tekst i klucz
    oraz zwracająca odszyfrowany tekst.  
    """

    # algorytm szyfrujący jest symetryczny
    encryption(cipher, key)

print("Witaj! Podaj klucz kodujący/dekodujący.") 
key = int(input())

print("Dziękuję. Teraz podawaj to co mam zaszyfrować lub odszyfrować.")
while True:
    inp = input()
    cipher = encryption(inp, key)
    print(cipher)
