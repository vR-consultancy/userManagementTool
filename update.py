
def update10():
    print('Update naar v1.0 draaien')
    from database import create_table, updateVersion
    
    versionTable = """CREATE TABLE IF NOT EXISTS version (
                    version text,
                    datum text
    );""" 
    create_table(versionTable)
    updateVersion(1.0)
