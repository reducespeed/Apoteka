import os
import json
from operator import itemgetter
from datetime import datetime, date
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pacijent import Pacijent
from lekar import Lekar
from lek import Lek
from recept import Recept


BAZA_FAJL = 'data.json'
BAZA_SADRZAJ = {}


class MyApp(Tk):

    def __init__(self, *args, **kwargs, ):
        self.frames = {}

        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menu = Menu(container)

        pageBar = Menu(menu, tearoff=0)
        fileBar = Menu(menu, tearoff=0)

        menu.add_cascade(menu=fileBar, label="File")
        fileBar.add_command(label="Exit", command=0)

        menu.add_cascade(menu=pageBar, label="Stranice")
        pageBar.add_command(label="Home", command=lambda: self.show_frame(HomePage))
        pageBar.add_command(label="Pacijenti", command=lambda: self.show_frame(PacijentiPage))
        pageBar.add_command(label="Lekari", command=lambda: self.show_frame(LekariPage))
        pageBar.add_command(label="Recepti", command=lambda: self.show_frame(ReceptiPage))
        pageBar.add_command(label="Lekovi", command=lambda: self.show_frame(LekoviPage))

        Tk.config(self, menu=menu)

        for page in (HomePage, PacijentiPage, LekariPage, ReceptiPage, LekoviPage):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


class HomePage(Frame):

    def __init__(self, parent, controler):
        Frame.__init__(self, parent)
        text = Label(self, text="Projekat Apoteka", font='Times 15')
        text.pack(side="top", fill="both", expand=True)


class PacijentiPage(Frame):

    def __init__(self, parent, controler):
        Frame.__init__(self, parent)

        # Frame za widgete sa leve strane ekrana
        self.leftFrame = Frame(self)
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=TRUE)
        # Labela koja stoji iznad polja za prikaz svih pacijenata
        self.spisakLabel = Label(self.leftFrame, text="Spisak pacijenata", font='Times 15')
        self.spisakLabel.pack(fill=X, padx=5, pady=5)
        # Lista svih pacijenata, omoguceno selektovanje samo jedne vrednosti
        self.spisakListBox = Listbox(self.leftFrame, selectmode=SINGLE)
        self.spisakListBox.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)
        self.spisakListBox.bind('<<ListboxSelect>>', self.prikaziPodatke)
        # Polje za unos pretrage pacijenata koje se nalazi ispod polja za prikaz pacijenata
        self.pretragaEntry = Entry(self.leftFrame)
        self.pretragaEntry.pack(side=LEFT, expand=TRUE, fill=BOTH, padx=5, pady=5)
        # Dugme koje otvara popup prozor sa receptima selektovanog pacijenta
        self.receptiButton = Button(self.leftFrame, text="Recepti", font='Times 15')
        self.receptiButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        # Frame za widgete sa desne strane ekrana
        self.rightFrame = Frame(self,)
        self.rightFrame.pack(side=RIGHT, fill=Y)
        # Labela koja stoji iznad polja za prikaz podataka pacijenata
        self.podaciLabel = Label(self.rightFrame, text="Podaci pacijenta", font='Times 15')
        self.podaciLabel.pack(fill=X, padx=5, pady=5)
        # Polje za prikaz podataka o pacijentu, read only
        self.podaciText = Text(self.rightFrame, state=DISABLED)
        self.podaciText.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)
        # Dugme koje otvara popup prozor sa formom za unos novog pacijenta
        self.dodajButton = Button(self.rightFrame, text="Dodaj", font='Times 15', command=self.dodajTopLevel)
        self.dodajButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        # Dugme koje otvara popup prozor sa formom za izmenu postojeceg pacijenta
        self.izmeniButton = Button(self.rightFrame, text="Izmeni", font='Times 15', state=DISABLED, command=self.izmeniTopLevel)
        self.izmeniButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        # Dugme za brisanje obelezenog pacijenta
        self.obrisiButton = Button(self.rightFrame, text="Izbrisi", font='Times 15', state=DISABLED)
        self.obrisiButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)

        # Izvlacenje liste svih pacijenata iz baze
        pacijenti = BAZA_SADRZAJ["Pacijent"]

        # Ubacivanje u listbox
        index = 0
        for pacijent in pacijenti:
            self.spisakListBox.insert(index, f'{pacijent["Ime"]} {pacijent["Prezime"]}')
            index += 1

    def prikaziPodatke(self, *args):
        index = self.spisakListBox.curselection()[0]

        # Formatiranje podataka o pacijentu za ispis
        text = (
            f'Ime: {BAZA_SADRZAJ["Pacijent"][index]["Ime"]}\n'
            f'Prezime: {BAZA_SADRZAJ["Pacijent"][index]["Prezime"]}\n'
            f'Datum rodjenja: {BAZA_SADRZAJ["Pacijent"][index]["Datum rodjenja"]}\n'
            f'JMBG: {BAZA_SADRZAJ["Pacijent"][index]["JMBG"]}\n'
            f'LBO: {BAZA_SADRZAJ["Pacijent"][index]["LBO"]}'
        )
            
        # Vracanje u normalan mod radi upisa teksta
        self.podaciText.config(state=NORMAL)
        # Brisanje sadrzaj texboxa
        self.podaciText.delete(1.0, END)
        # Unos podataka u textbox
        self.podaciText.insert(INSERT, text)
        # Vracanje u read-only mod
        self.podaciText.config(state=DISABLED)
        # Omogucavanje dugmadi za brisanja i izmene
        self.izmeniButton.config(state=NORMAL)
        self.obrisiButton.config(state=NORMAL)

    def dodajTopLevel(self):
        self.topLevel = Toplevel(self)
        self.topLevel.title("Novi pacijent")
        self.topLevel.geometry("300x250")
        self.topLevel.minsize(300, 250)
        self.topLevel.maxsize(300, 250)

        # Unos imena
        self.imeLabel = Label(self.topLevel, text="Ime:", font='Times 15')
        self.imeLabel.grid(row=0, column=0, padx=5, pady=5)
        self.imeEntry = Entry(self.topLevel)
        self.imeEntry.grid(row=0, column=1, padx=5, pady=5)
        # Unos prezimena
        self.prezimeLabel = Label(self.topLevel, text="Prezime:", font='Times 15')
        self.prezimeLabel.grid(row=1, column=0, padx=5, pady=5)
        self.prezimeEntry = Entry(self.topLevel)
        self.prezimeEntry.grid(row=1, column=1, padx=5, pady=5)
        # Unos datuma
        self.rodjenjeLabel = Label(self.topLevel, text="Datum rodjenja:", font='Times 15')
        self.rodjenjeLabel.grid(row=2, column=0, padx=5, pady=5)
        self.rodjenjeEntry = Entry(self.topLevel)
        self.rodjenjeEntry.grid(row=2, column=1, padx=5, pady=5)
        # Unos JMBG-a
        self.jmbgLabel = Label(self.topLevel, text="JMBG:", font='Times 15')
        self.jmbgLabel.grid(row=3, column=0, padx=5, pady=5)
        self.jmbgEntry = Entry(self.topLevel)
        self.jmbgEntry.grid(row=3, column=1, padx=5, pady=5)
        # Unos LBO-a
        self.lboLabel = Label(self.topLevel, text="LBO:", font='Times 15')
        self.lboLabel.grid(row=4, column=0, padx=5, pady=5)
        self.lboEntry = Entry(self.topLevel)
        self.lboEntry.grid(row=4, column=1, padx=5, pady=5)
        # Dugme za primenu pormena
        self.prihvatiButton = Button(self.topLevel, text="Prihvati", command=self.apply_dodajTopLevel)
        self.prihvatiButton.grid(row=5, column=0, padx=10, pady=10)
        # Dugme za odbacivanje promena
        self.odbaciButton = Button(self.topLevel, text="Odbaci", command=self.close_dodajTopLevel)
        self.odbaciButton.grid(row=5, column=1, padx=10, pady=10)
        # Omogucava da osnovni program bude nedostupan kada je popup strana aktivna
        self.topLevel.grab_set()

    def apply_dodajTopLevel(self):
        # vrednost iz polja ime
        ime = self.imeEntry.get()
        # vrednost iz polja prezime
        prezime = self.prezimeEntry.get()
        # vrednost iz pola datum rodjenja ['dan', 'mesec', 'godina']
        rodjenje = self.rodjenjeEntry.get().split('.')
        # formatiran datum u oblik koji nam odgovara za poredjenje datetime.date('godina', 'mesec', 'dan')
        datumRodjenja = date(int(rodjenje[2]), int(rodjenje[1]), int(rodjenje[0]))
        # danasnji datum u dormatu datetime.date('godina', 'mesec', 'dan')
        danasnjiDatum = datetime.now().date()
        # vrednost iz polja jmbg
        jmbg = self.jmbgEntry.get()
        # vrednos iz polja lbo
        lbo = self.lboEntry.get()
        # spisak svih jmbg i lbo-a iz baze
        jmbgLst = []
        lboLst = []

        # Iz sadrzaja baze se izvlaci lista recnika gde svaki recnik predstavlja jednog pacijenta
        # Ukoliko lista pacijenata (pacijenti) nije prazna prolazi se kroz svaki recnik (pacijent)
        # Radi se interacija kroz parove key-value
        # Na osnovu key vrednosti ("JMBG" ili "LBO") value se smesta u jednu od lista (jmbgLst ili lboLst)
        pacijenti = BAZA_SADRZAJ["Pacijent"]
        if pacijenti:
            for pacijent in pacijenti:
                for key, value in pacijent.items():
                    if key == "JMBG":
                        jmbgLst.append(value)
                    elif key == "LBO":
                        lboLst.append(value)

        # Provera uslova za dodavanje novog korisnika
        # Ime: bar dva karaktera
        # Prezime: bar dva karaktera
        # Datum: najkasnije danasnji
        # JMBG: jedinstvena vrednost duzine 13 karaktera
        # LBOL jedinstvem vrednost duzine 11 karaktera
        if len(ime) < 2:
            messagebox.showerror("Error", "Ime mora biti duze od 2 karaktera")
        elif len(prezime) < 2:
            messagebox.showerror("Error", "Prezime mora biti duze od 2 karaktera")
        elif datumRodjenja > danasnjiDatum:
            messagebox.showerror("Error", "Datum moze biti najkasnije danasnji")
        elif jmbg in jmbgLst:
            messagebox.showerror("Error", "JMBG postoji u bazi")
        elif len(jmbg) != 13:
            messagebox.showerror("Error", "JMBG mora biti 13 karaktera")
        elif lbo in lboLst:
            messagebox.showerror("Error", "LBO postoji u bazi")
        elif len(lbo) != 11:
            messagebox.showerror("Error", "LBO mora biti 11 karaktera")
        else:
            # Ako si svi gore uslovi ispunjeni kreira se novi objekat klase Pacijent sa vrednostima iz polja za unos
            novipacijent = Pacijent(jmbg=jmbg, ime=ime, prezime=prezime, datum_rodjenja=datumRodjenja.strftime("%d-%m-%Y"), lbo=lbo)
            # Opis ovog objekta se smesta u globalnu promenljivu kako bi bio dostupan u nastavku programa
            BAZA_SADRZAJ["Pacijent"].append(novipacijent.__str__())
            # Sortiranje pre upisa u fajl
            BAZA_SADRZAJ["Pacijent"].sort(key=itemgetter("Prezime", "Ime"))
            # Takodje ova promena se unosi i u fajl
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)

            # Brisanje teksta u polju za pretragu
            self.pretragaEntry.delete(0, END)
            # Brisanje liste za prikaz pacijenata
            self.spisakListBox.delete(0, END)
            # Ubacivanje u listu za prikaz
            index = 0
            selectIndex = 0
            for pacijent in BAZA_SADRZAJ["Pacijent"]:
                self.spisakListBox.insert(index, f'{pacijent["Ime"]} {pacijent["Prezime"]}')
                if novipacijent.__str__() == pacijent:
                    selectIndex = index

                index += 1

            # Selektovanje novog unosa
            self.spisakListBox.select_set(selectIndex)
            # Formatiranje podataka o pacijentu za ispis
            text = (
                f'Ime: {BAZA_SADRZAJ["Pacijent"][selectIndex]["Ime"]}\n'
                f'Prezime: {BAZA_SADRZAJ["Pacijent"][selectIndex]["Prezime"]}\n'
                f'Datum rodjenja: {BAZA_SADRZAJ["Pacijent"][selectIndex]["Datum rodjenja"]}\n'
                f'JMBG: {BAZA_SADRZAJ["Pacijent"][selectIndex]["JMBG"]}\n'
                f'LBO: {BAZA_SADRZAJ["Pacijent"][selectIndex]["LBO"]}'
            )
            
            # Vracanje u normalan mod radi upisa teksta
            self.podaciText.config(state=NORMAL)
            # Brisanje sadrzaj texboxa
            self.podaciText.delete(1.0, END)
            # Unos podataka u textbox
            self.podaciText.insert(INSERT, text)
            # Vracanje u read-only mod
            self.podaciText.config(state=DISABLED)
            # Unistavanje popup prozora
            self.topLevel.destroy()

    def close_dodajTopLevel(self):
        self.topLevel.destroy()

    def izmeniTopLevel(self):
        self.topLevel2 = Toplevel(self)
        self.topLevel2.title("Izmena pacijenta")
        self.topLevel2.geometry("300x250")
        self.topLevel2.minsize(300, 250)
        self.topLevel2.maxsize(300, 250)

        # Unos imena
        self.imeLabel2 = Label(self.topLevel2, text="Ime:", font='Times 15')
        self.imeLabel2.grid(row=0, column=0, padx=5, pady=5)
        self.imeEntry2 = Entry(self.topLevel2)
        self.imeEntry2.grid(row=0, column=1, padx=5, pady=5)
        # Unos prezimena
        self.prezimeLabel2 = Label(self.topLevel2, text="Prezime:", font='Times 15')
        self.prezimeLabel2.grid(row=1, column=0, padx=5, pady=5)
        self.prezimeEntry2 = Entry(self.topLevel2)
        self.prezimeEntry2.grid(row=1, column=1, padx=5, pady=5)
        # Unos datuma
        self.rodjenjeLabel2 = Label(self.topLevel2, text="Datum rodjenja:", font='Times 15')
        self.rodjenjeLabel2.grid(row=2, column=0, padx=5, pady=5)
        self.rodjenjeEntry2 = Entry(self.topLevel2)
        self.rodjenjeEntry2.grid(row=2, column=1, padx=5, pady=5)
        # Unos JMBG-a
        self.jmbgLabel2 = Label(self.topLevel2, text="JMBG:", font='Times 15')
        self.jmbgLabel2.grid(row=3, column=0, padx=5, pady=5)
        self.jmbgEntry2 = Entry(self.topLevel2)
        self.jmbgEntry2.grid(row=3, column=1, padx=5, pady=5)
        # Unos LBO-a
        self.lboLabel2 = Label(self.topLevel2, text="LBO:", font='Times 15')
        self.lboLabel2.grid(row=4, column=0, padx=5, pady=5)
        self.lboEntry2 = Entry(self.topLevel2)
        self.lboEntry2.grid(row=4, column=1, padx=5, pady=5)
        # Dugme za primenu pormena
        self.prihvatiButton2 = Button(self.topLevel2, text="Prihvati", command=self.apply_izmeniTopLevel)
        self.prihvatiButton2.grid(row=5, column=0, padx=10, pady=10)
        # Dugme za odbacivanje promena
        self.odbaciButton2 = Button(self.topLevel2, text="Odbaci", command=self.close_izmeniTopLevel)
        self.odbaciButton2.grid(row=5, column=1, padx=10, pady=10)

        # Trenutni podaci
        self.selectedIndex = self.spisakListBox.curselection()[0]
        self.staroIme = BAZA_SADRZAJ["Pacijent"][self.selectedIndex]["Ime"]
        self.staroPrezime = BAZA_SADRZAJ["Pacijent"][self.selectedIndex]["Prezime"]
        self.stariDatumRodjenja = BAZA_SADRZAJ["Pacijent"][self.selectedIndex]["Datum rodjenja"].replace("-", ".")
        jmbg = BAZA_SADRZAJ["Pacijent"][self.selectedIndex]["JMBG"]
        lbo = BAZA_SADRZAJ["Pacijent"][self.selectedIndex]["LBO"]

        # Popunjavanje polja
        self.imeEntry2.insert(0, self.staroIme)
        self.prezimeEntry2.insert(0, self.staroPrezime)
        self.rodjenjeEntry2.insert(0, self.stariDatumRodjenja)
        self.jmbgEntry2.insert(0, jmbg)
        self.lboEntry2.insert(0, lbo)

        # onemogucavanje polja lbo i jmbg
        self.jmbgEntry2.config(state=DISABLED)
        self.lboEntry2.config(state=DISABLED)
        # Omogucava da osnovni program bude nedostupan kada je popup strana aktivna
        self.topLevel2.grab_set()

    def apply_izmeniTopLevel(self):
        # vrednost iz polja ime
        novoIme = self.imeEntry2.get()
        # vrednost iz polja prezime
        novoPrezime = self.prezimeEntry2.get()
        # vrednost iz polja datum rodjenja
        rodjenje = self.rodjenjeEntry2.get()
        # vrednost iz pola datum rodjenja ['dan', 'mesec', 'godina']
        novoRodjenje = rodjenje.split('.')
        # formatiran datum u oblik koji nam odgovara za poredjenje datetime.date('godina', 'mesec', 'dan')
        noviDatumRodjenja = date(int(novoRodjenje[2]), int(novoRodjenje[1]), int(novoRodjenje[0]))
        # danasnji datum u dormatu datetime.date('godina', 'mesec', 'dan')
        danasnjiDatum = datetime.now().date()
        # vrednost iz polja jmbg
        jmbg = self.jmbgEntry2.get()
        # vrednos iz polja lbo
        lbo = self.lboEntry2.get()
        
        if len(novoIme) < 2:
            messagebox.showerror("Error", "Ime mora biti duze od 2 karaktera")
        elif len(novoPrezime) < 2:
            messagebox.showerror("Error", "Prezime mora biti duze od 2 karaktera")
        elif noviDatumRodjenja > danasnjiDatum:
            messagebox.showerror("Error", "Datum moze biti najkasnije danasnji")
        else:
            # Ukoliko je validacija prosla radi se izmena vrednosti
            BAZA_SADRZAJ["Pacijent"][self.selectedIndex]["Ime"] = novoIme
            BAZA_SADRZAJ["Pacijent"][self.selectedIndex]["Prezime"] = novoPrezime
            BAZA_SADRZAJ["Pacijent"][self.selectedIndex]["Datum rodjenja"] = noviDatumRodjenja.strftime("%d-%m-%Y")
            # Sortiranje pre upisa u fajl
            BAZA_SADRZAJ["Pacijent"].sort(key=itemgetter("Prezime", "Ime"))
            # Takodje ova promena se unosi i u fajl
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)

            # Brisanje teksta u polju za pretragu
            self.pretragaEntry.delete(0, END)
            # Brisanje liste za prikaz pacijenata
            self.spisakListBox.delete(0, END)
            # Ubacivanje u listu za prikaz
            index = 0
            selectIndex = 0
            for pacijent in BAZA_SADRZAJ["Pacijent"]:
                self.spisakListBox.insert(index, f'{pacijent["Ime"]} {pacijent["Prezime"]}')
                if jmbg == pacijent["JMBG"]:
                    selectIndex = index

                index += 1

            # Selektovanje novog unosa
            self.spisakListBox.select_set(selectIndex)
            # Formatiranje podataka o pacijentu za ispis
            text = (
                f'Ime: {BAZA_SADRZAJ["Pacijent"][selectIndex]["Ime"]}\n'
                f'Prezime: {BAZA_SADRZAJ["Pacijent"][selectIndex]["Prezime"]}\n'
                f'Datum rodjenja: {BAZA_SADRZAJ["Pacijent"][selectIndex]["Datum rodjenja"]}\n'
                f'JMBG: {BAZA_SADRZAJ["Pacijent"][selectIndex]["JMBG"]}\n'
                f'LBO: {BAZA_SADRZAJ["Pacijent"][selectIndex]["LBO"]}'
            )
            
            # Vracanje u normalan mod radi upisa teksta
            self.podaciText.config(state=NORMAL)
            # Brisanje sadrzaj texboxa
            self.podaciText.delete(1.0, END)
            # Unos podataka u textbox
            self.podaciText.insert(INSERT, text)
            # Vracanje u read-only mod
            self.podaciText.config(state=DISABLED)
            # Unistavanje popup prozora
            self.topLevel2.destroy()

    def close_izmeniTopLevel(self):
        self.topLevel2.destroy()


class LekariPage(Frame):

    def __init__(self, parent, controler):
        Frame.__init__(self, parent)

        self.leftFrame = Frame(self)
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.spisakLabel = Label(self.leftFrame, text="Spisak lekara", font='Times 15')
        self.spisakLabel.pack(fill=X, padx=5, pady=5)
        self.spisakListBox = Listbox(self.leftFrame, selectmode=SINGLE)
        self.spisakListBox.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)
        self.spisakListBox.bind('<<ListboxSelect>>', self.prikaziPodatke)
        self.pretragaEntry = Entry(self.leftFrame)
        self.pretragaEntry.pack(side=LEFT, expand=TRUE, fill=BOTH, padx=5, pady=5)
        self.receptiButton = Button(self.leftFrame, text="Recepti", font='Times 15')
        self.receptiButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.rightFrame = Frame(self,)
        self.rightFrame.pack(side=RIGHT, fill=Y)
        self.podaciLabel = Label(self.rightFrame, text="Podaci lekara", font='Times 15')
        self.podaciLabel.pack(fill=X, padx=5, pady=5)
        self.podaciText = Text(self.rightFrame, state=DISABLED)
        self.podaciText.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)
        self.dodajButton = Button(self.rightFrame, text="Dodaj", font='Times 15', command=self.dodajTopLevel)
        self.dodajButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.izmeniButton = Button(self.rightFrame, text="Izmeni", font='Times 15', state=DISABLED, command=self.izmeniTopLevel)
        self.izmeniButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.obrisiButton = Button(self.rightFrame, text="Izbrisi", font='Times 15', state=DISABLED)
        self.obrisiButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)

        lekari = BAZA_SADRZAJ["Lekar"]

        index = 0
        for lekar in lekari:
            self.spisakListBox.insert(index, f'{lekar["Ime"]} {lekar["Prezime"]}')
            index += 1

    def prikaziPodatke(self, *args):
        index = self.spisakListBox.curselection()[0]
        text = (
            f'Ime: {BAZA_SADRZAJ["Lekar"][index]["Ime"]}\n'
            f'Prezime: {BAZA_SADRZAJ["Lekar"][index]["Prezime"]}\n'
            f'Datum rodjenja: {BAZA_SADRZAJ["Lekar"][index]["Datum rodjenja"]}\n'
            f'JMBG: {BAZA_SADRZAJ["Lekar"][index]["JMBG"]}\n'
            f'Specijalizacija: {BAZA_SADRZAJ["Lekar"][index]["Specijalizacija"]}'
        )
            
        self.podaciText.config(state=NORMAL)
        self.podaciText.delete(1.0, END)
        self.podaciText.insert(INSERT, text)
        self.podaciText.config(state=DISABLED)
        self.izmeniButton.config(state=NORMAL)
        self.obrisiButton.config(state=NORMAL)

    def dodajTopLevel(self):
        self.topLevel = Toplevel(self)
        self.topLevel.title("Novi lekar")
        self.topLevel.geometry("300x250")
        self.topLevel.minsize(300, 250)
        self.topLevel.maxsize(300, 250)

        self.imeLabel = Label(self.topLevel, text="Ime:", font='Times 15')
        self.imeLabel.grid(row=0, column=0, padx=5, pady=5)
        self.imeEntry = Entry(self.topLevel)
        self.imeEntry.grid(row=0, column=1, padx=5, pady=5)
        self.prezimeLabel = Label(self.topLevel, text="Prezime:", font='Times 15')
        self.prezimeLabel.grid(row=1, column=0, padx=5, pady=5)
        self.prezimeEntry = Entry(self.topLevel)
        self.prezimeEntry.grid(row=1, column=1, padx=5, pady=5)
        self.rodjenjeLabel = Label(self.topLevel, text="Datum rodjenja:", font='Times 15')
        self.rodjenjeLabel.grid(row=2, column=0, padx=5, pady=5)
        self.rodjenjeEntry = Entry(self.topLevel)
        self.rodjenjeEntry.grid(row=2, column=1, padx=5, pady=5)
        self.jmbgLabel = Label(self.topLevel, text="JMBG:", font='Times 15')
        self.jmbgLabel.grid(row=3, column=0, padx=5, pady=5)
        self.jmbgEntry = Entry(self.topLevel)
        self.jmbgEntry.grid(row=3, column=1, padx=5, pady=5)
        self.specLabel = Label(self.topLevel, text="Specijalizacija:", font='Times 15')
        self.specLabel.grid(row=4, column=0, padx=5, pady=5)
        self.specEntry = Entry(self.topLevel)
        self.specEntry.grid(row=4, column=1, padx=5, pady=5)
        self.prihvatiButton = Button(self.topLevel, text="Prihvati", command=self.apply_dodajTopLevel)
        self.prihvatiButton.grid(row=5, column=0, padx=10, pady=10)
        self.odbaciButton = Button(self.topLevel, text="Odbaci", command=self.close_dodajTopLevel)
        self.odbaciButton.grid(row=5, column=1, padx=10, pady=10)
        self.topLevel.grab_set()

    def apply_dodajTopLevel(self):
        ime = self.imeEntry.get()
        prezime = self.prezimeEntry.get()
        # vrednost iz pola datum rodjenja ['dan', 'mesec', 'godina']
        rodjenje = self.rodjenjeEntry.get().split('.')
        # formatiran datum u oblik koji nam odgovara za poredjenje datetime.date('godina', 'mesec', 'dan')
        datumRodjenja = date(int(rodjenje[2]), int(rodjenje[1]), int(rodjenje[0]))
        # danasnji datum u dormatu datetime.date('godina', 'mesec', 'dan')
        danasnjiDatum = datetime.now().date()
        jmbg = self.jmbgEntry.get()
        spec = self.specEntry.get()
        jmbgLst = []

        lekari = BAZA_SADRZAJ["Lekar"]
        if lekari:
            for lekar in lekari:
                for key, value in lekar.items():
                    if key == "JMBG":
                        jmbgLst.append(value)

        if len(ime) < 2:
            messagebox.showerror("Error", "Ime mora biti duze od 2 karaktera")
        elif len(prezime) < 2:
            messagebox.showerror("Error", "Prezime mora biti duze od 2 karaktera")
        elif datumRodjenja > danasnjiDatum:
            messagebox.showerror("Error", "Datum moze biti najkasnije danasnji")
        elif jmbg in jmbgLst:
            messagebox.showerror("Error", "JMBG postoji u bazi")
        elif len(jmbg) != 13:
            messagebox.showerror("Error", "JMBG mora biti 13 karaktera")
        elif len(spec) < 2:
            messagebox.showerror("Error", "Specijalizacija mora biti duze od 2 karaktera")
        else:
            novilekar = Lekar(jmbg=jmbg, ime=ime, prezime=prezime, datum_rodjenja=datumRodjenja.strftime("%d-%m-%Y"), specijalizacija=spec)

            BAZA_SADRZAJ["Lekar"].append(novilekar.__str__())
            BAZA_SADRZAJ["Lekar"].sort(key=itemgetter("Prezime", "Ime"))
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)

            self.pretragaEntry.delete(0, END)
            self.spisakListBox.delete(0, END)
            index = 0
            selectIndex = 0
            for lekar in BAZA_SADRZAJ["Lekar"]:
                self.spisakListBox.insert(index, f'{lekar["Ime"]} {lekar["Prezime"]}')
                if novilekar.__str__() == lekar:
                    selectIndex = index

                index += 1

            self.spisakListBox.select_set(selectIndex)
            text = (
                f'Ime: {BAZA_SADRZAJ["Lekar"][selectIndex]["Ime"]}\n'
                f'Prezime: {BAZA_SADRZAJ["Lekar"][selectIndex]["Prezime"]}\n'
                f'Datum rodjenja: {BAZA_SADRZAJ["Lekar"][selectIndex]["Datum rodjenja"]}\n'
                f'JMBG: {BAZA_SADRZAJ["Lekar"][selectIndex]["JMBG"]}\n'
                f'Specijalizacija: {BAZA_SADRZAJ["Lekar"][selectIndex]["Specijalizacija"]}'
            )
            
            self.podaciText.config(state=NORMAL)
            self.podaciText.delete(1.0, END)
            self.podaciText.insert(INSERT, text)
            self.podaciText.config(state=DISABLED)
            self.topLevel.destroy()

    def close_dodajTopLevel(self):
        self.topLevel.destroy()

    def izmeniTopLevel(self):
        self.topLevel2 = Toplevel(self)
        self.topLevel2.title("Izmena lekara")
        self.topLevel2.geometry("300x250")
        self.topLevel2.minsize(300, 250)
        self.topLevel2.maxsize(300, 250)

        self.imeLabel2 = Label(self.topLevel2, text="Ime:", font='Times 15')
        self.imeLabel2.grid(row=0, column=0, padx=5, pady=5)
        self.imeEntry2 = Entry(self.topLevel2)
        self.imeEntry2.grid(row=0, column=1, padx=5, pady=5)
        self.prezimeLabel2 = Label(self.topLevel2, text="Prezime:", font='Times 15')
        self.prezimeLabel2.grid(row=1, column=0, padx=5, pady=5)
        self.prezimeEntry2 = Entry(self.topLevel2)
        self.prezimeEntry2.grid(row=1, column=1, padx=5, pady=5)
        self.rodjenjeLabel2 = Label(self.topLevel2, text="Datum rodjenja:", font='Times 15')
        self.rodjenjeLabel2.grid(row=2, column=0, padx=5, pady=5)
        self.rodjenjeEntry2 = Entry(self.topLevel2)
        self.rodjenjeEntry2.grid(row=2, column=1, padx=5, pady=5)
        self.jmbgLabel2 = Label(self.topLevel2, text="JMBG:", font='Times 15')
        self.jmbgLabel2.grid(row=3, column=0, padx=5, pady=5)
        self.jmbgEntry2 = Entry(self.topLevel2)
        self.jmbgEntry2.grid(row=3, column=1, padx=5, pady=5)
        self.lboLabel2 = Label(self.topLevel2, text="Specijalizacija:", font='Times 15')
        self.lboLabel2.grid(row=4, column=0, padx=5, pady=5)
        self.specEntry2 = Entry(self.topLevel2)
        self.specEntry2.grid(row=4, column=1, padx=5, pady=5)
        self.prihvatiButton2 = Button(self.topLevel2, text="Prihvati", command=self.apply_izmeniTopLevel)
        self.prihvatiButton2.grid(row=5, column=0, padx=10, pady=10)
        self.odbaciButton2 = Button(self.topLevel2, text="Odbaci", command=self.close_izmeniTopLevel)
        self.odbaciButton2.grid(row=5, column=1, padx=10, pady=10)

        self.selectedIndex = self.spisakListBox.curselection()[0]

        self.staroIme = BAZA_SADRZAJ["Lekar"][self.selectedIndex]["Ime"]
        self.staroPrezime = BAZA_SADRZAJ["Lekar"][self.selectedIndex]["Prezime"]
        self.stariDatumRodjenja = BAZA_SADRZAJ["Lekar"][self.selectedIndex]["Datum rodjenja"].replace("-", ".")
        jmbg = BAZA_SADRZAJ["Lekar"][self.selectedIndex]["JMBG"]
        self.staraSpec = BAZA_SADRZAJ["Lekar"][self.selectedIndex]["Specijalizacija"]

        self.imeEntry2.insert(0, self.staroIme)
        self.prezimeEntry2.insert(0, self.staroPrezime)
        self.rodjenjeEntry2.insert(0, self.stariDatumRodjenja)
        self.jmbgEntry2.insert(0, jmbg)
        self.specEntry2.insert(0, self.staraSpec)
        self.jmbgEntry2.config(state=DISABLED)  
        self.topLevel2.grab_set()

    def apply_izmeniTopLevel(self):
        novoIme = self.imeEntry2.get()
        novoPrezime = self.prezimeEntry2.get()
        rodjenje = self.rodjenjeEntry2.get()
        # vrednost iz pola datum rodjenja ['dan', 'mesec', 'godina']
        novoRodjenje = rodjenje.split('.')
        # formatiran datum u oblik koji nam odgovara za poredjenje datetime.date('godina', 'mesec', 'dan')
        noviDatumRodjenja = date(int(novoRodjenje[2]), int(novoRodjenje[1]), int(novoRodjenje[0]))
        # danasnji datum u dormatu datetime.date('godina', 'mesec', 'dan')
        danasnjiDatum = datetime.now().date()
        jmbg = self.jmbgEntry2.get()
        novaSpec = self.specEntry2.get()
        
        if len(novoIme) < 2:
            messagebox.showerror("Error", "Ime mora biti duze od 2 karaktera")
        elif len(novoPrezime) < 2:
            messagebox.showerror("Error", "Prezime mora biti duze od 2 karaktera")
        elif noviDatumRodjenja > danasnjiDatum:
            messagebox.showerror("Error", "Datum moze biti najkasnije danasnji")
        elif len(novaSpec) < 2:
            messagebox.showerror("Error", "Specijalizacija mora biti duza od 2 karaktera")
        else:
            BAZA_SADRZAJ["Lekar"][self.selectedIndex]["Ime"] = novoIme
            BAZA_SADRZAJ["Lekar"][self.selectedIndex]["Prezime"] = novoPrezime
            BAZA_SADRZAJ["Lekar"][self.selectedIndex]["Datum rodjenja"] = noviDatumRodjenja.strftime("%d-%m-%Y")
            BAZA_SADRZAJ["Lekar"][self.selectedIndex]["Specijalizacija"] = novaSpec  
            BAZA_SADRZAJ["Lekar"].sort(key=itemgetter("Prezime", "Ime"))
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)

            self.pretragaEntry.delete(0, END)
            self.spisakListBox.delete(0, END)
            index = 0
            selectIndex = 0
            for lekar in BAZA_SADRZAJ["Lekar"]:
                self.spisakListBox.insert(index, f'{lekar["Ime"]} {lekar["Prezime"]}')
                if jmbg == lekar["JMBG"]:
                    selectIndex = index

                index += 1

            self.spisakListBox.select_set(selectIndex)
            text = (
                f'Ime: {BAZA_SADRZAJ["Lekar"][selectIndex]["Ime"]}\n'
                f'Prezime: {BAZA_SADRZAJ["Lekar"][selectIndex]["Prezime"]}\n'
                f'Datum rodjenja: {BAZA_SADRZAJ["Lekar"][selectIndex]["Datum rodjenja"]}\n'
                f'JMBG: {BAZA_SADRZAJ["Lekar"][selectIndex]["JMBG"]}\n'
                f'Specijalizacija: {BAZA_SADRZAJ["Lekar"][selectIndex]["Specijalizacija"]}'
            )
            
            self.podaciText.config(state=NORMAL)
            self.podaciText.delete(1.0, END)
            self.podaciText.insert(INSERT, text)
            self.podaciText.config(state=DISABLED)
            self.topLevel2.destroy()

    def close_izmeniTopLevel(self):
        self.topLevel2.destroy()


class LekoviPage(Frame):

    def __init__(self, parent, controler):
        Frame.__init__(self, parent)

        self.leftFrame = Frame(self)
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.spisakLabel = Label(self.leftFrame, text="Spisak lekova", font='Times 15')
        self.spisakLabel.pack(fill=X, padx=5, pady=5)
        self.spisakListBox = Listbox(self.leftFrame, selectmode=SINGLE)
        self.spisakListBox.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)
        self.spisakListBox.bind('<<ListboxSelect>>', self.prikaziPodatke)
        self.pretragaEntry = Entry(self.leftFrame)
        self.pretragaEntry.pack(side=LEFT, expand=TRUE, fill=BOTH, padx=5, pady=5)
        self.receptiButton = Button(self.leftFrame, text="Recepti", font='Times 15')
        self.receptiButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.rightFrame = Frame(self,)
        self.rightFrame.pack(side=RIGHT, fill=Y)
        self.podaciLabel = Label(self.rightFrame, text="Podaci o leku", font='Times 15')
        self.podaciLabel.pack(fill=X, padx=5, pady=5)
        self.podaciText = Text(self.rightFrame, state=DISABLED)
        self.podaciText.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)
        self.dodajButton = Button(self.rightFrame, text="Dodaj", font='Times 15', command=self.dodajTopLevel)
        self.dodajButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.izmeniButton = Button(self.rightFrame, text="Izmeni", font='Times 15', state=DISABLED, command=self.izmeniTopLevel)
        self.izmeniButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.obrisiButton = Button(self.rightFrame, text="Izbrisi", font='Times 15', state=DISABLED)
        self.obrisiButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)

        lekovi = BAZA_SADRZAJ["Lek"]

        index = 0
        for lek in lekovi:
            self.spisakListBox.insert(index, f'{lek["Naziv leka"]}')
            index += 1

    def prikaziPodatke(self, *args):
        index = self.spisakListBox.curselection()[0]
        text = (
            f'Naziv: {BAZA_SADRZAJ["Lek"][index]["Naziv leka"]}\n'
            f'Proizvodjac: {BAZA_SADRZAJ["Lek"][index]["Proizvodjac leka"]}\n'
            f'Tip: {BAZA_SADRZAJ["Lek"][index]["Tip leka"]}\n'
            f'JKL: {BAZA_SADRZAJ["Lek"][index]["Sifra JKL"]}\n'
        )
            
        self.podaciText.config(state=NORMAL)
        self.podaciText.delete(1.0, END)
        self.podaciText.insert(INSERT, text)
        self.podaciText.config(state=DISABLED)
        self.izmeniButton.config(state=NORMAL)
        self.obrisiButton.config(state=NORMAL)

    def dodajTopLevel(self):
        self.topLevel = Toplevel(self)
        self.topLevel.title("Novi lek")
        self.topLevel.geometry("300x250")
        self.topLevel.minsize(300, 250)
        self.topLevel.maxsize(300, 250)

        self.nazivLabel = Label(self.topLevel, text="Naziv:", font='Times 15')
        self.nazivLabel.grid(row=0, column=0, padx=5, pady=5)
        self.nazivEntry = Entry(self.topLevel)
        self.nazivEntry.grid(row=0, column=1, padx=5, pady=5)
        self.proizvodjacLabel = Label(self.topLevel, text="Proizvodjac:", font='Times 15')
        self.proizvodjacLabel.grid(row=1, column=0, padx=5, pady=5)
        self.proizvodjacEntry = Entry(self.topLevel)
        self.proizvodjacEntry.grid(row=1, column=1, padx=5, pady=5)
        self.tipLabel = Label(self.topLevel, text="Tip:", font='Times 15')
        self.tipLabel.grid(row=2, column=0, padx=5, pady=5)
        self.tipEntry = Entry(self.topLevel)
        self.tipEntry.grid(row=2, column=1, padx=5, pady=5)
        self.jklLabel = Label(self.topLevel, text="JKL:", font='Times 15')
        self.jklLabel.grid(row=3, column=0, padx=5, pady=5)
        self.jklEntry = Entry(self.topLevel)
        self.jklEntry.grid(row=3, column=1, padx=5, pady=5)
        self.prihvatiButton = Button(self.topLevel, text="Prihvati", command=self.apply_dodajTopLevel)
        self.prihvatiButton.grid(row=5, column=0, padx=10, pady=10)
        self.odbaciButton = Button(self.topLevel, text="Odbaci", command=self.close_dodajTopLevel)
        self.odbaciButton.grid(row=5, column=1, padx=10, pady=10)
        self.topLevel.grab_set()

    def apply_dodajTopLevel(self):
        naziv = self.nazivEntry.get()
        proizvodjac = self.proizvodjacEntry.get()
        tip = self.tipEntry.get()
        jkl = self.jklEntry.get()
        jklLst = []

        lekovi = BAZA_SADRZAJ["Lek"]
        if lekovi:
            for lek in lekovi:
                for key, value in lek.items():
                    if key == "Sifra JKL":
                        jklLst.append(value)

        if len(naziv) < 2:
            messagebox.showerror("Error", "Naziv mora biti duzi od 2 karaktera")
        elif len(proizvodjac) < 2:
            messagebox.showerror("Error", "Proizvodjac mora biti duzi od 2 karaktera")
        elif len(tip) < 2:
            messagebox.showerror("Error", "Tip mora biti duzi od 2 karaktera")
        elif jkl in jklLst:
            messagebox.showerror("Error", "JKL postoji u bazi")
        elif len(jkl) != 7:
            messagebox.showerror("Error", "JKL mora biti 7 karaktera")
        else:
            novilek = Lek(sifra_jkl=jkl, naziv=naziv, proizvodac=proizvodjac, tip_leka=tip)

            BAZA_SADRZAJ["Lek"].append(novilek.__str__())
            BAZA_SADRZAJ["Lek"].sort(key=itemgetter("Naziv leka"))
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)

            self.pretragaEntry.delete(0, END)
            self.spisakListBox.delete(0, END)
            index = 0
            selectIndex = 0
            for lek in BAZA_SADRZAJ["Lek"]:
                self.spisakListBox.insert(index, f'{lek["Naziv leka"]}')
                if novilek.__str__() == lek:
                    selectIndex = index

                index += 1

            self.spisakListBox.select_set(selectIndex)
            text = (
                f'Naziv: {BAZA_SADRZAJ["Lek"][selectIndex]["Naziv leka"]}\n'
                f'Proizvodjac: {BAZA_SADRZAJ["Lek"][selectIndex]["Proizvodjac leka"]}\n'
                f'Tip: {BAZA_SADRZAJ["Lek"][selectIndex]["Tip leka"]}\n'
                f'JKL: {BAZA_SADRZAJ["Lek"][selectIndex]["Sifra JKL"]}\n'
            )
            
            self.podaciText.config(state=NORMAL)
            self.podaciText.delete(1.0, END)
            self.podaciText.insert(INSERT, text)
            self.podaciText.config(state=DISABLED)
            self.topLevel.destroy()

    def close_dodajTopLevel(self):
        self.topLevel.destroy()

    def izmeniTopLevel(self):
        self.topLevel2 = Toplevel(self)
        self.topLevel2.title("Izmena leka")
        self.topLevel2.geometry("300x250")
        self.topLevel2.minsize(300, 250)
        self.topLevel2.maxsize(300, 250)

        self.nazivLabel2 = Label(self.topLevel2, text="Naziv:", font='Times 15')
        self.nazivLabel2.grid(row=0, column=0, padx=5, pady=5)
        self.nazivEntry2 = Entry(self.topLevel2)
        self.nazivEntry2.grid(row=0, column=1, padx=5, pady=5)
        self.proizvodjacLabel2 = Label(self.topLevel2, text="Proizvodjac:", font='Times 15')
        self.proizvodjacLabel2.grid(row=1, column=0, padx=5, pady=5)
        self.proizvodjacEntry2 = Entry(self.topLevel2)
        self.proizvodjacEntry2.grid(row=1, column=1, padx=5, pady=5)
        self.tipLabel2 = Label(self.topLevel2, text="Tip:", font='Times 15')
        self.tipLabel2.grid(row=3, column=0, padx=5, pady=5)
        self.tipEntry2 = Entry(self.topLevel2)
        self.tipEntry2.grid(row=3, column=1, padx=5, pady=5)
        self.jklLabel2 = Label(self.topLevel2, text="JKL:", font='Times 15')
        self.jklLabel2.grid(row=4, column=0, padx=5, pady=5)
        self.jklEntry2 = Entry(self.topLevel2)
        self.jklEntry2.grid(row=4, column=1, padx=5, pady=5)
        self.prihvatiButton2 = Button(self.topLevel2, text="Prihvati", command=self.apply_izmeniTopLevel)
        self.prihvatiButton2.grid(row=5, column=0, padx=10, pady=10)
        self.odbaciButton2 = Button(self.topLevel2, text="Odbaci", command=self.close_izmeniTopLevel)
        self.odbaciButton2.grid(row=5, column=1, padx=10, pady=10)
        self.selectedIndex = self.spisakListBox.curselection()[0]
        
        self.stariNaziv = BAZA_SADRZAJ["Lek"][self.selectedIndex]["Naziv leka"]
        self.stariProizvodjac = BAZA_SADRZAJ["Lek"][self.selectedIndex]["Proizvodjac leka"]
        self.stariTip = BAZA_SADRZAJ["Lek"][self.selectedIndex]["Tip leka"]
        jkl = BAZA_SADRZAJ["Lek"][self.selectedIndex]["Sifra JKL"]

        self.nazivEntry2.insert(0, self.stariNaziv)
        self.proizvodjacEntry2.insert(0, self.stariProizvodjac)
        self.tipEntry2.insert(0, self.stariTip)
        self.jklEntry2.insert(0, jkl)
        self.jklEntry2.config(state=DISABLED)  
        self.topLevel2.grab_set()

    def apply_izmeniTopLevel(self):
        noviNaziv = self.nazivEntry2.get()
        noviProizvodjac = self.proizvodjacEntry2.get()
        noviTip = self.tipEntry2.get()
        jkl = self.jklEntry2.get()
        
        if len(noviNaziv) < 2:
            messagebox.showerror("Error", "Naziv mora biti duzi od 2 karaktera")
        elif len(noviProizvodjac) < 2:
            messagebox.showerror("Error", "Proizvodjac mora biti duze od 2 karaktera")
        elif len(noviTip) < 2:
            messagebox.showerror("Error", "Tip mora biti duza od 2 karaktera")
        else:
            BAZA_SADRZAJ["Lek"][self.selectedIndex]["Naziv leka"] = noviNaziv
            BAZA_SADRZAJ["Lek"][self.selectedIndex]["Proizvodjac leka"] = noviProizvodjac
            BAZA_SADRZAJ["Lek"][self.selectedIndex]["Tip leka"] = noviTip
            BAZA_SADRZAJ["Lek"].sort(key=itemgetter("Naziv leka"))
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)

            self.pretragaEntry.delete(0, END)
            self.spisakListBox.delete(0, END)
            index = 0
            selectIndex = 0
            for lek in BAZA_SADRZAJ["Lek"]:
                self.spisakListBox.insert(index, f'{lek["Naziv leka"]}')
                if jkl == lek["Sifra JKL"]:
                    selectIndex = index

                index += 1

            self.spisakListBox.select_set(selectIndex)
            text = (
                f'Naziv: {BAZA_SADRZAJ["Lek"][selectIndex]["Naziv leka"]}\n'
                f'Proizvodjac: {BAZA_SADRZAJ["Lek"][selectIndex]["Proizvodjac leka"]}\n'
                f'Tip: {BAZA_SADRZAJ["Lek"][selectIndex]["Tip leka"]}\n'
                f'JKL: {BAZA_SADRZAJ["Lek"][selectIndex]["Sifra JKL"]}\n'
            )
            
            self.podaciText.config(state=NORMAL)
            self.podaciText.delete(1.0, END)
            self.podaciText.insert(INSERT, text)
            self.podaciText.config(state=DISABLED)
            self.topLevel2.destroy()

    def close_izmeniTopLevel(self):
        self.topLevel2.destroy()









class ReceptiPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self.leftFrame = Frame(self)
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.spisakLabel = Label(self.leftFrame, text="Spisak receata", font='Times 15')
        self.spisakLabel.pack(fill=X, padx=5, pady=5)
        self.spisakListBox = Listbox(self.leftFrame, selectmode=SINGLE)
        self.spisakListBox.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)
        self.pretragaCombo = ttk.Combobox(self.leftFrame)
        self.pretragaCombo.pack(side=LEFT, expand=TRUE, fill=BOTH, padx=5, pady=5)
        self.rightFrame = Frame(self,)
        self.rightFrame.pack(side=RIGHT, fill=Y)
        self.podaciLabel = Label(self.rightFrame, text="Podaci o receptu", font='Times 15')
        self.podaciLabel.pack(fill=X, padx=5, pady=5)
        self.podaciText = Text(self.rightFrame, state=DISABLED)
        self.podaciText.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)
        self.dodajButton = Button(self.rightFrame, text="Dodaj", font='Times 15', command=self.dodajTopLevel)
        self.dodajButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.izmeniButton = Button(self.rightFrame, text="Izmeni", font='Times 15', state=DISABLED)
        self.izmeniButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.obrisiButton = Button(self.rightFrame, text="Izbrisi", font='Times 15', state=DISABLED, command=self.deleteRecept)
        self.obrisiButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)

        self.pretragaCombo.after(2000, self.updateCombo)
        self.pretragaCombo.bind('<<ComboboxSelected>>', self.updateList)
        self.spisakListBox.bind('<<ListboxSelect>>', self.prikaziPodatke)

    def deleteRecept(self):
        pacijentSelectedIndex = self.pretragaCombo.current()
        receptSelectedIndex = self.spisakListBox.curselection()[0]

        spisakRecepti = []

        pacijent = BAZA_SADRZAJ["Pacijent"][pacijentSelectedIndex - 1]
        for recept in BAZA_SADRZAJ["Recept"]:
            if recept["Pacijent"] == pacijent:
                spisakRecepti.append(recept)

        recept = spisakRecepti[receptSelectedIndex]
        
        answer = messagebox.askyesno(title='confirmation', message='Da li ste sigurni?')
        if answer:
            BAZA_SADRZAJ["Recept"].remove(recept)
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)

            self.updateList()
            self.podaciText.config(state=NORMAL)
            self.podaciText.delete(1.0, END)
            self.podaciText.config(state=DISABLED)

    def updateCombo(self):
        pacijenti = [""]
        for pacijent in BAZA_SADRZAJ["Pacijent"]:
            pacijenti.append(f'{pacijent["Ime"]} {pacijent["Prezime"]}')
        
        self.pretragaCombo['values'] = tuple()
        self.pretragaCombo['values'] = tuple(pacijenti)
        self.pretragaCombo.after(2000, self.updateCombo)

    def updateList(self, *args):
        recepti = []
        pacijentSelectedIndex = self.pretragaCombo.current()
        pacijent = BAZA_SADRZAJ["Pacijent"][pacijentSelectedIndex - 1]

        for recept in BAZA_SADRZAJ["Recept"]:
            if recept["Pacijent"] == pacijent:
                recepti.append(f'{recept["Lekar"]["Ime"]} - {recept["Lek"]["Naziv leka"]}')
        
        self.spisakListBox.delete(0, END)
        index = 0
        for recept in recepti:
            self.spisakListBox.insert(index, recept)
            index += 1

        self.podaciText.config(state=NORMAL)
        self.podaciText.delete(1.0, END)
        self.podaciText.config(state=DISABLED)
        self.obrisiButton.config(state=DISABLED)
        self.izmeniButton.config(state=DISABLED)

    def prikaziPodatke(self, *args):
        pacijentSelectedIndex = self.pretragaCombo.current()
        receptSelectedIndex = self.spisakListBox.curselection()[0]

        spisakRecepti = []

        pacijent = BAZA_SADRZAJ["Pacijent"][pacijentSelectedIndex - 1]
        for recept in BAZA_SADRZAJ["Recept"]:
            if recept["Pacijent"] == pacijent:
                spisakRecepti.append(recept)

        recept = spisakRecepti[receptSelectedIndex]

        text = (
            'Pacijent:\n'
            f'\tIme: {recept["Pacijent"]["Ime"]}\n'
            f'\tPrezime: {recept["Pacijent"]["Prezime"]}\n'
            f'\tJMBG: {recept["Pacijent"]["JMBG"]}\n'
            'Lekar:\n'
            f'\tIme: {recept["Lekar"]["Ime"]}\n'
            f'\tPrezime: {recept["Lekar"]["Prezime"]}\n'
            f'\tJMBG: {recept["Lekar"]["JMBG"]}\n'
            f'\tSpecijalizacija: {recept["Lekar"]["Specijalizacija"]}\n'
            'Lek:\n'
            f'\tNaziv: {recept["Lek"]["Naziv leka"]}\n'
            f'\tProizvodjac: {recept["Lek"]["Proizvodjac leka"]}\n'
            f'\tJKL: {recept["Lek"]["Sifra JKL"]}\n'
            f'Kolicina: {recept["Kolicina"]}\n'
            f'Izvestaj: {recept["Izvestaj"]}\n'
            f'Datum: {recept["Datum"]}\n' 
        )

        self.podaciText.config(state=NORMAL)
        self.podaciText.delete(1.0, END)
        self.podaciText.insert(INSERT, text)
        self.podaciText.config(state=DISABLED)
        self.izmeniButton.config(state=NORMAL)
        self.obrisiButton.config(state=NORMAL)

    def dodajTopLevel(self):
        self.topLevel = Toplevel(self)
        self.topLevel.title("Novi recept")
        self.topLevel.geometry("300x250")
        self.topLevel.minsize(300, 250)
        self.topLevel.maxsize(300, 250)

        self.lekarLabel = Label(self.topLevel, text="Lekar:", font='Times 15')
        self.lekarLabel.grid(row=0, column=0, padx=5, pady=5)
        self.lekarCombo = ttk.Combobox(self.topLevel)
        self.lekarCombo.grid(row=0, column=1, padx=5, pady=5)
        self.lekLabel = Label(self.topLevel, text="Lek:", font='Times 15')
        self.lekLabel.grid(row=1, column=0, padx=5, pady=5)
        self.lekCombo = ttk.Combobox(self.topLevel)
        self.lekCombo.grid(row=1, column=1, padx=5, pady=5)
        self.kolicinaLabel = Label(self.topLevel, text="Kolicina:", font='Times 15')
        self.kolicinaLabel.grid(row=2, column=0, padx=5, pady=5)
        self.kolicinaEntry = Entry(self.topLevel)
        self.kolicinaEntry.grid(row=2, column=1, padx=5, pady=5)
        self.izvestajLabel = Label(self.topLevel, text="Izvestaj:", font='Times 15')
        self.izvestajLabel.grid(row=3, column=0, padx=5, pady=5)
        self.izvestajEntry = Entry(self.topLevel)
        self.izvestajEntry.grid(row=3, column=1, padx=5, pady=5)
        self.datumLabel = Label(self.topLevel, text="Datum:", font='Times 15')
        self.datumLabel.grid(row=4, column=0, padx=5, pady=5)
        self.datumEntry = Entry(self.topLevel)
        self.datumEntry.grid(row=4, column=1, padx=5, pady=5)
        self.prihvatiButton = Button(self.topLevel, text="Prihvati", command=self.apply_dodajTopLevel)
        self.prihvatiButton.grid(row=5, column=0, padx=10, pady=10)
        self.odbaciButton = Button(self.topLevel, text="Odbaci", command=self.close_dodajTopLevel)
        self.odbaciButton.grid(row=5, column=1, padx=10, pady=10)
        self.topLevel.grab_set()

        lekari = [""]
        for lekar in BAZA_SADRZAJ["Lekar"]:
            lekari.append(f'{lekar["Ime"]} {lekar["Prezime"]}')
        
        lekovi = [""]
        for lek in BAZA_SADRZAJ["Lek"]:
            lekovi.append(f'{lek["Naziv leka"]}')
        
        self.lekarCombo['values'] = tuple(lekari)
        self.lekarCombo.current(0)
        self.lekCombo['values'] = tuple(lekovi)
        self.lekCombo.current(0)

    def apply_dodajTopLevel(self):
        pacijentIndexSelected = self.pretragaCombo.current()
        lekarIndexSelected = self.lekarCombo.current()
        lekIndexSelected = self.lekCombo.current()
        kolicina = int(self.kolicinaEntry.get())
        izvestaj = self.izvestajEntry.get()
        datum = self.datumEntry.get().split('.')
        # formatiran datum u oblik koji nam odgovara za poredjenje datetime.date('godina', 'mesec', 'dan')
        datumFormatiran = date(int(datum[2]), int(datum[1]), int(datum[0]))
        # danasnji datum u dormatu datetime.date('godina', 'mesec', 'dan')
        danasnjiDatum = datetime.now().date()

        if pacijentIndexSelected == 0:
            messagebox.showerror("Error", "Zatvorite prozor i selektujte pacijenta")
        elif lekarIndexSelected == 0:
            messagebox.showerror("Error", "Selektujte lekara")
        elif lekIndexSelected == 0:
            messagebox.showerror("Error", "Selektujte lek")
        elif kolicina < 1:
            messagebox.showerror("Error", "Kolicina mora biti veca od 0")
        elif datumFormatiran > danasnjiDatum:
            messagebox.showerror("Error", "Datum moze biti najkasnije danasnji")
        else:
            pacijent = BAZA_SADRZAJ["Pacijent"][pacijentIndexSelected - 1]
            lekar = BAZA_SADRZAJ["Lekar"][lekarIndexSelected - 1]
            lek = BAZA_SADRZAJ["Lek"][lekarIndexSelected - 1]
            novirecept = Recept(pacijent=pacijent, datum='-'.join(datum), izvestaj=izvestaj, lekar=lekar, lek=lek, kolicina=kolicina)

            BAZA_SADRZAJ["Recept"].append(novirecept.__str__())
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)
            
            self.topLevel.destroy()
            self.updateList()
            self.podaciText.config(state=NORMAL)
            self.podaciText.delete(1.0, END)
            self.podaciText.config(state=DISABLED)

    def close_dodajTopLevel(self):
        self.topLevel.destroy()





if __name__ == "__main__":

    # Ukoliko ne postoji json file ili je obrisan kreira se novi data.json.
    # U tako novokreirani fajl se upisuje inicijalna struktura.
    # Takodje, ta inicijalna struktura je dodeljena globalnoj promenljivoj
    if not os.path.isfile('data.json'):
        BAZA_SADRZAJ = {}
        BAZA_SADRZAJ['Pacijent'] = []
        BAZA_SADRZAJ['Lekar'] = []
        BAZA_SADRZAJ['Lek'] = []
        BAZA_SADRZAJ['Recept'] = []

        with open(BAZA_FAJL, 'w') as file:
            json.dump(BAZA_SADRZAJ, file, indent=4)
    # Ukoliko json file postoji ceta se sadrzaj iz njega.
    # Taj sadrzaj se smesta u globalnu promenljivu.
    else:
        with open(BAZA_FAJL) as file:
            BAZA_SADRZAJ = json.load(file)
        
        # Sortiranje pacijenata
        if BAZA_SADRZAJ["Pacijent"]:
            BAZA_SADRZAJ["Pacijent"].sort(key=itemgetter("Prezime", "Ime"))

        # Sortiranje lekara
        if BAZA_SADRZAJ["Lekar"]:
            BAZA_SADRZAJ["Lekar"].sort(key=itemgetter("Prezime", "Ime"))

        # Sortiranje leka
        if BAZA_SADRZAJ["Lek"]:
            BAZA_SADRZAJ["Lek"].sort(key=itemgetter("Naziv leka"))

    app = MyApp()
    app.title("Apoteka")
    app.geometry("800x600")
    app.mainloop()