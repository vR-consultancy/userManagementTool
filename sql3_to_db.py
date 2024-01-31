import os
import cx_Oracle
import pandas as pd
from sqlalchemy import types, create_engine
from pathlib import Path
from datetime import datetime
import keyring
import time
import sqlite3
from generalSnippets.databases import connect_CREF, write_to_DB
from database import *


# Tables definieren uit de database. Er is een aantal tables die wat aanpassingen nodig hebben.
tables = ['users','rtfunctions','rtapps','apps','functions','functionmatrix']


# Engine definieren
engine = connect_CREF()

# Itereren door tabellen lijst, en elke tabel wegschrijven naar database
for i in tables:
    t = readTable(i)
    print('Tabel in SQLite database:', i)
    dest = 'bb_gb_' + i.lower()
    print('Tabel in Oracle DB:', dest)
    if i in ['functions','apps']:
        try:
            t['sts_rec'] = t['sts_rec'].astype(int)
        except:
            pass
        try:
            t['toelichting'] = t['toelichting'].astype(str)
        except:
            pass
        try:
            t['dd_eind'] = t['dd_eind'].astype(str)
        except:
            pass
    write_to_DB(dest, engine, 'CREF', t, ifexists='replace')