import pandas as pd
import sqlite3
from sqlite3 import Error
from functions import *

 

def create_connection(dbFile='database.db'):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(dbFile)
        return conn
    except Error as e:
        print(e)

    return conn



def readTable(table):
    import pandas as pd
    con = create_connection()
    df = pd.read_sql_query("SELECT * from "+table, con)
    con.close()
    return df

def create_table(create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute('pragma foreign_keys = ON;')
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def delFunctionForUser(id_user, toelichting='Omzetting via managementtool'):
    sql = "UPDATE functions SET sts_rec=9, toelichting = '"+toelichting+"' WHERE id_user = '" + id_user + "';"
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute('pragma foreign_keys = ON;')
        c.execute(sql)
        conn.commit()

        return 'Oude functie op verwijderd gezet'

    except Error as e:
        print(e)
        return e    


def addFunctionToUser(id_function, id_user, dd_begin, dd_eind = '', sts_rec = 1, toelichting = ''):
    import uuid 
    from functions import dateTime_to_db
    if dd_begin == '':
        dd_begin= 'null'
    else:
        dd_begin = """'"""+ dateTime_to_db(dd_begin) +"""'"""

    if dd_eind == '':
        dd_eind= 'null'
    else:
        dd_eind = """'"""+ dateTime_to_db(dd_eind) +"""'"""

    if toelichting == '':
        toelichting= 'null'
    else:
        toelichting = """'"""+toelichting+"""'"""

    try:
        conn = create_connection()
        c = conn.cursor()
        sql = "INSERT INTO functions values ('"+\
            str(uuid.uuid4())+"','"+\
            id_function+"','"+\
            id_user+"',"+\
            dd_begin+","+\
            dd_eind+","+\
            toelichting+",'"+\
            str(sts_rec)+"');"
        c.execute('pragma foreign_keys = ON;')
        c.execute(sql)
        conn.commit()

        return 'Functie toegevoegd'

    except Error as e:
        print(e)
        return e

def changeFunctionMeta(id_function, name_function, sts_rec):
    def d(gegeven):

        if type(gegeven) == list:
            if gegeven == []:
                return "'1'"
            elif gegeven == ['Verwijderd']:
                return "'9'"
            else:
                print('Status record niet goed! opgeslagen met cijfer 7!')
                return "'7'"
        elif gegeven == None or gegeven == '':
            return "null"
        elif type(gegeven) == str:
            return "'"+gegeven+"'"
        elif isinstance(gegeven, datetime):
            return "'"+dateTime_to_db(gegeven)+"'"
        else:
            return "'"+gegeven+"'"


    sql = "UPDATE rtfunctions SET "+\
        "function = "+ d(name_function) +\
            ", sts_rec = " + d(sts_rec) +\
                " where id_function = " + d(id_function) + ";"

    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute('pragma foreign_keys = ON;')
        c.execute(sql)
        conn.commit()
        return "Functie aangepast"
    except Error as e:
        print(e)
        return e
        


def addFunction(function, sts_rec=1):
    import uuid 

    try:
        conn = create_connection()
        c = conn.cursor()
        sql = "INSERT INTO rtfunctions values ('"+\
            str(uuid.uuid4())+"','"+\
            function+"','"+\
            str(sts_rec)+"');"
        c.execute('pragma foreign_keys = ON;')
        c.execute(sql)
        conn.commit()    
        return 'Functie toegevoegd'

    except Error as e:
        print(e)
        return e

def addApp(name_app,sts_rec=1, toelichting = ''):
    import uuid 
    if toelichting == None:
        toelichting = ''
    try:
        conn = create_connection()
        c = conn.cursor()
        sql = "INSERT INTO rtapps values ('"+\
            str(uuid.uuid4())+"','"+\
            name_app +"','"+\
            str(sts_rec) + "','"+\
            toelichting+"');"
        c.execute('pragma foreign_keys = ON;')
        c.execute(sql)
        conn.commit()
        return 'App toegevoegd'

    except Error as e:
        print(e)
        return e




def addUserToApp(id_app, id_user, dd_begin, dd_eind='',toelichting = '',sts_rec=1):
    print(id_app, id_user)
    import uuid 
    from functions import dateTime_to_db
    if dd_begin == '':
        dd_begin= 'null'
    else:
        dd_begin = """'"""+ dateTime_to_db(dd_begin) +"""'"""

    if dd_eind == '':
        dd_eind= 'null'
    else:
        dd_eind = """'"""+ dateTime_to_db(dd_eind) +"""'"""

    if toelichting == '':
        toelichting= 'null'
    else:
        toelichting = """'"""+toelichting+"""'"""


    try:
        conn = create_connection()
        c = conn.cursor()
        sql = "INSERT INTO apps values ('"+\
            str(uuid.uuid4())+"','"+\
            id_app+"','"+\
            id_user+"',"+\
            dd_begin+","+\
            dd_eind+","+\
            toelichting+",'"+\
            str(sts_rec)+"');"
        c.execute('pragma foreign_keys = ON;')
        c.execute(sql)
        conn.commit()      
        return 'Gebruiker aan app toegevoegd'

    except Error as e:
        print(e)
        return e



def addUser(voornaam, voorvoegsel, achternaam, email, aduser, topdesk_in, topdesk_uit, dd_begin, toelichting='', dd_eind='', sts_rec=1, id_manager=''):
    import uuid



    def d(gegeven):

        if type(gegeven) == list:
            if gegeven == []:
                return "'1'"
            elif gegeven == ['Verwijderd']:
                return "'9'"
            else:
                print('Status record niet goed! opgeslagen met cijfer 7!')
                return "'7'"
        elif gegeven == None or gegeven == '':
            return "null"
        elif type(gegeven) == str:
            return "'"+gegeven+"'"
        elif type(gegeven) == int and gegeven in [1,9]:
            return "'"+str(gegeven)+"'"
        elif isinstance(gegeven, datetime):
            return "'"+dateTime_to_db(gegeven)+"'"
        else:
            return "'"+gegeven+"'"



    try:
        conn = create_connection()
        c = conn.cursor()
        sql = "INSERT INTO users values ('"+\
            str(uuid.uuid4())+"',"+\
            d(voornaam)+","+\
            d(voorvoegsel)+","+\
            d(achternaam)+","+\
            d(email)+","+\
            d(aduser)+","+\
            d(id_manager)+","+\
            d(topdesk_in)+","+\
            d(topdesk_uit)+","+\
            d(dd_begin)+","+\
            d(dd_eind)+","+\
            d(sts_rec)+","+\
            d(toelichting)+");"
        c.execute('pragma foreign_keys = ON;')
        c.execute(sql)
        conn.commit()
        print('Gebruiker toegevoegd')  
        return 'Gebruiker toegevoegd'

    except Error as e:
        print(e)
        return e


def changeAppMeta(id_app, name_app, sts_rec, toelichting=''):
    def d(gegeven):

        if type(gegeven) == list:
            if gegeven == []:
                return "'1'"
            elif gegeven == ['Verwijderd']:
                return "'9'"
            else:
                print('Status record niet goed! opgeslagen met cijfer 7!')
                return "'7'"
        elif gegeven == None or gegeven == '':
            return "null"
        elif type(gegeven) == str:
            return "'"+gegeven+"'"
        elif isinstance(gegeven, datetime):
            return "'"+dateTime_to_db(gegeven)+"'"
        else:
            return "'"+gegeven+"'"


    sql = "UPDATE rtapps SET "+\
        "name_app = "+ d(name_app) +\
            ", sts_rec = " + d(sts_rec) +\
                ", toelichting = " + d(toelichting) +\
                " where id_app = " + d(id_app) + ";"

    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute('pragma foreign_keys = ON;')
        c.execute(sql)
        conn.commit()
        return "Applicatie aangepast"
    except Error as e:
        print(e)
        return e
    
    


def changeUserMeta(id_user, voornaam, voorvoegsels, achternaam, email, aduser, topdesk_in, topdesk_uit, dd_begin, dd_eind, id_manager, toelichting, sts_rec):
    def d(gegeven):

        if type(gegeven) == list:
            if gegeven == []:
                return "'1'"
            elif gegeven == ['Verwijderd']:
                return "'9'"
            else:
                print('Status record niet goed! opgeslagen met cijfer 7!')
                return "'7'"
        elif gegeven == None or gegeven == '':
            return "null"
        elif type(gegeven) == str:
            return "'"+gegeven+"'"
        elif isinstance(gegeven, datetime):
            return "'"+dateTime_to_db(gegeven)+"'"
        else:
            return "'"+gegeven+"'"




    sql = "UPDATE users SET "+\
        "voornaam = " + d(voornaam) +\
            ",voorvoegsels = " + d(voorvoegsels) +\
                ",achternaam = " + d(achternaam) +\
                    ",email = " + d(email) +\
                        ",aduser =" + d(aduser) +\
                            ",topdesk_in =" + d(topdesk_in) +\
                                ",topdesk_uit = " + d(topdesk_uit) +\
                                    ",dd_begin = " + d(dd_begin) +\
                                        ",dd_eind = " + d(dd_eind) +\
                                            ", id_manager = " + d(id_manager) +\
                                                ", sts_rec =" + d(sts_rec) +\
                                                    " where id_user = " + d(id_user) +";"


    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute('pragma foreign_keys = ON;')
        c.execute(sql)
        conn.commit()
        return "Gebruiker aangepast"
    except Error as e:
        print(e)
        return e

    
def deleteAppsForUser(id_user):
    sql = "DELETE FROM apps where id_user = '"+\
        id_user +"';"


    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute('pragma foreign_keys = ON;')
        c.execute(sql)
        conn.commit()
        return "Apps verwijderd"
    except Error as e:
        print(e)
        return e    



def createDB(test=False):
    if test:
        import os
        try:
            os.remove('database.db')    
        except:
            pass
    conn = create_connection()
    usersTable = """CREATE TABLE IF NOT EXISTS users (
                    id_user text PRIMARY KEY,
                    voornaam text,
                    voorvoegsels text,
                    achternaam text,
                    email text,
                    aduser text,
                    id_manager text,
                    topdesk_in text,
                    topdesk_uit text,
                    dd_begin text,
                    dd_eind text,
                    sts_rec integer,
                    toelichting text
    );""" 

    rtappTable = """CREATE TABLE IF NOT EXISTS rtapps (
                id_app text PRIMARY KEY,
                name_app text,
                sts_rec integer,
                toelichting text
    );"""

    rtfunctionsTable = """CREATE TABLE IF NOT EXISTS rtfunctions (
                id_function text PRIMARY KEY,
                function text,
                sts_rec integer
    );"""

    functionsTable = """CREATE TABLE IF NOT EXISTS functions (
                id text PRIMARY KEY,
                id_function text,
                id_user text,
                dd_begin text,
                dd_eind text,
                toelichting text,
                sts_rec integer
    );"""


    appsTable = """CREATE TABLE IF NOT EXISTS apps (
                    id text PRIMARY KEY,
                    id_app text,
                    id_user text,
                    dd_begin text,
                    dd_eind text,
                    toelichting text,
                    sts_rec integer
    );""" 



    create_table(usersTable)
    create_table(rtappTable)
    create_table(functionsTable)
    create_table(rtfunctionsTable)
    create_table(appsTable)






    if test:
        print('TESTdata toevoegen!')
        import pandas as pd
        import numpy as np
        from datetime import datetime




        print('Gebruikers toevoegen')
        df = pd.read_excel('Gebruikersbeheer.xlsm', sheet_name='Data')
        df['Einddatum'] = df["Einddatum"].replace("NaT",np.NaN)
        df['Begindatum'] = df["Begindatum"].replace("NaT",np.NaN)
        df = df.fillna('')
        df['Status'] = df['Status'].apply(lambda x: 9 if x == 'X' else (1 if x == 'O' else x))
        for i in df.values.tolist():
            if pd.isna(i[-2]):
                i[-2] = ''
            if pd.isna(i[-3]):
                i[-3] = datetime(1900,1,1)
            addUser(i[2], i[3], i[4], i[5], i[6], i[-5], i[-4], i[-3], toelichting = i[-1], dd_eind=i[-2], sts_rec=i[0])

        print('Applicaties toevoegen')
        lijstApps = ['Suites4SociaalDomein',
            'SVB',
            'Schulinck',
            'Cognostoegang Sociaal Domein',
            'Suwinet',
            'InSZicht',
            'Inlichtingenbureau Zorg',
            'Inlichtingenbureau Inkomen',
            'Landelijke Rekentool',
            'Steunwijzer',
            'Divosa',
            'Szeebra',
            'NOPnet USD Intern',
            'WIZPortaal',
            'Welzorg',
            'MediPoint',
            'Mybility',
            'DUO - Inburgering',
            'DUO - Leerplicht',
            'Dilemma manager (jongerenwerk)',
            'JVS']
        
        for i in lijstApps:
            addApp(i)

        print('Functies toevoegen')
        for i in ['Administratie Werkcorporatie',
            'Administratie Wmo/Jeugd',
            'Adviseur bedrijfsvoering',
            'Beleidsmedewerker',
            'Buiten USD',
            'Contractmanagement',
            'Fraude',
            'Functioneel beheer',
            'Klantmanagement Bijzondere bijstand en minima',
            'Klantmanagement Inburgering',
            'Klantmanagement Inkomen',
            'Klantmanagement Jeugd',
            'Klantmanagement Werk',
            'Klantmanagement Werkcorporatie',
            'Klantmanagement Wmo',
            'Kwaliteit',
            'Leerplichtambtenaar',
            'Management Werkcorporatie',
            'Managementteam',
            'Sociaal Loket',
            'Terugvordering',
            'Toezicht',
            'Financieel Loket',
            ]:
            addFunction(i)

        print('Gebruikers aan apps toevoegen')
        users = readTable('users')
        rtapps = readTable('rtapps')
        
        
        for i in lijstApps:
            appUsers = df[(df['Status'].isin([1,9])) & (df[i] == 'X')]
            for u in appUsers.values.tolist():
                print(u[5])
                if pd.isna(u[-3]):
                    u[-3] = ''                                 
                addUserToApp(rtapps.set_index('name_app').loc[i, 'id_app'], users.set_index('email').loc[u[5],'id_user'], u[-3])

        activeUsers = df[df['Status'].isin([1,9])]
        functions = readTable('rtfunctions')
        from datetime import datetime
        for i in activeUsers.values.tolist():
            if pd.isna(i[-3]):
                i[-3] = datetime(1900,1,1)
            addFunctionToUser(functions.set_index('function').loc[i[8], 'id_function'], users.set_index('email').loc[i[5],'id_user'], i[-3])

def dframes():
    frames = {}
    users = readTable('users')
    rtfunctions = readTable('rtfunctions')
    rtapps = readTable('rtapps')
    apps = readTable('apps')
    functions = readTable('functions')

    users['Volledige naam'] = users['voornaam']+' '+ users['voorvoegsels'].apply(lambda x: '' if pd.isna(x) else ('' if x == '' else x +' ' )) + users['achternaam']
    users['Sorteernaam'] = users['Achternaam']+', ' + users['Voornaam'] + users['Voorvoegsels'].apply(lambda x: ' '+ x if not pd.isna(x) else (''))
     

def readTables():
    allTables = {'users': readTable('users'),
    'rtfunctions': readTable('rtfunctions'),
    'rtapps': readTable('rtapps'),
    'apps': readTable('apps'),
    'functions': readTable('functions')}
    
    # users table aanpassen
    allTables['users']['Volledige naam'] = allTables['users']['voornaam']+' '+ allTables['users']['voorvoegsels'].apply(lambda x: '' if pd.isna(x) else ('' if x == '' else x +' ' )) + allTables['users']['achternaam']
    allTables['users']['Sorteernaam'] = allTables['users']['achternaam']+', ' + allTables['users']['voornaam'] + allTables['users']['voorvoegsels'].apply(lambda x: ' '+ x if not pd.isna(x) else (''))
        
    allTables['users'] = allTables['users'].rename(columns = {'voornaam': 'Voornaam',
                                'voorvoegsels': 'Voorvoegsels',
                                'achternaam':'Achternaam',
                                'email': 'Emailadres',
                                'aduser':'AD gebruikersnaam',
                                'topdesk_in': 'TOPdesk in dienst',
                                'topdesk_uit':'TOPdesk uit dienst',
                                'dd_begin': 'Begindatum',
                                'dd_eind': 'Einddatum',
                                'sts_rec':'Status gebruiker',
                                'toelichting':'Toelichting'
            })

    allTables['rtapps'] = allTables['rtapps'].rename(columns = {'name_app': 'Applicatie'})

    # functions table aanpassen
    allTables['functions']['dd_begin'] = allTables['functions']['dd_begin'].apply(lambda x: db_to_dateTime(x) if not pd.isna(x) else (x))
    allTables['functions']['dd_eind'] = allTables['functions']['dd_eind'].apply(lambda x: db_to_dateTime(x) if not pd.isna(x) else (x))

    allTables['users'] = allTables['users'].merge(allTables['functions'], on='id_user', how='left')
    allTables['users'] = allTables['users'].merge(allTables['rtfunctions'], left_on='id_function',right_on='id_function', how='left')

    allTables['usersGUI'] = allTables['users'][['id_user','Volledige naam','Voornaam','Voorvoegsels','Achternaam','Emailadres','id_function','function']].rename(columns={'function':'Functie'})

    # alle data in 1 DF
    functies = allTables['functions'].merge(allTables['rtfunctions'], on= 'id_function').rename(columns = {
        'sts_rec_x': 'Status functieregel', 
        'sts_rec_y': 'Status functie', 
        'id': 'id_functieregel'
        })
    applicaties = allTables['apps'].merge(allTables['rtapps'], on = 'id_app').rename(columns = {
        'id':'id_appregel',
        'sts_rec_x': 'Status appregel', 
        'sts_rec_y':'Status app',
        'dd_begin':'Begindatum app',
        'dd_eind':'Einddatum app',
        'toelichting':'Toelichting app'
        })
    allTables['allData'] = allTables['users'].rename(columns = {
        'id':'id_functieregel', 
        'sts_rec_x':'Status functieregel', 
        'sts_rec_y':'Status functie', 
        'dd_begin': 'Begindatum functieregel', 
        'dd_eind':'Einddatum functieregel',
        'toelichting': 'Toelichting functieregel'
    }).merge(applicaties, on = 'id_user', how='left')


    return allTables


def usersPerApp(appID,functionID, userID):



    t = readTables()
    t['usersGUI'] = t['usersGUI'].fillna('')
    t['rtapps'] = t['rtapps'].fillna('')
    t['rtfunctions'] = t['rtfunctions'].fillna('')
    
    if functionID == [''] or functionID == [] or functionID == None:
        functionID = t['rtfunctions']['id_function'].fillna('').values.tolist()
    if appID == [''] or appID == [] or appID == None:
        appID = t['rtapps']['id_app'].fillna('').values.tolist()
    if userID == [''] or userID == [] or userID == None:
        userID = t['users']['id_user'].fillna('').values.tolist()


    return t['usersGUI'][t['usersGUI']['id_user'].isin(userID)].merge(t['apps'][t['apps']['id_app'].isin(appID)], on='id_user', how='left').merge(t['rtapps'], how='left').merge(t['functions'][t['functions']['id_function'].isin(functionID)], on=['id_user','id_function'], how='left')[['Applicatie','Voornaam','Voorvoegsels','Achternaam','Volledige naam','Emailadres','Functie']]
