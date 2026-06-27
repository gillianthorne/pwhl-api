def time_to_seconds(t):
    # map(int, value) has int applied to every item in value
    minutes, seconds = map(int, t.split(":"))
    return minutes * 60 + seconds

def format_time(t):
    return ":".join(str(t).split(":")[1:])

def time_convert(t):
    hours, seconds, minutes = str(t).split(":")

    if hours == "0":
        hours = "12"
    return f"{hours.rjust(2, "0")}:{minutes.rjust(2, "0")}:{seconds.rjust(2, "0")}"