
from mcpi import minecraft

import random
import math

mc = minecraft.Minecraft.create()


def get_random_coords(vil_start, vil_end, am):
    coords = []

    for i in range(am):
        x = random.randint(vil_start.x, vil_end.x)
        z = random.randint(vil_start.z, vil_end.z)
        coords.append((x, z))
        mc.setBlock(x,101, z, 3)

    return coords


def generate_path(vil_start, vil_end, am):
    coords = get_random_coords(vil_start, vil_end, am)
    for i in range(vil_start.x, vil_end.x):
        for j in range(vil_start.z, vil_end.z):
            closest_1 = closest_2 =  [vil_end.x ** 3, vil_end.y ** 3]
            distances = []
            for coord in coords:
                distances.append([coord, math.fabs(coord[0] - i) + math.fabs(coord[1] - j)])
            
            distances.sort(key = lambda list : list[1])

            distance_sub = distances[0][1] - distances[1][1]
            if distance_sub < 4 and distance_sub > -4:
                mc.setBlock(i,100,j, 1)