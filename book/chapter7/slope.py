from shapely.geometry import LineString
import math
from math import atan, pi


def get_average_curvature(line: LineString):
    coords = list(line.coords)
    if len(coords) < 3:
        return 0

    def slope(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        if dx == 0.0 and dy == 0.0:
            return None

        if dx == 0.0:
            return math.inf

        return dy / dx

    def angle_between(a, b, c):
        m1 = slope(a, b)
        m2 = slope(b, c)

        if m1 is None or m2 is None:
            return 0.0

        if m1 == math.inf and m2 != math.inf:
            val = pi/2 - atan(m2)
            if val < 0:
                return val + pi

            return val

        if m1 != math.inf and m2 == math.inf:
            val = pi/2 - atan(m1)
            if val < 0:
                return val + pi

            return val

        denominator = 1 + m1 * m2
        if denominator == 0:
            return pi/2

        tan_theta = (m2 - m1) / denominator
        angle = abs(atan(tan_theta))

        return angle

    angles = []
    for i in range(1, len(coords)-1):
        angle = angle_between(coords[i-1], coords[i], coords[i+1])
        angles.append(angle)

    return sum(angles) / len(angles)

from math import pi
from shapely.wkt import loads

# test case 1
line = loads("LINESTRING(2 2, 1 1, 2 0)")
assert pi/2 == get_average_curvature(line)

# test case 2
line2 = loads("LINESTRING(2 2, 1 1, 0 2)")
assert pi/2 == get_average_curvature(line2)

# test case 3
line3 = loads("LINESTRING(2 2, 1 1, 0 0)")
assert 0 == get_average_curvature(line3)

# test case 4
line4 = loads("LINESTRING(2 3, 2 4, 0 0)")
assert 0.46 == round(get_average_curvature(line4), 2)

# test case 5
line5 = loads("LINESTRING(3 3, 2 4, 2 7)")
assert 2.36 == round(get_average_curvature(line5), 2)

# additional test cases


line_1 = loads("LINESTRING(0 0, 5 5, 10 10)")
assert 0 == round(get_average_curvature(line_1), 2)

line_2 = loads("LINESTRING(2 2, 7 7, 12 12)")
print("s")
assert 0 == round(get_average_curvature(line_2), 2)

# perpendicular
line_3 = loads("LINESTRING(0 0, 10 0, 10 5)")
assert 1.57 == round(get_average_curvature(line_3), 2)

line_4 = loads("LINESTRING(0 0, 0 10, -5 10)")
assert 1.57 == round(get_average_curvature(line_4), 2)

line_5 = loads("LINESTRING(3 1, 3 7, 4 8, 5 9)")
assert 0.39 == round(get_average_curvature(line_5), 2)

line_6 = loads("LINESTRING(0 0, 5 3, 10 6)")
assert 0.0 == round(get_average_curvature(line_6), 2)

line_7 = loads("LINESTRING(0 5, 10 5, 15 5, 20 5)")
assert 0.0 == round(get_average_curvature(line_7), 2)

line_8 = loads("LINESTRING(0 0, 10 2, 12 4, 15 8)")
assert 0.36 == round(get_average_curvature(line_8), 2)

line_9 = loads("LINESTRING(0 0, 10 1, 15 1.5)")
assert 0.0 == round(get_average_curvature(line_9), 2)

line_10 = loads("LINESTRING(0 0, 10 1.1, 15 1.7)")
assert 0.01 == round(get_average_curvature(line_10), 2)

line_11 = loads("LINESTRING(0 0, 10 10, 20 20)")
assert 0.0 == round(get_average_curvature(line_11), 2)

line_12 = loads("LINESTRING(20 20, 10 10, 0 0)")
assert 0.0 == round(get_average_curvature(line_12), 2)

line_13  = loads("LINESTRING(2 3, 2 10, 3 12, 4 15)")
assert 0.3 == round(get_average_curvature(line_13), 2)

line_14  = loads("LINESTRING(0 0, 10 5, 12 6, 20 10)")
assert 0.0 == round(get_average_curvature(line_14), 2)

line_15 = loads("LINESTRING(0 0, 0.00001 10, 1 11, 2 12)")
assert 0.39 == round(get_average_curvature(line_15), 2)

line_16 = loads("LINESTRING(0 0, 0.00002 10, 2 11.5, 3 12.5)")
assert 0.53 == round(get_average_curvature(line_16), 2)

line_17 = loads("LINESTRING(0 0, 0 0, 5 5)")
assert 0.0 == round(get_average_curvature(line_17), 2)

line_18 = loads("LINESTRING(0 0, 10 0, 10 1)")
assert 1.57 == round(get_average_curvature(line_18), 2)

line_19 = loads("LINESTRING(2 3, 2 4, 0 0)")
assert 0.46 == round(get_average_curvature(line_19), 2)

line_20 = loads("LINESTRING(0 0, 5 0, 10 0)")
assert 0.0 == round(get_average_curvature(line_20), 2)
