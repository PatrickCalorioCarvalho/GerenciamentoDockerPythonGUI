#pip3 install docker
#pip3 install PySimpleGUI

import PySimpleGUI as sg
import docker


sg.theme('DarkBlue1')

btns = []
client = docker.from_env()
containers = client.containers.list(all=True)
for container in containers : 
    if container.status == 'exited':
        btns.append(sg.Button(enable_events=True, font=("", 15, ""),key="Contener-"+container.id,button_text=container.name,size=(16,8),button_color = ('black','gray')))

    if container.status == 'running':
        btns.append(sg.Button(enable_events=True, font=("", 15, ""),key="Contener-"+container.id,button_text=container.name,size=(16,8),button_color = ('black','dodger blue')))

colunas = 0
coluna = []
Linha = []
for btn in btns:
    if colunas == 3:
        Linha.append(btn)
        coluna.append([sg.Column([Linha])])
        Linha = []
        colunas = 0
    else:
        Linha.append(btn)
        colunas = colunas + 1
coluna.append([sg.Column([Linha])])

width, height = sg.Window.get_screen_size()
layout = [[sg.Column(coluna,key='view', scrollable=True,  vertical_scroll_only=True,size=(width - 20,height - 20))]]       
window = sg.Window('Docker Manager',layout,,layout,keep_on_top=True,no_titlebar = True).finalize()
window.maximize()
while True:
    event, value = window.read()
    if event in (sg.WIN_CLOSED, 'EXIT'):
        break
    elif "Contener-" in event :
        container = client.containers.get(event.replace("Contener-",""))
        if container.status == 'exited':
            container.start()
            window[event].update(button_color = ('black','dodger blue'))
        if container.status == 'running':
            container.stop()
            window[event].update(button_color = ('black','gray'))

window.close()