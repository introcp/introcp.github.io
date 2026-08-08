def hms(nsec):
    """Takes nsec (n. of seconds) and splits in hours, minutes, seconds"""
    hh = nsec // 3600
    nsec = nsec % 3600
    mm = nsec // 60
    ss = nsec % 60
    return hh, mm, ss


print(hms(4000))
print(hms(100000))
