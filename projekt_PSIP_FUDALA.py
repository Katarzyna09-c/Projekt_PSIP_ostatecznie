
# IMPORT POTRZEBNYCH BIBLIOTEK DO ZROBIENIA PROJEKTU ####################

import psycopg2 as ps
import requests as rq
from tkinter import *
from tkintermapview import TkinterMapView
from bs4 import BeautifulSoup


# POŁĄCZENIE Z BAZĄ DANYCH W POSTGRES ###########################
db_params = ps.connect(
    database='postgres',
    user='postgres',
    password='psip2023',
    host='localhost',
    port=5432
)
cursor = db_params.cursor()



# -------NADAWANIE NUMERU ID W STWORZONYCH TABELACH-------- ###########################

def id_dodawanie_biura():
    sql_query = "SELECT id FROM public.biura ORDER BY id ASC;"
    cursor.execute(sql_query)
    query_result = cursor.fetchall()

    index = [row[0] for row in query_result]
    new_id = 1 if not index else max(index) + 1

    return int(new_id)

def id_dodawanie_hotele():
    sql_query = "SELECT id FROM public.hotele ORDER BY id ASC;"
    cursor.execute(sql_query)
    query_result = cursor.fetchall()

    index = [row[0] for row in query_result]
    new_id = 1 if not index else max(index) + 1

    return int(new_id)

def id_dodawanie_pracownicy():
    sql_query = "SELECT id FROM public.pracownicy ORDER BY id ASC;"
    cursor.execute(sql_query)
    query_result = cursor.fetchall()

    index = [row[0] for row in query_result]
    new_id = 1 if not index else max(index) + 1

    return int(new_id)

# --------------DODAWANIE---------- ###################################


# ------------AKTUALIZACJA NUMERU ID W STWORZONYCH TABELACH------- #########################

def id_aktualizacja_biura():
    # Pobranie aktualnych danych z bazy danych
    sql_query_select = "SELECT id FROM public.biura ORDER BY id ASC;"
    cursor.execute(sql_query_select)
    query_result = cursor.fetchall()

    id_list = [row[0] for row in query_result]

    # Aktualizacja ID w bazie danych
    for numer, id in enumerate(id_list, start=1):
        sql_query_update = f"UPDATE public.biura SET id='{numer}' WHERE id='{id}';"
        cursor.execute(sql_query_update)
        db_params.commit()



def id_aktualizacja_hotele():
    # Pobranie aktualnych danych z bazy danych
    sql_query_select = "SELECT id FROM public.hotele ORDER BY id ASC;"
    cursor.execute(sql_query_select)
    query_result = cursor.fetchall()

    id_list = [row[0] for row in query_result]

    # Aktualizacja ID w bazie danych
    for numer, id in enumerate(id_list, start=1):
        sql_query_update = f"UPDATE public.hotele SET id='{numer}' WHERE id='{id}';"
        cursor.execute(sql_query_update)
        db_params.commit()



def id_aktualizacja_pracownicy():
    # Pobranie aktualnych danych z bazy danych
    sql_query_select = "SELECT id FROM public.pracownicy ORDER BY id ASC;"
    cursor.execute(sql_query_select)
    query_result = cursor.fetchall()

    id_list = [row[0] for row in query_result]

    # Aktualizacja ID w bazie danych
    for numer, id in enumerate(id_list, start=1):
        sql_query_update = f"UPDATE public.pracownicy SET id='{numer}' WHERE id='{id}';"
        cursor.execute(sql_query_update)
        db_params.commit()


# ------------AKTUALIZACJA----------------- ###############################


# ------------LOKALIZACJA----------------- ##################

def wspolrzedne(miejscowosc) -> list[float, float]:
    # pobranie strony internetowe
    adres_URL = f'https://pl.wikipedia.org/wiki/{miejscowosc}'
    response = rq.get(url=adres_URL)
    response_html = BeautifulSoup(response.text, 'html.parser')

    # pobranie współrzędnych z treści strony internetowej
    response_html_latitude = response_html.select('.latitude')[1].text  # .  class
    response_html_latitude = float(response_html_latitude.replace(',', '.'))
    response_html_longitude = response_html.select('.longitude')[1].text  # .  class
    response_html_longitude = float(response_html_longitude.replace(',', '.'))

    return [response_html_latitude, response_html_longitude]

# -----------LOGOWANIE DO SYSTEMU------------------- #################

def logowanie_do_systemu(event=None):

    haslo = wpisz_haslo.get()
    if haslo=='podroze3':

# DEfINIOWNIE WYGLĄDU RAMEK ################################

        root_okienko = Toplevel(okienko_logowanie)
        root_okienko.title('Sieć biur podróży')
        root_okienko.state('zoomed')

        root_biura=Frame(root_okienko)
        root_biura.grid(row=0, column=0)

        root_hotele = Frame(root_okienko)
        root_hotele.grid(row=1, column=0)

        root_pracownicy = Frame(root_okienko)
        root_pracownicy.grid(row=0, column=1)

        ramka_mapa = Frame(root_okienko)
        ramka_mapa.grid(row=1, column=1, columnspan=2, sticky=N)



# DEFINIOWANIE FUNKCJI W RAMCE MAPA ###############################


        def mapa_biura():
            #Pobranie danych biur z bazy danych
            sql_query = f"SELECT * FROM public.biura ORDER BY id ASC;"
            cursor.execute(sql_query)
            query_result = cursor.fetchall()

            #Wygląd mapy
            mapa = TkinterMapView(ramka_mapa, width=700, height=300, corner_radius=0)
            mapa.set_position(52.1, 19.4)
            mapa.set_zoom(6)
            mapa.grid(row=7, column=0, columnspan=3, pady=(5, 0))

            #Dodawanie markerów na mapie dla każdego biura
            for wiersz in query_result:
                biuro = wspolrzedne(wiersz[2])
                mapa.set_marker(biuro[0], biuro[1], text=f'{wiersz[1]}', font=('Times New Roman', 12), text_color='black')


        def mapa_pracowicy():
            #Pobieranie danych pracowników z dazy danych
            sql_query = f"SELECT * FROM public.pracownicy ORDER BY id ASC;"
            cursor.execute(sql_query)
            query_result = cursor.fetchall()

            #Wygląd mapy
            mapa = TkinterMapView(ramka_mapa, width=700, height=300, corner_radius=0)
            mapa.set_position(52.1, 19.4)
            mapa.set_zoom(6)
            mapa.grid(row=7, column=0, columnspan=3, pady=(10, 0))

            #Dodawanie markerów na mapie dla każdego pracownika
            for wiersz in query_result:
                pracownicy = wspolrzedne(wiersz[3])
                mapa.set_marker(pracownicy[0], pracownicy[1], text=f'{wiersz[1]} {wiersz[2]}', font=('Times New Roman', 12), text_color='black')


        def mapa_pracowicy_z_biura():
            #Pobranie nazwy biura
            biuro = entry_mapa_prac_biuro.get()

            #Zapytanie o pracowników przypisanych do danego biura
            sql_query = f"SELECT * FROM public.pracownicy WHERE biuro='{biuro}' ORDER BY id ASC;"
            cursor.execute(sql_query)
            query_result = cursor.fetchall()

            #Wygląd mapy
            mapa = TkinterMapView(ramka_mapa, width=700, height=300, corner_radius=0)
            mapa.set_position(52.1, 19.4)
            mapa.set_zoom(6)
            mapa.grid(row=7, column=0, columnspan=3, pady=(10, 0))

            #Dodawanie markerów na mapie dla każdego pracownika z danego biura
            for wiersz in query_result:
                prac_z_biura = wspolrzedne(wiersz[3])
                mapa.set_marker(prac_z_biura[0], prac_z_biura[1], text=f'{wiersz[1]} {wiersz[2]}', font=('Times New Roman', 12), text_color='black')


        def mapa_hotele_z_biura():
            #Pobranie nazwy biura
            biuro = entry_mapa_hotele_biuro.get()

            #Zapytanie o hotele przypisane do danego biura
            sql_query = f"SELECT * FROM public.hotele WHERE biuro='{biuro}' ORDER BY id ASC;"
            cursor.execute(sql_query)
            query_result = cursor.fetchall()

            #Wygląd mapy
            mapa = TkinterMapView(ramka_mapa, width=700, height=300, corner_radius=0)
            mapa.set_position(52.1, 19.4)
            mapa.set_zoom(6)
            mapa.grid(row=7, column=0, columnspan=3, pady=(10, 0))

            #Dodawanie markerów na mapie dla każdego hotelu z danego biura
            for wiersz in query_result:
                hotel_z_biura = wspolrzedne(wiersz[2])
                mapa.set_marker(hotel_z_biura[0], hotel_z_biura[1], text=f'{wiersz[1]}', font=('Times New Roman', 12), text_color='black')



        # DEFINIOWANIE WYGLĄDU RAMKI MAPY #################################################

        label_mapa_start = Label(ramka_mapa, text='Mapy', font=('Times New Roman', 14))
        label_mapa_start.grid(row=0, column=0, columnspan=3, pady=(10, 0))

        label_mapa_biura = Label(ramka_mapa, text='Mapa wszystkich biur podróży')
        label_mapa_biura.grid(row=1, column=0, sticky=W)

        button_mapa_biura = Button(ramka_mapa, text='Wyświetl', command=mapa_biura)
        button_mapa_biura.grid(row=1, column=1, sticky=E)

        label_mapa_pracownicy = Label(ramka_mapa, text='Mapa wszystkich pracowników')
        label_mapa_pracownicy.grid(row=2, column=0, sticky=W)

        button_mapa_pracownicy = Button(ramka_mapa, text='Wyświetl', command=mapa_pracowicy)
        button_mapa_pracownicy.grid(row=2, column=1, sticky=E)

        label_mapa_prac_biura_start = Label(ramka_mapa, text='Mapa pracowników biura')
        label_mapa_prac_biura_start.grid(row=3, column=0, sticky=W)

        label_mapa_prac_biuro = Label(ramka_mapa, text='Biuro')
        label_mapa_prac_biuro.grid(row=4, column=0, sticky=W)

        entry_mapa_prac_biuro = Entry(ramka_mapa)
        entry_mapa_prac_biuro.grid(row=4, column=1, sticky=E)

        button_mapa_prac_biuro = Button(ramka_mapa, text='Wyświetl', command=mapa_pracowicy_z_biura)
        button_mapa_prac_biuro.grid(row=3, column=1, sticky=E)

        label_mapa_hotele_biuro_start = Label(ramka_mapa, text='Mapa hopateli współpracujących z biurem')
        label_mapa_hotele_biuro_start.grid(row=5, column=0, sticky=W)

        label_mapa_hotele_biuro = Label(ramka_mapa, text='Biuro')
        label_mapa_hotele_biuro.grid(row=6, column=0, sticky=W)

        entry_mapa_hotele_biuro = Entry(ramka_mapa)
        entry_mapa_hotele_biuro.grid(row=6, column=1, sticky=E)

        button_mapa_hotele_biuro = Button(ramka_mapa, text='Wyświetl', command=mapa_hotele_z_biura)
        button_mapa_hotele_biuro.grid(row=5, column=1, sticky=E)



#DEFINICJA FUNKCJI RAMKI BIURA ##########################
        def biura_wyswietl():
            #Wyczyszczenie zawartości listbox przed wyświetleniem nowych danych
            listbox_biura.delete(0, END)

            #Zapytanie o dane biur
            sql_query = f"SELECT * FROM public.biura ORDER BY id ASC;"
            cursor.execute(sql_query)
            query_result = cursor.fetchall()

            #Wyświetlenie danych
            for index, wiersz in enumerate(query_result):
                listbox_biura.insert(index, f'Biuro: {wiersz[1]}')

            id_aktualizacja_biura()


        def biura_dodaj():
            #Pobranie danych
            nazwa=entry_biura_nazwa.get()
            miasta=entry_biura_miasta.get()
            przychod=entry_biura_przychod.get()

            # Generowanie nowego ID
            new_id = id_dodawanie_biura()

            # Zapytanie do dodania nowego biura
            sql_query = f"INSERT INTO public.biura(id, nazwa, miasta, przychod) VALUES ('{new_id}', '{nazwa}', '{miasta}', '{przychod}');"

            # Wykonanie zapytania i zatwierdzenie zmian w bazie danych
            cursor.execute(sql_query)
            db_params.commit()

            # Wyczyszczenie pól po dodaniu biura
            entry_biura_nazwa.delete(0, END)
            entry_biura_miasta.delete(0, END)
            entry_biura_przychod.delete(0, END)

            # Wywołanie funkcji
            biura_wyswietl()


        def biura_edytuj():
            # Pobranie danych
            sql_query = "SELECT * FROM public.biura ORDER BY id ASC;"
            cursor.execute(sql_query)
            query_result = cursor.fetchall()

            # Pobranie indeksu zaznaczonego elementu w listbox
            i = listbox_biura.index(ACTIVE)

            # Wyczyszczenie pól
            entry_biura_nazwa.delete(0, END)
            entry_biura_miasta.delete(0, END)
            entry_biura_przychod.delete(0, END)

            # Wypełnienie pól danymi zaznaczonego biura
            entry_biura_nazwa.insert(0, query_result[i][1])
            entry_biura_miasta.insert(0, query_result[i][2])
            entry_biura_przychod.insert(0, query_result[i][3])

            # Zmiana tekstu na przycisku i przypisanie nowej funkcji
            button_biura_dodaj.config(text='Zapisz zmiany', command=lambda: biura_aktualizuj(i))


        def biura_aktualizuj(i):
            # Pobranie danych
            sql_query_select = "SELECT * FROM public.biura ORDER BY id ASC;"
            cursor.execute(sql_query_select)
            query_result = cursor.fetchall()

            # Pobranie nowych danych z pól
            nazwa = entry_biura_nazwa.get()
            miasta = entry_biura_miasta.get()
            przychod = entry_biura_przychod.get()

            # Zapytanie do aktualizacji danych w bazie
            sql_query_update = f"UPDATE public.biura SET nazwa='{nazwa}', miasta='{miasta}', przychod='{przychod}' WHERE nazwa='{query_result[i][1]}' and miasta='{query_result[i][2]}' and przychod='{query_result[i][3]}';"
            cursor.execute(sql_query_update)
            db_params.commit()

            # Przywrócenie pierwotnego tekstu przycisku i przypisanie pierwotnej funkcji
            button_biura_dodaj.config(text='Dodaj biuro', command=biura_dodaj)

            # Wyczyszczenie pól
            entry_biura_nazwa.delete(0, END)
            entry_biura_miasta.delete(0, END)
            entry_biura_przychod.delete(0, END)

            # Odświeżenie wyświetlania danych
            biura_wyswietl()

        def biura_usun():
            # Pobranie indeksu zaznaczonego elementu w listbox
            i = listbox_biura.index(ACTIVE)

            # Zapytanie o usunięcie biura z bazy danych
            sql_query_1 = f"DELETE FROM public.biura WHERE id='{i+1}';"
            cursor.execute(sql_query_1)
            db_params.commit()

            # Odświeżenie wyświetlania danych
            biura_wyswietl()

        def biura_pokaz():
            #Pobieranie danych
            sql_query_1 = f"SELECT * FROM public.biura ORDER BY id ASC;"
            cursor.execute(sql_query_1)
            query_result = cursor.fetchall()

            # Pobranie indeksu zaznaczonego elementu w listbox
            i = listbox_biura.index(ACTIVE)

            # Pobranie danych biura z listy
            nazwa=query_result[i][1]
            miasto=query_result[i][2]
            przychod=query_result[i][3]

            # Aktualizacja etykiet w ramce szczegółów
            label_biura_nazwa_szczegoly_wartosc.config(text=nazwa)
            label_biura_miasto_szczegoly_wartosc.config(text=miasto)
            label_biura_przychod_szczegoly_wartosc.config(text=przychod)

        #Wygląd ramki
        ramka_biura_nazwa = Frame(root_biura)
        ramka_biura_nazwa.grid(row=0, column=0, columnspan=2)

        ramka_biura_lista = Frame(root_biura)
        ramka_biura_lista.grid(row=1, column=1)

        ramka_biura_wpisywanie = Frame(root_biura)
        ramka_biura_wpisywanie.grid(row=1, column=0)

        ramka_biura_szczegoly = Frame(root_biura)
        ramka_biura_szczegoly.grid(row=2, column=0, columnspan=2)


        # Wygląd ramki biura_nazwa #########################

        label_biura_lista = Label(ramka_biura_nazwa,
                                 text='Lista biur podróży', font=('Times New Roman', 14))

        label_biura_lista.grid(row=0, column=0, pady=(10, 0), padx=10, sticky="w")


        # Wygląd ramki biura_lista #############################

        button_pokaz_liste = Button(ramka_biura_lista, text='Wyświetl', command=biura_wyswietl)
        button_pokaz_liste.grid(row=0, column=0, columnspan=3)

        listbox_biura = Listbox(ramka_biura_lista, width=50, height=5)
        listbox_biura.grid(row=1, column=0, columnspan=3, pady=(10, 0))

        button_biura_szczegoly = Button(ramka_biura_lista, text='Wyświetl szczegóły', command=biura_pokaz)
        button_biura_szczegoly.grid(row=2, column=0)

        button_biura_usun = Button(ramka_biura_lista, text='Usuń rekord', command=biura_usun)
        button_biura_usun.grid(row=2, column=1)

        button_biura_edytuj = Button(ramka_biura_lista, text='Edytuj rekord', command=biura_edytuj)
        button_biura_edytuj.grid(row=2, column=2)


        #Wygląd ramki biura_wpisywanie ################################

        label_biura_nowy = Label(ramka_biura_wpisywanie, text='Edycja i dodawanie:', font=('Times New Roman', 12))
        label_biura_nowy.grid(row=0, column=0, columnspan=2)

        label_biura_nazwa = Label(ramka_biura_wpisywanie, text='Nazwa biura')
        label_biura_nazwa.grid(row=1, column=0, sticky=W)

        label_biura_miasta = Label(ramka_biura_wpisywanie, text='Siedziba biura')
        label_biura_miasta.grid(row=2, column=0, sticky=W)

        label_biura_przychod = Label(ramka_biura_wpisywanie, text='Przychód biura')
        label_biura_przychod.grid(row=3, column=0, sticky=W)

        #Wygląd pól do wpisywania
        entry_biura_nazwa = Entry(ramka_biura_wpisywanie)
        entry_biura_nazwa.grid(row=1, column=1, sticky=W)

        entry_biura_miasta = Entry(ramka_biura_wpisywanie)
        entry_biura_miasta.grid(row=2, column=1, sticky=W)

        entry_biura_przychod = Entry(ramka_biura_wpisywanie)
        entry_biura_przychod.grid(row=3, column=1, sticky=W)

        #Przycisk do dodawania rekordu
        button_biura_dodaj = Button(ramka_biura_wpisywanie, text='Dodaj rekord', command=biura_dodaj)
        button_biura_dodaj.grid(row=4, column=0, columnspan=2)


        # Wygląd ramki biura_szczegoly

        label_biura_opis_obiektu = Label(ramka_biura_szczegoly, text='Szczegóły biura podróży:', font=('Times New Roman', 12))
        label_biura_opis_obiektu.grid(row=0, column=0, columnspan=8, pady=10)

        label_biura_nazwa_szczegoly = Label(ramka_biura_szczegoly, text='Nazwa:')
        label_biura_nazwa_szczegoly.grid(row=1, column=0)


        label_biura_nazwa_szczegoly_wartosc = Label(ramka_biura_szczegoly, text=' ', width=15)
        label_biura_nazwa_szczegoly_wartosc.grid(row=2, column=0)

        label_biura_miasto_szczegoly = Label(ramka_biura_szczegoly, text='Miasto:')
        label_biura_miasto_szczegoly.grid(row=1, column=1)

        label_biura_miasto_szczegoly_wartosc = Label(ramka_biura_szczegoly, text=' ', width=15)
        label_biura_miasto_szczegoly_wartosc.grid(row=2, column=1)

        label_biura_przychod_szczegoly = Label(ramka_biura_szczegoly, text='Przychód:')
        label_biura_przychod_szczegoly.grid(row=1, column=2)

        label_biura_przychod_szczegoly_wartosc = Label(ramka_biura_szczegoly, text=' ', width=15)
        label_biura_przychod_szczegoly_wartosc.grid(row=2, column=2)


        #DEFINIOWANIE FUNKCJI W RAMCE HOTELE ######################################


        def hotele_wyswietl():
            #Wyczysczenie zawartości listbox przed wyświetleniem nowych danych
            listbox_hotele.delete(0, END)

            #Zapytanie o dane hoteli
            sql_query = f"SELECT * FROM public.hotele ORDER BY id ASC;"
            cursor.execute(sql_query)
            query_result = cursor.fetchall()

            #Wyświetlenie danych
            for index, wiersz in enumerate(query_result):
                listbox_hotele.insert(index, f'Hotel {wiersz[1]}')

            id_aktualizacja_hotele()


        def hotele_dodaj():
            # Pobranie danych
            nazwa = entry_hotele_nazwa.get()
            miasto = entry_hotele_miasta.get()
            pokoje = entry_hotele_liczba_pokoi.get()
            biuro = entry_hotele_biuro.get()

            # Pobranie nowego ID
            new_id = id_dodawanie_hotele()

            # Zapytanie o dodanie nowego hotelu do bazy danych
            sql_query_insert = f"INSERT INTO public.hotele(id, nazwa, miasto, liczba_pokoi, biuro) VALUES ('{new_id}', '{nazwa}', '{miasto}', '{pokoje}', '{biuro}');"
            cursor.execute(sql_query_insert)
            db_params.commit()

            # Wyczyszczenie pól po dodaniu rekordu
            entry_hotele_nazwa.delete(0, END)
            entry_hotele_miasta.delete(0, END)
            entry_hotele_liczba_pokoi.delete(0, END)
            entry_hotele_biuro.delete(0, END)

            # Odświeżenie wyświetlania danych
            hotele_wyswietl()


        def hotele_edytuj():
            # Pobranie danych o hotelach z bazy
            sql_query_select = f"SELECT * FROM public.hotele ORDER BY id ASC;"
            cursor.execute(sql_query_select)
            query_result = cursor.fetchall()

            # Pobranie indeksu zaznaczonego elementu
            selected_index = listbox_hotele.index(ACTIVE)

            # Wyczyszczenie pól
            entry_hotele_nazwa.delete(0, END)
            entry_hotele_miasta.delete(0, END)
            entry_hotele_liczba_pokoi.delete(0, END)
            entry_hotele_biuro.delete(0, END)

            # Wypełnienie pól danymi z zaznaczonego rekordu
            entry_hotele_nazwa.insert(0, query_result[selected_index][1])
            entry_hotele_miasta.insert(0, query_result[selected_index][2])
            entry_hotele_liczba_pokoi.insert(0, query_result[selected_index][3])
            entry_hotele_biuro.insert(0, query_result[selected_index][4])

            # Zmiana tekstu na przycisku i przypisanie nowej funkcji
            button_hotele_dodaj.config(text='Zapisz zmiany', command=lambda: hotele_aktualizuj(selected_index))


        def hotele_aktualizuj(i):
            # Pobranie danych hoteli z bazy danych
            sql_query_select = "SELECT * FROM public.hotele ORDER BY id ASC;"
            cursor.execute(sql_query_select)
            query_result = cursor.fetchall()

            # Pobranie nowych danych z pól
            nazwa = entry_hotele_nazwa.get()
            miasto = entry_hotele_miasta.get()
            liczba_pokoi = entry_hotele_liczba_pokoi.get()
            biuro = entry_hotele_biuro.get()

            # Zapytanie do aktualizacji danych w bazie
            sql_query_update = f"UPDATE public.hotele SET nazwa='{nazwa}', miasto='{miasto}', liczba_pokoi='{liczba_pokoi}', biuro='{biuro}' WHERE nazwa='{query_result[i][1]}' and miasto='{query_result[i][2]}' and liczba_pokoi='{query_result[i][3]}' and biuro='{query_result[i][4]}';"
            cursor.execute(sql_query_update)
            db_params.commit()

            # Przywrócenie pierwotnego tekstu przycisku i przypisanie pierwotnej funkcji
            button_hotele_dodaj.config(text='Dodaj hotel', command=hotele_dodaj)

            # Wyczyszczenie pól
            entry_hotele_nazwa.delete(0, END)
            entry_hotele_miasta.delete(0, END)
            entry_hotele_liczba_pokoi.delete(0, END)
            entry_hotele_biuro.delete(0, END)

            # Odświeżenie wyświetlania danych
            hotele_wyswietl()

        def hotele_usun():
            #Pobieranie indeksu zaznacone elementu w listbox
            i = listbox_hotele.index(ACTIVE)

            #Zapytanie o usunięcie biura z bazy danych
            sql_query = f"DELETE FROM public.hotele WHERE id='{i+1}';"
            cursor.execute(sql_query)
            db_params.commit()

            #Odświeżenie wyświetlania danych
            hotele_wyswietl()

        def hotele_pokaz():
            #Pobieranie danych
            sql_query = f"SELECT * FROM public.hotele ORDER BY id ASC;"
            cursor.execute(sql_query)
            query_result = cursor.fetchall()

            #Pobieranie indeksu zaznaczonego elementu w listbox
            i = listbox_hotele.index(ACTIVE)

            #Pobieranie danych hotelu
            nazwa=query_result[i][1]
            miasto=query_result[i][2]
            liczba_pokoi=query_result[i][3]
            biuro=query_result[i][4]

            #Aktualizacja etykiet w ramce ze szczegółami
            label_hotele_nazwa_szczegoly_wartosc.config(text=nazwa)
            label_hotele_miasto_szczegoly_wartosc.config(text=miasto)
            label_hotele_pokoje_szczegoly_wartosc.config(text=liczba_pokoi)
            label_hotele_biuro_szczegoly_wartosc.config(text=biuro)

        def hotele_wybrane():
            #Wyczyszenie listbox
            listbox_hotele.delete(0, END)
            #Pobranie wartości z pola
            wybor=entry_hotele_wybor.get()

            #Zapytanie SQL
            sql_query = f"SELECT * FROM public.hotele WHERE biuro='{wybor}' ORDER BY id ASC;"
            cursor.execute(sql_query)
            query_result = cursor.fetchall()

            #Weryfikacja i dodanie do listbox
            for index, wiersz in enumerate(query_result):
                listbox_hotele.insert(index, f'Hotel {wiersz[1]}')

# DEFINIOWANIE WYGLĄDU RAMKI HOTELI ###################################

        ramka_hotele_nazwa = Frame(root_hotele)
        ramka_hotele_nazwa.grid(row=0, column=0, columnspan=2)

        ramka_hotele_lista = Frame(root_hotele)
        ramka_hotele_lista.grid(row=1, column=1)

        ramka_hotele_wpisywanie = Frame(root_hotele)
        ramka_hotele_wpisywanie.grid(row=1, column=0)

        ramka_hotele_wybor=Frame(root_hotele)
        ramka_hotele_wybor.grid(row=2, column=0, columnspan=2)

        ramka_hotele_szczegoly = Frame(root_hotele)
        ramka_hotele_szczegoly.grid(row=3, column=0, columnspan=2)


        # Wygląd ramki hotele_nazwa ##################################

        label_hotele_lista = Label(ramka_hotele_nazwa, text='Lista hoteli współpracujących z biurami podróży', font=('Times New Roman', 14))

        label_hotele_lista.grid(row=0, column=0, pady=(10, 0))


        # Wygląd ramki hotele_lista ####################################

        button_pokaz_liste_hotele = Button(ramka_hotele_lista, text='Wyświetl', command=hotele_wyswietl)
        button_pokaz_liste_hotele.grid(row=0, column=0, columnspan=3)

        listbox_hotele = Listbox(ramka_hotele_lista, width=50, height=5)
        listbox_hotele.grid(row=1, column=0, columnspan=3, pady=(10, 0))

        button_hotele_szczegoly = Button(ramka_hotele_lista, text='Wyświetl szczegóły', command=hotele_pokaz)
        button_hotele_szczegoly.grid(row=2, column=0)

        button_hotele_usun = Button(ramka_hotele_lista, text='Usuń rekord', command=hotele_usun)
        button_hotele_usun.grid(row=2, column=1)

        button_hotele_edytuj = Button(ramka_hotele_lista, text='Edytuj rekord', command=hotele_edytuj)
        button_hotele_edytuj.grid(row=2, column=2)


        # Wygląd ramki hotele_wpisywanie ###################################

        label_hotele_nowy = Label(ramka_hotele_wpisywanie, text='Edycja i dodawanie:', font=('Times New Roman', 12))
        label_hotele_nowy.grid(row=0, column=0, columnspan=2)

        label_hotele_nazwa = Label(ramka_hotele_wpisywanie, text='Nazwa hotelu')
        label_hotele_nazwa.grid(row=1, column=0, sticky=W)

        label_hotele_miasta = Label(ramka_hotele_wpisywanie, text='Miasto hotelu')
        label_hotele_miasta.grid(row=2, column=0, sticky=W)

        label_hotele_liczba_pokoi = Label(ramka_hotele_wpisywanie, text='Liczba pokoi')
        label_hotele_liczba_pokoi.grid(row=3, column=0, sticky=W)

        label_hotele_biuro = Label(ramka_hotele_wpisywanie, text='Biuro')
        label_hotele_biuro.grid(row=4, column=0, sticky=W)

        entry_hotele_nazwa = Entry(ramka_hotele_wpisywanie)
        entry_hotele_nazwa.grid(row=1, column=1, sticky=W)

        entry_hotele_miasta = Entry(ramka_hotele_wpisywanie)
        entry_hotele_miasta.grid(row=2, column=1, sticky=W)

        entry_hotele_liczba_pokoi = Entry(ramka_hotele_wpisywanie)
        entry_hotele_liczba_pokoi.grid(row=3, column=1, sticky=W)

        entry_hotele_biuro = Entry(ramka_hotele_wpisywanie)
        entry_hotele_biuro.grid(row=4, column=1, sticky=W)

        button_hotele_dodaj = Button(ramka_hotele_wpisywanie, text='Dodaj rekord', command=hotele_dodaj)
        button_hotele_dodaj.grid(row=5, column=0, columnspan=2)


        # Wygląd ramki hotele_wybor ######################################

        label_hotele_wybor=Label(ramka_hotele_wybor, text='Wpisz biuro współpracujące z hotelami')
        label_hotele_wybor.grid(row=0, column=0, columnspan=2)

        entry_hotele_wybor=Entry(ramka_hotele_wybor)
        entry_hotele_wybor.grid(row=1, column=0)

        button_hotele_wybor=Button(ramka_hotele_wybor, text='Wybierz', command=hotele_wybrane)
        button_hotele_wybor.grid(row=1, column=1)


        #Wygląd ramki hotele_szczegoly ######################################

        label_hotele_opis_obiektu = Label(ramka_hotele_szczegoly, text='Szczegóły hotelu:', font=('Times New Roman', 12))
        label_hotele_opis_obiektu.grid(row=0, column=0, columnspan=8, pady=10)

        label_hotele_nazwa_szczegoly = Label(ramka_hotele_szczegoly, text='Nazwa:')
        label_hotele_nazwa_szczegoly.grid(row=1, column=0)

        label_hotele_nazwa_szczegoly_wartosc = Label(ramka_hotele_szczegoly, text=' ', width=20)
        label_hotele_nazwa_szczegoly_wartosc.grid(row=2, column=0)

        label_hotele_miasto_szczegoly = Label(ramka_hotele_szczegoly, text='Miasto:')
        label_hotele_miasto_szczegoly.grid(row=1, column=1)

        label_hotele_miasto_szczegoly_wartosc = Label(ramka_hotele_szczegoly, text=' ', width=20)
        label_hotele_miasto_szczegoly_wartosc.grid(row=2, column=1)

        label_hotele_pokoje_szczegoly = Label(ramka_hotele_szczegoly, text='Liczba pokoi:')
        label_hotele_pokoje_szczegoly.grid(row=1, column=2)

        label_hotele_pokoje_szczegoly_wartosc = Label(ramka_hotele_szczegoly, text=' ', width=20)
        label_hotele_pokoje_szczegoly_wartosc.grid(row=2, column=2)

        label_hotele_biuro_szczegoly = Label(ramka_hotele_szczegoly, text='Biuro:')
        label_hotele_biuro_szczegoly.grid(row=1, column=3)

        label_hotele_biuro_szczegoly_wartosc = Label(ramka_hotele_szczegoly, text=' ', width=20)
        label_hotele_biuro_szczegoly_wartosc.grid(row=2, column=3)


        # DEFINIOWANIE FUNKCJI W RAMCE PRACOWNICY #############################################


        def pracownicy_wyswietl():
            #Wyczyszczenie zawartości listbox przed wyświetleniem nowych danych
            listbox_pracownicy.delete(0, END)

            #Zapytanie o dane pracownika
            sql_query = f"SELECT * FROM public.pracownicy ORDER BY id ASC;"
            cursor.execute(sql_query)
            query_result = cursor.fetchall()

            #Wyświetlenie danych
            for index, wiersz in enumerate(query_result):
                listbox_pracownicy.insert(index, f'Pracownik {wiersz[1]} {wiersz[2]}')

            id_aktualizacja_pracownicy()


        def pracownicy_dodaj():
            # Pobieranie danych
            imie = entry_pracownicy_imie.get()
            nazwisko = entry_pracownicy_nazwisko.get()
            miasto = entry_pracownicy_miasto.get()
            biuro = entry_pracownicy_biuro.get()

            # Pobieranie nowego ID
            new_id = id_dodawanie_pracownicy()

            # Zapytanie o dodanie nowego pracownika do bazy danych
            sql_query = f"INSERT INTO public.pracownicy(id, imie, nazwisko, miasto, biuro) VALUES ('{new_id}', '{imie}', '{nazwisko}', '{miasto}', '{biuro}');"
            cursor.execute(sql_query)
            db_params.commit()

            # Wyczyszczenie pól po dodaniu rekordu
            entry_pracownicy_imie.delete(0, END)
            entry_pracownicy_nazwisko.delete(0, END)
            entry_pracownicy_miasto.delete(0, END)
            entry_pracownicy_biuro.delete(0, END)

            # Odświeżenie wyświetlania danych
            pracownicy_wyswietl()


        def pracownicy_edytuj():
            # Pobranie danych pracowników z bazy danych
            sql_query_select = "SELECT * FROM public.pracownicy ORDER BY id ASC;"
            cursor.execute(sql_query_select)
            query_result = cursor.fetchall()

            # Pobranie indeksu zaznaczonego elementu w listbox
            selected_index = listbox_pracownicy.index(ACTIVE)

            # Wyczyszczenie pól
            entry_pracownicy_imie.delete(0, END)
            entry_pracownicy_nazwisko.delete(0, END)
            entry_pracownicy_miasto.delete(0, END)
            entry_pracownicy_biuro.delete(0, END)

            # Wypełnienie pól danymi zaznaczonego pracownika
            entry_pracownicy_imie.insert(0, query_result[selected_index][1])
            entry_pracownicy_nazwisko.insert(0, query_result[selected_index][2])
            entry_pracownicy_miasto.insert(0, query_result[selected_index][3])
            entry_pracownicy_biuro.insert(0, query_result[selected_index][4])

            # Zmiana tekstu przycisku i przypisanie nowej funkcji
            button_pracownicy_dodaj.config(text='Zapisz zmiany', command=lambda: pracownicy_aktualizuj(selected_index))

        def pracownicy_aktualizuj(i):
            #Pobranie danych pracownikow z bazy danych
            sql_query = f"SELECT * FROM public.pracownicy ORDER BY id ASC;"
            cursor.execute(sql_query)
            query_result = cursor.fetchall()

            #Pobranie nowych danych z pól
            imie=entry_pracownicy_imie.get()
            nazwisko=entry_pracownicy_nazwisko.get()
            miasto=entry_pracownicy_miasto.get()
            biuro=entry_pracownicy_biuro.get()

            #Zapytanie do aktuazliacji danych w bazie
            sql_query_update = f"UPDATE public.pracownicy SET imie='{imie}',nazwisko='{nazwisko}', miasto='{miasto}', biuro='{biuro}' WHERE imie='{query_result[i][1]}' and nazwisko='{query_result[i][2]}' and miasto='{query_result[i][3]}' and biuro='{query_result[i][4]}';"
            cursor.execute(sql_query_update)
            db_params.commit()

            #Przywrócenie pierwotnego tekstu przycisku i jego funkcji
            button_pracownicy_dodaj.config(text='Dodaj rekord', command=pracownicy_dodaj)

            #Wyczyszczenie pól
            entry_pracownicy_imie.delete(0, END)
            entry_pracownicy_nazwisko.delete(0, END)
            entry_pracownicy_miasto.delete(0, END)
            entry_pracownicy_biuro.delete(0, END)

            #Usunięcie wszystkich elementów z listbox
            listbox_pracownicy.delete(0, END)

            #Odświeżenie wyświetlania danych
            pracownicy_wyswietl()

        def pracownicy_usun():
            #Pobieranie indeksu zaznaczonego eleemntu w listobox
            i = listbox_pracownicy.index(ACTIVE)

            #Zapytanie o usunięcie pracownika z bazy danych
            sql_query = f"DELETE FROM public.pracownicy WHERE id='{i+1}';"
            cursor.execute(sql_query)
            db_params.commit()

            #Odświeżenie wyświetlania danych
            pracownicy_wyswietl()

        def pracownicy_pokaz():
            #Pobieranie danych
            sql_query = f"SELECT * FROM public.pracownicy ORDER BY id ASC;"
            cursor.execute(sql_query)
            query_result = cursor.fetchall()

            #Pobieranie indeksu zaznaczonego elementu w listbox
            i = listbox_pracownicy.index(ACTIVE)

            #Pobieranie danych pracownika
            imie=query_result[i][1]
            nazwisko=query_result[i][2]
            miasto=query_result[i][3]
            biuro=query_result[i][4]


            #Aktualizacja etykiet w ramce ze szczegółami
            label_pracownicy_imie_szczegoly_wartosc.config(text=imie)
            label_pracownicy_nazwisko_szczegoly_wartosc.config(text=nazwisko)
            label_pracownicy_miasto_szczegoly_wartosc.config(text=miasto)
            label_pracownicy_biuro_szczegoly_wartosc.config(text=biuro)


        def pracownicy_wybrane():
            #Wyczysczenie listbox
            listbox_pracownicy.delete(0, END)
            #Pobranie wartości z pola
            wybor = entry_pracownicy_wybor.get()

            #Zapytanie SQL
            sql_query = f"SELECT * FROM public.pracownicy WHERE biuro='{wybor}' ORDER BY id ASC;"
            cursor.execute(sql_query)
            query_result = cursor.fetchall()

            #Weryfikacja i dodanie do listbox
            for index, wiersz in enumerate(query_result):
                listbox_pracownicy.insert(index, f'Pracownik {wiersz[1]} {wiersz[2]}')


        # DEFINIOWANIE WYGLĄDU RAMKI pracowników ############################################

        ramka_pracownicy_nazwa = Frame(root_pracownicy)
        ramka_pracownicy_nazwa.grid(row=0, column=0, columnspan=2)

        ramka_pracownicy_lista = Frame(root_pracownicy)
        ramka_pracownicy_lista.grid(row=1, column=1)

        ramka_pracownicy_wpisywanie = Frame(root_pracownicy)
        ramka_pracownicy_wpisywanie.grid(row=1, column=0)

        ramka_pracownicy_wybor=Frame(root_pracownicy)
        ramka_pracownicy_wybor.grid(row=2,column=0, columnspan=2)

        ramka_pracownicy_szczegoly = Frame(root_pracownicy)
        ramka_pracownicy_szczegoly.grid(row=3, column=0, columnspan=2)



        # Wygląd ramki pracownicy_nazwa #########################################################

        label_pracownicy_lista = Label(ramka_pracownicy_nazwa, text='Lista pracowników biur podróży', font=('Times New Roman', 14))
        label_pracownicy_lista.grid(row=0, column=0, pady=(10, 0))


        # Wygląd ramka pracownicy_lista ################################################################

        button_pokaz_liste_pracownicy = Button(ramka_pracownicy_lista, text='Wyświetl', command=pracownicy_wyswietl)
        button_pokaz_liste_pracownicy.grid(row=0, column=0, columnspan=3)

        listbox_pracownicy = Listbox(ramka_pracownicy_lista, width=50, height=5)
        listbox_pracownicy.grid(row=1, column=0, columnspan=3, pady=(10, 0))

        button_pracownicy_szczegoly = Button(ramka_pracownicy_lista, text='Wyświetl szczegóły', command=pracownicy_pokaz)
        button_pracownicy_szczegoly.grid(row=2, column=0)

        button_pracownicy_usun = Button(ramka_pracownicy_lista, text='Usuń rekord', command=pracownicy_usun)
        button_pracownicy_usun.grid(row=2, column=1)
        button_pracownicy_edytuj = Button(ramka_pracownicy_lista, text='Edytuj rekord', command=pracownicy_edytuj)
        button_pracownicy_edytuj.grid(row=2, column=2)


        # Wygląd ramki pracownicy_wpisywanie #######################################################

        label_pracownicy_nowy = Label(ramka_pracownicy_wpisywanie, text='Edycja i dodawanie:', font=('Times New Roman', 12))
        label_pracownicy_nowy.grid(row=0, column=0, columnspan=2)

        label_pracownicy_imie = Label(ramka_pracownicy_wpisywanie, text='Imię pracownika')
        label_pracownicy_imie.grid(row=1, column=0, sticky=W)

        label_pracownicy_nazwisko = Label(ramka_pracownicy_wpisywanie, text='Nazwisko pracownika')
        label_pracownicy_nazwisko.grid(row=2, column=0, sticky=W)

        label_pracownicy_miasto = Label(ramka_pracownicy_wpisywanie, text='Miasto pracownika')
        label_pracownicy_miasto.grid(row=3, column=0, sticky=W)

        label_pracownicy_biuro = Label(ramka_pracownicy_wpisywanie, text='Biuro pracownika')
        label_pracownicy_biuro.grid(row=4, column=0, sticky=W)

        entry_pracownicy_imie = Entry(ramka_pracownicy_wpisywanie)
        entry_pracownicy_imie.grid(row=1, column=1, sticky=W)

        entry_pracownicy_nazwisko = Entry(ramka_pracownicy_wpisywanie)
        entry_pracownicy_nazwisko.grid(row=2, column=1, sticky=W)

        entry_pracownicy_miasto = Entry(ramka_pracownicy_wpisywanie)
        entry_pracownicy_miasto.grid(row=3, column=1, sticky=W)

        entry_pracownicy_biuro = Entry(ramka_pracownicy_wpisywanie)
        entry_pracownicy_biuro.grid(row=4, column=1, sticky=W)

        button_pracownicy_dodaj = Button(ramka_pracownicy_wpisywanie, text='Dodaj rekord', command=pracownicy_dodaj)
        button_pracownicy_dodaj.grid(row=5, column=0, columnspan=2)


        # Wygląd ramki pracownicy_wybor ##############################################

        label_pracownicy_wybor=Label(ramka_pracownicy_wybor, text='Wpisz placówkę, żeby zobaczyć pracowników')
        label_pracownicy_wybor.grid(row=0, column=0, columnspan=2)

        entry_pracownicy_wybor=Entry(ramka_pracownicy_wybor)
        entry_pracownicy_wybor.grid(row=1, column=0)

        button_pracownicy_wybor=Button(ramka_pracownicy_wybor, text='Wybierz', command=pracownicy_wybrane)
        button_pracownicy_wybor.grid(row=1, column=1)


        #Wygląd  ramki pracownicy_szczegoly ########################################

        label_pracownicy_opis_obiektu = Label(ramka_pracownicy_szczegoly, text='Szczegóły pracownika:', font=('Times New Roman', 12))
        label_pracownicy_opis_obiektu.grid(row=0, column=0, columnspan=8, pady=10)

        label_pracownicy_imie_szczegoly = Label(ramka_pracownicy_szczegoly, text='Imię:')
        label_pracownicy_imie_szczegoly.grid(row=1, column=0)

        label_pracownicy_imie_szczegoly_wartosc = Label(ramka_pracownicy_szczegoly, text=' ', width=20)
        label_pracownicy_imie_szczegoly_wartosc.grid(row=2, column=0)

        label_pracownicy_nazwisko_szczegoly = Label(ramka_pracownicy_szczegoly, text='Nazwisko:')
        label_pracownicy_nazwisko_szczegoly.grid(row=1, column=1)

        label_pracownicy_nazwisko_szczegoly_wartosc = Label(ramka_pracownicy_szczegoly, text=' ', width=20)
        label_pracownicy_nazwisko_szczegoly_wartosc.grid(row=2, column=1)

        label_pracownicy_miasto_szczegoly = Label(ramka_pracownicy_szczegoly, text='Miasto:')
        label_pracownicy_miasto_szczegoly.grid(row=1, column=2)

        label_pracownicy_miasto_szczegoly_wartosc = Label(ramka_pracownicy_szczegoly, text=' ', width=20)
        label_pracownicy_miasto_szczegoly_wartosc.grid(row=2, column=2)

        label_pracownicy_biuro_szczegoly = Label(ramka_pracownicy_szczegoly, text='Biuro podróży:')
        label_pracownicy_biuro_szczegoly.grid(row=1, column=3)

        label_pracownicy_biuro_szczegoly_wartosc = Label(ramka_pracownicy_szczegoly, text=' ', width=20)
        label_pracownicy_biuro_szczegoly_wartosc.grid(row=2, column=3)

        root_okienko.mainloop()



#--------------WYGLAD RAMKI LOGOWANIA----------------#####################

okienko_logowanie = Tk()
okienko_logowanie.title('Zarzadzanie siecia biur podrozy')
okienko_logowanie.geometry('250x130')

ramka_logowanie = Frame(okienko_logowanie)
ramka_logowanie.grid(row=0, column=0)

logowanie_tytul = Label(ramka_logowanie, text='Wpisz \n haslo')
wpisz_haslo = Entry(ramka_logowanie, width=30)
przycisk_logowanie = Button(ramka_logowanie, text='Zatwierdz', command=logowanie_do_systemu)

logowanie_tytul.grid(row=0, column=0, columnspan=2)
wpisz_haslo.grid(row=1, column=0, padx=(3, 0))
przycisk_logowanie.grid(row=1, column=1, columnspan=2)

okienko_logowanie.mainloop()



