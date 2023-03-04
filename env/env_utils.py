MINUTES_IN_HOUR = 60
def get_timestring(t: float) -> str:
    hour = str(int(t))
    minute = round((t - int(t)) * MINUTES_IN_HOUR)
    prefix_zero = "0" if minute < 10 else ""
    return f"{hour}:{prefix_zero}{minute} PM"
