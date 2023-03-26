import decimal, json
from rich.prompt import Prompt
end_check = True
debug_info_start = ""
debug_info_end = ""
time = 0.0
exist = False
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
print(logo)
segment = int(Prompt.ask("How many Segments are there in the Video?"))
for _ in range(segment):
    while end_check:
        if exist == False:
            start_buffer = Prompt.ask("\n(Debug Info) What is the Starting Frame")
            exist = True
        else:
            start_buffer = input()
        debug_info_start = debug_info_start + start_buffer
        if start_buffer == "}":
            end_check = False
        else:
            continue
    end_check = True
    exist = False
    while end_check:
        if exist == False:
            end_buffer = Prompt.ask("\n(Debug Info) What is the Ending Frame")
            exist = True
        else:
            end_buffer = input()
        debug_info_end = debug_info_end + end_buffer
        if end_buffer == "}":
            end_check = False
        else:
            continue
    #Atleast JSON parsing is here now
    debug_info_start_dict = json.loads(debug_info_start)
    debug_info_end_dict = json.loads(debug_info_end)
    cmt_start = debug_info_start_dict['cmt']
    cmt_end = debug_info_end_dict['cmt']
    #todo Make this shit accurate :)
    time = (decimal.Decimal(cmt_end) - decimal.Decimal(cmt_start)) + decimal.Decimal(time)
#formats the time
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
#prints the time
print(f"Your final time is: {formatted_time}\n\n")
print(f"Mod Note: Retimed to {formatted_time} using PyTime")
#prompts the user to close the program
close = input("Press Enter to Close")