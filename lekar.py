from korisnik import Korisnik

class Lekar(Korisnik):

    def __init__(self, jmbg, ime, prezime, datum_rodjenja, specijalizacija):
        super().__init__(jmbg, ime, prezime, datum_rodjenja)
        self.__specijalizacija = specijalizacija

    def __str__(self):
        recnik = super().__str__()
        recnik["Specijalizacija"] = self.__specijalizacija

        return recnik

    @property
    def specijalizacija(self):
        return self.__specijalizacija

    @specijalizacija.setter
    def specijalizacija(self, nova_specijalizacija):
        self.__specijalizacija = nova_specijalizacija