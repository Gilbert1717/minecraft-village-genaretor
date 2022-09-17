from random import randint, randrange
import math

from mcpi import vec3
from mcpi import minecraft
from mcpi import block
from mcpi_query_performance import query_blocks

from models.Structure import Structure
from models.House import House

mc = minecraft.Minecraft.create()

### copy pasted from path_gen.py to circumvent circular dependency issues
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


mc = minecraft.Minecraft.create()

class Plot:
   
    def __init__(self, central_point, distance_from_path, direction) -> None:
        """takes voronoi points in a village as its central point."""
        self.central_point      = central_point
        self.distance_from_path = distance_from_path
        self.direction          = direction
        buffer_from_path        = 2

        self.plot_start = vec3.Vec3(self.central_point.x - int(self.distance_from_path/2) + buffer_from_path,
                                    self.central_point.y,
                                    self.central_point.z - int(self.distance_from_path/2) + buffer_from_path)
          
        self.plot_end   = vec3.Vec3(self.central_point.x + int(self.distance_from_path/2) - buffer_from_path,
                                    self.central_point.y,
                                    self.central_point.z + int(self.distance_from_path/2) - buffer_from_path)


        self.plot_length = self.plot_end.x - self.plot_start.x
        
        
        length_lower_bound = 12 if self.plot_length // 2 < 12 else self.plot_length // 2

        self.structure_length = randrange(length_lower_bound,   self.plot_length)
        self.structure_width  = randrange(9,                    self.structure_length)

        self.terrain_dict = dict()
        terrain_coords = []
        ground_blocks =[]

        for x in range(self.plot_start.x - 5, self.plot_end.x + 6):
            for z in range(self.plot_start.z - 5, self.plot_end.z + 6):
                terrain_coords.append((x,z))
        
        terrain_height = query_blocks(terrain_coords,'world.getHeight(%d,%d)',int)

        for query_result in terrain_height:
            x = query_result[0][0]
            z = query_result[0][1]
            y = query_result[1]
            self.terrain_dict[(x,z)] = y
            ground_blocks.append((x,y,z))
        
        ground_block_queries = query_blocks(ground_blocks,'world.getHeight(%d,%d)',int)

        for query_result in ground_block_queries:
            x = query_result[0][0]
            y = query_result[0][1]
            z = query_result[0][2]
            block_id = query_result[1]

    def get_structure(self):
            """contains complicated logic to determine direction and the "frontleft" of a structure inside a plot"""
            if self.direction == 'x-':
                structure_start = vec3.Vec3(randrange(self.plot_start.x, self.plot_end.x - self.structure_length),
                                            self.central_point.y,
                                            randrange(self.plot_start.z, self.plot_end.z - self.structure_width))
                structure = Structure(structure_start, self.structure_width, self.structure_length)

            elif self.direction =='x+':
                structure_start = vec3.Vec3(randrange(self.plot_end.x, self.plot_start.x + self.structure_length, -1),
                                            self.central_point.y,
                                            randrange(self.plot_end.z, self.plot_start.z + self.structure_width, -1))
                structure = Structure(structure_start, -self.structure_width, -self.structure_length)
                   
            elif self.direction =='z-':
                structure_start = vec3.Vec3(randrange(self.plot_end.x, self.plot_start.x + self.structure_width, -1),
                                            self.central_point.y,
                                            randrange(self.plot_start.z, self.plot_end.z - self.structure_length))
                structure = Structure(structure_start, -self.structure_width, self.structure_length)

            elif self.direction =='z+':
                structure_start = vec3.Vec3(randrange(self.plot_start.x, self.plot_end.x - self.structure_width),
                                            self.central_point.y,
                                            randrange(self.plot_end.z, self.plot_start.z + self.structure_length, -1))
                structure = Structure(structure_start, self.structure_width, -self.structure_length)
            
            self.structure = structure

            return structure
                

    def terraform_new_wip(self):
        terrain_coords = []
        for x in range(self.plot_start.x - 5, self.plot_end.x + 6):
            for z in range(self.plot_start.z - 5, self.plot_end.z + 6):
                terrain_coords.append((x,z))
        

        query_results = query_blocks(terrain_coords,'world.getHeight(%d,%d)',int)
        for result in query_results:
            print(result)

    def place_house(self, structure):
        house = House(structure)
        print(house.stories)
        house.create_house(mc)

    def generate_path_connection(self):
        if self.direction == 'x-':
            while True:
                pass
        elif self.direction =='x+':
            pass
        elif self.direction =='z-':
            pass
        elif self.direction =='z+':
            pass
    
    def get_prev_corner(self,x,z,):
        if self.is_corner(x,z):
            if x < self.plot_start.x:
                x += 1
            else:
                x -= 1

            if z < self.plot_start.z:
                z += 1
            else:
                z -= 1
        return x,z

    def is_corner(self,x,z):
        if x < self.plot_start.x or x > self.plot_end.x:
            if z < self.plot_start.z or z > self.plot_end.z:
                return True
        return False

    def get_corner_prev(self,x,z,dict):
        if x < self.plot_start.x:
            x += 1
        else:
            x -= 1

        if z < self.plot_start.z:
            z += 1
        else:
            z -= 1
        
        return dict[(x,z)]

    def terraform(self):
        y_and_noise = dict()
        completed = []

        mc.setBlocks(   self.plot_start.x,  self.plot_start.y + 1,  self.plot_start.z,
                        self.plot_end.x,    100,                    self.plot_end.z, block.AIR.id)
        noise = 0

        #iterates circularly around the plot. i indicates layer
        for i in range(1,4):
            print(i)
            x = self.plot_start.x - i
            for z in range(self.plot_start.z - (i-1), self.plot_end.z + i + 1): 
                #almost identical code on the next few for loops
                ###########################################################
                #switch between noise levels
                if i == 1:
                    if 1 == randint(1,10):
                        if noise == 0:
                            noise = 1
                        else:
                            noise = 0

                #checks if the previous layer is completed. also gets previous layer's y and noise level
                if self.is_corner(x,z):
                    if self.get_prev_corner(x,z) in completed:
                        completed.append((x,z))
                        print('completed',(x,z))
                        continue
                    if i == 1:
                        prev_y = self.central_point.y
                    else:
                        prev_y, prev_noise = self.get_corner_prev(x,z,y_and_noise)
                else:
                    if (x+1,z) in completed:
                        completed.append((x,z))
                        print('completed',(x,z))
                        continue
                    if i == 1:
                        prev_y = self.central_point.y
                    else:
                        prev_y, prev_noise = y_and_noise[(x + 1, z)]

                y = getBlockHeight(x,z)
    
                #checks if y is higher or lower than the y in the previous layer
                if y < prev_y : 
                    curr_y = prev_y -1 - noise
                    mc.setBlocks(   x, 50, z,
                                    x, curr_y , z,block.GRASS.id) 

                elif y > prev_y :
                    curr_y = prev_y + 1 + noise
                    mc.setBlocks(   x, curr_y, z,
                                    x, y, z,block.AIR.id)
                    mc.setBlocks(    x, 50, z,
                                    x, curr_y, z,block.GRASS.id)

                else:
                    curr_y = y
                    completed.append((x,z))
                
                y_and_noise[(x,z)] = (curr_y,noise)
                print('added',(x,z))
                ###########################################################

            z = self.plot_end.z + i
            for x in range(self.plot_start.x - (i-1), self.plot_end.x + i + 1): 
                ###########################################################
                if i == 1:
                    if 1 == randint(1,10):
                        if noise == 0:
                            noise = 1
                        else:
                            noise = 0

                if self.is_corner(x,z):
                    if self.get_prev_corner(x,z) in completed:
                        completed.append((x,z))
                        print('completed',(x,z))
                        continue
                    if i == 1:
                        prev_y = self.central_point.y
                    else:
                        prev_y, prev_noise = self.get_corner_prev(x,z,y_and_noise)
                else:
                    if (x,z-1) in completed:
                        completed.append((x ,z))
                        print('completed',(x,z))
                        continue
                    if i == 1:
                        prev_y = self.central_point.y
                    else:
                        prev_y, prev_noise = y_and_noise[(x , z-1)]

                y = getBlockHeight(x,z)

                if y < prev_y : 
                    curr_y = prev_y -1 - noise
                    mc.setBlocks(   x, 50, z,
                                    x, curr_y , z,block.GRASS.id) 

                elif y > prev_y :
                    curr_y = prev_y + 1+ noise
                    mc.setBlocks(   x, curr_y, z,
                                    x, y, z,block.AIR.id)
                    mc.setBlocks(    x, 50, z,
                                    x, curr_y, z,block.GRASS.id)
                else:
                    curr_y = y
                    completed.append((x,z))
                
                y_and_noise[(x,z)] = (curr_y,noise)
                print('added', (x,z))
                ###########################################################

            x = self.plot_end.x + i
            for z in range(self.plot_end.z + i,self.plot_start.z - i, -1):
                ###########################################################
                if i == 1:
                    if 1 == randint(1,10):
                        if noise == 0:
                            noise = 1
                        else:
                            noise = 0

                if self.is_corner(x,z):
                    if self.get_prev_corner(x,z) in completed:
                        completed.append((x,z))
                        print('completed',(x,z))
                        continue
                    if i == 1:
                        prev_y = self.central_point.y
                    else:
                        prev_y, prev_noise = self.get_corner_prev(x,z,y_and_noise)
                else:
                    if (x-1,z) in completed:
                        completed.append((x,z))
                        print('completed',(x,z))
                        continue
                    if i == 1:
                        prev_y = self.central_point.y
                    else:
                        prev_y, prev_noise = y_and_noise[(x -1, z)]

                y = getBlockHeight(x,z)

                if y < prev_y : 
                    mc.setBlocks(   x, 50, z,
                                    x, curr_y , z,block.GRASS.id) 

                elif y > prev_y :
                    curr_y = prev_y + 1+ noise
                    mc.setBlocks(   x, curr_y, z,
                                    x, y, z,block.AIR.id)
                    mc.setBlocks(    x, 50, z,
                                    x, curr_y, z,block.GRASS.id)
                else:
                    curr_y = y
                    completed.append((x,z))
                
                y_and_noise[(x,z)] = (curr_y,noise)
                print('added', (x,z))
                ###########################################################
            z = self.plot_start.z - i
            for x in range(self.plot_end.x + i, self.plot_start.x - (i + 1), -1):
                ###########################################################
                if i == 1:
                    if 1 == randint(1,10):
                        if noise == 0:
                            noise = 1
                        else:
                            noise = 0

                if self.is_corner(x,z):
                    if self.get_prev_corner(x,z) in completed:
                        completed.append((x,z))
                        print('completed',(x,z))
                        continue
                    if i == 1:
                        prev_y = self.central_point.y
                    else:
                        prev_y, prev_noise = self.get_corner_prev(x,z,y_and_noise)
                else:
                    if (x,z + 1) in completed:
                        completed.append((x ,z))
                        print('completed',(x,z))
                        continue
                    if i == 1:
                        prev_y = self.central_point.y
                    else:
                        prev_y, prev_noise = y_and_noise[(x, z+1)]

                y = getBlockHeight(x,z)

                if y < prev_y : 
                    curr_y = prev_y -1 - noise
                    mc.setBlocks(   x, 50, z,
                                    x, curr_y , z,block.GRASS.id) 

                elif y > prev_y :
                    curr_y = prev_y + 1 + noise
                    mc.setBlocks(   x, curr_y, z,
                                    x, y, z,block.AIR.id)
                    mc.setBlocks(    x, 50, z,
                                    x, curr_y, z,block.GRASS.id)
                else:
                    curr_y = y
                    completed.append((x,z))
                
                y_and_noise[(x,z)] = (curr_y,noise)
                print('added',(x,z))
                ###########################################################
    
    
if __name__ == '__main__':
    test_plot = Plot(mc.player.getTilePos(),20,'z+')
    test_plot.terraform_new_wip()
    test_plot.place_house(test_plot.get_structure())