def val_or_max(val, limit):
    if val > limit:
        return limit
    else:
        return val

def val_or_min(val, limit):
    if val < limit:
        return limit
    else:
        return val