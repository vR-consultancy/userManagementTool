
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

