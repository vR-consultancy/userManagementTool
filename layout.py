from dash import html, ALL, Patch
from dash import dcc
from styles import layoutStyles
import os, pathlib
from functions import *
from database import *


cssStyles = layoutStyles()

database = 'database.db'
if not os.path.isfile(database):
    from database import *
    
    createDB(test=True)
    print("Geen database gevonden. Er is een lege database aangemaakt.")


try:
    import json
    settings = json.load(open('settings.json'))
except:
    from deploy import createSettings
    createSettings()
    import json
    settings = json.load(open('settings.json'))


t = readTables()

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'backgroundColor': '#4e4e4e',
    'color':'white',
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #272b30',
    'backgroundColor': '#272b30',
    'color': 'white',
    'padding': '6px',
    'fontWeight': 'bold',
}


def mainLayout():
    return html.Div(
        children = [
        
        html.Div(
                id='header',
                style=cssStyles['block'],
                children = [
                    html.Div(
                        style = cssStyles['logo'],
                        children = [
                            html.Img(src='assets/logo.png',alt='Zet logo.png in de map \'assets\' om een logo weer te geven.')
                        ]
                    ),                        
                    html.Div(
                        style = cssStyles['title'],
                        children = [
                            html.H1(settings['companyname'] + ' - Gebruikersbeheer'),
                        ]
                    ),
                
                ]
                
            ), 
        html.Button('Refresh', id='refreshBtn', n_clicks=0),

        dcc.Tabs(
            style=tabs_styles,
                    
            children = [          
            dcc.Tab(
                style=tab_style, selected_style=tab_selected_style,  
                className='custom-tab',
                label='Gebruikers',
                children = [
                    html.Div(
                        id='backgroundTaskDiv'
                    ),
                    html.Div(
                        id='hiddenItems',
                        children = [
                            
                            dcc.Store(
                                id='chosenUser',
                                data=None
                            ),
                            dcc.Store(
                                id='chosenApp',
                                data=None
                            ),
                            dcc.Store(
                                id='chosenFunction',
                                data=None
                            ),
                            dcc.Store(
                                id='chosenApp_tbv_saveMeta',
                                data=None
                            ),
                            dcc.Store(
                                id='chosenUser_tbv_saveMeta',
                                data=None
                            ),
                            dcc.Store(
                                id='chosenUser_tbv_saveApps',
                                data=None
                            ),
                            dcc.Store(
                                id='chosenFunction_tbv_saveMeta',
                                data = None
                            ),
                            dcc.Interval(
                                id='tableTimer',
                                disabled = True,
                                n_intervals = 0,
                                interval=10000 # 10 seconds
                            ),

                            dcc.Interval(
                                id='resetSaveOutputTimer',
                                disabled = True,
                                n_intervals = 0,
                                interval=2000 # 2 seconds
                            ),                         
                            dcc.Interval(
                                id='resetSaveAppOutputTimer',
                                disabled = True,
                                n_intervals = 0,
                                interval=2000 # 2 seconds
                            ),                                   
                            dcc.Store(
                                id='toetevoegenApps',
                                data = []
                            ),   
                            dcc.Store(
                                id='newOrChangeUser',
                                data = None
                            ),                 
                        ]
                    ),






                    html.Div(id='Output'),





                    html.H1(''),



                    dcc.Markdown('## Filters'),
                    html.Div(
                        id = 'appKiezerDiv',
                        style = cssStyles['block'],
                        children=[

                            html.Div(
                                children = [
                                    html.Div(

                                        children = [
                                            html.Div(
                                                style={'display':'inline-block',
                                                    'width':'10%'},
                                                children = [
                                                    dcc.Markdown(
                                                        '### Applicatie',
                                                    )   
                                                ]
            
                                            ),
                                            html.Div(
                                                style={'display':'inline-block',
                                                    #    'width': '500px'},
                                                        'width': '80%'},
                                                children = [

                                                    dcc.Dropdown(
                                                        id = 'appChooserDropdown',
                                                        value = [],
                                                        options = [{'label':'(leeg)','value': ''}] + [{'label': i[1], 'value': i[0]} for i in t['rtapps'][t['rtapps']['sts_rec']==1].sort_values(by=['Applicatie']).values.tolist()],
                                                        multi=True,
                                                    )    
                                                ]
            
                                            ),
                                            html.Div(
                                                style={'display':'inline-block',
                                                    'width':'10%'},
                                                children = [
                                                    dcc.Checklist(
                                                        id='appInclVerwijderd',
                                                        options = ['Inclusief verwijderd'],
                                                        value = []
                                                    )

                                                ]
            
                                            ),                                                                  
                                        ]
                                    ),                            
                                    html.Div(

                                        children = [
                                            html.Div(
                                                style={'display':'inline-block',
                                                    'width':'10%'},
                                                children = [
                                                    dcc.Markdown(
                                                        '### Functie',
                                                    )   
                                                ]
            
                                            ),
                                            html.Div(
                                                style={'display':'inline-block',
                                                        'width': '80%'},
                                                children = [

                                                    dcc.Dropdown(
                                                        id = 'functionChooserDropdown',
                                                        options = [{'label':'(leeg)','value': ''}] + [{'label': i[1], 'value': i[0]} for i in t['rtfunctions'][t['rtfunctions']['sts_rec']==1].sort_values(by=['function']).values.tolist()],
                                                        multi=True,
                                                        value = []
                                                        
                                                    )    
                                                ]
            
                                            ),
                                            html.Div(
                                                style={'display':'inline-block',
                                                    'width':'10%'},
                                                children = [
                                                    dcc.Checklist(
                                                        id='functieInclVerwijderd',
                                                        options = ['Inclusief verwijderd'],
                                                        value = []
                                                    )

                                                ]
            
                                            ),                                                                 
                                            
                                        ]
                                    ),
                                    html.Div(

                                        children = [
                                            html.Div(
                                                style={'display':'inline-block',
                                                    'width':'10%'},
                                                children = [
                                                    dcc.Markdown(
                                                        '### Gebruiker',
                                                    )   
                                                ]
            
                                            ),
                                            html.Div(
                                                style={'display':'inline-block',
                                                        'width': '80%'},
                                                children = [

                                                    dcc.Dropdown(
                                                        id = 'userChooserDropdown',
                                                        options = [{'label':'(leeg)','value': ''}] + [{'label': str(i[14]) + '('+str(i[4])+')', 'value': i[0]} for i in t['users'].sort_values(by=['Sorteernaam']).values.tolist()],
                                                        multi=True,
                                                        value = []
                                                        
                                                    )    
                                                ]
            
                                            ),
                                            html.Div(
                                                style={'display':'inline-block',
                                                    'width':'10%'},
                                                children = [
                                                    dcc.Checklist(
                                                        id='userInclVerwijderd',
                                                        options = ['Inclusief verwijderd'],
                                                        value = []
                                                    )

                                                ]
            
                                            ),                                                                        
                                        ]
                                    ),                            
                                ]
                            ),
                            html.Button(
                                'Gebruiker wijzigen',
                                id = 'changeUserBtn',
                                n_clicks=0,
                                style = {'display':'none'},
                            ),
                            html.Button(
                                'Nieuwe gebruiker toevoegen',
                                id = 'newUserBtn',
                                n_clicks=0,
                                style = cssStyles['button'],
                            ),                            
                        ]
                    ),


                    html.H1(''),
                    html.Div(
                        id='changeUserTitleDiv', 
                        style = {'display':'none'},
                        children =[ html.H2('Wijzig gebruiker')] 
                    ),
                    html.H3(''),
                    html.Div(
                        id='changeUserDiv', 
                        style = {'display':'none'},
                        children = [
                            
                            html.Div(
                                id='changeUserMetaDiv',
                                style = cssStyles['changeUserBlock'],
                                children = [
                                    dcc.Checklist(
                                        id = 'userDeleted',
                                        options = ['Verwijderd'],
                                        value = []
                                    ),
                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block', 'width':'10%'},
                                                children = ['Voornaam']
                                            ),
                                            html.Div(
                                                style = {'display':'inline-block'},
                                                children = [
                                                    dcc.Input(
                                                        style = {'width':'400px'},
                                                        id='voornaam',
                                                        
                                                    )
                                                ]
                                            ),

                                        ]
                                    ),



                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block', 'width':'10%'},
                                                children = ['Voorvoegsel(s)']
                                            ),
                                            html.Div(
                                                style = {'display':'inline-block'},
                                                children = [
                                                    dcc.Input(
                                                        style = {'width':'400px'},
                                                        id='voorvoegsels',
                                                        
                                                    )
                                                ]
                                            ),                                    
                                        ]
                                    ),

                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block', 'width':'10%'},
                                                children = ['Achternaam']
                                            ),
                                            html.Div(
                                                style = {'display':'inline-block'},
                                                children = [
                                                    dcc.Input(
                                                        style = {'width':'400px'},
                                                        id='achternaam',
                                                        
                                                    )
                                                ]
                                            ),                                    
                                        ]
                                    ),


                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block', 'width':'10%'},
                                                children = ['Emailadres']
                                            ),
                                            html.Div(
                                                style = {'display':'inline-block'},
                                                children = [
                                                    dcc.Input(
                                                        style = {'width':'400px'},
                                                        id='email',
                                                        
                                                    )
                                                ]
                                            ),                                    
                                        ]
                                    ),


                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block', 'width':'10%'},
                                                children = ['AD gebruikersnaam']
                                            ),
                                            html.Div(
                                                style = {'display':'inline-block'},
                                                children = [
                                                    dcc.Input(
                                                        style = {'width':'400px'},
                                                        id='aduser',
                                                        
                                                    )
                                                ]
                                            ),                                    
                                        ]
                                    ),


                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block', 'width':'10%'},
                                                children = ['TOPdesk in dienst']
                                            ),
                                            html.Div(
                                                style = {'display':'inline-block'},
                                                children = [
                                                    dcc.Input(
                                                        style = {'width':'400px'},
                                                        id='topdesk_in',
                                                        
                                                    )
                                                ]
                                            ),                                    
                                        ]
                                    ),




                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block', 'width':'10%'},
                                                children = ['TOPdesk uit dienst']
                                            ),
                                            html.Div(
                                                style = {'display':'inline-block'},
                                                children = [
                                                    dcc.Input(
                                                        style = {'width':'400px'},
                                                        id='topdesk_uit',
                                                        
                                                    )
                                                ]
                                            ),                                    
                                        ]
                                    ),


                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block', 'width':'10%'},
                                                children = ['Begindatum']
                                            ),
                                            html.Div(
                                                style = {'display':'inline-block', 'width':'400px'},
                                                children = [
                                                    dcc.DatePickerSingle(
                                                        id='begindatum',
                                                        display_format = 'DD-MM-YYYY'
                                                        
                                                    )
                                                ]
                                            ),                                       
                                
                                        ]
                                    ),



                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block', 'width':'10%'},
                                                children = ['Einddatum']
                                            ),

                                            html.Div(
                                                style = {'display':'inline-block', 'width':'400px'},
                                                children = [
                                                    dcc.DatePickerSingle(
                                                        id='einddatum',
                                                        display_format = 'DD-MM-YYYY'
                                                        
                                                    )
                                                ]
                                            ),                                                                         
                                        ]
                                    ),




                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block', 'width':'10%'},
                                                children = ['Manager']
                                            ),
                                            html.Div(
                                                style = {'display':'inline-block'},
                                                children = [
                                                    dcc.Dropdown(
                                                        style = {'width':'400px'},
                                                        id='manager',
                                                        
                                                    )
                                                ]
                                            ),         
                                            html.Div(
                                                style = {'display':'inline-block'},
                                                children = ['(Voeg een gebruiker toe aan de functie \'Managementteam\' om een nieuwe manager toe te voegen)']
                                            ),                                                                       
                                        ]
                                    ),
                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block', 'width':'10%'},
                                                children = ['Functie']                                                
                                            ),
                                            html.Div(
                                                style = {'display':'inline-block'},
                                                children = [
                                                    dcc.Dropdown(
                                                        style = {'width':'400px'},
                                                        id='functie',
                                                        
                                                    )
                                                ]
                                            ),                                               
                                        ]
                                    ),
                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block', 'width':'10%'},
                                                children = ['Toelichting']
                                            ),
                                            html.Div(
                                                style = {'display':'inline-block'},
                                                children = [
                                                    dcc.Textarea(
                                                        style = {'width':'400px', 'height':'300'},
                                                        id='toelichting',
                                                        
                                                    )
                                                ]
                                            ),                                    
                                        ]
                                    ),
                                    html.Button(
                                        'Annuleren',
                                        id = 'cancelUserChangeBtn',
                                        n_clicks = 0,
                                        style = cssStyles['button'],
                                    ),
                                    html.Button(
                                        'Wijzigingen opslaan',
                                        id = 'saveMetaBtn',
                                        n_clicks = 0,
                                        style = cssStyles['button'],
                                    ),

                                    html.Div(
                                        id='saveMetaOutput',
                                        children = []
                                    ),






                                ]



                            ),

                            html.H3(''),

                            html.Div(
                                id='appsPerUserDiv',
                                style = cssStyles['changeUserBlock'],
                                children = [
                                    html.Div(
                                        id = 'changeUserAppsDiv',
                                    ),
                                    html.Button(
                                        'Applicatietoegang opslaan',
                                        id='saveAppsBtn',
                                        n_clicks= 0,
                                        style = cssStyles['button']
                                    ),
                                    html.Div(
                                        id='outputSaveApps'
                                    )
                                ]

                            ),      

                        ]
        
                    ),

                    html.H1(''),

                    html.Div(
                        
                        children = [
                            html.Div(id='titelTable', children =[ html.H2('Gebruikers')] ),
                            html.Div(
                                id = 'datatableDiv',
                                style = cssStyles['block'],
                                children = [
                                    
                                ]
                            ),      

                        ]
        
                    ),
                ]
            ),


            dcc.Tab(
                style=tab_style, selected_style=tab_selected_style,  
                label = 'Applicaties',
                children = [
                    html.Div(
                        children = [
                            dcc.Markdown('## Filters'),

                    html.Div(
                        id = 'appFilter',
                        style = cssStyles['block'],
                        children=[

                            html.Div(
                                children = [
                                    html.Div(

                                        children = [
                                            html.Div(
                                                style={'display':'inline-block',
                                                    'width':'10%'},
                                                children = [
                                                    dcc.Markdown(
                                                        '### Applicatie',
                                                    )   
                                                ]
            
                                            ),
                                            html.Div(
                                                style={'display':'inline-block',
                                                    #    'width': '500px'},
                                                        'width': '80%'},
                                                children = [

                                                    dcc.Dropdown(
                                                        id = 'appChangerChooserDropdown',
                                                        value = [],
                                                        options = [{'label': i[1], 'value': i[0]} for i in t['rtapps'].sort_values(by=['Applicatie']).values.tolist()],
                                                        multi=True,
                                                    )    
                                                ]
            
                                            ),                                                               
                                        ]
                                    ),                            
                          
                                ]

                            ),
                            html.Button(
                                'Nieuwe applicatie toevoegen',
                                id = 'newAppBtn',
                                n_clicks=0,
                                style = cssStyles['button'],
                            ),                            
                            html.Button(
                                'Applicatie wijzigen',
                                id = 'changeAppBtn',
                                n_clicks=0,
                                style = {'display':'none'},
                            ),
                        ]
                    ),


                    html.H1(''),


                    html.Div(
                        id='newAppTitleDiv', 
                        style = {'display':'none'},
                        children =[ html.H2('Nieuwe applicatie')] 
                    ),                    



                    html.Div(
                        id='newAppDiv',
                        style = {'display':'none'},
                        children = [
                            html.Div(
                                id='newAppMetaDiv',
                                style = {'display':'none'},
                                children = [
                                    dcc.Checklist(
                                        id='newAppDeleted',
                                        options = ['Verwijderd'],
                                        value = []
                                    ),
                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block','width': '10%'},
                                                children = ['Applicatie']


                                            ),
                                            html.Div(
                                                style = {'display':'inline-block'},
                                                children = [
                                                    dcc.Input(
                                                        style = {'width':'400px'},
                                                        id='newAppName'
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block','width': '10%'},
                                                children = ['Toelichting']


                                            ),
                                            html.Div(
                                                style = {'display':'inline-block'},
                                                children = [
                                                    dcc.Input(
                                                        style = {'width':'400px'},
                                                        id='newAppToelichting'
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),                                    
                                    html.Button(
                                        'Annuleren',
                                        id = 'cancelNewAppBtn',
                                        n_clicks = 0,
                                        style = cssStyles['button'],
                                    ),
                                    html.Button(
                                        'Nieuwe applicatie opslaan',
                                        id = 'saveNewAppBtn',
                                        n_clicks = 0,
                                        style = cssStyles['button'],
                                    ),

                                    html.Div(
                                        id='saveNewAppOutput',
                                        children = []
                                    ),






                                ]
                            )
                        ]
                    ),


                    html.Div(
                        id='changeAppTitleDiv', 
                        style = {'display':'none'},
                        children =[ html.H2('Wijzig applicatie')] 
                    ),                    



                    html.Div(
                        id='changeAppDiv',
                        style = {'display':'none'},
                        children = [
                            html.Div(
                                id='changeAppMetaDiv',
                                style = {'display':'none'},
                                children = [
                                    dcc.Checklist(
                                        id='appDeleted',
                                        options = ['Verwijderd'],
                                        value = []
                                    ),
                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block','width': '10%'},
                                                children = ['Applicatie']


                                            ),
                                            html.Div(
                                                style = {'display':'inline-block'},
                                                children = [
                                                    dcc.Input(
                                                        style = {'width':'400px'},
                                                        id='changeAppName'
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        children = [
                                            html.Div(
                                                style = {'display':'inline-block','width': '10%'},
                                                children = ['Toelichting']


                                            ),
                                            html.Div(
                                                style = {'display':'inline-block'},
                                                children = [
                                                    dcc.Input(
                                                        style = {'width':'400px'},
                                                        id='changeAppToelichting'
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Button(
                                        'Wijzigingen opslaan',
                                        id = 'saveAppMetaBtn',
                                        n_clicks = 0,
                                        style = cssStyles['button'],
                                    ),

                                    html.Div(
                                        id='saveAppMetaOutput',
                                        children = []
                                    ),






                                ]
                            )
                        ]
                    ),





                    html.H1(''),

                    html.Div(
                        
                        children = [
                            html.Div(id='titeApplTable', children =[ html.H2('Applicaties')] ),
                            html.Div(
                                id = 'datatableAppDiv',
                                style = cssStyles['block'],
                                children = [
                                    
                                ]
                            ),      

                        ]
        
                    ),




















                        ]
                    )
                ]
            ), 

            dcc.Tab(
                style=tab_style, selected_style=tab_selected_style,  
                label = 'Functies',
                children = [
                    html.Div(
                        children = [
                            dcc.Markdown('## Filters'),

                            html.Div(
                                id='functiesFilter',
                                style = cssStyles['block'],
                                children = [
                                    html.Div(
                                        children = [
                                            html.Div(
                                                children = [
                                                    html.Div(
                                                        style={'display':'inline-block',
                                                            'width':'10%'},
                                                        children = [
                                                            dcc.Markdown(
                                                                '### Functie',
                                                            )   
                                                        ]
                    
                                                    ),
                                                    html.Div(
                                                        style={'display':'inline-block',
                                                                'width': '80%'},
                                                        children = [

                                                            dcc.Dropdown(
                                                                id = 'functionChangerChooseDropdown',
                                                                value = [],
                                                                options = [{'label': '', 'value': ''}]+[{'label': i[1], 'value': i[0]} for i in t['rtfunctions'].values.tolist()],
                                                                multi=True,
                                                            )    
                                                        ]
                    
                                                    ),                                                        
                                                ]
                                            )
                                            
                                        ]
                                    ),

                                    html.Button(
                                        'Nieuwe functie toevoegen',
                                        id = 'newFunctionBtn',
                                        n_clicks=0,
                                        style = cssStyles['button'],
                                    ),                            
                                    html.Button(
                                        'Functie wijzigen',
                                        id = 'changeFunctionBtn',
                                        n_clicks=0,
                                        style = {'display':'none'},
                                    ),

                                    html.H1(''),

                                ]
                            ),

                            html.Div(
                                id='newFunctionTitleDiv',
                                style = {'display':'none'},
                                children = [html.H2('Nieuwe functie')]
                            ),


                            html.Div(
                                id='newFunctionDiv',
                                style = {'display':'none'},
                                children = [
                                    html.Div(
                                        id = 'newFunctionMetaDiv',
                                        style = {'display':'none'},
                                        children = [
                                            dcc.Checklist(
                                                id='newFunctionDeleted',
                                                options = ['Verwijderd'],
                                                value = []
                                            ),
                                            html.Div(
                                                children = [
                                                    html.Div(
                                                        style = {'display':'inline-block', 'width':'10%'},
                                                        children = ['Functie']
                                                    ),
                                                    html.Div(
                                                        style = {'display':'inline-block'},
                                                        children = [
                                                            dcc.Input(
                                                                style = {'width':'400px'},
                                                                id='newFunctionName'
                                                            )
                                                        ]                                                                
                                                    )
                                                ]
                                            ),


                                            html.Button(
                                                'Annuleren',
                                                id = 'cancelNewFunctionBtn',
                                                n_clicks = 0,
                                                style = cssStyles['button'],
                                            ),
                                            html.Button(
                                                'Nieuwe functie opslaan',
                                                id = 'saveNewFunctionBtn',
                                                n_clicks = 0,
                                                style = cssStyles['button'],
                                            ),

                                            html.Div(
                                                id='saveNewFunctionOutput',
                                                children = []
                                            ),



                                        ]
                                    )
                                ]
                            ),

                            html.Div(
                                id='changeFunctionTitleDiv',
                                style = {'display':'none'},
                                children = [html.H2('Wijzig functie')]
                            ),

                            html.Div(
                                id='changeFunctionDiv',
                                style = {'display':'none'},
                                children = [
                                    html.Div(
                                        id = 'changeFunctionMetaDiv',
                                        style = {'display':'none'},
                                        children = [
                                            dcc.Checklist(
                                                id = 'functionDeleted',
                                                options = ['Verwijderd'],
                                                value = []
                                            ),
                                            html.Div(
                                                children = [
                                                    html.Div(
                                                        style = {'display':'inline-block','width': '10%'},
                                                        children = ['Functie']                                                        
                                                    ),
                                                    html.Div(
                                                        style = {'display':'inline-block'},
                                                        children = [
                                                            dcc.Input(
                                                                style = {'width':'400px'},
                                                                id='changeFunctionName'
                                                            )
                                                        ]
                                                    ),                                                    
                                                ]
                                            ),
                                            html.Button(
                                                'Wijzigingen opslaan',
                                                id = 'saveFunctionMetaBtn',
                                                n_clicks = 0,
                                                style = cssStyles['button'],
                                            ),

                                            html.Div(
                                                id='saveFunctionMetaOutput',
                                                children = []
                                            ),


                                        ]
                                    )
                                ]
                            ),
                            html.H1(''),

                            html.Div(
                                
                                children = [
                                    html.Div(id='titleFunctionTable', children =[ html.H2('Applicaties')] ),
                                    html.Div(
                                        id = 'dataTableFunctionDiv',
                                        style = cssStyles['block'],
                                        children = [
                                            
                                        ]
                                    ),      

                                ]
                
                            ),                            






                        ]
                    )
                ]
            ),        
         
        ]),






        ]


        

    )
