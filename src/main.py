from json import loads as json_loads
from pyperclip import copy
import PySimpleGUI as sg
from decimal import Decimal as d
from math import floor as round_down

sg.theme('DarkGrey12')

class timer:
    def frame_round(time, fps): # Rounds to the nearest frame
        time = d(time)
        time = round(time, 3)
        output = d(time - time%(d(1)/fps)) #Credit to Slush0Puppy for this 1 Line of Code
        return round(output, 3)

    def format(time): # Formats the time to the SRC format
        time = str(time)
        time = time.split('.', 1)
        seconds = time[0]
        milliseconds = time[1]
        milliseconds = str(milliseconds)
        seconds = int(seconds)
        minutes = seconds//60
        hours = minutes//60
        if seconds > 60: #makes sure that the seconds are less than 60
            seconds = seconds - (minutes * 60)
        if minutes > 60: #makes sure that the minutes are less than 60
            minutes = minutes - (hours * 60)
        seconds = str(seconds)
        minutes = str(minutes)
        hours = str(hours)
        if seconds == '0':
            return (f'0s {milliseconds}ms')
        elif minutes == '0':
            if len(seconds) == 1:
                return (f'0{seconds}s {milliseconds}ms')
            else:
                return (f'{seconds}s {milliseconds}ms')
        elif hours == '0':
            return (f'{minutes}m {seconds}s {milliseconds}ms')
        else:
            return (f'{hours}h {minutes}m {seconds}s {milliseconds}ms')
        

    def load(dbi_end, dbi_start, fps):
        try:
            dbis_dict = json_loads(dbi_start)
        except:
            sg.popup('Error (Start)', 'Debug Info is not valid.', title = 'Error')
            return
        try:
            dbie_dict = json_loads(dbi_end)
        except:
            sg.popup('Error (End)', 'Debug Info is not valid.', title = 'Error')
            return
        try:
            cmt_end = dbie_dict['cmt']
            cmt_start = dbis_dict['cmt']
        except:
            sg.popup('Error (CMT)', 'CMT is not Valid.', title = 'fuck you rekto')
        cmt_start = timer.frame_round(d(cmt_start), fps)
        cmt_end = timer.frame_round(d(cmt_end), fps)
        try:
            time = (d(cmt_end) - d(cmt_start)) + d(time)
        except:
            sg.popup('Error (CMT)', 'CMT is not Valid.', title = 'fuck you rekto')
            return
        if -abs(time) == time:
            sg.popup('Error', 'The start is greater than the end.', title = 'Error')
            return
        main_window['dbis_loads'].update('')
        main_window['dbie_loads'].update('')
        sg.popup(f'Loads Added', title = 'Loads', font = ('Helvetica', 16))
        return loads

    def final(dbi_start, dbi_end, loads, fps):
        try:
            dbis_dict = json_loads(dbi_start)
        except:
            sg.popup('Error (Start)', 'Debug Info is not valid.', title = 'Error')
            return
        try:
            dbie_dict = json_loads(dbi_end)
        except:
            sg.popup('Error (End)', 'Debug Info is not valid.', title = 'Error')
            return
        try:
            cmt_end = dbie_dict['cmt']
            cmt_start = dbis_dict['cmt']
        except:
            sg.popup('Error (CMT)', 'CMT is not Valid.', title = 'fuck you rekto')
        cmt_start = timer.frame_round(d(cmt_start), fps)
        cmt_end = timer.frame_round(d(cmt_end), fps)
        time_loads = (d(cmt_end) - d(cmt_start))
        if -abs(time_loads) == time_loads:
            sg.popup('Error', 'The start is greater than the end.', title = 'Error')
            return
        loads = timer.frame_round(loads, fps)
        time_noloads = time_loads - loads
        no_loads = timer.format(time_noloads)
        with_loads = timer.format(time_loads)
        if loads == 0:
            final_confirm = sg.popup_yes_no(f'Without Loads: {no_loads}', 'Would you like the Mod Note to be Copied to the Clipboard?', title = 'Results')
            if final_confirm == 'Yes':
                copy(f'Mod Note: Retimed to {no_loads} https://github.com/ConnerConnerConner/PyTime')
            elif final_confirm == 'No':
               return 
        else:
            final_confirm = sg.popup_yes_no(f'Without Loads: {no_loads}, With Loads: {with_loads}', 'Mod Note Copied to Clipboard', title = 'Results')
        if final_confirm == 'Yes':
            copy(f'Mod Note: Retimed to {no_loads} using https://github.com/ConnerConnerConner/PyTime')
        elif final_confirm == 'No':
             return
main_layout = [
        [sg.Text('PyTime', font = ('Helvetica', 36)), sg.Text('   FPS', font = (' Helvetica', 30)), sg.InputText('60', size = (5, 1), key = 'fps', font = ('Helvetica', 30))],
        [sg.InputText(key = 'dbis', font = ('Helvetica', 16), pad = ((5, 0), (0, 0)), size = (20, 1)), sg.Text('  Debug Info Start', font = ('Helvetica', 16), justification = 'right')],
        [sg.InputText(key = 'dbie', font = ('Helvetica', 16), pad = ((5, 0), (0, 0)), size = (20, 1)), sg.Text('  Debug Info End', font = ('Helvetica', 16), justification = 'right')],
        [sg.InputText(key = 'dbis_loads', font = ('Helvetica', 14), pad = ((5, 0), (0, 0)), size = (15, 1)), sg.Text('   Debug Info Start (Loads)', font = ('Helvetica', 14), justification = 'right')],
        [sg.InputText(key = 'dbie_loads', font = ('Helvetica', 14), pad = ((5, 0), (0, 0)), size = (15, 1)), sg.Text('   Debug Info End (Loads)', font = ('Helvetica', 14), justification = 'right')],
        [sg.Button('Calculate', font = ('Helvetica', 16)), sg.Button('Add Loads', font = ('Helvetica', 16)), sg.Button('Remove All Loads', font = ('Helvetica', 16))]
    ]
main_window = sg.Window('PyTime', main_layout, resizable = False, element_justification = 'left', size=(447, 253),  icon='PyTime.ico')

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
        fps = values['fps']
        try:
            fps = d(fps)
        except:
            sg.popup('Error (FPS)', 'FPS is not a valid number.', title = 'Error')
            continue
        if not 'loads' in globals():
            loads = timer.load(dbis_loads, dbiel_loads, fps)
        else:
            try:
                loads = timer.load(dbis_loads, dbiel_loads, fps) + loads
            except:
                continue
    if event == 'Calculate':
        dbi_start = values['dbis']
        dbi_end = values['dbie']
        fps = values['fps']
        try:
            fps = d(fps)
        except:
            sg.popup('Error (FPS)', 'FPS is not an valid number.', title = 'Error')
            continue
        if not 'loads' in globals():
            loads = 0
        main_window['dbis'].update('')
        main_window['dbie'].update('')
        timer.final(dbi_start, dbi_end, loads, fps)

main_window.close()

#Credit to Rekto for Helping Me With Everything
#Credit to Slush0Puppy for Frane Rounding
#Credit to Me For Making This Shit
#Credit to You For Using This Shit
#Made by Conner Speedrunning