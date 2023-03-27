from decimal import Decimal as d
from json import loads as json_loads
from json.decoder import JSONDecodeError
from math import floor


def calculate_time(start_time: d, end_time: d, fps: int, loads: tuple = []):
    # Get LCT time
    start_time = parse_info(start_time)
    end_time = parse_info(end_time)

    for cell in loads:
        for cell in cell:
            cell = parse_info(cell)

    # Get frames from LCT
    start_time = get_frame(start_time, fps)
    start_time = get_frame(end_time, fps)

    for cell in loads:
        for cell in cell:
            cell = get_frame(cell, fps)

    # Calculate sum of loads'
    sum_of_loads = 0

    for cell in loads:
        sum_of_loads += (cell[1] - cell[0]) / fps
    sum_of_loads = round(sum_of_loads, 3)

    # Calculate time before loads
    with_loads = (end_time - start_time) / fps
    with_loads = round(with_loads, 3)

    # Calculate time after loads
    if not sum_of_loads == 0:
        without_loads = with_loads - sum_of_loads

    # Format time in SRC style
    if not sum_of_loads == 0:
        without_loads = format_time(without_loads)
    with_loads = format_time(with_loads)

    # Generate mod note
    if without_loads == with_loads:
        mod_note = f"Mod Note: Retimed to {with_loads} at {fps} FPS using [PyTime](https://github.com/ConnerConnerConner/PyTime)"
    else:
        mod_note = f"Mod Note: Retimed to {without_loads} without loads, and {with_loads} with loads at {fps} FPS using [PyTime](https://github.com/ConnerConnerConner/PyTime)"

    # Generate output dictionary

    output = {
        "without_loads": without_loads,
        "with_loads": with_loads,
        "mod_note": mod_note,
        "loads": (with_loads == without_loads),
    }
    return output


def parse_info(info: str):
    try:
        parsed_info = json_loads(info)
    except JSONDecodeError:
        raise TypeError("Invalid json.")
    except:
        raise RuntimeError("Failed to parse json.")
    try:
        lct = d(parsed_info["lct"])
    except KeyError or ValueError:
        raise TypeError("Invalid json.")
    return lct


def get_frame(time: d, fps: int):
    output = d(time) * d(fps)
    output = floor(output)
    return output


def format_time(time):
    time = str(time)
    time = time.split(".", 1)
    seconds = int(time[0])
    milliseconds = str(time[1])
    minutes = seconds // 60
    hours = minutes // 60
    seconds = seconds - (minutes * 60)
    minutes = minutes - (hours * 60)
    seconds = str(seconds).rjust(2, "0")
    minutes = str(minutes).rjust(2, "0")
    if len(str(hours)) < 2:
        hours = str(hours).rjust(2, "0")
    return f"{str(hours)}h {str(minutes)}m {str(seconds)}s {milliseconds}ms"
