
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