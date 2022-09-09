
from mcpi import minecraft
import random
import math
from mcpi import vec3
from mcpi import block

mc = minecraft.Minecraft.create()

#random width = 10-15
#random height = 16-20

def get_random_coords(vil_start, vil_end, amount):
    coords = []
    min_distance_between_coords =  40   

    for i in range(amount):
        condition_1 = False
        condition_2 = False

        while not (condition_1 and condition_2):
            x = random.randint(vil_start.x, vil_end.x)
            z = random.randint(vil_start.z, vil_end.z)

            condition_1 = True
            condition_2 = True

            for coord in coords:
                # if math.fabs(coord[0] - x) + math.fabs(coord[1] - z) < min_distance_between_coords:
                if math.sqrt((coord[0] - x) ** 2) + math.sqrt((coord[1] - z)** 2) < min_distance_between_coords:
                    condition_2 = False
                    break
            
        coords.append((x, z))
        mc.setBlock(x,101, z, 3)

    return coords

def place_plots(points, distance_dict):
    print(points)
    print(distance_dict)
    buffer = 2
    for point in points:
        mc.setBlocks(   point[0] - int(distance_dict[point]/2) + buffer,    100,     point[1] - int(distance_dict[point]/2) + buffer,
                        point[0] + int(distance_dict[point]/2) - buffer,    100,     point[1] + int(distance_dict[point]/2) - buffer, 17)


# https://en.wikipedia.org/wiki/Voronoi_diagram
def generate_path_and_plots(vil_start, vil_end, vor_amount):
    voronoi_points = get_random_coords(vil_start, vil_end, vor_amount)
    voronoi_distances = dict()
    path_coords_set = set()



    for x in range(vil_start.x, vil_end.x):
        for z in range(vil_start.z, vil_end.z):

            
            distances = []

            for coord in voronoi_points:
                distances.append([coord, math.fabs(coord[0] - x) + math.fabs(coord[1] - z)])
                # distances.append([coord, math.sqrt((coord[0] - i) ** 2 + (coord[1] - j) ** 2)])
            
            distances.sort(key = lambda list : list[1])



            distance_sub = distances[0][1] - distances[1][1]
            if distance_sub <= 1 and distance_sub >= -1:
                if distances[0][0] not in voronoi_distances:
                    voronoi_distances[distances[0][0]] = distances[0][1]

                elif voronoi_distances[distances[0][0]] > distances[0][1]:
                    voronoi_distances[distances[0][0]] = distances[0][1]
                if distances[1][0] not in voronoi_distances:
                    voronoi_distances[distances[1][0]] = distances[1][1]

                elif voronoi_distances[distances[1][0]] > distances[1][1]:
                    voronoi_distances[distances[1][0]] = distances[1][1]

                print(distances)
                path_coords_set.update({(x-1,z+1),  (x,z+1),    (x+1,z+1),
                                          (x-1,z),    (x,z),      (x+1,z),
                                          (x-1,z-1),  (x,z-1),    (x+1,z-1)})
                mc.setBlocks(   x-1,    100,    z-1, 
                                x+1,    100,    z+1, 1)

    place_plots(voronoi_points, voronoi_distances)

    return path_coords_set
    

if __name__ == '__main__':
    vil_length = 85
    num_points = 5

    vil_start = mc.player.getTilePos()
    vil_end = vec3.Vec3(vil_start.x + vil_length, 
                        vil_start.y,
                        vil_start.z + vil_length)

    generate_path_and_plots(vil_start, vil_end, num_points)