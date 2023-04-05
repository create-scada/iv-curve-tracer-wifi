def find_pmax_idx(generator):

    pmax = 0.0
    pmax_idx = 0

    for i, point in enumerate(generator(0, 4096, 10)):
        i *= 10
        voltage, current = point
        power = voltage * current

        if power > pmax:
            pmax = power
            pmax_idx = i

    return pmax_idx

def smooth(points, new_point_weight=0.3):

    points.sort(key=lambda x: x[0])

    voltage_mean = points[0][0]
    current_mean = points[0][1]

    for i in range(1, len(points)):
        voltage = points[i][0]
        current = points[i][1]

        voltage_mean = (voltage_mean * (1.0-new_point_weight)) + (voltage * new_point_weight)
        current_mean = (current_mean * (1.0-new_point_weight)) + (current * new_point_weight)

        points[i][0] = voltage_mean
        points[i][1] = current_mean

def get_oversample_region(points):
    '''
    max_dist = 0.0
    max_dist_idx = 0

    for i in range(1, len(points)):
        voltage1 = points[i][0]
        voltage2 = points[i-1][0]
        dist = voltage1 - voltage2

        if dist > max_dist:
            max_dist = dist
            max_dist_idx = i

    return max_dist_idx
    '''

    mid_voltage = points[-1][0] / 2.0
    for i in range(len(points)):
        (voltage, current) = points[i]
        if voltage > mid_voltage:
            return i
