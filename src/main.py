import curses, pyperclip, decimal, json
from curses import wrapper
from curses.textpad import Textbox, rectangle
def main(stdscr):
    time = 0
    menu_current = 0
    in_menu = True
    logo = """

                                 d8,                     
                          d8P   `8P                      
                        d888888P                          
    ?88,.d88b,?88   d8P   ?88'    88b  88bd8b,d88b  d8888b
    `?88'  ?88d88   88    88P     88P  88P'`?8P'?8bd8b_,dP
      88b  d8P?8(  d88    88b    d88  d88  d88  88P88b    
      888888P'`?88P'?8b   `?8b  d88' d88' d88'  88b`?888P'
      88P'           )88                                  
     d88            ,d8P                                  
     ?8P         `?888P'                                  

    """
    stdscr.clear()
    stdscr.addstr(6, 0, logo, curses.A_BOLD)
    stdscr.refresh()
    stdscr.getch()
    stdscr.clear()
    seg_win = curses.newwin(1, 8, 3, 2)
    seg_box = Textbox(seg_win)
    rectangle(stdscr, 2, 1, 4, 10)
    stdscr.addstr(1, 1, "How many Segments are there in this video?", curses.A_BOLD)
    stdscr.refresh()
    seg_box.edit()
    segment_count = seg_box.gather()
    segment_count = int(segment_count)
    stdscr.clear()
    for i in range(segment_count):
        stdscr.addstr(1, 1, "Copy the Debug Info of the Starting Frame", curses.A_BOLD)
        stdscr.addstr(2, 1, "Once this is done Press Any Key", curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()
        debug_info_start = pyperclip.paste()
        stdscr.clear()
        stdscr.addstr(1, 1, "Copy the Debug Info of the Ending Frame", curses.A_BOLD)
        stdscr.addstr(2, 1, "Once this is done Press Any Key", curses.A_BOLD)
        stdscr.getch()
        debug_info_end = pyperclip.paste()
        stdscr.refresh()
        stdscr.clear()
        debug_info_start_dict = json.loads(debug_info_start)
        debug_info_end_dict = json.loads(debug_info_end)
        cmt_start = debug_info_start_dict['cmt']
        cmt_end = debug_info_end_dict['cmt']
        time = (decimal.Decimal(cmt_end) - decimal.Decimal(cmt_start)) + decimal.Decimal(time)
    stdscr.addstr(1, 2, "[1] Just Time")
    stdscr.addstr(2, 2, "[2] Mod Time")
    stdscr.refresh()
    time = str(time)
    time = time.split(".", 1)
    if len(time) > 0:
        seconds = time[0]
        milliseconds = time[1]
        milliseconds = str(milliseconds)
        seconds = int(seconds)
    def seconds_to_time(seconds):
        seconds = int(seconds)
        minutes = seconds//60
        hours = minutes//60
        seconds = str(seconds)
        minutes = str(minutes)
        hours = str(hours)
        if seconds == "0":
            return ("0." + milliseconds)
        elif minutes == "0":
            if len(seconds) == 1:
                return (f"0{seconds}.{milliseconds}")
            else:
                return (f"{seconds}.{milliseconds}")
        elif hours == "0":
            return (f"{minutes}:{seconds}.{milliseconds}")
        else:
            return (f"{hours}:{minutes}:{seconds}.{milliseconds}")
    formatted_time = seconds_to_time(seconds)
    while in_menu:
        menu_select = stdscr.getkey()
        if menu_select == "1":
            menu_current = 1
            stdscr.clear()
            stdscr.addstr(1, 2, "[1] Just Time", curses.A_REVERSE)
            stdscr.addstr(2, 2, "[2] Mod Time")
            stdscr.refresh()
        elif menu_select == "2":
            menu_current = 2
            stdscr.clear()
            stdscr.addstr(1, 2, "[1] Just Time")
            stdscr.addstr(2, 2, "[2] Mod Time", curses.A_REVERSE)
            stdscr.refresh()
        elif menu_select == "q":
            if menu_current == 0:
                continue
            elif menu_current == 1:
                in_menu = False
                stdscr.clear()
                stdscr.addstr(1, 1, f"The Final Time is {formatted_time}", curses.A_BOLD)
                stdscr.addstr(2, 1, "Press Any Key to Exit", curses.A_BOLD)
                stdscr.refresh()
            elif menu_current == 2:
                in_menu = False
                stdscr.clear()
                pyperclip.copy(f"Mod Note: Retimed to {formatted_time} using PyTime")
                stdscr.addstr(1, 1, f"Mod Note: Retimed to {formatted_time} using PyTime", curses.A_BOLD)
                stdscr.addstr(2, 1, "Mod Note Has Been Copied to Clipboard", curses.A_BOLD)
                stdscr.addstr(3, 1, "Press Any Key to Exit", curses.A_BOLD)
                stdscr.refresh()
        else:
           continue
    stdscr.getch()

wrapper(main)