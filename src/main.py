import json
import pyperclip
import PySimpleGUI as sg
import os
from decimal import Decimal as d
import random

# Sets the theme for the GUI
sg.theme('DarkGrey12')

#Used to calculate the time between 2 times
class timer:
    def format(time):
        #changes time into a string and splits the string into an array between seconds and milliseconds
        time = str(time)
        time = time.split('.', 1)
        seconds = time[0]
        milliseconds = time[1]
        milliseconds = str(milliseconds)
        seconds = int(seconds)
        minutes = seconds//60
        hours = minutes//60
        if seconds > 60:
            seconds = seconds - 60
        seconds = str(seconds)
        minutes = str(minutes)
        hours = str(hours)
        if seconds == '0':
            return (f'0.{milliseconds}')
        elif minutes == '0':
            if len(seconds) == 1:
                return (f'0{seconds}.{milliseconds}')
            else:
                return (f'{seconds}.{milliseconds}')
        elif hours == '0':
            return (f'{minutes}:{seconds}.{milliseconds}')
        else:
            return (f'{hours}:{minutes}:{seconds}.{milliseconds}')
        

    def load(dbi_end, dbi_start):
        try:
            dbis_dict = json.loads(dbi_start)
        except:
            sg.popup('Error (Start)', 'Debug Info is not valid.', title = 'Error')
            return
        try:
            dbie_dict = json.loads(dbi_end)
        except:
            sg.popup('Error (End)', 'Debug Info is not valid.', title = 'Error')
            return
        try:
            cmt_end = dbie_dict['cmt']
            cmt_start = dbis_dict['cmt']
        except:
            sg.popup('Error (CMT)', 'CMT is not Valid.', title = 'fuck you rekto')
        try:
            time = (d(cmt_end) - d(cmt_start)) + d(time)
        except:
            sg.popup('Error (CMT)', 'CMT is not Valid.', title = 'fuck you rekto')
            return
        if -abs(time) == time:
            sg.popup('Error', 'The end is greater than the start.', title = 'Error')
            return
        main_window['dbis_loads'].update('')
        main_window['dbie_loads'].update('')
        sg.popup(f'Loads Added', title = 'Loads', font = ('Helvetica', 16))
        return loads

    def final(dbi_start, dbi_end, loads):
        try:
            dbis_dict = json.loads(dbi_start)
        except:
            sg.popup('Error (Start)', 'Debug Info is not valid.', title = 'Error')
            return
        try:
            dbie_dict = json.loads(dbi_end)
        except:
            sg.popup('Error (End)', 'Debug Info is not valid.', title = 'Error')
            return
        try:
            cmt_end = dbie_dict['cmt']
            cmt_start = dbis_dict['cmt']
        except:
            sg.popup('Error (CMT)', 'CMT is not Valid.', title = 'fuck you rekto')
        time = (d(cmt_end) - d(cmt_start))
        if -abs(time) == time:
            sg.popup('Error', 'The end is greater than the start.', title = 'Error')
            return
        time_loads = time
        time = time - loads
        no_loads = timer.format(time)
        with_loads = timer.format(time_loads)
        if loads == 0:
            final_confirm = sg.popup_yes_no(f'Without Loads: {no_loads}', 'Would you like the Mod Note to be Copied to the Clipboard?', title = 'Results')
            if final_confirm == 'Yes':
                pyperclip.copy(f'Mod Note: Retimed to {no_loads} https://github.com/ConnerConnerConner/PyTime')
            elif final_confirm == 'No':
               return 
        else:
            final_confirm = sg.popup_yes_no(f'Without Loads: {no_loads}, With Loads: {with_loads}', 'Mod Note Copied to Clipboard', title = 'Results')
        if final_confirm == 'Yes':
            pyperclip.copy(f'Mod Note: Retimed to {no_loads} using https://github.com/ConnerConnerConner/PyTime')
        elif final_confirm == 'No':
             return
if (random.randint(1, 1000) == 69):
    main_layout = [
        [sg.Text('conner solos rekto', font = ('Helvetica', 36))],
        [sg.InputText(key = 'dbis', font = ('Helvetica', 16), pad = ((5, 0), (0, 0)), size = (20, 1)), sg.Text('  Debug Info Start', font = ('Helvetica', 16), justification = 'right')],
        [sg.InputText(key = 'dbie', font = ('Helvetica', 16), pad = ((5, 0), (0, 0)), size = (20, 1)), sg.Text('  Debug Info End', font = ('Helvetica', 16), justification = 'right')],
        [sg.InputText(key = 'dbis_loads', font = ('Helvetica', 14), pad = ((5, 0), (0, 0)), size = (15, 1)), sg.Text('   Debug Info Start (Loads)', font = ('Helvetica', 14), justification = 'right')],
        [sg.InputText(key = 'dbie_loads', font = ('Helvetica', 14), pad = ((5, 0), (0, 0)), size = (15, 1)), sg.Text('   Debug Info End (Loads)', font = ('Helvetica', 14), justification = 'right')],
        [sg.Button('Calculate', font = ('Helvetica', 16)), sg.Button('Add Loads', font = ('Helvetica', 16)), sg.Button('Remove All Loads', font = ('Helvetica', 16))]
    ]
else:
    main_layout = [
        [sg.Text('PyTime', font = ('Helvetica', 36))],
        [sg.InputText(key = 'dbis', font = ('Helvetica', 16), pad = ((5, 0), (0, 0)), size = (20, 1)), sg.Text('  Debug Info Start', font = ('Helvetica', 16), justification = 'right')],
        [sg.InputText(key = 'dbie', font = ('Helvetica', 16), pad = ((5, 0), (0, 0)), size = (20, 1)), sg.Text('  Debug Info End', font = ('Helvetica', 16), justification = 'right')],
        [sg.InputText(key = 'dbis_loads', font = ('Helvetica', 14), pad = ((5, 0), (0, 0)), size = (15, 1)), sg.Text('   Debug Info Start (Loads)', font = ('Helvetica', 14), justification = 'right')],
        [sg.InputText(key = 'dbie_loads', font = ('Helvetica', 14), pad = ((5, 0), (0, 0)), size = (15, 1)), sg.Text('   Debug Info End (Loads)', font = ('Helvetica', 14), justification = 'right')],
        [sg.Button('Calculate', font = ('Helvetica', 16)), sg.Button('Add Loads', font = ('Helvetica', 16)), sg.Button('Remove All Loads', font = ('Helvetica', 16))]
    ]
main_window = sg.Window('PyTime', main_layout, resizable = False, element_justification = 'left', size=(447, 253),  icon=r'assets\PyTime.ico')

while True:
    event, values = main_window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Remove All Loads':
        lr_confirm = sg.popup_yes_no('Are you sure you want to remove all loads?', title = 'Remove All Loads', font = ('Helvetica', 16))
        if lr_confirm == 'Yes':
            main_window['dbis_loads'].update('')
            main_window['dbie_loads'].update('')
            loads = 0
        elif lr_confirm == 'No':
            continue
    if event == 'Add Loads':
        dbis_loads = values['dbis_loads']
        dbiel_loads = values['dbie_loads']
        if not 'loads' in globals():
            loads = timer.load(dbis_loads, dbiel_loads)
        else:
            try:
                loads = timer.load(dbis_loads, dbiel_loads) + loads
            except:
                continue
    if event == 'Calculate':
        dbi_start = values['dbis']
        dbi_end = values['dbie']
        if not 'loads' in globals():
            loads = 0
        main_window['dbis'].update('')
        main_window['dbie'].update('')
        timer.final(dbi_start, dbi_end, loads)

main_window.close()