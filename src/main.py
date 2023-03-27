def main():
    from json import loads as json_loads
    from json.decoder import JSONDecodeError
    from pyperclip import copy, paste
    import PySimpleGUI as sg
    from decimal import Decimal as d

    # GUI Theme
    sg.theme('DarkGrey12')
    
    # Variables
    loads = []

    # Gets the frame from CMT
    def get_frame(time, fps):
        output = d(time) * d(fps)
        output = round(output, 0)
        return output

    # Formats the time to the SRC format
    def format_time(time):
        time = str(time)
        time = time.split('.', 1)
        seconds = int(time[0])
        milliseconds = str(time[1])
        minutes = seconds // 60
        hours = minutes // 60
        if seconds >= 60:  # makes sure that the seconds are less than 60
            seconds = seconds - (minutes * 60)
        if minutes >= 60:  # makes sure that the minutes are less than 60
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
            sg.popup_error('Error (Start)', 'Debug Info is not valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        except KeyError:
            sg.popup_error('Error (Start)', 'CMT is not Valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        start_frame = get_frame(start_time, fps)
        try:
            end_time = json_loads(end_info)['cmt']
        except JSONDecodeError:
            sg.popup_error('Error (End)', 'Debug Info is not valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        except KeyError:
            sg.popup_error('Error (End)', 'CMT is not Valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        end_frame = get_frame(end_time, fps)
        # Calculates the Loads
        loads = (end_frame - start_frame) / fps
        loads = round(loads, 3)
        if start_frame > end_frame:  # Checks if the Start is greater than the End
            sg.popup_error('Error', 'The start is greater than the end.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        # Rounds the Loads to the nearest frame just in case the rounding is off
        return loads

    # Calculates the Final Time
    def calculate_time(start_info, end_info, load_array, fps):
        loads = 0
        for i in range(len(load_array)):
            loads =+ load_array[i]
        try:
            start_time = json_loads(start_info)['cmt']
        except JSONDecodeError:
            sg.popup_error('Error (Start)', 'Debug Info is not valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        except KeyError:
            sg.popup_error('Error (Start)', 'CMT is not Valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        start_frame = get_frame(start_time, fps)
        try:
            end_time = json_loads(end_info)['cmt']
        except JSONDecodeError:
            sg.popup_error('Error (End)', 'Debug Info is not valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        except KeyError:
            sg.popup_error('Error (End)', 'CMT is not Valid.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        end_frame = get_frame(end_time, fps)
        # Rounds the CMT to the nearest frame
        # Calculates the Final Time
        time_loads = (end_frame - start_frame) / fps
        time_loads - round(time_loads, 3)
        if start_time > end_time:  # Checks if the Start is greater than the End
            sg.popup_error('Error', 'The start is greater than the end.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        if loads > time_loads:  # Checks if the Loads are greater than the Time
            sg.popup_error('Error', 'The Loads is greater than the Time.',title='Error', icon=r'assets\pytime.ico')  # Error Message
            return
        # Rounds Loads for the millionth time
        time = time_loads - loads  # Gets the Time without Loads
        time = round(time, 3)
        # Formats the Time
        time = format_time(time)
        time_loads = format_time(time_loads)
        if loads == 0:
            final_confirm = sg.popup_yes_no(f'End Time: {time}', 'Would you like the Mod Note to be Copied to the Clipboard?',title='Results', icon=r'assets\pytime.ico')
            mod_note = f'Mod Note: Retimed to {time} at {fps} FPS using [PyTime](https://github.com/ConnerConnerConner/PyTime)'
        else:
            final_confirm = sg.popup_yes_no(f'Without Loads: {time}, With Loads: {time_loads}', 'Mod Note Copied to Clipboard', title='Results', icon=r'assets\pytime.ico')
            mod_note = f'Mod Note: Retimed to {time} without loads, and {time_loads} with loads at {fps} FPS using [PyTime](https://github.com/ConnerConnerConner/PyTime)'
        if final_confirm == 'Yes':
            copy(mod_note)
        elif final_confirm == 'No':
            return
        
    def loads_box_create():
        global loads
        current_cell = 0
        loop_contents= ''
        layout = [
        [sg.Text('Loads', font=('Helvetica', 36))],
        ]
        for time in loads:
            current_cell += 1
            next_cell = [sg.Text(f'{time}  ', font=('Helvetica', 24)), sg.Button('Remove Load', font=('Helvetica', 16), key=f'remove_load_{current_cell}')]
            layout.append(next_cell)
        print(loop_contents)
        load_window = sg.Window('Load Viewer - PyTime', layout, resizable=False, element_justification='left', icon=r'assets\pytime.ico')
        while True:
            event, values = load_window.read()  # Reads the Window
            if event == sg.WIN_CLOSED:  # Checks if the Window is Closed
                break
            for current_cell in range(1, (len(loads)+1)):
                if event == f'remove_load_{current_cell}':
                    lr_confirm = sg.popup_yes_no('Are you sure you want to remove this load?', title='Remove Load', font=('Helvetica', 16), icon=r'assets\pytime.ico')
                    if lr_confirm == 'Yes':
                        loads[int(current_cell)-1] = d(0)
                    elif lr_confirm == 'No':
                        continue
        load_window.close()
            
    # GUI Layout
    main_layout = [
        [sg.Text('PyTime', font=('Helvetica', 48)), sg.Text(' FPS', font=('Helvetica', 40)), sg.InputText('60', size=(4, 1), key='fps', font=('Helvetica', 36))],
        [sg.Button('Paste', font=('Helvetica', 10), key='start_paste'), sg.InputText(key='start', font=('Helvetica', 16), pad=((5, 0), (0, 0)), size=(20, 1)), sg.Text('  Debug Info Start', font=('Helvetica', 16), justification='right')],
        [sg.Button('Paste', font=('Helvetica', 10), key='end_paste'),sg.InputText(key='end', font=('Helvetica', 16), pad=((5, 0), (0, 0)), size=(20, 1)), sg.Text('  Debug Info End', font=('Helvetica', 16), justification='right')],
        [sg.Button('Paste', font=('Helvetica', 10), key='start_loads_paste'),sg.InputText(key='start_loads', font=('Helvetica', 14), pad=((5, 0), (0, 0)), size=(15, 1)),sg.Text('   Debug Info Start (Loads)', font=('Helvetica', 14), justification='right')],
        [sg.Button('Paste', font=('Helvetica', 10), key='end_loads_paste'),sg.InputText(key='end_loads', font=('Helvetica', 14), pad=((5, 0), (0, 0)), size=(15, 1)),sg.Text('   Debug Info End (Loads)', font=('Helvetica', 14), justification='right')],
        [sg.Button('Calculate', font=('Helvetica', 18)), sg.Button('Add Loads', font=('Helvetica', 18)), sg.Button('View Loads', font=('Helvetica', 18))]
    ]

    main_window = sg.Window('PyTime', main_layout, resizable=False, element_justification='left', size=(516, 275), finalize=True, icon=r'assets\pytime.ico')
    # Main Loop
    while True:
        event, values = main_window.read()  # Reads the Window
        if event == sg.WIN_CLOSED:  # Checks if the Window is Closed
            break
        if event == 'View Loads':  # Checks if the Remove All Loads Button is Pressed
            if loads == [] or loads == [0] or not loads in globals:
                sg.popup_error('Error (Loads)', 'There are no loads.', title='Error', icon=r'assets\pytime.ico')
            else:
                loads_box_create()
        if event == 'Add Loads':  # Checks if the Add Loads Button is Pressed
            # Gets the Values from the Input Boxes
            start_loads_info = values['start_loads']
            end_loads_info = values['end_loads']
            fps = values['fps']
            try:  # Checks if the FPS is Valid
                fps = d(fps)
            except ValueError:
                sg.popup_error('Error (FPS)', 'FPS is not a valid number.', title='Error', icon=r'assets\pytime.ico')  # Error Message
                continue
            if fps == 0:
                sg.popup_error('Error (FPS)', 'FPS cannot be 0.', title='Error', icon=r'assets\pytime.ico')
                continue
            else:
                loads.append(calculate_loads(start_loads_info, end_loads_info, fps))
            main_window['start_loads'].update('')
            main_window['end_loads'].update('')
            sg.popup(f'Loads Succsessfully Added', title='Loads', font=('Helvetica', 16), icon=r'assets\pytime.ico')  # Success Message
        if event == 'Calculate':
            # Gets the Values from the Input Boxes
            start_info = values['start']
            end_info = values['end']
            fps = values['fps']
            try:  # Checks if the FPS is Valid
                fps = d(fps)
            except ValueError:
                sg.popup_error('Error (FPS)', 'FPS is not an valid number.', title='Error', icon=r'assets\pytime.ico')
                continue
            if fps == 0:
                sg.popup_error('Error (FPS)', 'FPS cannot be 0.', title='Error', icon=r'assets\pytime.ico')
                continue
            else:
                loads = [0]
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
if __name__ == '__main__':
    main()