import os
import re
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


FONT = 'Times 15'
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
        fileBar.add_command(label="Exit", command=lambda: Tk.destroy(self))

        menu.add_cascade(menu=pageBar, label="Stranice")
        pageBar.add_command(label="Home", command=lambda: self.show_frame(PocetnaStranica))
        pageBar.add_command(label="Pacijenti", command=lambda: self.show_frame(PacijentiStranica))
        pageBar.add_command(label="Lekari", command=lambda: self.show_frame(LekariStranica))
        pageBar.add_command(label="Lekovi", command=lambda: self.show_frame(LekoviStranica))
        pageBar.add_command(label="Recepti", command=lambda: self.show_frame(ReceptiStranica))

        Tk.config(self, menu=menu)

        for page in (PocetnaStranica, PacijentiStranica, LekariStranica, ReceptiStranica, LekoviStranica):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PocetnaStranica)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


class PocetnaStranica(Frame):

    def __init__(self, parent, controler):
        Frame.__init__(self, parent)
        text = Label(self, text="Projekat Apoteka", font=FONT)
        text.pack(side="top", fill="both", expand=True)


class PacijentiStranica(Frame):

    def __init__(self, parent, controler):
        Frame.__init__(self, parent)

        self.leviFrame = Frame(self)
        self.leviFrame.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.spisakPacijenataLabel = Label(self.leviFrame, text="Spisak pacijenata", font=FONT)
        self.spisakPacijenataLabel.pack(fill=X, padx=5, pady=5)
        self.spisakPacijenataListBox = Listbox(self.leviFrame, selectmode=SINGLE, font=FONT)
        self.spisakPacijenataListBox.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)
        self.pretragaPacijenataEntry = Entry(self.leviFrame, font=FONT)
        self.pretragaPacijenataEntry.pack(side=LEFT, expand=TRUE, fill=BOTH, padx=5, pady=5)
        self.receptiPacijentaButton = Button(self.leviFrame, text="Recepti", font=FONT, command=self.toplevel_recepti_pacijenta)
        self.receptiPacijentaButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.desniFrame = Frame(self,)
        self.desniFrame.pack(side=RIGHT, fill=Y)
        self.podaciPacijentaLabel = Label(self.desniFrame, text="Podaci pacijenta", font=FONT)
        self.podaciPacijentaLabel.pack(fill=X, padx=5, pady=5)
        self.podaciPacijentaText = Text(self.desniFrame, font=FONT, state=DISABLED)
        self.podaciPacijentaText.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)
        self.dodajPacijentaButton = Button(self.desniFrame, text="Dodaj", font=FONT, command=self.toplevel_dodaj_pacijenta)
        self.dodajPacijentaButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.izmeniPacijentaButton = Button(self.desniFrame, text="Izmeni", font=FONT, state=DISABLED, command=self.toplevel_izmeni_pacijenta)
        self.izmeniPacijentaButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.obrisiPacijentaButton = Button(self.desniFrame, text="Izbrisi", font=FONT, state=DISABLED, command=self.izbrisi_pacijenta)
        self.obrisiPacijentaButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)

        self.listaPacijenata = []

        self.osvezi_listu_pacijenata()
        self.popuni_listu_pacijenata()
        self.spisakPacijenataListBox.bind('<<ListboxSelect>>', self.prikazi_podatke_pacijenta)
        self.pretragaPacijenataEntry.bind('<KeyRelease>', self.osvezi_listu_pacijenata)

    def toplevel_dodaj_pacijenta(self):
        self.toplevelDodajPacijenta = Toplevel(self)
        self.toplevelDodajPacijenta.title("Novi pacijent")

        self.imePacijentaLabel = Label(self.toplevelDodajPacijenta, text="Ime:", font=FONT)
        self.imePacijentaLabel.grid(row=0, column=0, padx=5, pady=5)
        self.imePacijentaEntry = Entry(self.toplevelDodajPacijenta, font=FONT)
        self.imePacijentaEntry.grid(row=0, column=1, padx=5, pady=5)
        self.prezimePacijentaLabel = Label(self.toplevelDodajPacijenta, text="Prezime:", font=FONT)
        self.prezimePacijentaLabel.grid(row=1, column=0, padx=5, pady=5)
        self.prezimePacijentaEntry = Entry(self.toplevelDodajPacijenta, font=FONT)
        self.prezimePacijentaEntry.grid(row=1, column=1, padx=5, pady=5)
        self.datumRodjenjaPacijentaLabel = Label(self.toplevelDodajPacijenta, text="Datum rodjenja:", font=FONT)
        self.datumRodjenjaPacijentaLabel.grid(row=2, column=0, padx=5, pady=5)
        self.datumRodjenjaPacijentaEntry = Entry(self.toplevelDodajPacijenta, font=FONT)
        self.datumRodjenjaPacijentaEntry.grid(row=2, column=1, padx=5, pady=5)
        self.jmbgPacijentaLabel = Label(self.toplevelDodajPacijenta, text="JMBG:", font=FONT)
        self.jmbgPacijentaLabel.grid(row=3, column=0, padx=5, pady=5)
        self.jmbgPacijentaEntry = Entry(self.toplevelDodajPacijenta, font=FONT)
        self.jmbgPacijentaEntry.grid(row=3, column=1, padx=5, pady=5)
        self.lboPacijentaLabel = Label(self.toplevelDodajPacijenta, text="LBO:", font=FONT)
        self.lboPacijentaLabel.grid(row=4, column=0, padx=5, pady=5)
        self.lboPacijentaEntry = Entry(self.toplevelDodajPacijenta, font=FONT)
        self.lboPacijentaEntry.grid(row=4, column=1, padx=5, pady=5)
        self.prihvatiPacijentaButton = Button(self.toplevelDodajPacijenta, text="Prihvati", command=self.toplevel_dodaj_pacijenta_prihvati)
        self.prihvatiPacijentaButton.grid(row=5, column=0, padx=10, pady=10)
        self.odbaciPacijentaButton = Button(self.toplevelDodajPacijenta, text="Odbaci", command=self.toplevel_dodaj_pacijenta_odbaci)
        self.odbaciPacijentaButton.grid(row=5, column=1, padx=10, pady=10)

        self.toplevelDodajPacijenta.grab_set()

    def toplevel_dodaj_pacijenta_prihvati(self):
        imePacijenta = self.imePacijentaEntry.get()
        prezimePacijenta = self.prezimePacijentaEntry.get()
        datumRodjenjaPacijenta = self.datumRodjenjaPacijentaEntry.get()
        jmbgPacijenta = self.jmbgPacijentaEntry.get()
        lboPacijenta = self.lboPacijentaEntry.get()

        if self.validacija_podataka_pacijenta(imePacijenta, prezimePacijenta, datumRodjenjaPacijenta, jmbgPacijenta, lboPacijenta):
            novipacijent = Pacijent(jmbg=jmbgPacijenta, ime=imePacijenta, prezime=prezimePacijenta, datum_rodjenja=datumRodjenjaPacijenta, lbo=lboPacijenta)
            
            BAZA_SADRZAJ["Pacijent"].append(novipacijent.__str__())
            BAZA_SADRZAJ["Pacijent"].sort(key=itemgetter("Prezime", "Ime"))
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)

            self.pretragaPacijenataEntry.delete(0, END)
            self.osvezi_listu_pacijenata()
            self.popuni_listu_pacijenata()
            
            indexNovogPacijenta = self.listaPacijenata.index(novipacijent.__str__())
            self.spisakPacijenataListBox.select_set(indexNovogPacijenta)     

            self.prikazi_podatke_pacijenta()

            self.toplevelDodajPacijenta.destroy()

    def toplevel_dodaj_pacijenta_odbaci(self):
        self.toplevelDodajPacijenta.destroy()

    def toplevel_izmeni_pacijenta(self):
        self.toplevelIzmeniPacijenta = Toplevel(self)
        self.toplevelIzmeniPacijenta.title("Izmena pacijenta")

        self.novoImePacijentaLabel = Label(self.toplevelIzmeniPacijenta, text="Ime:", font=FONT)
        self.novoImePacijentaLabel.grid(row=0, column=0, padx=5, pady=5)
        self.novoImePacijentaEntry = Entry(self.toplevelIzmeniPacijenta, font=FONT)
        self.novoImePacijentaEntry.grid(row=0, column=1, padx=5, pady=5)
        self.novoPrezimePacijentaLabel = Label(self.toplevelIzmeniPacijenta, text="Prezime:", font=FONT)
        self.novoPrezimePacijentaLabel.grid(row=1, column=0, padx=5, pady=5)
        self.novoPrezimePacijentaEntry = Entry(self.toplevelIzmeniPacijenta, font=FONT)
        self.novoPrezimePacijentaEntry.grid(row=1, column=1, padx=5, pady=5)
        self.noviDatumRodjenjaPacijentaLabel = Label(self.toplevelIzmeniPacijenta, text="Datum rodjenja:", font=FONT)
        self.noviDatumRodjenjaPacijentaLabel.grid(row=2, column=0, padx=5, pady=5)
        self.noviDatumRodjenjaPacijentaEntry = Entry(self.toplevelIzmeniPacijenta, font=FONT)
        self.noviDatumRodjenjaPacijentaEntry.grid(row=2, column=1, padx=5, pady=5)
        self.noviJmbgPacijentaLabel = Label(self.toplevelIzmeniPacijenta, text="JMBG:", font=FONT)
        self.noviJmbgPacijentaLabel.grid(row=3, column=0, padx=5, pady=5)
        self.noviJmbgPacijentaEntry = Entry(self.toplevelIzmeniPacijenta, font=FONT)
        self.noviJmbgPacijentaEntry.grid(row=3, column=1, padx=5, pady=5)
        self.noviLboPacijentaLabel = Label(self.toplevelIzmeniPacijenta, text="LBO:", font=FONT)
        self.noviLboPacijentaLabel.grid(row=4, column=0, padx=5, pady=5)
        self.noviLboPacijentaEntry = Entry(self.toplevelIzmeniPacijenta, font=FONT)
        self.noviLboPacijentaEntry.grid(row=4, column=1, padx=5, pady=5)
        self.prihvatiNovogPacijentaButton = Button(self.toplevelIzmeniPacijenta, text="Prihvati", command=self.toplevel_izmeni_pacijenta_prihvati)
        self.prihvatiNovogPacijentaButton.grid(row=5, column=0, padx=10, pady=10)
        self.odbaciNovogPacijentaButton = Button(self.toplevelIzmeniPacijenta, text="Odbaci", command=self.toplevel_izmeni_pacijenta_odbaci)
        self.odbaciNovogPacijentaButton.grid(row=5, column=1, padx=10, pady=10)

        self.stariPacijent = {}
        indexTuple = self.spisakPacijenataListBox.curselection()
        if indexTuple:
            index = indexTuple[0]

            self.stariPacijent = self.listaPacijenata[index]
            self.novoImePacijentaEntry.insert(0, self.stariPacijent["Ime"])
            self.novoPrezimePacijentaEntry.insert(0, self.stariPacijent["Prezime"])
            self.noviDatumRodjenjaPacijentaEntry.insert(0, self.stariPacijent["Datum rodjenja"])
            self.noviJmbgPacijentaEntry.insert(0, self.stariPacijent["JMBG"])
            self.noviLboPacijentaEntry.insert(0, self.stariPacijent["LBO"])

            self.noviJmbgPacijentaEntry.config(state=DISABLED)
            self.noviLboPacijentaEntry.config(state=DISABLED)

            self.toplevelIzmeniPacijenta.grab_set()

    def toplevel_izmeni_pacijenta_prihvati(self):
        novoImePacijenta = self.novoImePacijentaEntry.get()
        novoPrezimePacijenta = self.novoPrezimePacijentaEntry.get()
        noviDatumRodjenjaPacijenta = self.noviDatumRodjenjaPacijentaEntry.get()
        noviJmbgPacijenta = self.noviJmbgPacijentaEntry.get()
        noviLboPacijenta = self.noviLboPacijentaEntry.get()

        if self.validacija_izmene_podataka_pacijenta(novoImePacijenta, novoPrezimePacijenta, noviDatumRodjenjaPacijenta):
            BAZA_SADRZAJ["Pacijent"].remove(self.stariPacijent)

            novipacijent = Pacijent(jmbg=noviJmbgPacijenta, ime=novoImePacijenta, prezime=novoPrezimePacijenta, datum_rodjenja=noviDatumRodjenjaPacijenta, lbo=noviLboPacijenta)
            
            BAZA_SADRZAJ["Pacijent"].append(novipacijent.__str__())
            BAZA_SADRZAJ["Pacijent"].sort(key=itemgetter("Prezime", "Ime"))

            for recept in BAZA_SADRZAJ["Recept"]:
                if recept["Pacijent"] == self.stariPacijent:
                    recept["Pacijent"] = novipacijent.__str__()

            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)

            self.pretragaPacijenataEntry.delete(0, END)
            self.osvezi_listu_pacijenata()
            self.popuni_listu_pacijenata()
            
            indexNovogPacijenta = self.listaPacijenata.index(novipacijent.__str__())
            self.spisakPacijenataListBox.select_set(indexNovogPacijenta)     

            self.prikazi_podatke_pacijenta()

            self.toplevelIzmeniPacijenta.destroy()

    def toplevel_izmeni_pacijenta_odbaci(self):
        self.toplevelIzmeniPacijenta.destroy()

    def toplevel_recepti_pacijenta(self):
        self.toplevelRecepti = Toplevel(self)
        self.toplevelRecepti.title("Recepti")
        self.receptiPacijentaText = Text(self.toplevelRecepti, state=DISABLED)
        self.receptiPacijentaText.pack(padx=5, pady=5)
        self.izadjiButton = Button(self.toplevelRecepti, text="Izadji", command=self.toplevel_recepti_pacijenta_zatvori)
        self.izadjiButton.pack(padx=5, pady=5)
        
        self.toplevel_recepti_pacijenta_popuni()
        self.toplevelRecepti.grab_set()

    def toplevel_recepti_pacijenta_popuni(self, *args):
        text = ""

        indexTuple = self.spisakPacijenataListBox.curselection()
        if indexTuple:
            index = indexTuple[0]
            pacijent = self.listaPacijenata[index]
            for recept in BAZA_SADRZAJ["Recept"]:
                if recept["Pacijent"] == pacijent:
                    text += (
                        f'Pacijent:\n\tIme: {recept["Pacijent"]["Ime"]}\n\tPrezime: {recept["Pacijent"]["Prezime"]}\n\tLBO: {recept["Pacijent"]["LBO"]}\n'
                        f'Lekar:\n\tIme: {recept["Lekar"]["Ime"]}\n\tPrezime: {recept["Lekar"]["Prezime"]}\n\tJMBG: {recept["Lekar"]["JMBG"]}\n'
                        f'Lek:\n\tNaziv: {recept["Lek"]["Naziv leka"]}\n\tProizvodjac: {recept["Lek"]["Proizvodjac leka"]}\n\tJKL: {recept["Lek"]["Sifra JKL"]}\n'
                        f'Kolicina: {recept["Kolicina"]}\n'
                        f'Izvestaj: {recept["Izvestaj"]}\n'
                        f'Datum: {recept["Datum"]}\n\n'
                        '------------------------------------------------------\n'
                    )
            
        self.receptiPacijentaText.config(state=NORMAL)
        self.receptiPacijentaText.delete(1.0, END)
        self.receptiPacijentaText.insert(INSERT, text)
        self.receptiPacijentaText.config(state=DISABLED)

    def toplevel_recepti_pacijenta_zatvori(self):
        self.toplevelRecepti.destroy()

    def izbrisi_pacijenta(self):
        if messagebox.askyesno(title="Potvrda", message="Bice obrisani i povezani recepti!"):
            
            indexTuple = self.spisakPacijenataListBox.curselection()
            if indexTuple:
                index = indexTuple[0]
                
                pacijent = self.listaPacijenata[index]
                recepti = [recept for recept in BAZA_SADRZAJ["Recept"] if recept["Pacijent"] == pacijent]
                        
                BAZA_SADRZAJ["Pacijent"].remove(pacijent)
                for recept in recepti:
                    BAZA_SADRZAJ["Recept"].remove(recept)

            BAZA_SADRZAJ["Pacijent"].sort(key=itemgetter("Prezime", "Ime"))
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)
            
            self.pretragaPacijenataEntry.delete(0, END)
            self.osvezi_listu_pacijenata()
            self.popuni_listu_pacijenata()

    def osvezi_listu_pacijenata(self, *args):
        sadrzajPretrage = self.pretragaPacijenataEntry.get()
        self.listaPacijenata = []

        if self.pretragaPacijenataEntry.get() == "":
            self.listaPacijenata = BAZA_SADRZAJ["Pacijent"]
        
        else:
            for pacijent in BAZA_SADRZAJ["Pacijent"]:
                if pacijent["Ime"].lower().find(sadrzajPretrage.lower()) != -1 or pacijent["Prezime"].lower().find(sadrzajPretrage.lower()) != -1:
                    self.listaPacijenata.append(pacijent)

        self.popuni_listu_pacijenata(self)

    def popuni_listu_pacijenata(self, *args):
        self.spisakPacijenataListBox.delete(0, END)
        self.podaciPacijentaText.config(state=NORMAL)
        self.podaciPacijentaText.delete(1.0, END)
        self.podaciPacijentaText.config(state=DISABLED)
        
        for pacijent in self.listaPacijenata:
            self.spisakPacijenataListBox.insert(self.listaPacijenata.index(pacijent), f'{pacijent["Ime"]} {pacijent["Prezime"]}')

    def prikazi_podatke_pacijenta(self, *args):
        text = ""
        
        indexTuple = self.spisakPacijenataListBox.curselection()
        if indexTuple:
            index = indexTuple[0]

            text = (
                f'Ime: {self.listaPacijenata[index]["Ime"]}\n'
                f'Prezime: {self.listaPacijenata[index]["Prezime"]}\n'
                f'Datum rodjenja: {self.listaPacijenata[index]["Datum rodjenja"]}\n'
                f'JMBG: {self.listaPacijenata[index]["JMBG"]}\n'
                f'LBO: {self.listaPacijenata[index]["LBO"]}'
            )
            
        self.podaciPacijentaText.config(state=NORMAL)
        self.podaciPacijentaText.delete(1.0, END)
        self.podaciPacijentaText.insert(INSERT, text)
        self.podaciPacijentaText.config(state=DISABLED)
        self.izmeniPacijentaButton.config(state=NORMAL)
        self.obrisiPacijentaButton.config(state=NORMAL)

    def validacija_podataka_pacijenta(self, ime, prezime, datum, jmbg, lbo):
        oblikDatuma = r"^(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](\d\d\d\d)"
        jmbgLst = []
        lboLst = []

        for pacijent in BAZA_SADRZAJ["Pacijent"]:
            for key, value in pacijent.items():
                if key == "JMBG":
                    jmbgLst.append(value)
                elif key == "LBO":
                    lboLst.append(value)
        
        if len(ime) < 2:
            messagebox.showerror("Error", "Ime mora biti duze od 2 karaktera")
        elif len(prezime) < 2:
            messagebox.showerror("Error", "Prezime mora biti duze od 2 karaktera")
        elif not re.match(oblikDatuma, datum):
            messagebox.showerror("Error", "Datum mora biti u formatu dd.MM.yyyy")
        elif date(int(datum.split('.')[2]), int(datum.split('.')[1]), int(datum.split('.')[0])) > datetime.now().date():
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
            return True

    def validacija_izmene_podataka_pacijenta(self, ime, prezime, datum):
        oblikDatuma = r"^(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](\d\d\d\d)"
        
        if len(ime) < 2:
            messagebox.showerror("Error", "Ime mora biti duze od 2 karaktera")
        elif len(prezime) < 2:
            messagebox.showerror("Error", "Prezime mora biti duze od 2 karaktera")
        elif not re.match(oblikDatuma, datum):
            messagebox.showerror("Error", "Datum mora biti u formatu dd.MM.yyyy")
        elif date(int(datum.split('.')[2]), int(datum.split('.')[1]), int(datum.split('.')[0])) > datetime.now().date():
            messagebox.showerror("Error", "Datum moze biti najkasnije danasnji")
        else:
            return True


class LekariStranica(Frame):

    def __init__(self, parent, controler):
        Frame.__init__(self, parent)

        self.leviFrame = Frame(self)
        self.leviFrame.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.spisakLekaraLabel = Label(self.leviFrame, text="Spisak pacijenata", font=FONT)
        self.spisakLekaraLabel.pack(fill=X, padx=5, pady=5)
        self.spisakLekaraListBox = Listbox(self.leviFrame, selectmode=SINGLE, font=FONT)
        self.spisakLekaraListBox.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)
        self.pretragaLekaraEntry = Entry(self.leviFrame, font=FONT)
        self.pretragaLekaraEntry.pack(side=LEFT, expand=TRUE, fill=BOTH, padx=5, pady=5)
        self.receptiLekaraButton = Button(self.leviFrame, text="Recepti", font=FONT, command=self.toplevel_recepti_lekara)
        self.receptiLekaraButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.desniFrame = Frame(self,)
        self.desniFrame.pack(side=RIGHT, fill=Y)
        self.podaciLekaraLabel = Label(self.desniFrame, text="Podaci pacijenta", font=FONT)
        self.podaciLekaraLabel.pack(fill=X, padx=5, pady=5)
        self.podaciLekaraText = Text(self.desniFrame, font=FONT, state=DISABLED)
        self.podaciLekaraText.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)
        self.dodajLekaraButton = Button(self.desniFrame, text="Dodaj", font=FONT, command=self.toplevel_dodaj_lekara)
        self.dodajLekaraButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.izmeniLekaraButton = Button(self.desniFrame, text="Izmeni", font=FONT, state=DISABLED, command=self.toplevel_izmeni_lekara)
        self.izmeniLekaraButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.obrisiLekaraButton = Button(self.desniFrame, text="Izbrisi", font=FONT, state=DISABLED, command=self.izbrisi_lekara)
        self.obrisiLekaraButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)

        self.listaLekara = []

        self.osvezi_listu_lekara()
        self.popuni_listu_lekara()
        self.spisakLekaraListBox.bind('<<ListboxSelect>>', self.prikazi_podatke_lekara)
        self.pretragaLekaraEntry.bind('<KeyRelease>', self.osvezi_listu_lekara)

    def toplevel_dodaj_lekara(self):
        self.toplevelDodajLekara = Toplevel(self)
        self.toplevelDodajLekara.title("Novi lekar")

        self.imeLekaraLabel = Label(self.toplevelDodajLekara, text="Ime:", font=FONT)
        self.imeLekaraLabel.grid(row=0, column=0, padx=5, pady=5)
        self.imeLekaraEntry = Entry(self.toplevelDodajLekara, font=FONT)
        self.imeLekaraEntry.grid(row=0, column=1, padx=5, pady=5)
        self.prezimeLekaraLabel = Label(self.toplevelDodajLekara, text="Prezime:", font=FONT)
        self.prezimeLekaraLabel.grid(row=1, column=0, padx=5, pady=5)
        self.prezimeLekaraEntry = Entry(self.toplevelDodajLekara, font=FONT)
        self.prezimeLekaraEntry.grid(row=1, column=1, padx=5, pady=5)
        self.datumRodjenjaLekaraLabel = Label(self.toplevelDodajLekara, text="Datum rodjenja:", font=FONT)
        self.datumRodjenjaLekaraLabel.grid(row=2, column=0, padx=5, pady=5)
        self.datumRodjenjaLekaraEntry = Entry(self.toplevelDodajLekara, font=FONT)
        self.datumRodjenjaLekaraEntry.grid(row=2, column=1, padx=5, pady=5)
        self.jmbgLekaraLabel = Label(self.toplevelDodajLekara, text="JMBG:", font=FONT)
        self.jmbgLekaraLabel.grid(row=3, column=0, padx=5, pady=5)
        self.jmbgLekaraEntry = Entry(self.toplevelDodajLekara, font=FONT)
        self.jmbgLekaraEntry.grid(row=3, column=1, padx=5, pady=5)
        self.specijalizacijaLekaraLabel = Label(self.toplevelDodajLekara, text="Specijalizacija:", font=FONT)
        self.specijalizacijaLekaraLabel.grid(row=4, column=0, padx=5, pady=5)
        self.specijalizacijaLekaraEntry = Entry(self.toplevelDodajLekara, font=FONT)
        self.specijalizacijaLekaraEntry.grid(row=4, column=1, padx=5, pady=5)
        self.prihvatiLekaraButton = Button(self.toplevelDodajLekara, text="Prihvati", command=self.toplevel_dodaj_lekara_prihvati)
        self.prihvatiLekaraButton.grid(row=5, column=0, padx=10, pady=10)
        self.odbaciLekaraButton = Button(self.toplevelDodajLekara, text="Odbaci", command=self.toplevel_dodaj_lekara_odbaci)
        self.odbaciLekaraButton.grid(row=5, column=1, padx=10, pady=10)

        self.toplevelDodajLekara.grab_set()

    def toplevel_dodaj_lekara_prihvati(self):
        imeLekara = self.imeLekaraEntry.get()
        prezimeLekara = self.prezimeLekaraEntry.get()
        datumRodjenjaLekara = self.datumRodjenjaLekaraEntry.get()
        jmbgLekara = self.jmbgLekaraEntry.get()
        specijalizacijaLekara = self.specijalizacijaLekaraEntry.get()

        if self.validacija_podataka_lekara(imeLekara, prezimeLekara, datumRodjenjaLekara, jmbgLekara, specijalizacijaLekara):
            novilekar = Lekar(jmbg=jmbgLekara, ime=imeLekara, prezime=prezimeLekara, datum_rodjenja=datumRodjenjaLekara, specijalizacija=specijalizacijaLekara)
            
            BAZA_SADRZAJ["Lekar"].append(novilekar.__str__())
            BAZA_SADRZAJ["Lekar"].sort(key=itemgetter("Prezime", "Ime"))
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)

            self.pretragaLekaraEntry.delete(0, END)
            self.osvezi_listu_lekara()
            self.popuni_listu_lekara()
            
            indexNovogLekara = self.listaLekara.index(novilekar.__str__())
            self.spisakLekaraListBox.select_set(indexNovogLekara)     

            self.prikazi_podatke_lekara()

            self.toplevelDodajLekara.destroy()

    def toplevel_dodaj_lekara_odbaci(self):
        self.toplevelDodajLekara.destroy()

    def toplevel_izmeni_lekara(self):
        self.toplevelIzmeniLekara = Toplevel(self)
        self.toplevelIzmeniLekara.title("Izmena lekara")

        self.novoImeLekaraLabel = Label(self.toplevelIzmeniLekara, text="Ime:", font=FONT)
        self.novoImeLekaraLabel.grid(row=0, column=0, padx=5, pady=5)
        self.novoImeLekaraEntry = Entry(self.toplevelIzmeniLekara, font=FONT)
        self.novoImeLekaraEntry.grid(row=0, column=1, padx=5, pady=5)
        self.novoPrezimeLekaraLabel = Label(self.toplevelIzmeniLekara, text="Prezime:", font=FONT)
        self.novoPrezimeLekaraLabel.grid(row=1, column=0, padx=5, pady=5)
        self.novoPrezimeLekaraEntry = Entry(self.toplevelIzmeniLekara, font=FONT)
        self.novoPrezimeLekaraEntry.grid(row=1, column=1, padx=5, pady=5)
        self.noviDatumRodjenjaLekaraLabel = Label(self.toplevelIzmeniLekara, text="Datum rodjenja:", font=FONT)
        self.noviDatumRodjenjaLekaraLabel.grid(row=2, column=0, padx=5, pady=5)
        self.noviDatumRodjenjaLekaraEntry = Entry(self.toplevelIzmeniLekara, font=FONT)
        self.noviDatumRodjenjaLekaraEntry.grid(row=2, column=1, padx=5, pady=5)
        self.noviJmbgLekaraLabel = Label(self.toplevelIzmeniLekara, text="JMBG:", font=FONT)
        self.noviJmbgLekaraLabel.grid(row=3, column=0, padx=5, pady=5)
        self.noviJmbgLekaraEntry = Entry(self.toplevelIzmeniLekara, font=FONT)
        self.noviJmbgLekaraEntry.grid(row=3, column=1, padx=5, pady=5)
        self.novaSpecijalizacijaLekaraLabel = Label(self.toplevelIzmeniLekara, text="Specijalizacija:", font=FONT)
        self.novaSpecijalizacijaLekaraLabel.grid(row=4, column=0, padx=5, pady=5)
        self.novaSpecijalizacijaLekaraEntry = Entry(self.toplevelIzmeniLekara, font=FONT)
        self.novaSpecijalizacijaLekaraEntry.grid(row=4, column=1, padx=5, pady=5)
        self.prihvatiNovogLekaraButton = Button(self.toplevelIzmeniLekara, text="Prihvati", command=self.toplevel_izmeni_lekara_prihvati)
        self.prihvatiNovogLekaraButton.grid(row=5, column=0, padx=10, pady=10)
        self.odbaciNovogLekaraButton = Button(self.toplevelIzmeniLekara, text="Odbaci", command=self.toplevel_izmeni_lekara_odbaci)
        self.odbaciNovogLekaraButton.grid(row=5, column=1, padx=10, pady=10)

        self.stariLekar = {}
        indexTuple = self.spisakLekaraListBox.curselection()
        if indexTuple:
            index = indexTuple[0]

            self.stariLekar = self.listaLekara[index]
            self.novoImeLekaraEntry.insert(0, self.stariLekar["Ime"])
            self.novoPrezimeLekaraEntry.insert(0, self.stariLekar["Prezime"])
            self.noviDatumRodjenjaLekaraEntry.insert(0, self.stariLekar["Datum rodjenja"])
            self.noviJmbgLekaraEntry.insert(0, self.stariLekar["JMBG"])
            self.novaSpecijalizacijaLekaraEntry.insert(0, self.stariLekar["Specijalizacija"])

            self.noviJmbgLekaraEntry.config(state=DISABLED)

            self.toplevelIzmeniLekara.grab_set()

    def toplevel_izmeni_lekara_prihvati(self):
        novoImeLekara = self.novoImeLekaraEntry.get()
        novoPrezimeLekara = self.novoPrezimeLekaraEntry.get()
        noviDatumRodjenjaLekara = self.noviDatumRodjenjaLekaraEntry.get()
        noviJmbgLekara = self.noviJmbgLekaraEntry.get()
        novaSpecijalizacijaLekara = self.novaSpecijalizacijaLekaraEntry.get()

        if self.validacija_izmene_podataka_lekara(novoImeLekara, novoPrezimeLekara, noviDatumRodjenjaLekara, novaSpecijalizacijaLekara):
            BAZA_SADRZAJ["Lekar"].remove(self.stariLekar)

            novilekar = Lekar(jmbg=noviJmbgLekara, ime=novoImeLekara, prezime=novoPrezimeLekara, datum_rodjenja=noviDatumRodjenjaLekara, specijalizacija=novaSpecijalizacijaLekara)
            
            BAZA_SADRZAJ["Lekar"].append(novilekar.__str__())
            BAZA_SADRZAJ["Lekar"].sort(key=itemgetter("Prezime", "Ime"))

            for recept in BAZA_SADRZAJ["Recept"]:
                if recept["Lekar"] == self.stariLekar:
                    recept["Lekar"] = novilekar.__str__()

            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)

            self.pretragaLekaraEntry.delete(0, END)
            self.osvezi_listu_lekara()
            self.popuni_listu_lekara()
            
            indexNovogLekara = self.listaLekara.index(novilekar.__str__())
            self.spisakLekaraListBox.select_set(indexNovogLekara)     

            self.prikazi_podatke_lekara()

            self.toplevelIzmeniLekara.destroy()

    def toplevel_izmeni_lekara_odbaci(self):
        self.toplevelIzmeniLekara.destroy()

    def toplevel_recepti_lekara(self):
        self.toplevelReceptiLekara = Toplevel(self)
        self.toplevelReceptiLekara.title("Recepti")
        self.receptiLekaraText = Text(self.toplevelReceptiLekara, state=DISABLED)
        self.receptiLekaraText.pack(padx=5, pady=5)
        self.izadjiButton2 = Button(self.toplevelReceptiLekara, text="Izadji", command=self.toplevel_recepti_lekara_zatvori)
        self.izadjiButton2.pack(padx=5, pady=5)
        
        self.toplevel_recepti_lekara_popuni()
        self.toplevelReceptiLekara.grab_set()

    def toplevel_recepti_lekara_popuni(self, *args):
        text = ""

        indexTuple = self.spisakLekaraListBox.curselection()
        if indexTuple:
            index = indexTuple[0]
            lekar = self.listaLekara[index]
            for recept in BAZA_SADRZAJ["Recept"]:
                if recept["Lekar"] == lekar:
                    text += (
                        f'Pacijent:\n\tIme: {recept["Pacijent"]["Ime"]}\n\tPrezime: {recept["Pacijent"]["Prezime"]}\n\tLBO: {recept["Pacijent"]["LBO"]}\n'
                        f'Lekar:\n\tIme: {recept["Lekar"]["Ime"]}\n\tPrezime: {recept["Lekar"]["Prezime"]}\n\tJMBG: {recept["Lekar"]["JMBG"]}\n'
                        f'Lek:\n\tNaziv: {recept["Lek"]["Naziv leka"]}\n\tProizvodjac: {recept["Lek"]["Proizvodjac leka"]}\n\tJKL: {recept["Lek"]["Sifra JKL"]}\n'
                        f'Kolicina: {recept["Kolicina"]}\n'
                        f'Izvestaj: {recept["Izvestaj"]}\n'
                        f'Datum: {recept["Datum"]}\n\n'
                        '------------------------------------------------------\n'
                    )
            
        self.receptiLekaraText.config(state=NORMAL)
        self.receptiLekaraText.delete(1.0, END)
        self.receptiLekaraText.insert(INSERT, text)
        self.receptiLekaraText.config(state=DISABLED)

    def toplevel_recepti_lekara_zatvori(self):
        self.toplevelReceptiLekara.destroy()

    def izbrisi_lekara(self):
        if messagebox.askyesno(title="Potvrda", message="Bice obrisani i povezani recepti!"):
            
            indexTuple = self.spisakLekaraListBox.curselection()
            if indexTuple:
                index = indexTuple[0]
                
                lekar = self.listaLekara[index]
                recepti = [recept for recept in BAZA_SADRZAJ["Recept"] if recept["Lekar"] == lekar]
                        
                BAZA_SADRZAJ["Lekar"].remove(lekar)
                for recept in recepti:
                    BAZA_SADRZAJ["Recept"].remove(recept)

            BAZA_SADRZAJ["Lekar"].sort(key=itemgetter("Prezime", "Ime"))
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)
            
            self.pretragaLekaraEntry.delete(0, END)
            self.osvezi_listu_lekara()
            self.popuni_listu_lekara()

    def osvezi_listu_lekara(self, *args):
        sadrzajPretrage = self.pretragaLekaraEntry.get()
        self.listaLekara = []

        if self.pretragaLekaraEntry.get() == "":
            self.listaLekara = BAZA_SADRZAJ["Lekar"]
        
        else:
            for lekar in BAZA_SADRZAJ["Lekar"]:
                if lekar["Ime"].lower().find(sadrzajPretrage.lower()) != -1 or lekar["Prezime"].lower().find(sadrzajPretrage.lower()) != -1:
                    self.listaLekara.append(lekar)

        self.popuni_listu_lekara(self)

    def popuni_listu_lekara(self, *args):
        self.spisakLekaraListBox.delete(0, END)
        self.podaciLekaraText.config(state=NORMAL)
        self.podaciLekaraText.delete(1.0, END)
        self.podaciLekaraText.config(state=DISABLED)
        
        for lekar in self.listaLekara:
            self.spisakLekaraListBox.insert(self.listaLekara.index(lekar), f'{lekar["Ime"]} {lekar["Prezime"]}')

    def prikazi_podatke_lekara(self, *args):
        text = ""
        
        indexTuple = self.spisakLekaraListBox.curselection()
        if indexTuple:
            index = indexTuple[0]

            text = (
                f'Ime: {self.listaLekara[index]["Ime"]}\n'
                f'Prezime: {self.listaLekara[index]["Prezime"]}\n'
                f'Datum rodjenja: {self.listaLekara[index]["Datum rodjenja"]}\n'
                f'JMBG: {self.listaLekara[index]["JMBG"]}\n'
                f'Specijalizacija: {self.listaLekara[index]["Specijalizacija"]}'
            )
            
        self.podaciLekaraText.config(state=NORMAL)
        self.podaciLekaraText.delete(1.0, END)
        self.podaciLekaraText.insert(INSERT, text)
        self.podaciLekaraText.config(state=DISABLED)
        self.izmeniLekaraButton.config(state=NORMAL)
        self.obrisiLekaraButton.config(state=NORMAL)

    def validacija_podataka_lekara(self, ime, prezime, datum, jmbg, specijalizacija):
        oblikDatuma = r"^(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](\d\d\d\d)"
        jmbgLst = []

        for lekar in BAZA_SADRZAJ["Lekar"]:
            for key, value in lekar.items():
                if key == "JMBG":
                    jmbgLst.append(value)
        
        if len(ime) < 2:
            messagebox.showerror("Error", "Ime mora biti duze od 2 karaktera")
        elif len(prezime) < 2:
            messagebox.showerror("Error", "Prezime mora biti duze od 2 karaktera")
        elif not re.match(oblikDatuma, datum):
            messagebox.showerror("Error", "Datum mora biti u formatu dd.MM.yyyy")
        elif date(int(datum.split('.')[2]), int(datum.split('.')[1]), int(datum.split('.')[0])) > datetime.now().date():
            messagebox.showerror("Error", "Datum moze biti najkasnije danasnji")
        elif jmbg in jmbgLst:
            messagebox.showerror("Error", "JMBG postoji u bazi")
        elif len(jmbg) != 13:
            messagebox.showerror("Error", "JMBG mora biti 13 karaktera")
        elif len(specijalizacija) < 2:
            messagebox.showerror("Error", "Specijalizacija mora biti duza od 2 karaktera")
        else:
            return True

    def validacija_izmene_podataka_lekara(self, ime, prezime, datum, specijalizacija):
        oblikDatuma = r"^(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](\d\d\d\d)"
        
        if len(ime) < 2:
            messagebox.showerror("Error", "Ime mora biti duze od 2 karaktera")
        elif len(prezime) < 2:
            messagebox.showerror("Error", "Prezime mora biti duze od 2 karaktera")
        elif not re.match(oblikDatuma, datum):
            messagebox.showerror("Error", "Datum mora biti u formatu dd.MM.yyyy")
        elif date(int(datum.split('.')[2]), int(datum.split('.')[1]), int(datum.split('.')[0])) > datetime.now().date():
            messagebox.showerror("Error", "Datum moze biti najkasnije danasnji")
        elif len(specijalizacija) < 2:
            messagebox.showerror("Error", "Specijalizacija mora biti duza od 2 karaktera")
        else:
            return True


class LekoviStranica(Frame):

    def __init__(self, parent, controler):
        Frame.__init__(self, parent)

        self.leviFrame = Frame(self)
        self.leviFrame.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.spisakLekovaLabel = Label(self.leviFrame, text="Spisak lekova", font=FONT)
        self.spisakLekovaLabel.pack(fill=X, padx=5, pady=5)
        self.spisakLekovaListBox = Listbox(self.leviFrame, selectmode=SINGLE, font=FONT)
        self.spisakLekovaListBox.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)
        self.pretragaLekovaEntry = Entry(self.leviFrame, font=FONT)
        self.pretragaLekovaEntry.pack(side=LEFT, expand=TRUE, fill=BOTH, padx=5, pady=5)
        self.desniFrame = Frame(self,)
        self.desniFrame.pack(side=RIGHT, fill=Y)
        self.podaciLekovaLabel = Label(self.desniFrame, text="Podaci lekova", font=FONT)
        self.podaciLekovaLabel.pack(fill=X, padx=5, pady=5)
        self.podaciLekovaText = Text(self.desniFrame, font=FONT, state=DISABLED)
        self.podaciLekovaText.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)
        self.dodajLekButton = Button(self.desniFrame, text="Dodaj", font=FONT, command=self.toplevel_dodaj_lek)
        self.dodajLekButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.izmeniLekButton = Button(self.desniFrame, text="Izmeni", font=FONT, state=DISABLED, command=self.toplevel_izmeni_lek)
        self.izmeniLekButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.obrisiLekButton = Button(self.desniFrame, text="Izbrisi", font=FONT, state=DISABLED, command=self.izbrisi_lek)
        self.obrisiLekButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)

        self.listaLekova = []

        self.osvezi_listu_lekova()
        self.popuni_listu_lekova()
        self.spisakLekovaListBox.bind('<<ListboxSelect>>', self.prikazi_podatke_leka)
        self.pretragaLekovaEntry.bind('<KeyRelease>', self.osvezi_listu_lekova)

    def toplevel_dodaj_lek(self):
        self.toplevelDodajLek = Toplevel(self)
        self.toplevelDodajLek.title("Novi lek")

        self.nazivLekaLabel = Label(self.toplevelDodajLek, text="Naziv:", font=FONT)
        self.nazivLekaLabel.grid(row=0, column=0, padx=5, pady=5)
        self.nazivLekaEntry = Entry(self.toplevelDodajLek, font=FONT)
        self.nazivLekaEntry.grid(row=0, column=1, padx=5, pady=5)
        self.proizvodjacLekaLabel = Label(self.toplevelDodajLek, text="Proizvodjac:", font=FONT)
        self.proizvodjacLekaLabel.grid(row=1, column=0, padx=5, pady=5)
        self.proizvodjacLekaEntry = Entry(self.toplevelDodajLek, font=FONT)
        self.proizvodjacLekaEntry.grid(row=1, column=1, padx=5, pady=5)
        self.tipLekaLabel = Label(self.toplevelDodajLek, text="Tip:", font=FONT)
        self.tipLekaLabel.grid(row=2, column=0, padx=5, pady=5)
        self.tipLekaEntry = Entry(self.toplevelDodajLek, font=FONT)
        self.tipLekaEntry.grid(row=2, column=1, padx=5, pady=5)
        self.jklLekaLabel = Label(self.toplevelDodajLek, text="JKL:", font=FONT)
        self.jklLekaLabel.grid(row=3, column=0, padx=5, pady=5)
        self.jklLekaEntry = Entry(self.toplevelDodajLek, font=FONT)
        self.jklLekaEntry.grid(row=3, column=1, padx=5, pady=5)
        self.prihvatiLekButton = Button(self.toplevelDodajLek, text="Prihvati", command=self.toplevel_dodaj_lek_prihvati)
        self.prihvatiLekButton.grid(row=5, column=0, padx=10, pady=10)
        self.odbaciLekButton = Button(self.toplevelDodajLek, text="Odbaci", command=self.toplevel_dodaj_lek_odbaci)
        self.odbaciLekButton.grid(row=5, column=1, padx=10, pady=10)

        self.toplevelDodajLek.grab_set()

    def toplevel_dodaj_lek_prihvati(self):
        nazivLeka = self.nazivLekaEntry.get()
        proizvodjacLeka = self.proizvodjacLekaEntry.get()
        tipLeka = self.tipLekaEntry.get()
        jklLeka = self.jklLekaEntry.get()

        if self.validacija_podataka_leka(nazivLeka, proizvodjacLeka, tipLeka, jklLeka):
            novilek = Lek(sifra_jkl=jklLeka, naziv=nazivLeka, proizvodac=proizvodjacLeka, tip_leka=tipLeka)
            
            BAZA_SADRZAJ["Lek"].append(novilek.__str__())
            BAZA_SADRZAJ["Lek"].sort(key=itemgetter("Naziv leka"))
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)

            self.pretragaLekovaEntry.delete(0, END)
            self.osvezi_listu_lekova()
            self.popuni_listu_lekova()
            
            indexNovogLeka = self.listaLekova.index(novilek.__str__())
            self.spisakLekovaListBox.select_set(indexNovogLeka)     

            self.prikazi_podatke_leka()

            self.toplevelDodajLek.destroy()

    def toplevel_dodaj_lek_odbaci(self):
        self.toplevelDodajLek.destroy()

    def toplevel_izmeni_lek(self):
        self.toplevelIzmeniLek = Toplevel(self)
        self.toplevelIzmeniLek.title("Izmena leka")

        self.noviNazivLekaLabel = Label(self.toplevelIzmeniLek, text="Naziv:", font=FONT)
        self.noviNazivLekaLabel.grid(row=0, column=0, padx=5, pady=5)
        self.noviNazivLekaEntry = Entry(self.toplevelIzmeniLek, font=FONT)
        self.noviNazivLekaEntry.grid(row=0, column=1, padx=5, pady=5)
        self.noviProizvodjacLekaLabel = Label(self.toplevelIzmeniLek, text="Proizvnodjac:", font=FONT)
        self.noviProizvodjacLekaLabel.grid(row=1, column=0, padx=5, pady=5)
        self.noviProizvodjacLekaEntry = Entry(self.toplevelIzmeniLek, font=FONT)
        self.noviProizvodjacLekaEntry.grid(row=1, column=1, padx=5, pady=5)
        self.noviTipLekaLabel = Label(self.toplevelIzmeniLek, text="Tip:", font=FONT)
        self.noviTipLekaLabel.grid(row=2, column=0, padx=5, pady=5)
        self.noviTipLekaEntry = Entry(self.toplevelIzmeniLek, font=FONT)
        self.noviTipLekaEntry.grid(row=2, column=1, padx=5, pady=5)
        self.noviJklLekaLabel = Label(self.toplevelIzmeniLek, text="JKL:", font=FONT)
        self.noviJklLekaLabel.grid(row=3, column=0, padx=5, pady=5)
        self.noviJklLekaEntry = Entry(self.toplevelIzmeniLek, font=FONT)
        self.noviJklLekaEntry.grid(row=3, column=1, padx=5, pady=5)
        self.prihvatiNoviLekButton = Button(self.toplevelIzmeniLek, text="Prihvati", command=self.toplevel_izmeni_lek_prihvati)
        self.prihvatiNoviLekButton.grid(row=5, column=0, padx=10, pady=10)
        self.odbaciNoviLekButton = Button(self.toplevelIzmeniLek, text="Odbaci", command=self.toplevel_izmeni_lek_odbaci)
        self.odbaciNoviLekButton.grid(row=5, column=1, padx=10, pady=10)

        self.stariLek = {}
        indexTuple = self.spisakLekovaListBox.curselection()
        if indexTuple:
            index = indexTuple[0]

            self.stariLek = self.listaLekova[index]
            self.noviNazivLekaEntry.insert(0, self.stariLek["Naziv leka"])
            self.noviProizvodjacLekaEntry.insert(0, self.stariLek["Proizvodjac leka"])
            self.noviTipLekaEntry.insert(0, self.stariLek["Tip leka"])
            self.noviJklLekaEntry.insert(0, self.stariLek["Sifra JKL"])

            self.noviJklLekaEntry.config(state=DISABLED)

            self.toplevelIzmeniLek.grab_set()

    def toplevel_izmeni_lek_prihvati(self):
        noviNazivLeka = self.noviNazivLekaEntry.get()
        noviProizvodjacLeka = self.noviProizvodjacLekaEntry.get()
        noviTipLeka = self.noviTipLekaEntry.get()
        noviJklLeka = self.noviJklLekaEntry.get()

        if self.validacija_izmene_podataka_leka(noviNazivLeka, noviProizvodjacLeka, noviTipLeka):
            BAZA_SADRZAJ["Lek"].remove(self.stariLek)

            novilek = Lek(sifra_jkl=noviJklLeka, naziv=noviNazivLeka, proizvodac=noviProizvodjacLeka, tip_leka=noviTipLeka)
            
            BAZA_SADRZAJ["Lek"].append(novilek.__str__())
            BAZA_SADRZAJ["Lek"].sort(key=itemgetter("Naziv leka"))

            for recept in BAZA_SADRZAJ["Recept"]:
                if recept["Lek"] == self.stariLek:
                    recept["Lek"] = novilek.__str__()

            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)

            self.pretragaLekovaEntry.delete(0, END)
            self.osvezi_listu_lekova()
            self.popuni_listu_lekova()
            
            indexNovogLeka = self.listaLekova.index(novilek.__str__())
            self.spisakLekovaListBox.select_set(indexNovogLeka)     

            self.prikazi_podatke_leka()

            self.toplevelIzmeniLek.destroy()

    def toplevel_izmeni_lek_odbaci(self):
        self.toplevelIzmeniLek.destroy()

    def izbrisi_lek(self):
        if messagebox.askyesno(title="Potvrda", message="Bice obrisani i povezani recepti!"):
            
            indexTuple = self.spisakLekovaListBox.curselection()
            if indexTuple:
                index = indexTuple[0]
                
                lek = self.listaLekova[index]
                recepti = [recept for recept in BAZA_SADRZAJ["Recept"] if recept["Lek"] == lek]
                        
                BAZA_SADRZAJ["Lek"].remove(lek)
                for recept in recepti:
                    BAZA_SADRZAJ["Recept"].remove(recept)

            BAZA_SADRZAJ["Lek"].sort(key=itemgetter("Naziv leka"))
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)
            
            self.pretragaLekovaEntry.delete(0, END)
            self.osvezi_listu_lekova()
            self.popuni_listu_lekova()

    def osvezi_listu_lekova(self, *args):
        sadrzajPretrage = self.pretragaLekovaEntry.get()
        self.listaLekova = []

        if self.pretragaLekovaEntry.get() == "":
            self.listaLekova = BAZA_SADRZAJ["Lek"]
        
        else:
            for lek in BAZA_SADRZAJ["Lek"]:
                if lek["Naziv leka"].lower().find(sadrzajPretrage.lower()) != -1:
                    self.listaLekova.append(lek)

        self.popuni_listu_lekova(self)

    def popuni_listu_lekova(self, *args):
        self.spisakLekovaListBox.delete(0, END)
        self.podaciLekovaText.config(state=NORMAL)
        self.podaciLekovaText.delete(1.0, END)
        self.podaciLekovaText.config(state=DISABLED)
        
        for lek in self.listaLekova:
            self.spisakLekovaListBox.insert(self.listaLekova.index(lek), f'{lek["Naziv leka"]}')

    def prikazi_podatke_leka(self, *args):
        text = ""
        
        indexTuple = self.spisakLekovaListBox.curselection()
        if indexTuple:
            index = indexTuple[0]

            text = (
                f'Naziv: {self.listaLekova[index]["Naziv leka"]}\n'
                f'Proizvodjac: {self.listaLekova[index]["Proizvodjac leka"]}\n'
                f'Tip: {self.listaLekova[index]["Tip leka"]}\n'
                f'JKL: {self.listaLekova[index]["Sifra JKL"]}'
            )
            
        self.podaciLekovaText.config(state=NORMAL)
        self.podaciLekovaText.delete(1.0, END)
        self.podaciLekovaText.insert(INSERT, text)
        self.podaciLekovaText.config(state=DISABLED)
        self.izmeniLekButton.config(state=NORMAL)
        self.obrisiLekButton.config(state=NORMAL)

    def validacija_podataka_leka(self, naziv, proizvodjac, tip, jkl):
        jklLst = []

        for lek in BAZA_SADRZAJ["Lek"]:
            for key, value in lek.items():
                if key == "Sifra JKL":
                    jklLst.append(value)
        
        if len(naziv) < 2:
            messagebox.showerror("Error", "Naziv mora biti duze od 2 karaktera")
        elif len(proizvodjac) < 2:
            messagebox.showerror("Error", "Proizvodjac mora biti duze od 2 karaktera")
        elif len(tip) < 2:
            messagebox.showerror("Error", "Tip mora biti duze od 2 karaktera")
        elif jkl in jklLst:
            messagebox.showerror("Error", "JKL postoji u bazi")
        elif len(jkl) != 7:
            messagebox.showerror("Error", "JKL mora biti 7 karaktera")
        else:
            return True

    def validacija_izmene_podataka_leka(self, naziv, proizvodjac, tip):        
        if len(naziv) < 2:
            messagebox.showerror("Error", "Naziv mora biti duze od 2 karaktera")
        elif len(proizvodjac) < 2:
            messagebox.showerror("Error", "Proizvodjac mora biti duze od 2 karaktera")
        elif len(tip) < 2:
            messagebox.showerror("Error", "Tip mora biti duze od 2 karaktera")
        else:
            return True


class ReceptiStranica(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self.leftFrame = Frame(self)
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.spisakRecepataLabel = Label(self.leftFrame, text="Spisak receata", font=FONT)
        self.spisakRecepataLabel.pack(fill=X, padx=5, pady=5)
        self.spisakRecepataListBox = Listbox(self.leftFrame, selectmode=SINGLE, font=FONT)
        self.spisakRecepataListBox.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)        
        self.pretragaPacijenataCombo = ttk.Combobox(self.leftFrame, font=FONT)
        self.pretragaPacijenataCombo.pack(side=LEFT, expand=TRUE, fill=BOTH, padx=5, pady=5)
        self.rightFrame = Frame(self,)
        self.rightFrame.pack(side=RIGHT, fill=Y)
        self.podaciReceptaLabel = Label(self.rightFrame, text="Podaci o receptu", font=FONT)
        self.podaciReceptaLabel.pack(fill=X, padx=5, pady=5)
        self.podaciReceptaText = Text(self.rightFrame, font=FONT, state=DISABLED)
        self.podaciReceptaText.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)
        self.dodajReceptButton = Button(self.rightFrame, text="Dodaj", font=FONT, command=self.toplevel_dodaj_recept)
        self.dodajReceptButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.izmeniReceptButton = Button(self.rightFrame, text="Izmeni", font=FONT, state=DISABLED, command=self.toplevel_izmeni_recept)
        self.izmeniReceptButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)
        self.obrisiReceptButton = Button(self.rightFrame, text="Izbrisi", font=FONT, state=DISABLED, command=self.izbrisi_recept)
        self.obrisiReceptButton.pack(side=LEFT, expand=TRUE, fill=X, padx=5, pady=5)

        self.spisakPacijenata = []
        self.spisakRecepata = []

        self.pretragaPacijenataCombo.after(250, self.osvezi_combo_polje_pacijenata)
        self.pretragaPacijenataCombo.bind('<<ComboboxSelected>>', self.osvezi_listu_recepata)
        self.spisakRecepataListBox.bind('<<ListboxSelect>>', self.prikazi_podatke_recepta)

    def toplevel_dodaj_recept(self):
        selektovaniPacijentIndex = self.pretragaPacijenataCombo.current()
        
        if selektovaniPacijentIndex == 0:
            messagebox.showerror("Error", "Selektujte pacijenta")
        else:
            self.spisakLekara = []
            lekari = [""]
            self.spisakLekova = []
            lekovi = [""]
        
            for lekar in BAZA_SADRZAJ["Lekar"]:
                self.spisakLekara.append(lekar)
                lekari.append(f'{lekar["Ime"]} {lekar["Prezime"]}')
        
            for lek in BAZA_SADRZAJ["Lek"]:
                self.spisakLekova.append(lek)
                lekovi.append(f'{lek["Naziv leka"]}')

            self.toplevelDodajRecept = Toplevel(self)
            self.toplevelDodajRecept.title("Novi recept")
            self.lekarLabel = Label(self.toplevelDodajRecept, text="Lekar:", font=FONT)
            self.lekarLabel.grid(row=0, column=0, padx=5, pady=5)
            self.lekarCombo = ttk.Combobox(self.toplevelDodajRecept)
            self.lekarCombo.grid(row=0, column=1, padx=5, pady=5)
            self.lekLabel = Label(self.toplevelDodajRecept, text="Lek:", font=FONT)
            self.lekLabel.grid(row=1, column=0, padx=5, pady=5)
            self.lekCombo = ttk.Combobox(self.toplevelDodajRecept)
            self.lekCombo.grid(row=1, column=1, padx=5, pady=5)
            self.kolicinaLabel = Label(self.toplevelDodajRecept, text="Kolicina:", font=FONT)
            self.kolicinaLabel.grid(row=2, column=0, padx=5, pady=5)
            self.kolicinaEntry = Entry(self.toplevelDodajRecept)
            self.kolicinaEntry.grid(row=2, column=1, padx=5, pady=5)
            self.izvestajLabel = Label(self.toplevelDodajRecept, text="Izvestaj:", font=FONT)
            self.izvestajLabel.grid(row=3, column=0, padx=5, pady=5)
            self.izvestajEntry = Entry(self.toplevelDodajRecept)
            self.izvestajEntry.grid(row=3, column=1, padx=5, pady=5)
            self.datumLabel = Label(self.toplevelDodajRecept, text="Datum:", font=FONT)
            self.datumLabel.grid(row=4, column=0, padx=5, pady=5)
            self.datumEntry = Entry(self.toplevelDodajRecept)
            self.datumEntry.grid(row=4, column=1, padx=5, pady=5)
            self.prihvatiReceptButton = Button(self.toplevelDodajRecept, text="Prihvati", command=self.toplevel_dodaj_recept_prihvati)
            self.prihvatiReceptButton.grid(row=5, column=0, padx=10, pady=10)
            self.odbaciReceptButton = Button(self.toplevelDodajRecept, text="Odbaci", command=self.toplevel_dodaj_recept_odbaci)
            self.odbaciReceptButton.grid(row=5, column=1, padx=10, pady=10)
        
            self.lekarCombo['values'] = tuple(lekari)
            self.lekarCombo.current(0)
            self.lekCombo['values'] = tuple(lekovi)
            self.lekCombo.current(0)

            self.toplevelDodajRecept.grab_set()

    def toplevel_dodaj_recept_prihvati(self):
        selektovaniPacijentIndex = self.pretragaPacijenataCombo.current()
        selektovaniLekarIndex = self.lekarCombo.current()
        selektovaniLekIndex = self.lekCombo.current()
        kolicina = int(self.kolicinaEntry.get()) if self.kolicinaEntry.get() != '' else 0
        izvestaj = self.izvestajEntry.get()
        datum = self.datumEntry.get()

        if self.validacija_podataka_recepta(selektovaniLekarIndex, selektovaniLekIndex, kolicina, datum):
            pacijent = self.spisakPacijenata[selektovaniPacijentIndex - 1]
            lekar = self.spisakLekara[selektovaniLekarIndex - 1]
            lek = self.spisakLekova[selektovaniLekIndex - 1]

            novirecept = Recept(pacijent=pacijent, datum=datum, izvestaj=izvestaj, lekar=lekar, lek=lek, kolicina=kolicina)

            BAZA_SADRZAJ["Recept"].append(novirecept.__str__())
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)

            self.osvezi_listu_recepata()
            self.popuni_listu_recepata()
            
            indexNovogRecepta = self.spisakRecepata.index(novirecept.__str__())
            self.spisakRecepataListBox.select_set(indexNovogRecepta)     

            self.prikazi_podatke_recepta()

            self.toplevelDodajRecept.destroy()

    def toplevel_dodaj_recept_odbaci(self):
        self.toplevelDodajRecept.destroy()

    def toplevel_izmeni_recept(self):
        indexTuple = self.spisakRecepataListBox.curselection()
        if indexTuple:
            index = indexTuple[0]
            self.stariRecept = self.spisakRecepata[index]
        
            self.spisakLekara = []
            lekari = [""]
            self.spisakLekova = []
            lekovi = [""]
        
            for lekar in BAZA_SADRZAJ["Lekar"]:
                self.spisakLekara.append(lekar)
                lekari.append(f'{lekar["Ime"]} {lekar["Prezime"]}')
        
            for lek in BAZA_SADRZAJ["Lek"]:
                self.spisakLekova.append(lek)
                lekovi.append(f'{lek["Naziv leka"]}')
            
            self.toplevelIzmeniRecept = Toplevel(self)
            self.toplevelIzmeniRecept.title("Novi recept")
            self.noviLekarLabel = Label(self.toplevelIzmeniRecept, text="Lekar:", font=FONT)
            self.noviLekarLabel.grid(row=0, column=0, padx=5, pady=5)
            self.noviLekarCombo = ttk.Combobox(self.toplevelIzmeniRecept)
            self.noviLekarCombo.grid(row=0, column=1, padx=5, pady=5)
            self.noviLekLabel = Label(self.toplevelIzmeniRecept, text="Lek:", font=FONT)
            self.noviLekLabel.grid(row=1, column=0, padx=5, pady=5)
            self.noviLekCombo = ttk.Combobox(self.toplevelIzmeniRecept)
            self.noviLekCombo.grid(row=1, column=1, padx=5, pady=5)
            self.novaKolicinaLabel = Label(self.toplevelIzmeniRecept, text="Kolicina:", font=FONT)
            self.novaKolicinaLabel.grid(row=2, column=0, padx=5, pady=5)
            self.novaKolicinaEntry = Entry(self.toplevelIzmeniRecept)
            self.novaKolicinaEntry.grid(row=2, column=1, padx=5, pady=5)
            self.noviIzvestajLabel = Label(self.toplevelIzmeniRecept, text="Izvestaj:", font=FONT)
            self.noviIzvestajLabel.grid(row=3, column=0, padx=5, pady=5)
            self.noviIzvestajEntry = Entry(self.toplevelIzmeniRecept)
            self.noviIzvestajEntry.grid(row=3, column=1, padx=5, pady=5)
            self.noviDatumLabel = Label(self.toplevelIzmeniRecept, text="Datum:", font=FONT)
            self.noviDatumLabel.grid(row=4, column=0, padx=5, pady=5)
            self.noviDatumEntry = Entry(self.toplevelIzmeniRecept)
            self.noviDatumEntry.grid(row=4, column=1, padx=5, pady=5)
            self.prihvatiIzmenuReceptaButton = Button(self.toplevelIzmeniRecept, text="Prihvati", command=self.toplevel_izmeni_recept_prihvati)
            self.prihvatiIzmenuReceptaButton.grid(row=5, column=0, padx=10, pady=10)
            self.odbaciIzmenuReceptButton = Button(self.toplevelIzmeniRecept, text="Odbaci", command=self.toplevel_izmeni_recept_odbaci)
            self.odbaciIzmenuReceptButton.grid(row=5, column=1, padx=10, pady=10)
        
            self.noviLekarCombo['values'] = tuple(lekari)
            self.noviLekarCombo.set(f'{self.stariRecept["Lekar"]["Ime"]} {self.stariRecept["Lekar"]["Prezime"]}')
            self.noviLekCombo['values'] = tuple(lekovi)
            self.noviLekCombo.set(f'{self.stariRecept["Lek"]["Naziv leka"]}')
            self.novaKolicinaEntry.insert(0, f'{self.stariRecept["Kolicina"]}')
            self.noviIzvestajEntry.insert(0, f'{self.stariRecept["Izvestaj"]}')
            self.noviDatumEntry.insert(0, f'{self.stariRecept["Datum"]}')

            self.toplevelIzmeniRecept.grab_set()

    def toplevel_izmeni_recept_prihvati(self):
        noviSelektovaniPacijentIndex = self.pretragaPacijenataCombo.current()
        noviSelektovaniLekarIndex = self.noviLekarCombo.current()
        noviSelektovaniLekIndex = self.noviLekCombo.current()
        novaKolicina = int(self.novaKolicinaEntry.get()) if self.novaKolicinaEntry.get() != '' else 0
        noviIzvestaj = self.noviIzvestajEntry.get()
        noviDatum = self.noviDatumEntry.get()

        if self.validacija_podataka_recepta(noviSelektovaniLekarIndex, noviSelektovaniLekIndex, novaKolicina, noviDatum):
            BAZA_SADRZAJ["Recept"].remove(self.stariRecept)

            noviPacijent = self.spisakPacijenata[noviSelektovaniPacijentIndex - 1]
            noviLekar = self.spisakLekara[noviSelektovaniLekarIndex - 1]
            noviLek = self.spisakLekova[noviSelektovaniLekIndex - 1]

            novirecept = Recept(pacijent=noviPacijent, datum=noviDatum, izvestaj=noviIzvestaj, lekar=noviLekar, lek=noviLek, kolicina=novaKolicina)

            BAZA_SADRZAJ["Recept"].append(novirecept.__str__())
            with open(BAZA_FAJL, 'w') as file:
                json.dump(BAZA_SADRZAJ, file, indent=4)

            self.osvezi_listu_recepata()
            self.popuni_listu_recepata()
            
            indexNovogRecepta = self.spisakRecepata.index(novirecept.__str__())
            self.spisakRecepataListBox.select_set(indexNovogRecepta)     

            self.prikazi_podatke_recepta()

            self.toplevelIzmeniRecept.destroy()

    def toplevel_izmeni_recept_odbaci(self):
        self.toplevelIzmeniRecept.destroy()

    def izbrisi_recept(self):
        if messagebox.askyesno(title="Potvrda", message="Bice obrisan selektovani recept!"):
            indexTuple = self.spisakRecepataListBox.curselection()
            if indexTuple:
                index = indexTuple[0]
                recept = self.spisakRecepata[index]

                BAZA_SADRZAJ["Recept"].remove(recept)
                with open(BAZA_FAJL, 'w') as file:
                    json.dump(BAZA_SADRZAJ, file, indent=4)
            
                self.osvezi_listu_recepata()
                self.popuni_listu_recepata()

    def osvezi_combo_polje_pacijenata(self):
        self.spisakPacijenata = []
        pacijenti = [""]
    
        for pacijent in BAZA_SADRZAJ["Pacijent"]:
            self.spisakPacijenata.append(pacijent)
            pacijenti.append(f'{pacijent["Ime"]} {pacijent["Prezime"]}')
            
        self.pretragaPacijenataCombo['values'] = tuple(pacijenti)
        self.pretragaPacijenataCombo.after(250, self.osvezi_combo_polje_pacijenata)

    def osvezi_listu_recepata(self, *args):
        self.spisakRecepata = []
        selektovaniPacijentIndex = self.pretragaPacijenataCombo.current()

        if selektovaniPacijentIndex != 0:
            pacijent = self.spisakPacijenata[selektovaniPacijentIndex - 1]
            for recept in BAZA_SADRZAJ["Recept"]:
                if recept["Pacijent"] == pacijent:
                    self.spisakRecepata.append(recept)
        
        self.popuni_listu_recepata()

    def popuni_listu_recepata(self, *args):
        self.spisakRecepataListBox.delete(0, END)
        self.podaciReceptaText.config(state=NORMAL)
        self.podaciReceptaText.delete(1.0, END)
        self.podaciReceptaText.config(state=DISABLED)
        
        for recept in self.spisakRecepata:
            self.spisakRecepataListBox.insert(self.spisakRecepata.index(recept), f'{recept["Lekar"]["Ime"]} - {recept["Lek"]["Naziv leka"]}')

    def prikazi_podatke_recepta(self, *args):
        text = ""

        indexTuple = self.spisakRecepataListBox.curselection()
        if indexTuple:
            index = indexTuple[0]
            recept = self.spisakRecepata[index]
            text += (
                f'Pacijent:\n\tIme: {recept["Pacijent"]["Ime"]}\n\tPrezime: {recept["Pacijent"]["Prezime"]}\n\tLBO: {recept["Pacijent"]["LBO"]}\n'
                f'Lekar:\n\tIme: {recept["Lekar"]["Ime"]}\n\tPrezime: {recept["Lekar"]["Prezime"]}\n\tJMBG: {recept["Lekar"]["JMBG"]}\n'
                f'Lek:\n\tNaziv: {recept["Lek"]["Naziv leka"]}\n\tProizvodjac: {recept["Lek"]["Proizvodjac leka"]}\n\tJKL: {recept["Lek"]["Sifra JKL"]}\n'
                f'Kolicina: {recept["Kolicina"]}\n'
                f'Izvestaj: {recept["Izvestaj"]}\n'
                f'Datum: {recept["Datum"]}'
            )
            
        self.podaciReceptaText.config(state=NORMAL)
        self.podaciReceptaText.delete(1.0, END)
        self.podaciReceptaText.insert(INSERT, text)
        self.podaciReceptaText.config(state=DISABLED)
        self.izmeniReceptButton.config(state=NORMAL)
        self.obrisiReceptButton.config(state=NORMAL)

    def validacija_podataka_recepta(self, lekarIndex, lekIndex, kolicina, datum):
        oblikDatuma = r"^(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](\d\d\d\d)"

        if lekarIndex == 0:
            messagebox.showerror("Error", "Selektujte lekara")
        elif lekIndex == 0:
            messagebox.showerror("Error", "Selektujte lek")
        elif kolicina < 1:
            messagebox.showerror("Error", "Kolicina mora biti veca od 1")
        elif not re.match(oblikDatuma, datum):
            messagebox.showerror("Error", "Datum mora biti u formatu dd.MM.yyyy")
        elif date(int(datum.split('.')[2]), int(datum.split('.')[1]), int(datum.split('.')[0])) > datetime.now().date():
            messagebox.showerror("Error", "Datum moze biti najkasnije danasnji")
        else:
            return True










if __name__ == "__main__":

    if not os.path.isfile('data.json'):
        BAZA_SADRZAJ = {}
        BAZA_SADRZAJ['Pacijent'] = []
        BAZA_SADRZAJ['Lekar'] = []
        BAZA_SADRZAJ['Lek'] = []
        BAZA_SADRZAJ['Recept'] = []

        with open(BAZA_FAJL, 'w') as file:
            json.dump(BAZA_SADRZAJ, file, indent=4)

    else:
        with open(BAZA_FAJL) as file:
            BAZA_SADRZAJ = json.load(file)
        
        if BAZA_SADRZAJ["Pacijent"]:
            BAZA_SADRZAJ["Pacijent"].sort(key=itemgetter("Prezime", "Ime"))

        if BAZA_SADRZAJ["Lekar"]:
            BAZA_SADRZAJ["Lekar"].sort(key=itemgetter("Prezime", "Ime"))

        if BAZA_SADRZAJ["Lek"]:
            BAZA_SADRZAJ["Lek"].sort(key=itemgetter("Naziv leka"))

    app = MyApp()
    app.title("Apoteka")
    app.mainloop()