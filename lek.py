class Lek:

    def __init__(self, sifra_jkl, naziv, proizvodac, tip_leka):
        self.__sifraJKL = sifra_jkl
        self.__naziv = naziv
        self.__proizvodjac = proizvodac
        self.__tipLeka = tip_leka

    def __str__(self):
        recnik = {}
        recnik["Naziv leka"] = self.__naziv
        recnik["Proizvodjac leka"] = self.__proizvodjac
        recnik["Tip leka"] = self.__tipLeka
        recnik["Sifra JKL"] = self.__sifraJKL

        return recnik

    @property
    def sifra_jkl(self):
        return self.__sifraJKL

    @sifra_jkl.setter
    def sifra_jkl(self, nova_sifra_jkl):
        self.__sifraJKL = nova_sifra_jkl

    @property
    def naziv(self):
        return self.__naziv

    @naziv.setter
    def naziv(self, novi_naziv):
        self.__naziv = novi_naziv

    @property
    def proizvodjac(self):
        return self.__proizvodjac

    @proizvodjac.setter
    def proizvodjac(self, novi_proizvodjac):
        self.__proizvodjac = novi_proizvodjac

    @property
    def tip(self):
        return self.__tipLeka

    @tip.setter
    def tip(self, novi_tip):
        self.__tipLeka = novi_tip