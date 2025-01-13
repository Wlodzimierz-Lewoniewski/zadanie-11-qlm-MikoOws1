import numpy as np
from collections import Counter

def tokenizacja(tekst):
    znaki = '"!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    tekst = ''.join(znak for znak in tekst if znak not in znaki)
    return tekst.lower().split()

def qlm_sortuj(dokumenty, zapytanie, lambda_wartosc=0.5):
    tokeny_dokumenty = [tokenizacja(dok) for dok in dokumenty]
    licznik_terminow = [Counter(dok) for dok in tokeny_dokumenty]
    dlugosci_dokumentow = [len(dok) for dok in tokeny_dokumenty]

    dlugosc_zbioru = sum(dlugosci_dokumentow)
    licznik_zbioru = Counter()
    for terminy in licznik_terminow:
        licznik_zbioru.update(terminy)

    model_zbioru = {termin: liczba / dlugosc_zbioru for termin, liczba in licznik_zbioru.items()}
    zapytanie_tokeny = tokenizacja(zapytanie)

    wyniki = []

    for indeks, (terminy_dok, dlugosc_dok) in enumerate(zip(licznik_terminow, dlugosci_dokumentow)):
        model_dok = {termin: liczba / dlugosc_dok for termin, liczba in terminy_dok.items()}
        wynik = 0

        for termin in zapytanie_tokeny:
            prawd_zbioru = model_zbioru.get(termin, 0)
            prawd_dok = model_dok.get(termin, 0)
            prawd_gladkie = (lambda_wartosc * prawd_dok + (1 - lambda_wartosc) * prawd_zbioru)

            if prawd_gladkie > 0:
                wynik += np.log(prawd_gladkie)

        wyniki.append((indeks, wynik))

    posortowane_dokumenty = sorted(wyniki, key=lambda x: (-x[1], x[0]))
    return [dok[0] for dok in posortowane_dokumenty]

if __name__ == "__main__":
    n = int(input().strip())
    dokumenty = [input().strip() for _ in range(n)]
    zapytanie = input().strip()
    wynik_sortowania = qlm_sortuj(dokumenty, zapytanie)
    print(wynik_sortowania)
