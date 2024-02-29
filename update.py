
def update10():
    print('Update naar v1.0 draaien')
    from database import create_table, updateVersion
    
    versionTable = """CREATE TABLE IF NOT EXISTS version (
                    version text,
                    datum text
    );""" 
    create_table(versionTable)
    updateVersion(1.0)



def update11():
    print('Update naar v1.1 draaien')
    from database import create_table, updateVersion

    matrixTable = """CREATE TABLE IF NOT EXISTS functionmatrix (
                    id text,
                    id_function text,
                    id_app text,
                    sts_rec integer
    );"""     

    create_table(matrixTable)
    updateVersion(1.1)

def update12():
    print('Update naar v1.2 draaien')
    from database import create_connection, updateVersion
    con = create_connection()
    sql = """ALTER TABLE rtapps ADD url text;"""     
    try:
        c = con.cursor()
        c.execute('pragma foreign_keys = ON;')
        c.execute(sql)
        con.commit()
    except Error as e:
        print(e)
    updateVersion(1.2)


def update13():
    print('Update naar v1.3 draaien')
    from database import create_connection, updateVersion
    con = create_connection()
    sql = """ALTER TABLE rtapps ADD sso text;"""     
    try:
        c = con.cursor()
        c.execute('pragma foreign_keys = ON;')
        c.execute(sql)
        con.commit()
    except Error as e:
        print(e)
    updateVersion(1.3)    