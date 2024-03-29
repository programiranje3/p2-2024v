from datetime import datetime
from sys import stderr
from putnik import Putnik

class Let:

    poletanje_dt_format = '%Y-%m-%d %H:%M'

    def __init__(self, broj_leta, poletanje_dt):
        self.broj_leta = broj_leta
        self.vreme_poletanja = poletanje_dt
        self.putnici = list()

    @property
    def vreme_poletanja(self):
        if not hasattr(self, '_Let__vreme_poletanja'):
            self.__vreme_poletanja = None
        return self.__vreme_poletanja

    @vreme_poletanja.setter
    def vreme_poletanja(self, value):
        if not isinstance(value, (datetime, str)):
            stderr.write(f"Iz vreme_poletanja.setter: ocekivan ulazni argument tipa datetime ili str; "
                         f"umesto toga, primljena vrednost tipa {type(value)}\n")
            return
        if isinstance(value, str):
            value = datetime.strptime(value, Let.poletanje_dt_format)
        if value > datetime.now():
            self.__vreme_poletanja = value
        else:
            stderr.write("Iz vreme_poletanja.setter: vreme poletanja se mora odnositi na neki trenutak u buducnosti\n")

    def dodaj_putnika(self, obj):
        if not isinstance(obj, Putnik):
            stderr.write("Iz dodaj_putnika: ulazni argument nije objekat klase Putnik\n")
            return
        if obj in self.putnici:
            stderr.write("Iz dodaj_putnika: putnik se vec nalazi u listi putnika\n")
            return
        if not obj.COVID_bezbedan:
            stderr.write("Iz dodaj_putnika: putnik nema validno uverenje da je COVID bezbedan\n")
            return

        self.putnici.append(obj)
        print(f"Putnik {obj.ime} je uspesno dodat u listu putnika")



if __name__ == '__main__':

    lh1411 = Let('LF1411', '2024-05-05 6:50')
    lh992 = Let('LH992', '2024-05-25 12:20')

    print("\nLETOVI:\n")
    print(lh1411)
    print()
    print(lh992)
    print()

    bob = Putnik("Bob Smith", "UK", "123456", True)
    john = Putnik("John Smith", "USA", 987656, True)
    anna = Putnik("Anna Smith", "Spain", "987659")
    luis = Putnik.covid_bezbedan_Francuz("Luis Bouve", "123654")

    print(f"\nDodavanje putnika na let {lh1411.broj_leta}")
    for p in [bob, john, anna, luis]:
        lh1411.dodaj_putnika(p)

    print(f"\nPokusaj dodavanja putnika koji je vec u listi putnika za let {lh1411.broj_leta}:")
    lh1411.dodaj_putnika(Putnik("J Smith", "USA", "987656", True))
    print()

    print(f"\nPodaci o letu {lh1411.broj_leta} nakon dodavanja putnika na let:\n")
    print(lh1411)
    print()

    # do_poletanja = lh1411.vreme_do_poletanja()
    # if do_poletanja:
    #     dani, sati, mins = do_poletanja
    #     print(f"Vreme preostalo do poletanja leta {lh1411.broj_leta}: "
    #           f"{dani} dana, {sati} sati, i {mins} minuta")
    #
    # print()
    #
    # print("\nPUTNICI NA LETU LH1411 (iter / next):")
    # p_iter = iter(lh1411)
    # try:
    #     while True:
    #         print(next(p_iter))
    # except StopIteration:
    #     print("Svi putnici su izlistani")
    #
    # print()
    # print("\nPUTNICI NA LETU LH1411 (FOR petlja):")
    # for p in iter(lh1411):
    #     print(p)


