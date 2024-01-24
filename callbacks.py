from dash.dependencies import Output, Input
from dash import no_update
from dash import dash_table
from dash import dcc
from dash import ALL, Patch
import pandas as pd
from functions import *
from styles import layoutStyles
from dash import html
from dash import dcc
from dash.exceptions import PreventUpdate
from database import *

cssStyles = layoutStyles()

def register_callbacks(app):




    ## USERS


    @app.callback(
        [
            Output('changeUserTitleDiv', 'style'),
            Output('changeUserDiv','style'),
            Output('changeUserBtn', 'n_clicks'),
            Output('changeUserAppsDiv', 'children'),
            Output('userDeleted','value'),
            Output('voornaam', 'value'),
            Output('voorvoegsels', 'value'),
            Output('achternaam', 'value'),
            Output('email', 'value'),
            Output('aduser', 'value'),
            Output('topdesk_in', 'value'),
            Output('topdesk_uit', 'value'),
            Output('begindatum', 'date'),
            Output('einddatum', 'date'),
            Output('manager', 'value'),
            Output('manager','options'),
            Output('toelichting', 'value'),
            Output('newUserBtn','n_clicks'),
            Output('newOrChangeUser','data'),
            Output('functie','value'),
            Output('functie','options'),
            Output('appsPerUserDiv','style'),
            Output('changeUserTitleDiv','children'),
            Output('cancelUserChangeBtn','n_clicks'),
            Output('newUserBtn','children'),
            Output('newUserBtn','style'),

        ],
        [
            Input('changeUserBtn', 'n_clicks'),
            Input('chosenUser','data'),
            Input('newUserBtn','n_clicks'),
            Input('cancelUserChangeBtn','n_clicks'),
        ]
        
    )
    def functie(changeUserBtn, chosenUser, newUserBtn, cancelUserChangeBtn):
        changeUserTitleDivStyle_r = no_update
        changeUserDiv_r = no_update
        changeUserBtn_r = 0,
        changeUserAppsDiv_r = no_update
        userDeleted_r = no_update
        voornaam_r = no_update 
        voorvoegsels_r = no_update 
        achternaam_r = no_update 
        email_r = no_update 
        aduser_r = no_update 
        topdesk_in_r = no_update 
        topdesk_uit_r = no_update 
        begindatum_r = no_update 
        einddatum_r = no_update 
        manager_r = no_update 
        manager_options_r = no_update
        toelichting_r = no_update 
        newUserBtn_r = 0
        newOrChangeUser_r = no_update
        functie_r = no_update
        functieOptions_r = no_update
        appsPerUserDivStyle_r = no_update
        changeUserTitleDivChildren_r = no_update
        cancelUserChangeBtn_r = 0
        newUserBtnChildren_r = 'Nieuwe gebruiker toevoegen'
        newUserBtnStyle_r = cssStyles['button']



        patched_children = Patch()
        for i in range(100):
            del patched_children[i]

        t = readTables()

        d = t['allData'][t['allData']['id_user'] == chosenUser]

        uData = t['users'][t['users']['id_user']==chosenUser].reset_index().to_dict()

        if changeUserBtn > 0:
            newUserBtnStyle_r = cssStyles['button']
            newUserBtnChildren_r = 'Gebruiker kopiëren'
            newOrChangeUser_r = 'change'
            if uData['Status gebruiker'][0]==1:
                userDeleted_r = []
            else:
                userDeleted_r = ['Verwijderd']
            voornaam_r = uData['Voornaam'][0]
            voorvoegsels_r = uData['Voorvoegsels'][0]
            achternaam_r = uData['Achternaam'][0]
            email_r = uData['Emailadres'][0]
            aduser_r = uData['AD gebruikersnaam'][0]
            topdesk_in_r = uData['TOPdesk in dienst'][0]
            topdesk_uit_r = uData['TOPdesk uit dienst'][0]
            functie_r = uData['id_function'][0]

            try:
                begindatum_r = db_to_dateTime(uData['Begindatum'][0]).date()
            except:
                begindatum_r = None
            try:
                einddatum_r = db_to_dateTime(uData['Einddatum'][0]).date()
            except:
                einddatum_r = None
            manager_r = uData['id_manager'][0]
            toelichting_r = uData['Toelichting'][0]

            managers = t['users'][t['users']['function']== 'Managementteam'][['id_user','Sorteernaam','Status gebruiker']].rename(columns={'Sorteernaam':'managerNaam'})
            deletedManager = managers[managers['Status gebruiker']==9]['managerNaam'].values.tolist()
            managers['managerNaam'] = managers['managerNaam'].apply(lambda x: x + ' (verwijderd)' if x in deletedManager else (x))

            manager_options_r = [{'label': i[1], 'value': i[0]} for i in managers.sort_values(by=['Status gebruiker','managerNaam']).values.tolist()]

            functieOptions_r = [{'label': i[1], 'value': i[0]} for i in t['rtfunctions'][t['rtfunctions']['sts_rec']==1].values.tolist()]


            changeUserTitleDivStyle_r = {'display':'block'}
            changeUserDiv_r = cssStyles['block']

            x = 0
            for i in t['rtapps'][['id_app','Applicatie']].sort_values(by=['Applicatie']).values.tolist():
                if len(d[d['id_app']==i[0]])>0:
                    v = [i[1] + ' ('+i[0]+')']
                else:
                    v = []
                p = html.Div(
                    children = [

                        html.Div(
                            style = {'display':'inline-block'},
                            children = [
                                dcc.Checklist(
                                    id = {'type': 'appsChecklist','index': i[0]},
                                    options = [i[1] + ' ('+i[0]+')'],
                                    value = v
                                )
                            ]
                        )
                    ]
                )

                x += 1

                patched_children.append(p)

                changeUserAppsDiv_r = patched_children

        elif newUserBtn > 0:
            newUserBtnStyle_r = {'display':'none'}
            newOrChangeUser_r = 'new'

            managers = t['users'][t['users']['function']== 'Managementteam'][['id_user','Sorteernaam','Status gebruiker']].rename(columns={'Sorteernaam':'managerNaam'})
            deletedManager = managers[managers['Status gebruiker']==9]['managerNaam'].values.tolist()
            managers['managerNaam'] = managers['managerNaam'].apply(lambda x: x + ' (verwijderd)' if x in deletedManager else (x))

            manager_options_r = [{'label': i[1], 'value': i[0]} for i in managers.sort_values(by=['Status gebruiker','managerNaam']).values.tolist()]
            functieOptions_r = [{'label': i[1], 'value': i[0]} for i in t['rtfunctions'][t['rtfunctions']['sts_rec']==1].values.tolist()]

            userDeleted_r = []
            voornaam_r = None
            voorvoegsels_r = None
            achternaam_r = None
            email_r = None
            aduser_r = None
            topdesk_in_r = None
            topdesk_uit_r = None
            begindatum_r = None
            einddatum_r = None
            manager_r = None
            toelichting_r = None
            functie_r = None


            changeUserTitleDivStyle_r = {'display':'block'}
            changeUserDiv_r = cssStyles['block']


            x = 0
            for i in t['rtapps'][['id_app','Applicatie']].sort_values(by=['Applicatie']).values.tolist():
                v = []
                p = html.Div(
                    children = [

                        html.Div(
                            style = {'display':'inline-block'},
                            children = [
                                dcc.Checklist(
                                    id = {'type': 'appsChecklist','index': i[0]},
                                    options = [i[1] + ' ('+i[0]+')'],
                                    value = v
                                )
                            ]
                        )
                    ]
                )

                x += 1

                patched_children.append(p)

                changeUserAppsDiv_r = patched_children

        elif cancelUserChangeBtn > 0:
            newUserBtnStyle_r = cssStyles['button']
            changeUserBtnStyle_r = cssStyles['button']
            changeUserDiv_r = {'display':'none'}


        if newOrChangeUser_r == 'new':
            appsPerUserDivStyle_r = {'display':'none'}
            changeUserTitleDivChildren_r = html.H2('Nieuwe gebruiker')
        elif newOrChangeUser_r == 'change':
            changeUserTitleDivChildren_r = html.H2('Wijzig gebruiker')
            appsPerUserDivStyle_r = cssStyles['changeUserBlock']


        elif chosenUser == None:
            changeUserTitleDivStyle_r = {'display':'none'}
            changeUserDiv_r = {'display':'none'}
            changeUserAppsDiv_r = html.Div()
        

        return [
            changeUserTitleDivStyle_r,
            changeUserDiv_r,
            0,
            changeUserAppsDiv_r,
            userDeleted_r,
            voornaam_r,
            voorvoegsels_r,
            achternaam_r,
            email_r,
            aduser_r,
            topdesk_in_r,
            topdesk_uit_r,
            begindatum_r,
            einddatum_r,
            manager_r,
            manager_options_r, 
            toelichting_r,
            newUserBtn_r,
            newOrChangeUser_r,
            functie_r,
            functieOptions_r,
            appsPerUserDivStyle_r,
            changeUserTitleDivChildren_r,
            cancelUserChangeBtn_r,
            newUserBtnChildren_r,
            newUserBtnStyle_r,
        ]

    @app.callback(
        [
            Output('defaultAppsDiv','children'),

        ],
        [
            Input('functie_tbv_functiematrix','data'),
        ]
    )

    def funct(functie):
        t = readTables()
        f = t['functionmatrix'].merge(t['rtapps'], on='id_app', how='left')
        txt = ''
        for i in f[f['id_function']==functie]['Applicatie'].values.tolist():
            txt += '* '+ i + '\n'
        
        return [dcc.Markdown(txt)]


    @app.callback(
        [
            Output('changeFunctionMatrixBtn','n_clicks'),
            Output('changeFunctionAppsDiv','children'),
            Output('changeFunctionMatrixTitleDiv','style'),
            Output('appsPerFunctionDiv','style'),
            Output('saveAppsMatrixBtn','style'),
        ],
        [
            Input('changeFunctionMatrixBtn','n_clicks'),
            Input('chosenFunctionMatrix','data'),

        ]
    )

    def func(changeFunctionMatrixBtn, chosenFunctionMatrix):
        changeFunctionMatrixBtn_r = 0
        changeFunctionMatrixTitleDivStyle_r = no_update
        appsPerFunctionDivStyle_r = no_update 
        changeFunctionAppsDiv_r = no_update
        saveAppsMatrixBtnStyle_r = no_update

        patched_childrenFunctionMatrix = Patch()
        for i in range(500):
            del patched_childrenFunctionMatrix[i]
        

        if changeFunctionMatrixBtn > 0:

            appsPerFunctionDivStyle_r = cssStyles['changeUserBlock']
            changeFunctionMatrixTitleDivStyle_r = {'display':'block'}
            saveAppsMatrixBtnStyle_r = cssStyles['button']

            t = readTables()
            
            for i in t['rtapps'][['id_app','Applicatie']].sort_values(by=['Applicatie']).values.tolist():
                if len(t['functionmatrix'][(t['functionmatrix']['id_function']==chosenFunctionMatrix) & (t['functionmatrix']['id_app'] == i[0])]) > 0:
                    v = [i[1] + ' ('+ i[0]+')']
                else:
                    v = []
                p = html.Div(
                    children = [
                        html.Div(
                            style = {'display':'inline-block'},
                            children = [
                                dcc.Checklist(
                                    id = {'type': 'functionMatrixChecklist','index': i[0]},
                                    options = [i[1] + ' ('+i[0]+')'],
                                    value = v
                                )
                            ]
                        )                        
                    ]
                )


                patched_childrenFunctionMatrix.append(p)


                changeFunctionAppsDiv_r = patched_childrenFunctionMatrix

        elif chosenFunctionMatrix == None or chosenFunctionMatrix == []:
            changeFunctionMatrixTitleDivStyle_r = {'display':'none'}
            appsPerFunctionDivStyle_r = {'display':'none'}
            changeFunctionAppsDiv_r = html.Div()

            saveAppsMatrixBtnStyle_r = {'display':'none'}
        


        return [
            changeFunctionMatrixBtn_r,
            changeFunctionAppsDiv_r,
            changeFunctionMatrixTitleDivStyle_r,
            appsPerFunctionDivStyle_r,
            saveAppsMatrixBtnStyle_r,

        ]




    @app.callback(
        [
            Output('saveMetaOutput','children'),
            Output('saveMetaBtn','n_clicks'),
            Output('functie_tbv_functiematrix','data'),
        ],
        [
            Input('saveMetaBtn','n_clicks'),
            Input('userDeleted','value'),
            Input('voornaam','value'),
            Input('voorvoegsels','value'),
            Input('achternaam','value'),
            Input('email','value'),
            Input('aduser','value'),
            Input('topdesk_in','value'),
            Input('topdesk_uit','value'),
            Input('begindatum','date'),
            Input('einddatum','date'),
            Input('manager','value'),
            Input('toelichting','value'),
            Input('chosenUser_tbv_saveMeta', 'data'),
            Input('newOrChangeUser','data'),
            Input('functie','value'),


        ]
    )


    def functie(saveMetaBtn,userDeleted, voornaam, voorvoegsels, achternaam, email, aduser, topdesk_in, topdesk_uit, begindatum, einddatum, manager, toelichting, chosenUser, newOrChangeUser, functie):
        saveMetaOutput_r = no_update 
        saveMetaBtn_r = 0
        functie_tbv_functiematrixData_r = no_update

        if begindatum != None:
            begindatum += '_00:00'
        if einddatum != None:
            einddatum += '_00:00'            

        if saveMetaBtn > 0:
       
            if newOrChangeUser == 'change':
                o = changeUserMeta(chosenUser, voornaam, voorvoegsels, achternaam, email, aduser, topdesk_in, topdesk_uit, begindatum, einddatum, manager, toelichting, userDeleted)
                o += '\n\n' + delFunctionForUser(chosenUser)
                o += '\n\n' + addFunctionToUser(functie, chosenUser, datetime.now())
                saveMetaOutput_r = o
            elif newOrChangeUser == 'new':
                if userDeleted == []:
                    userDeleted = 1
                elif userDeleted == ['Verwijderd']:
                    userDeleted = 9
                else:
                    print('Logisch verwijderd niet uit te lezen. Ik heb er 7 van gemaakt.')
                    userDeleted = 7
                o = addUser(voornaam, voorvoegsels, achternaam, email, aduser, topdesk_in, topdesk_uit, begindatum, toelichting=toelichting, dd_eind=einddatum, sts_rec=userDeleted, id_manager=manager)

                u = readTable('users')
                chosenUser = u.values.tolist()[-1][0]                

                o += addFunctionToUser(functie, chosenUser, datetime.now())
                saveMetaOutput_r = o

        functie_tbv_functiematrixData_r = functie


        return [
            saveMetaOutput_r ,
            saveMetaBtn_r,
            functie_tbv_functiematrixData_r,
        ]






    @app.callback(
        [
            Output('outputSaveApps','children'),
            Output('saveAppsBtn','n_clicks'),
        ],
        [
            Input('saveAppsBtn','n_clicks'),
            Input({'type': 'appsChecklist','index': ALL}, "value"),
            Input('chosenUser_tbv_saveApps','data'),
        ]
    )
    def functietje(saveAppsBtn, values,chosenUser):
        outputSaveApps_r = no_update
        saveAppsBtn_r = 0



        if saveAppsBtn > 0:
            deleteAppsForUser(chosenUser)
            for i in values:
                if i != []:
                    addUserToApp(i[0][-37:-1], chosenUser, datetime.now())



        return [
            outputSaveApps_r,
            saveAppsBtn_r,
        ]




    @app.callback(
        [
            Output('outputSaveAppsMatrix','children'),
            Output('saveAppsMatrixBtn','n_clicks'),
            Output('functieMatrixHelper','data'),
        ],
        [
            Input('saveAppsMatrixBtn','n_clicks'),
            Input({'type': 'functionMatrixChecklist','index': ALL}, "value"),
            Input('chosenFunctionMatrix_tbv_saveMeta','data'),
        ]
    )
    def functietje(saveAppsMatrixBtn, values,chosenFunctionMatrix):
        outputSaveAppsMatrix_r = no_update
        saveAppsMatrixBtn_r = 0
        functieMatrixHelper_r = no_update



        if saveAppsMatrixBtn > 0:
            vals = []
            for val in values:
                if not val == []:
                    vals.append(val[0][-37:-1])
            changeFunctionMatrix(chosenFunctionMatrix, vals)
            functieMatrixHelper_r = 'something'



        return [
            outputSaveAppsMatrix_r,
            saveAppsMatrixBtn_r,
            functieMatrixHelper_r,
        ]



    @app.callback(
            [
                Output('datatableDiv', 'children'),
                Output('userChooserDropdown', 'options'),
                Output('functionChooserDropdown','options'),
                Output('appChooserDropdown','options'),
                Output('changeUserBtn','style'),
                Output('chosenUser','data'),
                Output('chosenUser_tbv_saveMeta','data'),
                Output('chosenUser_tbv_saveApps','data'),
                Output('chosenApp','data'),
                Output('changeAppBtn','style'),
                Output('chosenApp_tbv_saveMeta','data'),
                Output('datatableAppDiv','children'),
                Output('chosenFunction','data'),
                Output('changeFunctionBtn','style'),
                Output('chosenFunction_tbv_saveMeta','data'),
                Output('dataTableFunctionDiv','children'),
                Output('appChangerChooserDropdown','options'),
                Output('functionChangerChooseDropdown', 'options'),
                Output('functionMatrixChangerChooseDropdown','options'),
                Output('changeFunctionMatrixBtn','style'),
                Output('chosenFunctionMatrix_tbv_saveMeta','data'),
                Output('chosenFunctionMatrix','data'),

            ],
            [
                Input('refreshBtn', 'n_clicks'),
                Input('appChooserDropdown', 'value'),
                Input('functionChooserDropdown', 'value'),
                Input('userChooserDropdown', 'value'),
                Input('appInclVerwijderd', 'value'),
                Input('functieInclVerwijderd', 'value'),
                Input('userInclVerwijderd','value'),
                Input('appChangerChooserDropdown','value'),
                Input('changeUserTitleDiv', 'style'),
                Input('functionChangerChooseDropdown','value'),
                Input('functionMatrixChangerChooseDropdown','value'),
                Input('changeFunctionMatrixTitleDiv','style'),





            ]
    )
    def functie(refreshBtn, appChooserDropdown, functionChooserDropdown, userChooserDropdown, appInclVerwijderd, functieInclVerwijderd, userInclVerwijderd, appChangerChooserDropdown, changeUserTitleDivStyle, functionChangerChooseDropdown, functionMatrixChangerChooseDropdown, changeFunctionMatrixTitleDivStyle):
        datatableDiv_r = no_update
        userChooserDropdown_r = no_update
        functionChooserDropdown_r = no_update
        appChooserDropdown_r = no_update
        changeUserBtnStyle_r = no_update
        chosenUserData_r = no_update
        chosenUser_tbv_saveMeta_r = no_update
        chosenUser_tbv_saveApps_r = no_update
        chosenAppData_r = no_update
        changeAppBtnStyle_r = no_update
        chosenApp_tbv_saveMeta_r = no_update
        datatableAppDiv_r = no_update
        chosenFunctionData_r = no_update
        changeFunctionBtnStyle_r = no_update
        chosenFunction_tbv_saveMeta_r = no_update
        datatableFunctionDiv_r = no_update
        appChangerChooserDropdownOptions_r = no_update
        functionChangerChooseDropdownOptions_r = no_update
        functionMatrixChangerChooseDropdownOptions_r = no_update
        changeFunctionMatrixBtnStyle_r = no_update 
        chosenFunctionMatrixData_r = no_update 
        chosenFunctionMatrix_tbv_saveMeta_r = no_update    

        def inclVerwijderd(gegeven):
            if gegeven == ['Inclusief verwijderd']:
                gegeven = [1,9,'']
            else:
                gegeven = [1,'']
            return gegeven

        functieInclVerwijderd = inclVerwijderd(functieInclVerwijderd)
        userInclVerwijderd = inclVerwijderd(userInclVerwijderd)
        appInclVerwijderd = inclVerwijderd(appInclVerwijderd)


        t = readTables()

        if functionChooserDropdown == [''] or functionChooserDropdown == [] or functionChooserDropdown == None:
            functionChooserDropdown = t['rtfunctions'][t['rtfunctions']['sts_rec'].isin(functieInclVerwijderd)]['id_function'].values.tolist() + ['']
        elif '' in functionChooserDropdown:
            functionChooserDropdown += ['']
        if appChooserDropdown == [''] or appChooserDropdown == [] or appChooserDropdown == None:
            appChooserDropdown = t['rtapps'][t['rtapps']['sts_rec'].isin(appInclVerwijderd)]['id_app'].values.tolist() + ['']
        elif '' in appChooserDropdown:
            appChooserDropdown += ['']
        if userChooserDropdown == [''] or userChooserDropdown == [] or userChooserDropdown == None:
            userChooserDropdown = t['users'][t['users']['Status gebruiker'].isin(userInclVerwijderd)]['id_user'].values.tolist() + ['']
        elif '' in userChooserDropdown:
            userChooserDropdown += ['']
        if functionChangerChooseDropdown == [''] or functionChangerChooseDropdown == [] or functionChangerChooseDropdown == None: 
            functionChangerChooseDropdown = t['rtfunctions']['id_function'].values.tolist() + ['']
        
        if functionMatrixChangerChooseDropdown == [''] or functionMatrixChangerChooseDropdown == [] or functionMatrixChangerChooseDropdown == None: 
            functionMatrixChangerChooseDropdown = t['rtfunctions']['id_function'].values.tolist() + ['']
        

        t['allData'] = t['allData'].fillna('')
        
        ddData = t['allData'][(t['allData']['id_function'].isin(functionChooserDropdown))\
            & (t['allData']['id_app'].isin(appChooserDropdown))\
                & (t['allData']['id_user'].isin(userChooserDropdown))\
                    & (t['allData']['Status app'].isin(appInclVerwijderd))\
                        & (t['allData']['Status gebruiker'].isin(userInclVerwijderd))\
                            & (t['allData']['Status functie'].isin(functieInclVerwijderd))].sort_values(by=['Sorteernaam','function','Applicatie'])

        appChooserDropdown_r = [{'label':'(leeg)','value': ''}] + [{'label': i[1], 'value': i[0]} for i in t['rtapps'][t['rtapps']['sts_rec'].isin(appInclVerwijderd)].sort_values(by=['Applicatie']).values.tolist()]
        appChangerChooserDropdownOptions_r = [{'label':'(leeg)','value': ''}] + [{'label': i[1], 'value': i[0]} for i in t['rtapps'].sort_values(by=['Applicatie']).values.tolist()]
        functionChooserDropdown_r = [{'label':'(leeg)','value': ''}] + [{'label': i[1], 'value': i[0]} for i in t['rtfunctions'][t['rtfunctions']['sts_rec'].isin(functieInclVerwijderd)].sort_values(by=['function']).values.tolist()]
        functionChangerChooseDropdownOptions_r = [{'label':'(leeg)','value': ''}] + [{'label': i[1], 'value': i[0]} for i in t['rtfunctions'].sort_values(by=['function']).values.tolist()]
        functionMatrixChangerChooseDropdownOptions_r = [{'label':'(leeg)','value': ''}] + [{'label': i[1], 'value': i[0]} for i in t['rtfunctions'].sort_values(by=['function']).values.tolist()]
        userChooserDropdown_r = [{'label':'(leeg)','value': ''}] + [{'label': i[1] + ' ('+i[2]+')', 'value': i[0]} for i in ddData[['id_user','Sorteernaam', 'Emailadres']].drop_duplicates().values.tolist()]



        df = usersPerApp(appChooserDropdown, functionChooserDropdown, userChooserDropdown)
        
        table = dash_table.DataTable(
                data=df.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df.columns],
                filter_action="native",
                sort_action="native",
                sort_mode='multi',                
                style_table={"width": "100%", "align": 'center'},
                style_filter={'backgroundColor': 'black'}, 
                style_header={'backgroundColor': 'black'},
                style_cell={'backgroundColor': '#303230', 'color': 'white'}
                )

        if appChangerChooserDropdown == []:
            appsChosen = t['rtapps']['id_app'].values.tolist()+ ['']
        else:
            appsChosen = appChangerChooserDropdown

        

        apps = t['rtapps'][t['rtapps']['id_app'].isin(appsChosen)].sort_values(by=['Applicatie']).rename(columns = {
            'id_app': 'Applicatie-ID',
            'sts_rec': 'Verwijderd',
        })

        functions = t['rtfunctions'][t['rtfunctions']['id_function'].isin(functionChangerChooseDropdown)].sort_values(by='function').rename(columns = {'id_function':'Functie-ID','function':'Functie','sts_rec':'Verwijderd'})

        functionsTable = dash_table.DataTable(
                data=functions.to_dict("records"),
                columns=[{"name": i, "id": i} for i in functions.columns],
                filter_action="native",
                sort_action="native",
                sort_mode='multi',                   
                style_table={"width": "100%", "align": 'center'},
                style_filter={'backgroundColor': 'black'}, 
                style_header={'backgroundColor': 'black'},
                style_cell={'backgroundColor': '#303230', 'color': 'white'}
                )   

        appsTable = dash_table.DataTable(
                data=apps.to_dict("records"),
                columns=[{"name": i, "id": i} for i in apps.columns],
                filter_action="native",
                sort_action="native",
                sort_mode='multi',                   
                style_table={"width": "100%", "align": 'center'},
                style_filter={'backgroundColor': 'black'}, 
                style_header={'backgroundColor': 'black'},
                style_cell={'backgroundColor': '#303230', 'color': 'white'}
                )        

        datatableAppDiv_r = html.Div(
            children = [
                html.H1(''),
                appsTable,
                html.H1('')
            ]
        )

        datatableFunctionDiv_r = html.Div(
            children = [
                html.H1(''),
                functionsTable,
                html.H1('')
            ]
        )

        datatableDiv_r = html.Div(
            children = [
                html.H1(''),
                table,
                html.H1('')
            ])
        if len(functionChangerChooseDropdown) == 1 and functionChangerChooseDropdown != ['']:
            changeFunctionBtnStyle_r = cssStyles['button']
            chosenFunctionData_r = functionChangerChooseDropdown[0]
        else:
            changeFunctionBtnStyle_r = {'display':'none'}
            chosenFunctionData_r = None

        if len(functionMatrixChangerChooseDropdown) == 1 and functionMatrixChangerChooseDropdown != ['']:
            if changeFunctionMatrixTitleDivStyle == {'display':'none'}:
                changeFunctionMatrixBtnStyle_r = cssStyles['button']
            else:
                changeFunctionMatrixBtnStyle_r = {'display':'none'}
            chosenFunctionMatrixData_r = functionMatrixChangerChooseDropdown[0]
        else:
            changeFunctionMatrixBtnStyle_r = {'display':'none'}
            chosenFunctionMatrixData_r = None


        if len(appChangerChooserDropdown) == 1 and appChangerChooserDropdown != ['']:
            changeAppBtnStyle_r = cssStyles['button']
            chosenAppData_r = appChangerChooserDropdown[0]
        else:
            changeAppBtnStyle_r = {'display':'none'}
            chosenAppData_r = None


        if len(userChooserDropdown) == 1 and userChooserDropdown != ['']:
            if changeUserTitleDivStyle == {'display':'none'}:
                changeUserBtnStyle_r = cssStyles['button']
            else:
                changeUserBtnStyle_r = {'display':'none'}
            chosenUserData_r = userChooserDropdown[0]
        else:
            
            changeUserBtnStyle_r = {'display':'none'}
            chosenUserData_r = None

        chosenUser_tbv_saveMeta_r = chosenUserData_r
        chosenUser_tbv_saveApps_r = chosenUserData_r
        chosenApp_tbv_saveMeta_r = chosenAppData_r
        chosenFunction_tbv_saveMeta_r = chosenFunctionData_r
        chosenFunctionMatrix_tbv_saveMeta_r = chosenFunctionMatrixData_r

        return [
            datatableDiv_r,
            userChooserDropdown_r,
            functionChooserDropdown_r,
            appChooserDropdown_r,
            changeUserBtnStyle_r,
            chosenUserData_r,
            chosenUser_tbv_saveMeta_r,
            chosenUser_tbv_saveApps_r,
            chosenAppData_r,
            changeAppBtnStyle_r,
            chosenApp_tbv_saveMeta_r,
            datatableAppDiv_r,
            chosenFunctionData_r,
            changeFunctionBtnStyle_r,
            chosenFunction_tbv_saveMeta_r,
            datatableFunctionDiv_r,
            appChangerChooserDropdownOptions_r,
            functionChangerChooseDropdownOptions_r,
            functionMatrixChangerChooseDropdownOptions_r,
            changeFunctionMatrixBtnStyle_r,
            chosenFunctionMatrixData_r,
            chosenFunctionMatrix_tbv_saveMeta_r,
            ]
        



    ## APPS
    @app.callback(
        [
            Output('changeAppTitleDiv','style'),
            Output('changeAppDiv','style'),
            Output('changeAppBtn','n_clicks'),
            Output('appDeleted','value'),
            Output('changeAppName', 'value'),
            Output('changeAppMetaDiv','style'),
            Output('changeAppToelichting','value'),

        ],
        [
            Input('changeAppBtn', 'n_clicks'),
            Input('chosenApp','data'),
        ]
        
    )
    def funct(changeAppBtn, chosenApp):
        changeAppTitleDivStyle_r = no_update
        changeAppDivStyle_r = no_update 
        changeAppBtn_r = 0
        appDeleted_r = no_update
        changeAppName_r = no_update
        changeAppMetaDivStyle_r = no_update
        changeAppToelichting_r = no_update


        t = readTables()

        aData = t['rtapps'][t['rtapps']['id_app'] == chosenApp ].reset_index().to_dict()


        if changeAppBtn > 0:
            if aData['sts_rec'][0]==1:
                appDeleted_r = []
            else:
                appDeleted_r = [['Verwijderd'][0]]
            changeAppName_r = aData['Applicatie'][0]
            toelichting_r = aData['toelichting'][0]


            changeAppDivStyle_r = cssStyles['block']
            changeAppTitleDivStyle_r = {'display':'block'}
            changeAppMetaDivStyle_r = cssStyles['changeUserBlock']




        elif chosenApp == None or chosenApp == []:
            changeAppTitleDivStyle_r = {'display':'none'}
            changeAppDivStyle_r = html.Div()
            changeAppMetaDivStyle_r = {'display':'none'}





        return [
            changeAppTitleDivStyle_r,
            changeAppDivStyle_r,
            changeAppBtn_r,
            appDeleted_r,
            changeAppName_r,
            changeAppMetaDivStyle_r,
            changeAppToelichting_r,

        ]







    @app.callback(
        [
            Output('newAppTitleDiv','style'),
            Output('newAppDiv','style'),
            Output('newAppBtn','n_clicks'),
            Output('newAppMetaDiv','style'),
            Output('cancelNewAppBtn','n_clicks'),

        ],
        [
            Input('newAppBtn', 'n_clicks'),
            Input('cancelNewAppBtn','n_clicks'),
        ]
        
    )
    def funct(newAppBtn, cancelNewAppBtn):
        newAppTitleDivStyle_r = no_update
        newAppDivStyle_r = no_update 
        newAppBtn_r = 0
        newAppMetaDivStyle_r = no_update
        cancelNewAppBtn_r = 0


        if newAppBtn > 0:

            newAppDivStyle_r = cssStyles['block']
            newAppTitleDivStyle_r = {'display':'block'}
            newAppMetaDivStyle_r = cssStyles['changeUserBlock']




        elif cancelNewAppBtn > 0:
            newAppTitleDivStyle_r = {'display':'none'}
            newAppDivStyle_r = html.Div()
            newAppMetaDivStyle_r = {'display':'none'}





        return [
            newAppTitleDivStyle_r,
            newAppDivStyle_r,
            newAppBtn_r,
            newAppMetaDivStyle_r,
            cancelNewAppBtn_r,

        ]




    @app.callback(
        [
            Output('saveAppMetaOutput','children'),
            Output('saveAppMetaBtn','n_clicks'),
            Output('resetSaveAppOutputTimer', 'disabled'),
            Output('resetSaveAppOutputTimer','n_intervals'),
        ],
        [
            Input('saveAppMetaBtn','n_clicks'),
            Input('appDeleted','value'),
            Input('changeAppName','value'),
            Input('chosenApp_tbv_saveMeta', 'data'),
            Input('resetSaveAppOutputTimer','n_intervals'),
            Input('resetSaveAppOutputTimer', 'disabled'),            
            Input('changeAppToelichting','value'),


        ]
    )

    def fu(saveAppMetaBtn, appDeleted, changeAppName, chosenApp, resetSaveAppOutputTimer, disabled, changeAppToelichting):
        saveAppMetaOutput_r = no_update 
        saveAppMetaBtn_r = 0
        resetSaveAppOutputTimerDisabled_r = no_update
        resetSaveAppOutputTimerInterval_r = no_update
        resetSaveAppOutputTimerInterval_r = 0


        if saveAppMetaBtn > 0:

            resetSaveAppOutputTimerDisabled_r = False
            
            o = changeAppMeta(chosenApp, changeAppName, appDeleted, toelichting = changeAppToelichting)
            saveAppMetaOutput_r = o


        if resetSaveAppOutputTimer > 0:

            resetSaveAppOutputTimerDisabled_r = True
            saveAppMetaOutput_r = None
            





        return [
            saveAppMetaOutput_r,
            saveAppMetaBtn_r, 
            resetSaveAppOutputTimerDisabled_r,
            resetSaveAppOutputTimerInterval_r,
        ]




    @app.callback(
        [
            Output('saveNewAppOutput', 'children'),
            Output('saveNewAppBtn','n_clicks'),
        ],
        [
            Input('saveNewAppBtn', 'n_clicks'),
            Input('newAppName','value'),
            Input('newAppToelichting', 'value'),
            Input('newAppDeleted','value'),
        ]
    )

    def nieuweApp(saveNewApp, appName, newAppToelichting, appDeleted):
        saveNewAppOutput_r = no_update
        saveNewAppBtn_r = 0

        if appDeleted == []:
            appDeleted = 1
        elif appDeleted == ['Verwijderd']:
            appDeleted = 9            
        else:
            print('Geen juiste waarde bij Verwijderd. 7 gevuld!')
            appDeleted = 7



        if saveNewApp > 0:
            o = addApp(appName, sts_rec=appDeleted, toelichting = newAppToelichting)
            saveNewAppOutput_r = o

        return [
            saveNewAppOutput_r,
            saveNewAppBtn_r,
        ]



    ## FUNCTIES




    @app.callback(
        [
            Output('newFunctionTitleDiv','style'),
            Output('newFunctionDiv','style'),
            Output('newFunctionBtn','n_clicks'),
            Output('newFunctionMetaDiv','style'),
            Output('cancelNewFunctionBtn','n_clicks'),

        ],
        [
            Input('newFunctionBtn', 'n_clicks'),
            Input('cancelNewFunctionBtn','n_clicks'),
        ]
        
    )
    def funct(newFunctionBtn, cancelNewFunctionBtn):
        newFunctionTitleDivStyle_r = no_update
        newFunctionDivStyle_r = no_update 
        newFunctionBtn_r = 0
        newFunctionMetaDivStyle_r = no_update
        cancelNewFunctionBtn_r = 0


        if newFunctionBtn > 0:

            newFunctionDivStyle_r = cssStyles['block']
            newFunctionTitleDivStyle_r = {'display':'block'}
            newFunctionMetaDivStyle_r = cssStyles['changeUserBlock']




        elif cancelNewFunctionBtn > 0:
            newFunctionTitleDivStyle_r = {'display':'none'}
            newFunctionDivStyle_r = html.Div()
            newFunctionMetaDivStyle_r = {'display':'none'}





        return [
            newFunctionTitleDivStyle_r,
            newFunctionDivStyle_r,
            newFunctionBtn_r,
            newFunctionMetaDivStyle_r,
            cancelNewFunctionBtn_r,

        ]    

    @app.callback(
        [
            Output('saveNewFunctionOutput', 'children'),
            Output('saveNewFunctionBtn','n_clicks'),
        ],
        [
            Input('saveNewFunctionBtn', 'n_clicks'),
            Input('newFunctionName','value'),
            Input('newFunctionDeleted','value'),
        ]
    )

    def nieuweFunctie(saveNewFunction, functionName, functionDeleted):
        saveNewFunctionOutput_r = no_update
        saveNewFunctionBtn_r = 0

        if functionDeleted == []:
            functionDeleted = 1
        elif functionDeleted == ['Verwijderd']:
            functionDeleted = 9            
        else:
            print('Geen juiste waarde bij Verwijderd. 7 gevuld!')
            functionDeleted = 7



        if saveNewFunction > 0:
            o = addFunction(functionName, sts_rec=functionDeleted)
            saveNewFunctionOutput_r = o

        return [
            saveNewFunctionOutput_r,
            saveNewFunctionBtn_r,
        ]


    @app.callback(
        [
            Output('saveFunctionMetaOutput','children'),
            Output('saveFunctionMetaBtn','n_clicks'),

        ],
        [
            Input('saveFunctionMetaBtn','n_clicks'),
            Input('functionDeleted','value'),
            Input('changeFunctionName','value'),
            Input('chosenFunction_tbv_saveMeta','data'),
        ]
    )

    def fu(saveFunctionMetaBtn, functionDeleted, changeFunctionName, chosenFunction):
        saveFunctionMetaOutput_r = no_update 
        saveFunctionMetaBtn_r = 0



        if saveFunctionMetaBtn > 0:

            o = changeFunctionMeta(chosenFunction, changeFunctionName, functionDeleted)
            saveFunctionMetaOutput_r = o


            





        return [
            saveFunctionMetaOutput_r,
            saveFunctionMetaBtn_r, 
        ]



    @app.callback(
        [
            Output('changeFunctionTitleDiv','style'),
            Output('changeFunctionDiv','style'),
            Output('changeFunctionBtn','n_clicks'),
            Output('functionDeleted','value'),
            Output('changeFunctionName', 'value'),
            Output('changeFunctionMetaDiv','style'),

        ],
        [
            Input('changeFunctionBtn', 'n_clicks'),
            Input('chosenFunction','data')
        ]
        
    )
    def funct(changeFunctionBtn, chosenFunction):
        changeFunctionTitleDivStyle_r = no_update
        changeFunctionDivStyle_r = no_update 
        changeFunctionBtn_r = 0
        functionDeleted_r = no_update
        changeFunctionName_r = no_update
        changeFunctionMetaDivStyle_r = no_update


        t = readTables()

        aData = t['rtfunctions'][t['rtfunctions']['id_function'] == chosenFunction ].reset_index().to_dict()


        if changeFunctionBtn > 0:
            if aData['sts_rec'][0]==1:
                functionDeleted_r = []
            else:
                functionDeleted_r = ['Verwijderd']
            changeFunctionName_r = aData['function'][0]

            changeFunctionDivStyle_r = cssStyles['block']
            changeFunctionTitleDivStyle_r = {'display':'block'}
            changeFunctionMetaDivStyle_r = cssStyles['changeUserBlock']




        elif chosenFunction == None or chosenFunction == []:
            changeFunctionTitleDivStyle_r = {'display':'none'}
            changeFunctionDivStyle_r = html.Div()
            changeFunctionMetaDivStyle_r = {'display':'none'}





        return [
            changeFunctionTitleDivStyle_r,
            changeFunctionDivStyle_r,
            changeFunctionBtn_r,
            functionDeleted_r,
            changeFunctionName_r,
            changeFunctionMetaDivStyle_r,

        ]


