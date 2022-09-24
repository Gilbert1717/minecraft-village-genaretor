
from mcpi import minecraft
from mcpi import vec3
from mcpi import block

from fast_query_and_interpolation.mcpi_query_performance import query_blocks

import random
import math

from Plot import Plot
from models import PathObjects

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
                path_coords.append(vec3.Vec3(x, 0, z)) # get the y coord later
        
                ############ this code block populates voronoi_distances with a voronoi point's distance to the closest path.
                ############ used to determine plot sizes
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
                    # creates a list of path blocks located in the village border, used for path connection algorithms later on
    

    
    plots = generate_plots(vil_center, voronoi_points, voronoi_distances)

    return path_coords,intersection_coords,bordering_paths, plots

def get_path_height(path_coords):
    """iteratively gets path block heights until the block at y-level is in the list of ground blocks"""
    path_coords_tuple = []
    path_height_set = set() # used set instead of list because query_blocks returns duplicate results for some reason
    height_dict = dict()
    block_dict = dict()
    ground =  [ block.GRASS.id, block.DIRT.id, block.WATER_STATIONARY.id, block.SAND.id, block.WATER_FLOWING.id,
                    block.STONE.id, block.CLAY.id, block.MYCELIUM.id, block.SANDSTONE.id, block.ICE.id]

    for coord in path_coords:
        path_coords_tuple.append((coord.x,coord.z))

    Done = False

    while not Done:
        Done = True
        redo = set()
        path_height_set = set()
            
        query_results = query_blocks(path_coords_tuple,'world.getHeight(%d,%d)',int)

        for query_result in query_results:
            x = query_result[0][0]
            z = query_result[0][1]
            y = query_result[1]
                
            height_dict[(x,z)] = y
            path_height_set.add((x,y,z))
        

        query_results = query_blocks(path_height_set,'world.getBlock(%d,%d,%d)',int)
        
        for query_result in query_results:
            x,y,z = query_result[0]
            block_id = query_result[1]

            if block_id == 0: #prevents an infinite loop when the block is a seagrass
                height_dict[(x,z)] = y
                block_dict[(x,z)] = block.WATER.id
                    
            elif block_id not in ground:
                Done = False
                redo.add((x,y,z))
                

            height_dict[(x,z)] = y
            block_dict[(x,z)] = block_id

            
        if Done:
            break
        else:
            for x,y,z in redo: #deletes the non-ground blocks
                mc.setBlock(x,y,z,block.AIR.id)

            #re-assign terrain cords for the next iteration
            path_coords_tuple = []
            for x,y,z in redo:
                path_coords_tuple.append((x,z))
    
    return height_dict


def getBlockHeight(block_x, block_z):
    """DOES NOT WORK IF SETWORLDSPAWN HEIGHT IS NOT SET TO 0"""
    y = mc.getHeight(block_x, block_z)
    groundblock_pos = vec3.Vec3(block_x, y, block_z)
    ground_block = mc.getBlock(groundblock_pos)
    
    while (ground_block != block.GRASS.id and ground_block != block.DIRT.id and
            ground_block !=block.WATER_STATIONARY.id and ground_block != block.WATER_FLOWING.id 
            and ground_block != block.SAND.id and ground_block != block.STONE.id):
        
        y = y - 1
        ground_block = mc.getBlock(block_x, y, block_z)

    return y

def alternateCheckSteepPath(height_dict, front_doors):
    """compares items in height dict with its surrounding blocks' height, if it's lower than -1, raise the surrounding block.
    if the surrounding block is a front door path, lower the current block instead. repeat until done"""
    front_doors_tuple = [(front_door.x, front_door.z) for front_door in front_doors]
    for front_door in front_doors:
        height_dict[(front_door.x, front_door.z)] = front_door.y # makes sure that the front door path height is level with the front door
    
    final_path_height_dict = height_dict.copy()
    looping_path_height_dict = height_dict.copy()
    #the algorithm adds and removes blocks to the looping dict depending on whether it could be a steep block.
    #algorithm ends when len(looping dict) is 0 or loop_counter = 99999

    front_doors_tuple = [(front_door.x, front_door.z) for front_door in front_doors]
    for front_door in front_doors:
        height_dict[(front_door.x, front_door.z)] = front_door.y
    raised_paths = set()

    done = False
    loop_counter = 0

    while not done:
        loop_counter += 1
        to_be_deleted = []  # not able to change a dict's size during iteration,
        to_be_added = []    # these 2 variables stores items temporarily until after the end of the for loop

        for curr_x, curr_z in looping_path_height_dict:
            curr_y = looping_path_height_dict[(curr_x),(curr_z)]
            surrounding_blocks = [  (curr_x + 1, curr_z + 1), 
                                    (curr_x    , curr_z + 1),
                                    (curr_x - 1, curr_z + 1),
                                    (curr_x + 1, curr_z),
                                    (curr_x - 1, curr_z),
                                    (curr_x + 1, curr_z - 1),
                                    (curr_x   , curr_z - 1),
                                    (curr_x - 1, curr_z - 1),]

            dict_change = False
            for surrounding_x,surrounding_z in surrounding_blocks:
                    
                if (surrounding_x, surrounding_z) in final_path_height_dict:
                    surrounding_block_y = final_path_height_dict[(surrounding_x,surrounding_z)]

                    if surrounding_block_y < curr_y -1 and (surrounding_x,surrounding_z) not in front_doors_tuple:
                        #raise the surrounding block by 1
                        final_path_height_dict[(surrounding_x,surrounding_z)] = surrounding_block_y + 1
                        to_be_added.append((surrounding_x,surrounding_z,surrounding_block_y + 1))
                        raised_paths.add((surrounding_x,surrounding_z))
                        
                        dict_change = True

                    elif surrounding_block_y < curr_y -1 and (surrounding_x,surrounding_z) in front_doors_tuple:
                        #raise the current block by 1
                        final_path_height_dict[(curr_x,curr_z)] = curr_y - 1
                        
                        to_be_added.append((curr_x,curr_z,curr_y - 1))
                        raised_paths.add((curr_x,curr_z))
                        
                        dict_change = True

            if not dict_change:
                to_be_deleted.append((curr_x,curr_z))


        for item in to_be_deleted:
            looping_path_height_dict.pop(item)

        for x,z,y in to_be_added:
            looping_path_height_dict[(x,z)] = y

        if len(looping_path_height_dict) == 0:
            done = True
        else:
            done = False
        
        if loop_counter == 99999:
            print('steep path function has given up')
            break
                        
    new_path_coords = []
    for x,z in final_path_height_dict:
        new_path_coords.append(vec3.Vec3(x, final_path_height_dict[(x,z)], z))
    
    return new_path_coords,raised_paths,final_path_height_dict

def remove_dead_ends(path_coords, intersections, bordering_paths, vil_start, vil_end): 
    ###### FUNCTION NOT USED ANYMORE!!!!! TOO MANY COMPLICATIONS WITH UNINTENDED PATH BLOCK DELETIONS
    ###### USING add_construction_blockades() INSTEAD
    #traverses the path away in all 4 direction from all intersection blocks,
    #if it doesnt encounter another intersection block, delete the traversed path
    for bordering_block in bordering_paths:

        ### checks if the bordering path has been connected by another plot
        curr_block = bordering_block
        surrounding_blocks = [  vec3.Vec3(curr_block.x + 1, 0, curr_block.z + 1), 
                                vec3.Vec3(curr_block.x    , 0, curr_block.z + 1),
                                vec3.Vec3(curr_block.x - 1, 0, curr_block.z + 1),
                                vec3.Vec3(curr_block.x + 1, 0, curr_block.z),
                                vec3.Vec3(curr_block.x - 1, 0, curr_block.z),
                                vec3.Vec3(curr_block.x + 1, 0, curr_block.z - 1),
                                vec3.Vec3(curr_block.x    , 0, curr_block.z - 1),
                                vec3.Vec3(curr_block.x - 1, 0, curr_block.z - 1),]
        in_intersections = False
        for surrounding_block in surrounding_blocks:
            if surrounding_block in intersections:
                in_intersections = True
        ###
        if in_intersections: # if yes, there is no need to remove the path
            continue
        else: # if no, traverse the path towards the village until you hit an intersection block 
            #checks for the traversal axis and direction
            if curr_block.x == vil_start.x:
                axis = 'x'
                dir = 1
            elif curr_block.x == vil_end.x:
                axis = 'x'
                dir = -1
            elif curr_block.z == vil_start.z:
                axis = 'z'
                dir = 1
            elif curr_block.z == vil_end.z:
                axis = 'z'
                dir = -1
            
            if axis == 'x':
                traversed = []

                while curr_block not in intersections:
                    next_blocks_in_intersections = False
                    next_blocks_not_in_path_coords = False
                    potential_next_blocks = [   vec3.Vec3(curr_block.x + dir, 0, curr_block.z + 1),
                                                vec3.Vec3(curr_block.x + dir, 0, curr_block.z    ),
                                                vec3.Vec3(curr_block.x + dir, 0, curr_block.z - 1),
                                                vec3.Vec3(curr_block.x,       0, curr_block.z + 1),
                                                vec3.Vec3(curr_block.x,       0, curr_block.z - 1),]


                    for block in potential_next_blocks:
                        if block in path_coords and block not in intersections:
                            curr_block = block
                            traversed.append(curr_block)
                        
                        if block in intersections:
                            next_blocks_in_intersections = True

                            for block2 in potential_next_blocks:
                                if block2 in traversed:
                                    traversed.remove(block2)
                        
                        if block not in path_coords:
                            next_blocks_not_in_path_coords = True

                    if next_blocks_in_intersections or next_blocks_not_in_path_coords:
                        for block in traversed:
                            if block in path_coords:
                                path_coords.remove(block)
                        break
            else:
                traversed = []

                while curr_block not in intersections:
                    next_blocks_in_intersections = False
                    next_blocks_not_in_path_coords = False
                    potential_next_blocks = [   vec3.Vec3(curr_block.x + 1, 0, curr_block.z + dir),
                                                vec3.Vec3(curr_block.x    , 0, curr_block.z + dir),
                                                vec3.Vec3(curr_block.x - 1, 0, curr_block.z + dir),
                                                vec3.Vec3(curr_block.x + 1, 0, curr_block.z      ),
                                                vec3.Vec3(curr_block.x - 1, 0, curr_block.z      )]

                    for block in potential_next_blocks:
                        if block in path_coords and block not in intersections:
                            curr_block = block
                            traversed.append(curr_block)
                        
                        if block in intersections:
                            next_blocks_in_intersections = True

                            for block2 in potential_next_blocks:
                                if block2 in traversed:
                                    traversed.remove(block2)
                        
                        if block not in path_coords:
                            next_blocks_not_in_path_coords = True

                    if next_blocks_in_intersections or next_blocks_not_in_path_coords:
                        for block in traversed:
                            if block in path_coords:
                                path_coords.remove(block)
                        break

def add_support_blocks(potentially_unsupported):
    """adds fence posts below unsupported structures"""
    ground =  [ block.GRASS.id, block.DIRT.id, block.SAND.id,
                    block.STONE.id, block.CLAY.id, block.MYCELIUM.id, block.SANDSTONE.id]
    height_dict = dict()
    height_tuple = []
    
    for a_block in potentially_unsupported:
        height_dict[(a_block.x, a_block.z)] = a_block.y - 1
        height_tuple.append((a_block.x, a_block.y - 1, a_block.z))
    
    done = False
    while not done:
        done = True
        redo = set()
        blocks_below = query_blocks(height_tuple,'world.getBlock(%d,%d,%d)',int)

        for query,result in blocks_below:
            x,y,z = query
            block_id = result
            if block_id not in ground:
                done = False
                redo.add((x,y-1,z))
                mc.setBlock(x,y,z,block.FENCE.id)
        

        height_tuple = [] # prepares height_tuple for the next loop
        for x,y,z in redo:
            height_tuple.append((x,y,z))

                


def add_construction_blockades(bordering_paths, intersections, height_dict, vil_start, vil_end):
    """adds construction blockades to the dead ends"""
    intersections_tuple = [(vec.x,vec.z) for vec in intersections]
    filtered_bordering_paths = []

    for dead_end in bordering_paths:
        ### checks if the dead end has been connected by another plot,
       
        curr_block = dead_end
        surrounding_blocks = [  (curr_block.x + 1, curr_block.z + 1), 
                                (curr_block.x    , curr_block.z + 1),
                                (curr_block.x - 1, curr_block.z + 1),
                                (curr_block.x + 1, curr_block.z),
                                (curr_block.x - 1, curr_block.z),
                                (curr_block.x + 1, curr_block.z - 1),
                                (curr_block.x    , curr_block.z - 1),
                                (curr_block.x - 1, curr_block.z - 1),]
        satisfies_condition = True
        for surrounding_block in surrounding_blocks:
            
            if surrounding_block in intersections_tuple :
                satisfies_condition = False
        
        if satisfies_condition:
            filtered_bordering_paths.append((dead_end.x,dead_end.z))
        
    for x,z in filtered_bordering_paths:
        y = height_dict[(x,z)]
        #checks for the dead end direction
        if x == vil_start.x:
            axis = 'x'
                
        elif x == vil_end.x:
            axis = 'x'
                
        elif z == vil_start.z:
            axis = 'z'
                
        elif z == vil_end.z:
            axis = 'z'

        PathObjects.Path_Objects.construction_blockade(mc,x,y,z,axis)

def add_lamp_posts(intersections, height_dict):
    intersections_tuple = [(vec.x,vec.z) for vec in intersections]
    used_intersections = []

    for intersection in intersections:
        
        curr_block = intersection
        surrounding_blocks = [  (curr_block.x + 1, curr_block.z + 1), 
                                (curr_block.x    , curr_block.z + 1),
                                (curr_block.x - 1, curr_block.z + 1),
                                (curr_block.x + 1, curr_block.z),
                                (curr_block.x - 1, curr_block.z),
                                (curr_block.x + 1, curr_block.z - 1),
                                (curr_block.x    , curr_block.z - 1),
                                (curr_block.x - 1, curr_block.z - 1),]

        viable = True

        for surrounding_block in surrounding_blocks:
            if surrounding_block in intersections_tuple or surrounding_block in used_intersections:
                viable = False

        if viable:
            y = height_dict[(curr_block.x, curr_block.z)]
            PathObjects.Path_Objects.lampPost(mc, curr_block.x, y, curr_block.z)

        
        

if __name__ == '__main__':
    vil_length = 85
    num_points = 5

    vil_start = mc.player.getTilePos()
    vil_end = vec3.Vec3(vil_start.x + vil_length, 
                        vil_start.y,
                        vil_start.z + vil_length)
    
    generate_path_and_plots(vil_start, vil_end, num_points)

   