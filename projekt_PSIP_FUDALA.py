
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



def id_dodawanie_biura():
    sql_query = "SELECT id FROM public.biura ORDER BY id ASC;"
    cursor.execute(sql_query)
    query_result = cursor.fetchall()

    index = [row[0] for row in query_result]
    new_id = 1 if not index else max(index) + 1

    return int(new_id)