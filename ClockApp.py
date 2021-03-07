import PySimpleGUI as sg
import time

default_text = 'title'

Preferences = {
    'header_font': {'font': ('Helvetica', 25)},
    'spinbox_font': {'font': ('Helvetica', 12)},
    'align_center': {'justification': 'center', 'size': (400, 1)},
    'separator': {'pad': (10, 10), 'color': 'black'},
    'progressBar': {'size': (20, 10), 'key': 'pB'}
}

layout = [[sg.Text("Clock Application", **Preferences['align_center'], **Preferences['header_font'])],
          [sg.HorizontalSeparator(**Preferences['separator'])],
          [sg.Text("1. Timer", **Preferences['header_font'])],
          [sg.Text("Please specify the title: ")],
          [sg.InputText(default_text, **Preferences['align_center'], key='-InputText-')],
          [sg.Text("Hours: "), sg.Spin(values=list(range(24)), **Preferences['spinbox_font'], key='-H-'),
           sg.Text("Minutes: "), sg.Spin(values=list(range(60)), **Preferences['spinbox_font'], key='-M-'),
           sg.Text("Seconds: "), sg.Spin(values=list(range(60)), **Preferences['spinbox_font'], key='-S-')],
          [sg.Button("Start!", size=(10, 2))],
          [sg.Text('Completion: '), sg.ProgressBar(100, **Preferences['progressBar'])],
          [sg.HorizontalSeparator(**Preferences['separator'])]]
layout = [[sg.Column(layout, element_justification='c')]]
window = sg.Window("Clock Application", layout, size=(400, 400), icon='clock.ico')

# Elements in the window
progress: sg.ProgressBar = window.find_element('pB')


def maxTicks(h, m, s):
    return s + m*60 + h*3600 - 1


def is_initialized(h, m, s):
    total = h + m + s
    return not total == 0


counter = None
max_time = 0
pressed = False
offset = None

while True:
    event, values = window.read(timeout=1000)  # updating every 10 milli-sec
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == "Start!" and is_initialized(values['-H-'], values['-M-'], values['-S-']):
        max_time = maxTicks(values['-H-'], values['-M-'], values['-S-'])
        counter = 0
        progress.update_bar(counter, max_time)
        #  t = threading.Thread()  # draw the progress bar in parallel
        pressed = True
        time.sleep(1)
    if pressed:
        counter += 1
        progress.update_bar(counter, max_time)

    if (counter is not None) and counter == max_time:
        if values['-InputText-'] == default_text:
            sg.popup('Timer finished!')
        else:
            sg.popup(values['-InputText-'])
