"""
Zaprogramuj iterator który przetwarza strumień tekstowy i zwraca kolejne słowa
z tekstu (dla utrudnienia uwzględnij dzielenie słów na końcach wierszy),
pomijając białe znaki i znaki interpunkcyjne. Korzystając z tej implementacji
zaprogramuj obliczanie statystyki długości słów w tekście, tj. ile jest słów
długości 1, ile długości 2 etc.
"""

class WordsIterator:
    def __init__(self, stream):
        self.stream = stream
        self.line = self.stream.readline()

    def __next__(self):
        while True:
            word, space, self.line = self.line.partition(' ')
            if word[-2:] == '-\n':
                word = word[:-2]
                self.__next__()
                word = word + self.__next__()
            word = word.strip('!()-[]{};:\'"\,<>./?@#$%^&*_~')

            if space:
                return word
            else:
                next_chunk = self.stream.readline()
                if next_chunk:
                    self.line = next_chunk
                    return word.rstrip('\n.')
                else:
                    return word.rstrip('\n')

    def __iter__(self):
        return self

def lengths(word, dict):
    if len(word) not in dict:
        dict[len(word)] = 1
    else:
        dict[len(word)] += 1

text = open('input.txt', 'r')

word = WordsIterator(text)
words_lengths = {} # key = length of word, value = amount of words that length
while 1:
    new_word = word.__next__()
    if new_word == '': break
    lengths(new_word, words_lengths)
print(words_lengths)
text.close()