from mcpi.minecraft import Minecraft
from mcpi import block
from models.Floor import *
from mcpi import vec3
from RandomiseMaterial import RandomiseMaterial
import random 

rm = RandomiseMaterial()

         


class House:
    def __init__ (self,structure,stories = random.randint(0,2)):
        self.structure = structure
        self.stories = stories
        self.height = structure.height * stories
        self.floors = []
        
    
    def create_floor(self, mc: Minecraft):
        material = random.randint(1,2)
        colour = random.randint(1,3)
        for storey in range(self.stories):
            structure = self.structure
            floor = Floor(structure, storey)
            print(floor.frontleft.y)
            create_blocks(mc, floor.frontleft, floor.backright, material, colour)
            self.floors.append(floor)

    def create_rooms(self,mc):
        for floor in self.floors:
            floor.create_room(mc,floor)
            

    def create_roof(self,mc):
        start_point = vec3.Vec3(self.structure.frontleft.x,
                                self.structure.frontleft.y + self.structure.height * self.stories, 
                                self.structure.frontleft.z)
        end_point = vec3.Vec3(self.structure.backright.x,
                                self.structure.backright.y + self.structure.height * self.stories, 
                                self.structure.backright.z)
        print(end_point.y)
        create_blocks(mc, start_point, end_point)

            
   
        
    def create_walls(self,mc):
        for floor in self.floors:
            endpoint1 = vec3.Vec3(floor.backleft.x, floor.backleft.y + self.structure.height, floor.backleft.z)
            endpoint2 = vec3.Vec3(floor.frontright.x, floor.frontright.y + self.structure.height, floor.frontright.z)
            create_blocks(mc, floor.frontleft, endpoint1)
            create_blocks(mc, endpoint1, floor.backright)
            create_blocks(mc, floor.backright, endpoint2)
            create_blocks(mc, endpoint2, floor.frontleft)
            
    
    def back_window(self,mc):
        x_offset = 3
        window_height = 3
        window_width = 6

        window_x = self.structure.position.x + x_offset
        window_y = self.structure.position.y + 1
        window_z = self.structure.position.z + self.structure.length 
        
        mc.setBlocks(window_x, window_y, window_z, window_x + window_width, window_y + window_height,window_z,102)
    
    def side_window(self,mc,vector):
        
        i = random.randint(1,3)
        window_height = 1
        window_width = random.randint(3,self.structure.length//(i + 1) - 1)
        

        window_x = vector.x 
        window_y = vector.y + 2
        window_z = vector.z - window_width
         
        
        for x in range(i):
            z_offset =  self.structure.length//(i + 1) + random.randint(1,3)
            window_z = window_z + z_offset
            mc.setBlocks(window_x, window_y, window_z + 1, window_x, window_y + window_height ,window_z + window_width - 1,102)
            x += 1
            
    
        

    def front_window(self,mc):
        window_x = self.structure.x + 3
        window_y = self.structure.y + 3
        window_height = window_x + 2
        window_width = window_y + 2
        mc.setBlocks(window_x, window_y, self.structure.z, window_width,window_height,self.structure.z,102)

    def front(self,mc):
        create_door(mc,self.structure.frontleft,self.structure.frontright)
        # self.front_window(mc)

    

    def create_house(self,mc):
        self.create_floor(mc)
        self.create_roof(mc)
        self.create_rooms(mc)
        self.create_walls(mc)
        self.front(mc)
        self.back_window(mc)
        self.side_window(mc,self.structure.frontleft)
        self.side_window(mc,self.structure.frontright)
        


