from sys import stderr
from datetime import datetime
from lab6.lab6_enums import UslugaNaLetu

class Putnik:

    def __init__(self, ime, zemlja, pasos, cena_karte, COVID_bezbedan=False):
        self.ime = ime
        self.drzava = zemlja
        self.pasos = pasos
        self.COVID_bezbedan = COVID_bezbedan
        self.cena_karte = cena_karte
        self.usluge = []


    @property
    def pasos(self):
        # if not hasattr(self, '_Putnik__pasos'):
        #     self.__pasos = None
        # return self.__pasos
        try:
            return self.__pasos
        except AttributeError:
            self.__pasos = None
            return self.__pasos


    @pasos.setter
    def pasos(self, value):
        if isinstance(value, str) and len(value) == 6 and all([ch.isdigit() for ch in value]):
            self.__pasos = value
            return
        if isinstance(value, int) and len(str(value)) == 6:
            self.__pasos = str(value)
            return
        stderr.write(f"Iz pasos.setter: Greska pri postavljanju vrednosti atributu 'pasos': "
                     f"pogresna vrednost ulaznog argumenta ({value})\n")


    @property
    def cena_karte(self):
        try:
            return self.__cena_karte
        except AttributeError:
            self.__cena_karte = None
            return self.__cena_karte

    @cena_karte.setter
    def cena_karte(self, value):
        if not isinstance(value, (str, float, int)):
            stderr.write("Iz cena_karte.setter: pogresna vrednost ulaznog argumenta\n")
            return
        if isinstance(value, (str, float)):
            try:
                value = int(value)
            except ValueError as err:
                stderr.write(f"Iz cena_karte.setter: {err}\n")
                return
        if value > 0:
            self.__cena_karte = value


    def __str__(self):
        putnik_str = f"{self.ime}\n"
        putnik_str += f"\tDrzava: {self.drzava}\n"
        putnik_str += f"\tBroj pasosa: {self.pasos if self.pasos else 'nepoznat'}\n"
        putnik_str += f"\tCOVID status: {'bezbedan' if self.COVID_bezbedan else 'inficiran'}\n"
        putnik_str += f"\tCena karte: {self.cena_karte if self.cena_karte else 'karta jos nije placena'}\n"
        if len(self.usluge) == 0:
            putnik_str += "\tNema dodatnih usluga"
        else:
            putnik_str += f"\tDodatne usluge: {', '.join([usluga.value for usluga in self.usluge])}"
        return putnik_str


    @classmethod
    def covid_bezbedan_Francuz(cls, ime, pasos, cena_karte):
        return cls(ime, "Francuska", pasos, cena_karte, True)


    def __eq__(self, other):
        if not isinstance(other, Putnik):
            return False

        if self.drzava and other.drzava and self.pasos and other.pasos:
            return self.drzava == other.drzava and self.pasos == other.pasos

        stderr.write("Iz __eq__: Nije moguce uporediti dva data objekta klase Putnik jer bar jedan od njih "
                     "nema sve podatke potrebne za poredjenje\n")


    def azuriraj_COVID_bezbedan(self, tip_uverenja, datum_uverenja):
        if (not isinstance(tip_uverenja, str)) or (tip_uverenja.lower() not in ['vakcinacija', 'negativan_test']):
            stderr.write("Iz azuriraj_COVID_bezbedan: pogresna vrednost za ulazni argument 'tip_uverenja'\n")
            return
        if not isinstance(datum_uverenja, (str, datetime)):
            stderr.write("Iz azuriraj_COVID_bezbedan: pogresna vrednost za ulazni argument 'datum_uverenja'\n")
            return
        if isinstance(datum_uverenja, str):
            datum_uverenja = datetime.strptime(datum_uverenja, '%d/%m/%Y')

        dt_delta = datetime.now() - datum_uverenja
        self.COVID_bezbedan = (tip_uverenja.lower() == 'vakcinacija' and dt_delta.days < 365) or \
                (tip_uverenja.lower() == 'negativan_test' and dt_delta.days < 3)



if __name__ == '__main__':

    bob = Putnik("Bob Smith", "UK", "123456", 250.0, True)
    john = Putnik("John Smith", "USA", 987656, 450, True)
    anna = Putnik("Anna Smith", "Spain", "987659", 375)
    luis = Putnik.covid_bezbedan_Francuz("Luis Bouve", "123654", 225)

    print("PUTNICI:\n")
    print(bob)
    print(john)
    print(anna)
    print(luis)

    print("\nPUTNICI NAKON UPDATE-a COVID STATUS-a:\n")
    anna.azuriraj_COVID_bezbedan('vakcinacija', '01/02/2024')
    print(anna)

    luis.azuriraj_COVID_bezbedan('negativan_test', '20/03/2024')
    print(luis)
    print()

    print("Provera da li su 'bob' i 'john' reference na istog putnika")
    print("Isti putnik" if bob == john else "Razliciti putnici")
    print()
    print("Provera da li su 'john' i 'johnny' reference na istog putnika")
    johnny = Putnik("Johnny Smith", "USA", 987656, False)
    print("Isti putnik" if john == johnny else "Razliciti putnici")
