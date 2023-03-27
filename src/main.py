from json import loads as json_loads
from pyperclip import copy, paste
import PySimpleGUI as sg
from decimal import Decimal as d

# GUI Theme
sg.theme('DarkGrey12')


class ReTime:  # Class for all timer related functions
    def frame_round(time, fps):  # Rounds to the nearest frame
        time = d(round(time, 3))
        # Credit to Slush0Puppy for this 1 Line of Code
        output = d(time - time % (d(1) / fps))
        return round(output, 3)

    # Formats the time to the SRC format
    def format(time):
        time = str(time)
        time = time.split('.', 1)
        seconds = int(time[0])
        milliseconds = str(time[1])
        minutes = seconds // 60
        hours = minutes // 60
        if seconds > 59.999:  # makes sure that the seconds are less than 60
            seconds = seconds - (minutes * 60)
        if minutes > 59.999:  # makes sure that the minutes are less than 60
            minutes = minutes - (hours * 60)
        # Converts Integers to Strings
        # Combines the time into a single string
        seconds = str(seconds).rjust(2, '0')
        minutes = str(minutes).rjust(2, '0')
        if len(hours) < 2:
            hours = str(hours).rjust(2, '0')
        return f'{str(hours)}h {str(minutes)}m {str(seconds)}s {milliseconds}ms'

    # Calculates the loads
    def loads(dbi_start, dbi_end, fps):
        try:  # Turns JSON into a Dictionary and Checks if it is Valid (Start)
            dbis_dict = json_loads(dbi_start)
        except:
            sg.popup('Error (Start)', 'Debug Info is not valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        try:  # Turns JSON into a Dictionary and Checks if it is Valid (End)
            dbie_dict = json_loads(dbi_end)
        except:
            sg.popup('Error (End)', 'Debug Info is not valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        try:  # Gets the CMT from the Dictionary
            cmt_end = dbie_dict['cmt']
            cmt_start = dbis_dict['cmt']
        except:
            sg.popup('Error (CMT)', 'CMT is not Valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
        # Rounds the CMT to the nearest frame
        cmt_start = ReTime.frame_round(d(cmt_start), fps)
        cmt_end = ReTime.frame_round(d(cmt_end), fps)
        # Calculates the Loads
        loads = (d(cmt_end) - d(cmt_start))
        if -abs(loads) == loads:  # Checks if the Start is greater than the End
            sg.popup('Error', 'The start is greater than the end.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        # Rounds the Loads to the nearest frame just in case the rounding is off
        loads = ReTime.frame_round(loads, fps)
        sg.popup(f'Loads Added', title='Loads', font=('Helvetica', 16), icon=r'assets\pytime.ico')  # Success Message
        return loads

    # Calculates the Final Time
    def final(dbi_start, dbi_end, loads, fps):
        try:  # Turns JSON into a Dictionary and Checks if it is Valid (Start)
            dbis_dict = json_loads(dbi_start)
        except:
            sg.popup('Error (Start)', 'Debug Info is not valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        try:  # Turns JSON into a Dictionary and Checks if it is Valid (End)
            dbie_dict = json_loads(dbi_end)
        except:
            sg.popup('Error (End)', 'Debug Info is not valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        try:  # Gets the CMT from the Dictionary
            cmt_end = dbie_dict['cmt']
            cmt_start = dbis_dict['cmt']
        except:
            sg.popup('Error (CMT)', 'CMT is not Valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
        # Rounds the CMT to the nearest frame
        cmt_start = ReTime.frame_round(d(cmt_start), fps)
        cmt_end = ReTime.frame_round(d(cmt_end), fps)
        # Calculates the Final Time
        time_loads = (d(cmt_end) - d(cmt_start))
        if -abs(time_loads) == time_loads:  # Checks if the Start is greater than the End
            sg.popup('Error', 'The start is greater than the end.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        if loads > time_loads:  # Checks if the Loads are greater than the Time
            sg.popup('Error', 'The Loads is greater than the Time.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        # Rounds Loads for the millionth time
        loads = ReTime.frame_round(loads, fps)
        time_no_loads = time_loads - loads  # Gets the Time without Loads
        # Formats the Time
        no_loads = ReTime.format(time_no_loads)
        with_loads = ReTime.format(time_loads)
        if loads == 0:
            final_confirm = sg.popup_yes_no(f'Without Loads: {no_loads}', 'Would you like the Mod Note to be Copied to the Clipboard?',title='Results', icon=r'assets\pytime.ico')
            if final_confirm == 'Yes':
                copy(
                    f'Mod Note: Retimed to {no_loads} at {fps} FPS using [PyTime](https://github.com/ConnerConnerConner/PyTime)')
            elif final_confirm == 'No':
                return
        else:
        # makes sure that the minutes are less than 60
            final_confirm = sg.popup_yes_no(f'Without Loads: {no_loads}, With Loads: {with_loads}', 'Mod Note Copied to Clipboard', title='Results', icon=r'assets\pytime.ico')
        if final_confirm == 'Yes':
            copy(f'Mod Note: Retimed to {no_loads} at {fps} FPS using [PyTime](https://github.com/ConnerConnerConner/PyTime)')
        elif final_confirm == 'No':
            return


# GUI Layout
main_layout = [
    [sg.Text('PyTime', font=('Helvetica', 48)), sg.Text(' FPS', font=('Helvetica', 40)), sg.InputText('60', size=(4, 1), key='fps', font=('Helvetica', 36))],
    [sg.Button('Paste', font=('Helvetica', 10), key='paste_dbis'), sg.InputText(key='dbis', font=('Helvetica', 16), pad=((5, 0), (0, 0)), size=(20, 1)), sg.Text('  Debug Info Start', font=('Helvetica', 16), justification='right')],
    [sg.Button('Paste', font=('Helvetica', 10), key='paste_dbie'),sg.InputText(key='dbie', font=('Helvetica', 16), pad=((5, 0), (0, 0)), size=(20, 1)), sg.Text('  Debug Info End', font=('Helvetica', 16), justification='right')],
    [sg.Button('Paste', font=('Helvetica', 10), key='paste_dbis_loads'),sg.InputText(key='dbis_loads', font=('Helvetica', 14), pad=((5, 0), (0, 0)), size=(15, 1)),sg.Text('   Debug Info Start (Loads)', font=('Helvetica', 14), justification='right')],
    [sg.Button('Paste', font=('Helvetica', 10), key='paste_dbie_loads'),sg.InputText(key='dbie_loads', font=('Helvetica', 14), pad=((5, 0), (0, 0)), size=(15, 1)),sg.Text('   Debug Info End (Loads)', font=('Helvetica', 14), justification='right')],
    [sg.Button('Calculate', font=('Helvetica', 18)), sg.Button('Add Loads', font=('Helvetica', 18)), sg.Button('Remove All Loads', font=('Helvetica', 18))]
]
main_window = sg.Window('PyTime', main_layout, resizable=False, element_justification='left', size=(516, 275), finalize=True, icon=r'assets\pytime.ico')

# Main Loop
while True:
    event, values = main_window.read()  # Reads the Window
    if event == sg.WIN_CLOSED:  # Checks if the Window is Closed
        break
    if event == 'Remove All Loads':  # Checks if the Remove All Loads Button is Pressed
        lr_confirm = sg.popup_yes_no('Are you sure you want to remove all loads?', title='Remove All Loads', font=('Helvetica', 16), icon=r'assets\pytime.ico')  # Confirmation Message
        if lr_confirm == 'Yes':
            # Clears Loads Input Boxes
            main_window['dbis_loads'].update('')
            main_window['dbie_loads'].update('')
            loads = 0  # Sets Loads to 0
        elif lr_confirm == 'No':
            continue
    if event == 'Add Loads':  # Checks if the Add Loads Button is Pressed
        # Gets the Values from the Input Boxes
        dbis_loads = values['dbis_loads']
        dbiel_loads = values['dbie_loads']
        fps = values['fps']
        try:  # Checks if the FPS is Valid
            fps = d(fps)
        except:
            sg.popup('Error (FPS)', 'FPS is not a valid number.',
                     title='Error')  # Error Message
            continue
        if not 'loads' in globals() or loads == 0:  # Checks if Loads exists
            try:
                # Calculates Loads
                loads = ReTime.loads(dbis_loads, dbiel_loads, fps)
                main_window['dbis_loads'].update('')
                main_window['dbie_loads'].update('')
            except:
                continue
        else:
            try:
                loads = ReTime.loads(dbis_loads, dbiel_loads, fps) + loads
                main_window['dbis_loads'].update('')  # Calculates Loads
                main_window['dbie_loads'].update('')
            except:
                continue
    if event == 'Calculate':
        # Gets the Values from the Input Boxes
        dbi_start = values['dbis']
        dbi_end = values['dbie']
        fps = values['fps']
        try:  # Checks if the FPS is Valid
            fps = d(fps)
        except:
            sg.popup('Error (FPS)', 'FPS is not an valid number.', title='Error', icon=r'assets\pytime.ico')
            continue
        if fps == 0:
            sg.popup('Error (FPS)', 'FPS cannot be 0.', title='Error', icon=r'assets\pytime.ico')
            continue
        else:
            if not 'loads' in globals():  # Check if the Loads Variables Exists
                loads = 0  # Sets Loads to 0
            # Runs the Final Function
            ReTime.final(dbi_start, dbi_end, loads, fps)
            # Clears Input Boxes
            main_window['dbis'].update('')
            main_window['dbie'].update('')
    # Checks if the Paste Button is Pressed
    # Pastes the Clipboard to the Input Box
    if event == 'paste_dbis':
        main_window['dbis'].update(paste())
    if event == 'paste_dbie':
        main_window['dbie'].update(paste())
    if event == 'paste_dbis_loads':
        main_window['dbis_loads'].update(paste())
    if event == 'paste_dbie_loads':
        main_window['dbie_loads'].update(paste())

main_window.close()  # Closes the Window
# Made by Conner Speedrunning
