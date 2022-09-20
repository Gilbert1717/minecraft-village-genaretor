
from mcpi import minecraft
from mcpi import vec3
from mcpi import block

from fast_query_and_interpolation.mcpi_query_performance import query_blocks

import random
import math

from Plot import Plot

mc = minecraft.Minecraft.create()


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

        coords.append(vec3.Vec3(x, getBlockHeight(x,z), z))
        
        
        mc.setBlock(x,
                    getBlockHeight(x,z) + 1,
                    z,
                    block.BOOKSHELF.id)
    
    return coords

def generate_plots(vil_center,points, distance_dict):
    plots = []
    direction = ''
    for point in points:
        if random.randint(0,1):
            if point.x - vil_center.x > 0:
                direction ='x-'
            else:
                direction = 'x+'
            
            if point.z- vil_center.z > 0:
                away = 'z+'
            else:
                away = 'z-'

        else:
            if point.z- vil_center.z > 0:
                direction = 'z-'
            else:
                direction = 'z+'
            
            if point.x - vil_center.x > 0:
                away = 'x+'
            else:
                away = 'x+'
        # away is used later on to connect the plots with the voronoi path
        
        new_plot = Plot(point,distance_dict[(point.x,point.z)], direction, away)
        plots.append(new_plot)
    
    return plots

# https://en.wikipedia.org/wiki/Voronoi_diagram
def generate_path_and_plots(vil_start, vil_end, vil_center, vor_amount):
    
    voronoi_points = get_random_coords(vil_start, vil_end, vor_amount)
    voronoi_distances = dict()
    path_coords = []
    intersection_coords = []
    bordering_paths = []


    for x in range(vil_start.x, vil_end.x + 1):
        for z in range(vil_start.z, vil_end.z + 1):

            distances = [] # list of distances from the current x,z iteration to all voronoi points

            for coord in voronoi_points:
                distances.append([(coord.x, coord.z), abs(coord.x - x) + abs(coord.z - z)])
            
            distances.sort(key = lambda list : list[1]) # sorts distances in order of ascending distance

            
            distance_sub = distances[0][1] - distances[1][1] # difference in distance between the 2 closest vornoi points
            
            if distance_sub >= -1 and distance_sub <= 1:
                path_coords.append(vec3.Vec3(x, 0, z)) # get the y coord later with getblockheight
        
                ############ this code block populates voronoi_distances with a voronoi point's distance to the closest path.
                if distances[0][0] not in voronoi_distances:
                    voronoi_distances[distances[0][0]] = distances[0][1]

                elif voronoi_distances[distances[0][0]] > distances[0][1]:
                    voronoi_distances[distances[0][0]] = distances[0][1]
                if distances[1][0] not in voronoi_distances:
                    voronoi_distances[distances[1][0]] = distances[1][1]

                elif voronoi_distances[distances[1][0]] > distances[1][1]:
                    voronoi_distances[distances[1][0]] = distances[1][1]
                ###########

                distance_sub2 = distances[1][1] - distances[2][1] #difference in distance between the 2nd and 3rd closest points
                if distance_sub2 >= -1 and distance_sub2 <= 1:
                        intersection_coords.append(vec3.Vec3(x,0,z)) 

                if (x == vil_start.x or x == vil_end.x) or (z == vil_start.z or z == vil_end.z):
                    bordering_paths.append(vec3.Vec3(x,0,z))
    

    
    plots = generate_plots(vil_center, voronoi_points, voronoi_distances)

    return path_coords,intersection_coords,bordering_paths, plots

def get_path_height(path_coords):
    path_coords_tuple = []
    for coord in path_coords:
        path_coords_tuple.append((coord.x,coord.z))

    query_results = query_blocks(path_coords_tuple,'world.getHeight(%d,%d)',int)
    #DOES NOT CHECK FOR LEAVES OR TREES OR WATER
    #TODO: MAKE IT CHECK LEAVES AND OTHER STUFF
    for result in query_results:
        mc.setBlocks(   result[0][0]-1,    result[1],    result[0][1]-1, 
                        result[0][0]+1,    result[1],    result[0][1]+1, block.COBBLESTONE.id)

    #for coord in path_coords:
        #print('getting block height for', coord.x, coord.z)
        #coord.y = getBlockHeight(coord.x, coord.z)
    #    mc.setBlock(coord.x, coord.y, coord.z, block.COBBLESTONE.id)
    
    
    #for coord in path_coords:
    #    mc.setBlocks(   coord.x-1,    coord.y,    coord.z-1, 
    #                    coord.x+1,    coord.y,    coord.z+1, block.COBBLESTONE.id)
        #mc.setBlock(   coord.x,    100,    coord.z, block.GLOWING_OBSIDIAN)


    


def getBlockHeight(block_x, block_z):
    """DOES NOT WORK IF SETWORLDSPAWN HEIGHT IS NOT SET TO 0"""
    y = mc.getHeight(block_x, block_z)
    
    ground_block = mc.getBlock(block_x, y, block_z)
    
    while (ground_block != block.GRASS.id and ground_block != block.DIRT.id and
            ground_block !=block.WATER_STATIONARY.id and ground_block != block.WATER_FLOWING.id 
            and ground_block != block.SAND.id and ground_block != block.STONE.id):
        
        y = y - 1
        ground_block = mc.getBlock(block_x, y, block_z)
        #print(block_x, y, block_z, ground_block)

    return y
    
def checkSteepPath(path_coords): # Function to return a list of y-axis blocks that are one unit apart.
    
    check_neighbours = [] # Creates a list to append and check y-axis blocks
    one_unit = 1
    
    for coord in path_coords: # Loops through x,z coords to find y-axis
        coord.y = getBlockHeight(coord.x, coord.z)
        
        check_neighbours.append(coord.y)
    
    for index, block_y in enumerate(check_neighbours[:-1]): #Changes the next block to have a height difference of one unit max.
    
        difference = check_neighbours[index + 1] - check_neighbours[index]
    
        if difference > 1:
            check_neighbours[index + 1] = check_neighbours[index + 1] - (difference - one_unit)
    
    #TODO: Do the reverse so that blocks can go down a steep hill, not only up.
    #TODO: Place the path with these y-coords and set the blocks above them to air.
    return check_neighbours

def remove_dead_ends(path_coords, intersections):
    #traverse the path away from the village centre
    traversed = []
                    
    curr_block = new_path

    while curr_block not in intersection_coords:
        blocks_in_path_coords = False
        potential_next_blocks = [   Vec3(curr_block.x + 1, 0, curr_block.z + n),
                                    Vec3(curr_block.x    , 0, curr_block.z + n),
                                    Vec3(curr_block.x - 1, 0, curr_block.z + n),]

        for block in potential_next_blocks:
             if block in path_coords:
                curr_block = block
                traversed.append(curr_block)
                blocks_in_path_coords = True
                 continue
                        
        if not blocks_in_path_coords:
            for block in traversed:
                if block in path_coords:
                    path_coords.remove(block)
                break
                    
if __name__ == '__main__':
    vil_length = 85
    num_points = 5

    vil_start = mc.player.getTilePos()
    vil_end = vec3.Vec3(vil_start.x + vil_length, 
                        vil_start.y,
                        vil_start.z + vil_length)
    
    generate_path_and_plots(vil_start, vil_end, num_points)

   