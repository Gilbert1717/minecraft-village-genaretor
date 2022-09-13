
from mcpi import minecraft
from mcpi import vec3
from mcpi import block

import random
import math

from House import Structure
from House import McPosition

from Plot import Plot

mc = minecraft.Minecraft.create()

#random width = 10-15
#random height = 16-20

def get_random_coords(vil_start, vil_end, amount):
    coords = []
    min_distance_between_coords =  40   

    for i in range(amount):
        too_close = True
        
        while too_close:
            x = random.randint(vil_start.x, vil_end.x)
            z = random.randint(vil_start.z, vil_end.z)
            too_close = False
            
            for coord in coords:
                # if math.fabs(coord[0] - x) + math.fabs(coord[1] - z) < min_distance_between_coords:
                
                if math.sqrt((coord.x - x) ** 2) + math.sqrt((coord.z - z)** 2) < min_distance_between_coords:
                    too_close = True
                    break
            
        coords.append(vec3.Vec3(x, 0, z))
        
        
        mc.setBlock(x,
                    100,
                    z,
                    3)
    
    return coords

def generate_plots(points, distance_dict):
    plots = []
    for point in points:
        new_plot = Plot(point,distance_dict[point])
        plots.append(new_plot)

    return plots

# https://en.wikipedia.org/wiki/Voronoi_diagram
def generate_path_and_plots(vil_start, vil_end, vor_amount):
    
    voronoi_points = get_random_coords(vil_start, vil_end, vor_amount)
    voronoi_distances = dict()
    path_coords = []


    for x in range(vil_start.x, vil_end.x):
        for z in range(vil_start.z, vil_end.z):

            distances = [] # list of distances from the current x,z iteration to all voronoi points

            for coord in voronoi_points:
                distances.append([(coord.x, coord.z), math.fabs(coord.x - x) + math.fabs(coord.z - z)])
            
            distances.sort(key = lambda list : list[1]) # sorts distances in order of ascending distance

            
            distance_sub = distances[0][1] - distances[1][1] # difference in distance between the 2 closest vornoi points

            if distance_sub <= 1 and distance_sub >= -1:

                path_coords.append(vec3.Vec3(x, 0, z)) # get the y coord later with getblockheight
        
                ############ this code block populates voronoi_distances with a voronoi point's distance to the closest path
                if distances[0][0] not in voronoi_distances:
                    voronoi_distances[distances[0][0]] = distances[0][1]

                elif voronoi_distances[distances[0][0]] > distances[0][1]:
                    voronoi_distances[distances[0][0]] = distances[0][1]
                if distances[1][0] not in voronoi_distances:
                    voronoi_distances[distances[1][0]] = distances[1][1]

                elif voronoi_distances[distances[1][0]] > distances[1][1]:
                    voronoi_distances[distances[1][0]] = distances[1][1]
                ###########

                
                #mc.setBlock(   x,    getBlockHeight(x, z),    z, 1)
                #mc.setBlocks(   x-1,    100,    z-1, 
                                #x+1,    100,    z+1, 1)
    
    for coord in path_coords:
        print('getting block height for', coord.x, coord.z)
        coord.y = getBlockHeight(coord.x, coord.z)

        mc.setBlock(coord.x, coord.y, coord.z, block.COBBLESTONE.id)
    
    for coord in path_coords:
        print('placing blocks')
        mc.setBlocks(   coord.x-1,    coord.y,    coord.z-1, 
                        coord.x+1,    coord.y,    coord.z+1, block.COBBLESTONE.id)
        
    generate_plots(voronoi_points, voronoi_distances)   

    return path_coords  


def getBlockHeight(block_x, block_z):
    
    y = mc.getHeight(block_x, block_z)
    
    ground_block = mc.getBlock(block_x, y, block_z)
    
    if ground_block == block.DIRT.id or ground_block == block.GRASS.id:
        
        return y
    
    else:
        
        while ground_block != block.DIRT.id or ground_block == block.GRASS.id:
            y = y - 1
            ground_block = mc.getBlock(block_x, y, block_z)
            
        return y
    

if __name__ == '__main__':
    vil_length = 85
    num_points = 5

    vil_start = mc.player.getTilePos()
    vil_end = vec3.Vec3(vil_start.x + vil_length, 
                        vil_start.y,
                        vil_start.z + vil_length)
    
    generate_path_and_plots(vil_start, vil_end, num_points)
   