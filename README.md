# Projekat Apoteka

Implementirati **Python** graficku aplikaciju za rad apoteke. Koristiti sledece biblioteke:

- Tkinter
- NumPy
- pickle ili json

Aplikacija rukuje sledecim elementima:

- Korisnik:

  - JMBG (***jedinstven***, 13 karaktera)
  - Ime (bar 2 karaktera)
  - Prezime (bar 2 karaktera)
  - Datum rodjenja (klasa ***date***, najkasnije tekuci datum)

- Pacijent - nasledjuje klasu **Korisnik** i definise sledece atribute:

  - LBO (***jedinstven***, 11 karaktera)
  - Recepti (povezani podaci)

- Lekar - nasledjuje klasu **Korisnik** i definise sledece atribute):

  - Specijalizacija (bar 2 karaktera)
  - Recepti (povezani podaci)

- Lek:
  
  - Sifra jedinstvene klasifikacije leka (***jedinstvena***, 7 karaktera)
  - Naziv (bar 2 karaktera)
  - Proizvodjac (bar 2 karaktera)
  - Tip leka (bar 2 karaktera)
  - Recepti (povezani podaci)

- Recept:

  - Pacijent (povezani podatak)
  - Datum i vreme (klasa ***datetime***, najkasnije tekuci datum)
  - Izvestaj
  - Lekar (povezani podatak)
  - Lek (povezani podatak)
  - Kolicina (numericki podatak veci od 0)

**Glavni prozor** aplikacije treba da kroz meni omoguci **izlaz iz aplikacije** u jednom podmeniju, a **pristup prozoru sa pacijentima, prozoru sa lekarima, prozoru sa receptima i prozoru sa lekovima** u drugom podmeniju.

- [x] Svi prozori aplikacije treba da su **modalni**.
- [x] Pri unosu i izmeni podataka treba implementirati zastitu unosa od nevalidnih podataka u
odnosu na ogranicenja. Potrebno je spreciti unos, odnosno izmenu, ukoliko bilo koji podatak nije validan, a o tome obavestiti korisnika.
- [x] Za unos i izmenu datuma, odnosno datuma i vremena upotrebiti jedno od sledeceg:
  - Entry („dd.MM.yyyy.“ za datum, odnosno „dd.MM.yyyy. HH:mm“ za datum i vreme)
  - 3 Spinbox-a (dan, mesec, godina) za datum, odnosno 5 Spinbox-a (dan, mesec, godina, sati minuti) za datum i vreme
  - Pronaci modul(e) koji implementira(ju) widget(e) za odabir datuma, odnosno
vremena i ukljuciti ih projekat

**Pri pokretanju resenje treba da ima ucitanog bar 1 pacijenta, 1 lekara, 2 leka i 2 recepta.**

---

## Pacijenti

- [x] Prikaz liste svih pacijenata sortiranih u rastucem redosledu prezimena, pa imena, koji odgovaraju pretrazi koja se vrsi uz pomoc sadrzaja tekstualnog polja iznad prikazane liste.

- [x] Promena sadrzaja tekstualnog polja automatski treba da izvrsi osvezavanje pretrage. Pretraga se vrsi po poklapanju dela imena ili prezimena pacijenta pri cemu se ignorsu razlike izmedju velikih i malih slova. Prazan sadrzaj tekstualnog polja za pretragu treba obuhvati sve pacijente.

- [x] Pored prikazane liste pacijenata treba prikazati podatke o obelezenom pacijentu, pri cemu njihova izmena u ovom prozoru nije moguca.

- [x] ***Treba omoguciti komandu za dodavanje pacijenta.***

- [x] Prozor za dodavanje pacijenta treba da omoguci unos svih podataka pacijenta Recepti pacijenta se ne dodaju u ovom prozoru.

- [x] Treba omoguciti komandu za povratak iz prozora za dodavanje pacijenta.

- [x] Treba omoguciti komandu za potvrdu unosa.

- [x] Po potvrdi unosa treba sacuvati podatke, osveziti pretragu po svim pacijentima i automatski isprazniti polje za pretragu u prozoru sa pacijentima. Pri cemu dodati pacijent treba da je obelezen u listi i prikazan pored nje.

- [x] ***Treba omoguciti komandu za izmenu pacijenta.***

- [x] Prozor za izmenu pacijenta treba da omoguci unos svih podataka pacijenta na isti nacin kao i prozor za dodavanje pacijenta, osim izmene LBO-a i JMBG-a koju treba onemoguciti (LBO i JMBG ipak treba da se vide). Recepti pacijenta se ne menjaju u ovom prozoru.

- [x] Treba omoguciti komandu za povratak iz prozora za izmenu pacijenta.

- [x] Treba omoguciti komandu za potvrdu izmene pacijenta. 

- [x] Po potvrdi izmene treba sacuvati podatke i osveziti pretragu po svim pacijentima (i automatski isprazniti polje za pretragu) u prozoru sa pacijentima, pri cemu dodati pacijent treba da je obelezen u listi i prikazan pored nje.

- [x] ***Treba omoguciti komandu za brisanje pacijenta.***

- [x] Brisanjem pacijenta se brisu svi njegovi recepti. Pri brisanju treba traziti potvrdu od korisnika da je siguran da zeli da izvrsi brisanje, uz upozorenje da ce time biti izbrisana i svi recepti pacijenta.

- [x] ***Treba omoguciti i komandu za prikaz recepata obelezenog pacijenta.***

- [x] Treba omoguciti komandu za povratak koja zatvara prozor za prikaz recepata.

- [x] **Komande za izmenu i brisanje obelezenog pacijenta treba da su onemogucene ukoliko u listi nije obelezen nijedan pacijent.**

---

## Lekari

- [x] Prikaz liste svih lekara sortiranih u rastucem redosledu prezimena, pa imena, koji odgovaraju pretrazi koja se vrsi uz pomoc sadrzaja tekstualnog polja iznad prikazane liste.

- [x] Promena sadrzaja tekstualnog polja automatski treba da izvrsi osvezavanje pretrage. Pretraga se vrsi po poklapanju dela imena ili prezimena lekara pri cemu se ignorsu razlike izmedju velikih i malih slova. Prazan sadrzaj tekstualnog polja za pretragu treba obuhvati sve lekare.

- [x] Pored prikazane liste lekara treba prikazati podatke o obelezenom lekaru, pri cemu njihova izmena u ovom prozoru nije moguca.

- [x] ***Treba omoguciti komandu za dodavanje lekara.***

- [x] Prozor za dodavanje lekara treba da omoguci unos svih podataka lekara. Recepti lekara se ne dodaju u ovom prozoru.

- [x] Treba omoguciti komandu za povratak iz prozora za dodavanje lekara.

- [x] Treba omoguciti komandu za potvrdu unosa.

- [x] Po potvrdi unosa treba sacuvati podatke, osveziti pretragu po svim lekarima i automatski isprazniti polje za pretragu u prozoru sa lekarima. Pri cemu dodati lekar treba da je obelezen u listi i prikazan pored nje.

- [x] ***Treba omoguciti komandu za izmenu lekara.***

- [x] Prozor za izmenu lekara treba da omoguci unos svih podataka lekara na isti nacin kao i prozor za dodavanje lekara, osim izmene JMBG-a koju treba onemoguciti (JMBG ipak treba da se vidi). Recepti pacijen se ne menjaju u ovom prozoru.

- [x] Treba omoguciti komandu za povratak iz prozora za izmenu lekara.

- [x] Treba omoguciti komandu za potvrdu izmene lekara.

- [x] Po potvrdi izmene treba sacuvati podatke i osveziti pretragu po svim lekarima (i automatski isprazniti polje za pretragu) u prozoru sa lekarima, pri cemu dodati lekar treba da je obelezen u listi i prikazan pored nje.

- [x] ***Treba omoguciti komandu za brisanje lekara.***

- [x] Brisanjem lekara se brisu svi njegovi recepti. Pri brisanju treba traziti potvrdu od korisnika da je siguran da zeli da izvrsi brisanje, uz upozorenje da ce time biti izbrisana i svi recepti lekara.

- [x] ***Treba omoguciti i komandu za prikaz recepata obelezenog lekara.***

- [x] Treba omoguciti komandu za povratak koja zatvara prozor za prikaz recepata.

- [x] **Komande za izmenu i brisanje obelezenog lekara treba da su onemogucene ukoliko u listi nije obelezen nijedan lekar.**

---

## Lekovi

- [x] Prikaz liste svih lekova sortiranih u rastucem redosledu naziva, koji odgovaraju pretrazi koja se vrsi uz pomoc sadrzaja tekstualnog polja iznad prikazane liste.

- [x] Promena sadrzaja tekstualnog polja automatski treba da izvrsi osvezavanje pretrage. Pretraga se vrsi po poklapanju dela naziva leka pri cemu se ignorsu razlike izmedju velikih i malih slova. Prazan sadrzaj tekstualnog polja za pretragu treba obuhvati sve lekove.

- [x] Pored prikazane liste lekova treba prikazati podatke o obelezenom leku, pri cemu njihova izmena u ovom prozoru nije moguca.

- [x] ***Treba omoguciti komandu za dodavanje lekova.***

- [x] Prozor za dodavanje lekova treba da omoguci unos svih podataka leka.

- [x] Treba omoguciti komandu za povratak iz prozora za dodavanje leka.

- [x] Treba omoguciti komandu za potvrdu unosa.

- [x] Po potvrdi unosa treba sacuvati podatke, osveziti pretragu po svim lekovima i automatski isprazniti polje za pretragu u prozoru sa lekovima. Pri cemu dodati lek treba da je obelezen u listi i prikazan pored nje.

- [x] ***Treba omoguciti komandu za izmenu lekova.***

- [x] Prozor za izmenu leka treba da omoguci unos svih podataka leka na isti nacin kao i prozor za dodavanje leka, osim izmene JKL-a koju treba onemoguciti (JKL ipak treba da se vidi).

- [x] Treba omoguciti komandu za povratak iz prozora za izmenu leka.

- [x] Treba omoguciti komandu za potvrdu izmene leka.

- [x] Po potvrdi izmene treba sacuvati podatke i osveziti pretragu po svim lekovima (i automatski isprazniti polje za pretragu) u prozoru sa lekovima, pri cemu dodati lek treba da je obelezen u listi i prikazan pored nje.

- [x] ***Treba omoguciti komandu za brisanje leka.***

- [x] Brisanjem leka se brisu svi njegovi recepti. Pri brisanju treba traziti potvrdu od korisnika da je siguran da zeli da izvrsi brisanje, uz upozorenje da ce time biti izbrisana i svi recepti leka.

- [x] **Komande za izmenu i brisanje obelezenog lekara treba da su onemogucene ukoliko u listi nije obelezen nijedan lekar.**

---

## Recepti

- [x] Prikaz liste svih recepata za pacijenta odabranog u combo-boxu iznad same liste. 

- [x] Promena sadrzaja combo-boxa automatski treba da izvrsi osvezavanje liste.

- [x] Pored prikazane liste recepara treba prikazati podatke o obelezenom receptu, pri cemu njihova izmena u ovom prozoru nije moguca.

- [x] ***Treba omoguciti komandu za dodavanje recepta.***

- [x] Prozor za dodavanje recepta treba da omoguci unos svih ostalih podataka o receptu dok pacijent za koga se pise recept treba da bude bas onaj koji je odabran u combo-boxu.

- [x] Treba omoguciti komandu za povratak iz prozora za dodavanje recepta.

- [x] Treba omoguciti komandu za potvrdu unosa.

- [x] Po potvrdi unosa treba sacuvati podatke i osveziti pretragu po odabranom pacijentu u prozoru sa receptima.

- [x] ***Treba omoguciti komandu za izmenu recepata.***

- [x] Prozor za izmenu recepta treba da omoguci unos svih podataka recepta na isti nacin kao
i prozor za dodavanje recepta.

- [x] Treba omoguciti komandu za povratak iz prozora za izmenu recepta.

- [x] Treba omoguciti komandu za potvrdu izmene leka.

- [x] Po potvrdi izmene treba sacuvati podatke i osveziti pretragu po odabranom pacijentu u prozoru sa receptima.

- [x] ***Treba omoguciti komandu za brisanje recepta.***

- [x] Brisanjem recepta se ne brisu nijedni povezani podaci. Pri brisanju treba traziti potvrdu od korisnika da je siguran da zeli da izvrsi brisanje.

- [x] **Komande za izmenu i brisanje obelezenog pacijenta treba da su onemogucene ukoliko u listi nije obelezen nijedan pacijent, dok komanda za dodavanje treba da je onemogucena sve dok nije odabran pacijent u combo-boxu.**