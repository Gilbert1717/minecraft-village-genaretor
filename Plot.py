from random import randrange
import math

from mcpi import vec3
from mcpi import minecraft
from mcpi import block

from models.Structure import Structure
from models.House import House


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

        mc.setBlocks(   self.plot_start.x,  self.plot_start.y,  self.plot_start.z, 
                        self.plot_end.x,    self.plot_end.y,    self.plot_end.z, block.DIAMOND_ORE)

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

    def terraform(self):
        mc.setBlocks(   self.plot_start.x,  self.plot_start.y + 1,  self.plot_start.z,
                        self.plot_end.x,    100,                    self.plot_end.z, block.AIR.id)
        for i in range(1,4):
            x = self.plot_start.x - i
            for z in range(self.plot_start.z - (i-1), self.plot_end.z + i + 1): 
                y = mc.getHeight(x,z)
                mc.setBlock(x,y,z, block.COAL_ORE.id)

            z = self.plot_end.z + i
            for x in range(self.plot_start.x - (i-1), self.plot_end.x + i + 1): 
                y = mc.getHeight(x,z)
                mc.setBlock(x,y,z, block.COAL_ORE.id)

            x = self.plot_end.x + i
            
            for z in range(self.plot_end.z + i,self.plot_start.z - i, -1): 
                y = mc.getHeight(x,z)
                mc.setBlock(x,y,z, block.COAL_ORE.id)

            z = self.plot_start.z - i
            for x in range(self.plot_end.x + i, self.plot_start.x - (i + 1), -1): 
                y = mc.getHeight(x,z)
                mc.setBlock(x,y,z, block.COAL_ORE.id)