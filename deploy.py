from database import *

def createSettings():
    settings = {}
    settings['companyname'] = input('Geef naam organisatie/bedrijf')

    import json

    with open('settings.json','w') as fp:
        json.dump(settings, fp)
    print('Instellingen weggeschreven naar \'settings.json\'.')