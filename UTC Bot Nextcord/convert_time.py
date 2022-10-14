def convert_time_str(time):
    if float(time) < 0:
        return float(time)
    if type(time) == type("string"):
        time = convert_time_str(convert_time_float(time))
        return time
    # float to str format mm:ss.ms using only necessary numbers
    time = float(time)
    
    if time >= 60:
        mins = int(time//60)
        sec = int(time%60)
        temp, ms = str(time).split(".")
        if len(str(sec)) == 1:
            sec = f"0{sec}"
        ms = f"{ms}0"
        time_str = f"{mins}:{sec}.{ms[:2]}"

    else:
        sec = int(time%60)
        temp, ms = str(time).split(".")
        ms = f"{ms}0"
        if len(str(sec)) == 1:
            sec = f"{sec}"
        time_str = f"{sec}.{ms[:2]}"      
    return time_str

def convert_time_float(time):
    # str to float
    time = str(time)
    if ":" in time:
        mins, temp = time.split(":")
        sec, ms = str(float(temp)).split(".")
        ms = f"{ms}0"
        time_float = int(mins)*60+int(sec)+int(ms[:2])/100
        return time_float
    else:
        sec, ms = str(float(time)).split(".")
        ms = f"{ms}0"
        time_float = int(sec)+int(ms[:2])/100
        return time_float

def mean(times_list):
    mean = 0
    for x in range(len(times_list)):
        times_list[x] = convert_time_float(times_list[x])
        mean += times_list[x]
    min_time = times_list[0]
    max_time = times_list[0]
    for i in range(len(times_list)):
        if times_list[i] < min_time:
            min_time = times_list[i]
        if times_list[i] > max_time:
            max_time = times_list[i]
    mean += -max_time-min_time  
    return convert_time_float(mean/3)