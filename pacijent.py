from korisnik import Korisnik

class Pacijent(Korisnik):

    def __init__(self, jmbg, ime, prezime, datum_rodjenja, lbo):
        super().__init__(jmbg, ime, prezime, datum_rodjenja)
        self.__lbo = lbo

    def __str__(self):
        recnik = super().__str__()
        recnik["LBO"] = f"{self.__lbo}"

        return recnik

    @property
    def lbo(self):
        return self.__lbo

    @lbo.setter
    def lbo(self, novi_lbo):
        self.__lbo = novi_lbo
