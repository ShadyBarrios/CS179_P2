import os
from coordinate import Coordinate

def valid_file(file_name: str) -> bool:
    # must be txt file
    if file_name[-4:] != ".txt":
        print("ERROR: File must be .txt type.")
        return False
    
    # must exist to be read
    if not os.path.isfile(file_name):
        print(f"ERROR: {file_name} not found")
        return False

    line_count = 0
    with open(file_name, "r") as file:
        data = file.read()
        line_count = data.count('\n')
    
    # check coordinate count
    if(line_count > 4096):
        print(f"ERROR: There must be at most 4096 nodes in {file_name}")
        return False
    elif(line_count == 0):
        print(f"ERROR: {file_name} is empty")
        return False
    
    return True

def parse_input(file_name: str) -> list[Coordinate]:
    coordinates:list[Coordinate] = []
    index = 0

    try:
        with open(file_name, "r") as file:
            while True:
                line = file.readline()
                index += 1

                # readline returns "" when EOF
                if line == "":
                    break

                coordinate_str = line.split()
                if len(coordinate_str) != 2:
                    print(f"ERROR: Improper coordinate formatting at line {index}")
                    exit()
                
                try:
                    x = float(coordinate_str[0])
                    y = float(coordinate_str[1])

                    if x < 0 or y < 0:
                        print(f"ERROR: Negative coordinates at line {index}")
                        exit()
                except ValueError:
                    print(f"ERROR: Improper coordinate at line {index}")
                    exit()

                coordinate = Coordinate(x,y)
                coordinates.append(coordinate)
    except FileNotFoundError:
        print(f"ERROR: {file_name} not found")
        exit()
    
    return coordinates

def parse_time(hour:int, minute:int):
    if hour < 0 or minute < 0:
        print("ERROR: Time components are negative...")
        exit()

    if minute >= 60:
        minute_rollover = (minute // 60)
        minute -= minute_rollover * 60
        hour += minute_rollover
    
    if hour >= 24:
        hour_rollover = (hour // 24)
        hour -= hour_rollover * 24
    
    if hour >= 12:
        meridiem = "pm"
    else:
        meridiem = "am"
    
    if hour == 0:
        hour = 12
    
    if hour > 12:
        hour -= 12
    
    time = f"{hour:02d}:{minute:02d}{meridiem}"
    return time

def write_to_file(locations:list[int], file_name:str) -> bool:
    try:
        with open(file_name, "w") as file:
            for location in locations:
                line = f"{location}\n"
                file.write(line)
        return True
    except FileNotFoundError:
        print(f"ERROR: {file_name} could not be opened")
        return False