from json import loads as json_loads
from json.decoder import JSONDecodeError
from pyperclip import copy, paste
import PySimpleGUI as sg
from decimal import Decimal as d

# GUI Theme
sg.theme('DarkGrey12')

# Formats the time to the SRC format
def format_time(time):
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
    if len(str(hours)) < 2:
        hours = str(hours).rjust(2, '0')
    return f'{str(hours)}h {str(minutes)}m {str(seconds)}s {milliseconds}ms'

# Calculates the loads
def calculate_loads(start_info, end_info, fps):
    try:
        start_time = json_loads(start_info)['cmt']
    except JSONDecodeError:
        sg.popup('Error (Start)', 'Debug Info is not valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
        return
    except KeyError:
        sg.popup('Error (Start CMT)', 'CMT is not Valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
        return
    try:
        end_time = json_loads(end_info)['cmt']
    except JSONDecodeError:
        sg.popup('Error (End)', 'Debug Info is not valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
        return
    except KeyError:
        sg.popup('Error (End CMT)', 'CMT is not Valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
        return
    # Calculates the Loads
    loads = d(end_time) - d(start_time)
    loads = round(d(loads - loads % (d(1) / fps)), 3)
    if -abs(loads) == loads:  # Checks if the Start is greater than the End
        sg.popup('Error', 'The start is greater than the end.',title='Error', icon=r'assets\pytime.ico')  # Error Message
        return
    # Rounds the Loads to the nearest frame just in case the rounding is off
    sg.popup(f'Loads Added', title='Loads', font=('Helvetica', 16), icon=r'assets\pytime.ico')  # Success Message
    return loads

# Calculates the Final Time
def calculate_time(start_info, end_info, loads, fps):
    try:
        start_time = json_loads(start_info)['cmt']
    except JSONDecodeError:
        sg.popup('Error (Start)', 'Debug Info is not valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
        return
    except KeyError:
        sg.popup('Error (Start CMT)', 'CMT is not Valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
        return
    try:
        end_time = json_loads(end_info)['cmt']
    except JSONDecodeError:
        sg.popup('Error (End)', 'Debug Info is not valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
        return
    except KeyError:
        sg.popup('Error (End CMT)', 'CMT is not Valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
        return
    # Rounds the CMT to the nearest frame
    # Calculates the Final Time
    time_loads = d(end_time) - d(start_time)
    time_loads = round(d(time_loads - time_loads % (d(1) / fps)), 3)
    if -abs(time_loads) == time_loads:  # Checks if the Start is greater than the End
        sg.popup('Error', 'The start is greater than the end.',title='Error', icon=r'assets\pytime.ico')  # Error Message
        return
    if loads > time_loads:  # Checks if the Loads are greater than the Time
        sg.popup('Error', 'The Loads is greater than the Time.',title='Error', icon=r'assets\pytime.ico')  # Error Message
        return
    # Rounds Loads for the millionth time
    time = time_loads - loads  # Gets the Time without Loads
    # Formats the Time
    time = format_time(time)
    time_loads = format_time(time_loads)
    if loads == 0:
        final_confirm = sg.popup_yes_no(f'Without Loads: {time}', 'Would you like the Mod Note to be Copied to the Clipboard?',title='Results', icon=r'assets\pytime.ico')
        if final_confirm == 'Yes':
            copy(f'Mod Note: Retimed to {time} at {fps} FPS using [PyTime](https://github.com/ConnerConnerConner/PyTime)')
        elif final_confirm == 'No':
            return
    else:
    # makes sure that the minutes are less than 60
        final_confirm = sg.popup_yes_no(f'Without Loads: {time}, With Loads: {time_loads}', 'Mod Note Copied to Clipboard', title='Results', icon=r'assets\pytime.ico')
    if final_confirm == 'Yes':
        copy(f'Mod Note: Retimed to {time} at {fps} FPS using [PyTime](https://github.com/ConnerConnerConner/PyTime)')
    elif final_confirm == 'No':
        return

# GUI Layout
main_layout = [
    [sg.Text('PyTime', font=('Helvetica', 48)), sg.Text(' FPS', font=('Helvetica', 40)), sg.InputText('60', size=(4, 1), key='fps', font=('Helvetica', 36))],
    [sg.Button('Paste', font=('Helvetica', 10), key='start_paste'), sg.InputText(key='start', font=('Helvetica', 16), pad=((5, 0), (0, 0)), size=(20, 1)), sg.Text('  Debug Info Start', font=('Helvetica', 16), justification='right')],
    [sg.Button('Paste', font=('Helvetica', 10), key='end_paste'),sg.InputText(key='end', font=('Helvetica', 16), pad=((5, 0), (0, 0)), size=(20, 1)), sg.Text('  Debug Info End', font=('Helvetica', 16), justification='right')],
    [sg.Button('Paste', font=('Helvetica', 10), key='start_loads_paste'),sg.InputText(key='start_loads', font=('Helvetica', 14), pad=((5, 0), (0, 0)), size=(15, 1)),sg.Text('   Debug Info Start (Loads)', font=('Helvetica', 14), justification='right')],
    [sg.Button('Paste', font=('Helvetica', 10), key='end_loads_paste'),sg.InputText(key='end_loads', font=('Helvetica', 14), pad=((5, 0), (0, 0)), size=(15, 1)),sg.Text('   Debug Info End (Loads)', font=('Helvetica', 14), justification='right')],
    [sg.Button('Calculate', font=('Helvetica', 18)), sg.Button('Add Loads', font=('Helvetica', 18)), sg.Button('Remove All Loads', font=('Helvetica', 18))]
]

try:
    main_window = sg.Window('PyTime', main_layout, resizable=False, element_justification='left', size=(516, 275), finalize=True, icon=r'assets\pytime.ico')
except Exception:
    print('Error: There is no $DISPLAY environment variable.')
else:
        # Main Loop
        while True:
            event, values = main_window.read()  # Reads the Window
            if event == sg.WIN_CLOSED:  # Checks if the Window is Closed
                break
            if event == 'Remove All Loads':  # Checks if the Remove All Loads Button is Pressed
                lr_confirm = sg.popup_yes_no('Are you sure you want to remove all loads?', title='Remove All Loads', font=('Helvetica', 16), icon=r'assets\pytime.ico')  # Confirmation Message
                if lr_confirm == 'Yes':
                    # Clears Loads Input Boxes
                    main_window['start_loads'].update('')
                    main_window['end_loads'].update('')
                    loads = 0  # Sets Loads to 0
                elif lr_confirm == 'No':
                    continue
            if event == 'Add Loads':  # Checks if the Add Loads Button is Pressed
                # Gets the Values from the Input Boxes
                start_loads_info = values['start_loads']
                end_loads_info = values['end_loads']
                fps = values['fps']
                try:  # Checks if the FPS is Valid
                    fps = d(fps)
                except Exception:
                    sg.popup('Error (FPS)', 'FPS is not a valid number.',
                            title='Error')  # Error Message
                    continue
                if not 'loads' in globals() or loads == 0:  # Checks if Loads exists
                    try:
                        # Calculates Loads
                        loads = calculate_loads(start_loads_info, end_loads_info, fps)
                        main_window['start_loads'].update('')
                        main_window['end_loads'].update('')
                    except Exception:
                        continue
                else:
                    try:
                        loads += calculate_loads(start_loads_info, end_loads_info, fps) 
                        main_window['start_loads'].update('')  # Calculates Loads
                        main_window['end_loads'].update('')
                    except Exception:
                        continue
            if event == 'Calculate':
                # Gets the Values from the Input Boxes
                start_info = values['start']
                end_info = values['end']
                fps = values['fps']
                try:  # Checks if the FPS is Valid
                    fps = d(fps)
                except Exception:
                    sg.popup('Error (FPS)', 'FPS is not an valid number.', title='Error', icon=r'assets\pytime.ico')
                    continue
                if fps == 0:
                    sg.popup('Error (FPS)', 'FPS cannot be 0.', title='Error', icon=r'assets\pytime.ico')
                    continue
                else:
                    if not 'loads' in globals():  # Check if the Loads Variables Exists
                        loads = 0  # Sets Loads to 0
                    # Runs the Final Function
                    calculate_time(start_info, end_info, loads, fps)
                    # Clears Input Boxes
                    main_window['start'].update('')
                    main_window['end'].update('')
            # Checks if the Paste Button is Pressed
            # Pastes the Clipboard to the Input Box
            if event == 'start_paste':
                main_window['start'].update(paste())
            if event == 'end_paste':
                main_window['end'].update(paste())
            if event == 'start_loads_paste':
                main_window['start_loads'].update(paste())
            if event == 'end_loads_paste':
                main_window['end_loads'].update(paste())

        main_window.close()  # Closes the Window
    # Made by Conner Speedrunning
