class Korisnik:

    def __init__(self, jmbg, ime, prezime, datum_rodjenja):
        self.__jmbg = jmbg
        self.__ime = ime
        self.__prezime = prezime
        self.__datumRodjenja = datum_rodjenja

    def __str__(self):
        recnik = {}
        recnik["Ime"] = self.__ime
        recnik["Prezime"] = self.__prezime
        recnik["Datum rodjenja"] = self.__datumRodjenja
        recnik["JMBG"] = self.__jmbg

        return recnik 

    @property
    def jmbg(self):
        return self.__jmbg
        
    @jmbg.setter
    def jmbg(self, novi_jmbg):
        self.__jmbg = novi_jmbg
        
    @property
    def ime(self):
        return self.__ime
        
    @ime.setter
    def ime(self, novo_ime):
        self.__ime = novo_ime
        
    @property
    def prezime(self):
        return self.__prezime
        
    @prezime.setter
    def prezime(self, novo_prezime):
        self.__prezime = novo_prezime
        
    @property
    def datum_rodjenja(self):
        return self.__datumRodjenja
        
    @datum_rodjenja.setter
    def datum_rodjenja(self, novi_datum):
        self.__datumRodjenja = novi_datum