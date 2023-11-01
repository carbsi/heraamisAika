import json
from datetime import datetime, timedelta

class Heratys:
    def __init__(self, aika, paivamaara):
        self.aika = datetime.strptime(aika, "%H:%M").time()
        self.paivamaara = datetime.strptime(paivamaara, "%d.%m.%Y").date()

class HeratystenSeuranta:
    def __init__(self):
        self.heratykset = []
        self.lataa_heratykset()

    def lisaa_heratys(self, aika, paivamaara):
        heratys = Heratys(aika, paivamaara)
        self.heratykset.append(heratys)
        self.tallenna_heratykset()

    def nayta_heratykset(self, alkupaivamaara, loppupaivamaara):
        alku = datetime.strptime(alkupaivamaara, "%d.%m.%Y").date()
        loppu = datetime.strptime(loppupaivamaara, "%d.%m.%Y").date()
        aikojen_summa = timedelta()
        lukumaara = 0
        for heratys in self.heratykset:
            if alku <= heratys.paivamaara <= loppu:
                print(f"{heratys.paivamaara.strftime('%d.%m.%Y')} - {heratys.aika.strftime('%H:%M')}")
                heratysaika = datetime.combine(datetime.min, heratys.aika) - datetime.min
                aikojen_summa += heratysaika
                lukumaara += 1

        if lukumaara > 0:
            keskiarvo = (datetime.min + aikojen_summa // lukumaara).time()
            print(f"Keskiarvo heräämisajasta: {keskiarvo.strftime('%H:%M')}")
        else:
            print("Ei herätyksiä valitulla aikavälillä.")

    def tallenna_heratykset(self):
        with open("heratykset.json", "w") as tiedosto:
            json.dump([{"aika": heratys.aika.strftime("%H:%M"), "paivamaara": heratys.paivamaara.strftime("%d.%m.%Y")} for heratys in self.heratykset], tiedosto)

    def lataa_heratykset(self):
        try:
            with open("heratykset.json", "r") as tiedosto:
                data = json.load(tiedosto)
                self.heratykset = [Heratys(heratys['aika'], heratys['paivamaara']) for heratys in data]
        except FileNotFoundError:
            pass

def main():
    seuranta = HeratystenSeuranta()

    while True:
        print("\nHeratysten Seuranta")
        print("1. Lisaa Heratys")
        print("2. Nayta Heratykset")
        print("3. Poistu")

        valinta = input("Anna valinta: ")

        if valinta == '1':
            aika = input("Anna heratysaika (HH:MM): ")
            paivamaara = input("Anna paivamaara (PP.KK.VVVV): ")
            seuranta.lisaa_heratys(aika, paivamaara)
        elif valinta == '2':
            alkupaivamaara = input("Anna alkupaivamaara (PP.KK.VVVV): ")
            loppupaivamaara = input("Anna loppupaivamaara (PP.KK.VVVV): ")
            seuranta.nayta_heratykset(alkupaivamaara, loppupaivamaara)
        elif valinta == '3':
            break
        else:
            print("Virheellinen valinta.")

if __name__ == "__main__":
    main()
