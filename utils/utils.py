def time_to_seconds(t):
    # map(int, value) has int applied to every item in value
    minutes, seconds = map(int, t.split(":"))
    return minutes * 60 + seconds

def format_time(t):
    return ":".join(str(t).split(":")[1:])