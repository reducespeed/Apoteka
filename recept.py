from pacijent import Pacijent
from lekar import Lekar
from lek import Lek
from datetime import datetime
import json

class Recept:

    def __init__(self, pacijent, datum, izvestaj, lekar, lek, kolicina) -> None:
        self.__pacijent = pacijent
        self.__datum = datum
        self.__izvestaj = izvestaj
        self.__lekar = lekar
        self.__lek = lek
        self.__kolicina = kolicina

    def __str__(self) -> dict:
        recept = {
            "Pacijent": self.__pacijent,
            "Datum": self.__datum,
            "Izvestaj": self.__izvestaj,
            "Lekar": self.__lekar,
            "Lek": self.__lek,
            "Kolicina": self.__kolicina
        }

        return recept