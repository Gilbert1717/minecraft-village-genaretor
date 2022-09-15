from random import randint, randrange
import math

from mcpi import vec3
from mcpi import minecraft
from mcpi import block

from models.Structure import Structure
from models.House import House
import path_gen


mc = minecraft.Minecraft.create()

class Plot:
    """takes voronoi points in a village as its central point."""
    def __init__(self, central_point, distance_from_path, direction) -> None:
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

        mc.setBlocks(   self.plot_start.x,  self.plot_start.y - 1,  self.plot_start.z, 
                        self.plot_end.x,    self.plot_end.y,    self.plot_end.z, block.GRASS.id)

        self.plot_length = self.plot_end.x - self.plot_start.x
        
        
        length_lower_bound = 10 if self.plot_length // 2 < 10 else self.plot_length // 2

        self.structure_length = randrange(length_lower_bound,   self.plot_length)
        self.structure_width  = randrange(9,                    self.structure_length)


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
                
    def place_house(self, structure):
        house = House(structure)
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

                y = path_gen.getBlockHeight(x,z)

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

                y = path_gen.getBlockHeight(x,z)

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

                y = path_gen.getBlockHeight(x,z)

                if y < prev_y : # dont do this, instead check if its higher or lower when compared to the previous layer within a certain margin
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

                y = path_gen.getBlockHeight(x,z)

                if y < prev_y : # dont do this, instead check if its higher or lower when compared to the previous layer within a certain margin
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
    test_plot.terraform()