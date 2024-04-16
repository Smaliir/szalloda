from abc import ABC, abstractmethod
from datetime import datetime

# Szoba absztrakt osztály
class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

    @abstractmethod
    def info(self):
        pass

# EgyágyasSzoba osztály
class EgyagyasSzoba(Szoba):
    def info(self):
        return f"Egyágyas szoba, szobaszám: {self.szobaszam}, ár: {self.ar} Ft/éj"

# KétagyasSzoba osztály
class KetagyasSzoba(Szoba):
    def info(self):
        return f"Kétagyas szoba, szobaszám: {self.szobaszam}, ár: {self.ar} Ft/éj"

# Szálloda osztály
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = {}

    def szoba_hozzaadas(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szobaszam, datum):
        if datum < datetime.now().date():
            return "Hibás dátum, visszamenőleg nem lehet szobát foglalni."
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                if (datum, szobaszam) not in self.foglalasok:
                    self.foglalasok[(datum, szobaszam)] = szoba
                    return f"Foglalás sikeres: {szoba.info()}, dátum: {datum}"
        return "A szoba nem elérhető."

    def foglalas_lemondas(self, szobaszam, datum):
        key = (datum, szobaszam)
        if key in self.foglalasok:
            del self.foglalasok[key]
            return "A foglalás törölve."
        return "Nincs ilyen foglalás."

    def foglalasok_listaja(self):
        if not self.foglalasok:
            return "Nincsenek foglalások."
        return "\n".join([f"Dátum: {datum}, {self.foglalasok[(datum, szobaszam)].info()}" for datum, szobaszam in self.foglalasok])

# Felhasználói interakció
def felhasznaloi_interfesz(szalloda):
    while True:
        print("\n1 - Foglalás létrehozása")
        print("2 - Foglalás lemondása")
        print("3 - Foglalások listázása")
        print("4 - Kilépés")
        valasztas = input("Válassz egy opciót: ")

        if valasztas == '1':
            szobaszam = int(input("Szobaszám: "))
            datum = input("Dátum (yyyy-mm-dd): ")
            try:
                datum = datetime.strptime(datum, '%Y-%m-%d').date()
                print(szalloda.foglalas(szobaszam, datum))
            except ValueError:
                print("Hibás dátumformátum.")
        elif valasztas == '2':
            szobaszam = int(input("Szobaszám: "))
            datum = input("Dátum (yyyy-mm-dd): ")
            try:
                datum = datetime.strptime(datum, '%Y-%m-%d').date()
                print(szalloda.foglalas_lemondas(szobaszam, datum))
            except ValueError:
                print("Hibás dátumformátum.")
        elif valasztas == '3':
            print(szalloda.foglalasok_listaja())
        elif valasztas == '4':
            print("Kilépés...")
            break
        else:
            print("Érvénytelen opció.")

# Adatok inicializálása és tesztelése
def rendszer_inditas():
    szalloda = Szalloda("Hotel Zafír")
    szalloda.szoba_hozzaadas(EgyagyasSzoba(101, 15000))
    szalloda.szoba_hozzaadas(KetagyasSzoba(102, 20000))
    szalloda.szoba_hozzaadas(KetagyasSzoba(103, 22000))
    # 5 foglalás inicializálása
    datumok = ["2024-12-24", "2024-12-25", "2024-12-26", "2024-12-27", "2024-12-28"]
    for i, datum in enumerate(datumok):
        szalloda.foglalas(101 + i % 3, datetime.strptime(datum, '%Y-%m-%d').date())

    felhasznaloi_interfesz(szalloda)

rendszer_inditas()
