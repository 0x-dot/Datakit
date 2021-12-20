### Copyright (c) 2021-2022, Giuseppe Giordano ###

import sqlite3


import PySimpleGUI as sg


def imported(filename,namedb):
    conn = sqlite3.connect(f"{namedb}")
    cursor=conn.cursor()
    with open(f"{filename}",encoding="utf8") as infile:
        for line in infile:
            data = line.split()
            cursor.execute(f"INSERT INTO contatti(id,nome,cognome,telefono) VALUES ('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}')")
            conn.commit()
        cursor.close()

def delete(id,namedb):
    if(namedb!=0):
        conn = sqlite3.connect(f"{namedb}")
        cursor=conn.cursor()
        cursor.execute(f"DELETE FROM contatti WHERE id='{id}'")
        conn.commit()
        result=cursor.rowcount
        cursor.close()
        return result


def Update(nuovonome, nuovocognome, nuovotelefono,id, namedb):
    if(namedb!=0):
        conn = sqlite3.connect(f"{namedb}")
        cursor=conn.cursor()
        cursor.execute(f"UPDATE contatti SET nome = '{nuovonome}',cognome='{nuovocognome}', telefono='{nuovotelefono}' WHERE id = '{id}'")
        conn.commit()
        result=cursor.rowcount
        cursor.close()
        return result


def insert(nome,cognome,telefono,namedb):
    if(nome!=0 and cognome !=0 and telefono!=0 and namedb!=0):
        conn = sqlite3.connect(f"{namedb}")
        cursor=conn.cursor()
        id=getmaxid(namedb)
        print(id)
        cursor.execute(f"INSERT INTO contatti(id,nome,cognome,telefono) VALUES('{id}','{nome}','{cognome}','{telefono}')")
        conn.commit()
        result=cursor.rowcount
        cursor.close()
        return result

def getmaxid(namedb):
    conn = sqlite3.connect(f"{namedb}")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM contatti")
    result=len(cursor.fetchall())
    cursor.close()
    return result

def search(nome,cognome,namedb):
    if(nome!=0 and cognome !=0 and namedb!=0):
        conn = sqlite3.connect(f"{namedb}")
        cursor=conn.cursor()
        cursor.execute(f"SELECT * FROM contatti WHERE Nome LIKE '{nome}' AND Cognome LIKE '{cognome}'")
        result=cursor.fetchall()
        return result

def connect(path):
    print(path)
    conn = sqlite3.connect(f"{path}")
    cursor=conn.cursor()
    cursor.execute("select * from contatti")
    result=cursor.fetchall()
    conn.close()
    return result

def checkvariable(variable):

    if variable!="":
        return True
    else:
        return False

def checkstring(string):
    my_str=string
    final_str=my_str[-3:]
    return final_str

def main ():


    layout=[[sg.Text("Scelta file Database: "),
             sg.Input(), sg.FileBrowse(key="-IN-")],[sg.Button("Inizia")],
            [sg.Button("Visualizza database",disabled=True),sg.Button("Ricerca",disabled=True)],
            [sg.Text("Scelta file da importare : "),
             sg.Input(), sg.FileBrowse(key="-import-"),sg.Button("Import",disabled=True)],
            ]

    window= sg.Window("Datakit",layout)
    window2_active= False
    window3_active=False

    while True:
        event,values=window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            break


        elif event == "Inizia":
            if(checkstring(values["-IN-"]))==".db":
                window["Visualizza database"].update(disabled=False)
                window["Ricerca"].update(disabled=False)
                window["Import"].update(disabled=False)
            else:
                sg.popup("Il file importato non è un .db")
        elif event=="Import":
            imported(values['-import-'],values['-IN-'])
            sg.popup("inserimento completato")
        if not window2_active and event == "Visualizza database":
            window2_active=True

            layout2= [[sg.Text('Lista contatti')],
                      [sg.Listbox(connect(values["-IN-"]), size=(60,10), key='list'),sg.Text("Inserire id da eliminare"),sg.InputText(key='deleteid',size=(4,4)),sg.Button('Delete',button_color='RED')],
                      [sg.Button('Ok')]]

            win2=sg.Window("Datakit").layout(layout2)
            if window2_active:
                event2,values2=win2.read()
                if event2 == sg.WIN_CLOSED or event2=='Exit' or event2=="Ok":
                    window2_active=False
                    win2.close()
                if event2=="Delete":
                    delete(values2['deleteid'],values['-IN-'])
                    sg.popup("Contatto cancellato")
                    window2_active=False
                    win2.close()


        if not window3_active and event=="Ricerca":
            window3_active=True

            layout3 = [
                [sg.Text('Ricerca Contatto in archivio',text_color='Black')],
                [sg.Text("Nome", size=(15, 1)), sg.InputText(key="Name")],
                [sg.Text("Cognome",size=(15, 1)), sg.InputText(key="SURNAME")],
                [sg.Button("Cerca")],

                [sg.Text('Inserimento Contatto in archivio ',text_color='Black')],
                [sg.Text("Nome", size=(15, 1)), sg.InputText(key="Name1")],
                [sg.Text("Cognome",size=(15, 1)), sg.InputText(key="Surname1")],
                [sg.Text("Telefono",size=(15, 1)), sg.InputText(key="Phone1")],
                [sg.Button("inserisci")],
                [sg.Text('Modifica contatto esistente',text_color='Black')],
                [sg.Text("IDcontatto da modificare", size=(15, 2)), sg.InputText(key="ID",size=(4,4)),],
                [sg.Text("Nuovo Nome", size=(15, 1)), sg.InputText(key="Name3")],
                [sg.Text("Nuovo Cognome",size=(15, 1)), sg.InputText(key="Surname3")],
                [sg.Text("Nuovo Telefono",size=(15, 1)), sg.InputText(key="Phone3")],
                [sg.Button("Modifica"), sg.Button("Exit")]]

            win3=sg.Window("Datakit").layout(layout3)
            if window3_active:
                event3,values3=win3.read()
                if event3=="Cerca":

                    if checkvariable(values["-IN-"])==False:
                        print("questa è value quando è Falsa ",checkvariable(values["-IN-"]))
                        sg.popup("Attenzione problema database")



                    if checkvariable(values["-IN-"])==True:
                        print("questa è value quando è Vera ",checkvariable(values["-IN-"]))
                        variable=search(values3["Name"],values3["SURNAME"],values["-IN-"])
                        if len(variable)>0:
                            sg.popup("la ricerca ha dato il seguente risultato\n",f'{variable}')
                        else:
                            sg.popup("Attenzione","la ricerca non ha dato nessun risultato")

                window3_active=False
                if event3=="inserisci":
                    window3_active=False
                    ins=insert(values3["Name1"],values3["Surname1"],values3["Phone1"],values["-IN-"])
                    sg.popup("Inserimento avvenuto \n",f'{ins}')

                if event3=="Modifica":
                    window3_active=False
                    Update(values3["Name3"],values3["Surname3"],values3["Phone3"],values3["ID"],values["-IN-"])
                    sg.popup("modifica avvenuta")

                if event3 == sg.WIN_CLOSED or event3=='Exit':
                    window3_active=False
                win3.close()





if __name__ == '__main__':
    main()