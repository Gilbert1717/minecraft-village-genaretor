from mcpi.minecraft import Minecraft
from mcpi import block
import random 

class McPosition:
    def __init__ (self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

class Structure:
    def __init__ (self,x,y,z,width = random.randrange(8,16),length = random.randrange(10,20),height = 5,):
        self.height = height
        self.width = width
        self.length = length
        self.x = x - width//2
        self.y = y
        self.z = z - length//2
        self.frontleft = McPosition(self.x, self.y, self.z)
        self.frontright = McPosition(self.x + self.width, self.y, self.z)
        self.backleft = McPosition(self.x, self.y, self.z + self.length)
        self.backright = McPosition(self.x + self.width, self.y, self.z + self.length)

class Floor:
    def __init__ (self,structure,storey):
        self.structure = structure
        self.structure.y = structure.y + structure.height * storey
        self.frontleft = self.structure.frontleft
        self.frontright = self.structure.frontright
        self.backleft = self.structure.backleft
        self.backright = self.structure.backright
    

    def create(self,mc,material = 1,color = 3):
        start_x = self.frontleft.x
        start_y = self.frontleft.y
        start_z = self.frontleft.z
        end_x = self.backright.x
        end_y = self.backright.y
        end_z = self.backright.z
        mc.setBlocks(start_x, start_y, start_z, end_x, end_y, end_z, material ,color)


    def create_room(self,mc,width,length,material = 1,color = 1): 
        if width > 4 and length > 4:
            if width >= length:
                split = random.randint(int(width/2),width - 3) 
                mc.setBlocks(self.structure.x + split,self.structure.y + 1,self.structure.z,
                    self.structure.x + split,self.structure.y + self.structure.height - 1,self.structure.z + length, 
                    material, color)
                width = split
                stop = random.randint(0,3)
                if stop != 0:
                    self.create_room(mc,width,length)
            else:
                split = random.randint(int(length/2),length - 3)
                mc.setBlocks(self.structure.x, self.structure.y + 1, self.structure.z + split,
                self.structure.x + width, self.structure.y + self.structure.height - 1, self.structure.z + split, 
                material, color)
                length = split
                stop = random.randint(0,3)
                if stop != 0:          
                    self.create_room(mc,width,length)


        
class House:
    def __init__ (self,structure,stories = random.randint(0,2)):
        self.structure = structure
        self.stories = stories
        self.floors = []
        
    
    def create_floor(self,mc):
        material = random.randint(1,2)
        colour = random.randint(1,3)
        for storey in range(self.stories):
            floor = Floor(mc,self.structure,storey)
            floor.create(mc,material,colour)
            self.floors.append(floor)

    def create_rooms(self,mc):
        for floor in self.floors:
            floor.create_room(mc,self.structure.width,self.structure.length)
            

    def create_roof(self,mc):
        self.create_wall(mc,self.structure.frontleft,self.structure.backright)


            
    def create_wall(self,mc,start_point,end_point,material = 1,color = 3):
        start_x = start_point.x
        start_y = start_point.y
        start_z = start_point.z
        end_x = end_point.x
        end_y = end_point.y
        end_z = end_point.z
        mc.setBlocks(start_x, start_y, start_z, end_x, end_y, end_z, material ,color)
        
    def create_walls(self,mc):
        for floor in self.floors:
            endpoint1 = McPosition(floor.backleft.x, floor.backleft.y + self.structure.height, floor.backleft.z)
            endpoint2 = McPosition(floor.frontright.x, floor.frontright.y + self.structure.height, floor.frontright.z)
            self.create_wall(mc,floor.frontleft,endpoint1)
            self.create_wall(mc,endpoint1,floor.backright)
            self.create_wall(mc,floor.backright,endpoint2)
            self.create_wall(mc,endpoint2,floor.frontleft)
            
    
    def back_window(self,mc):
        window_x = self.x + 3
        window_y = self.y + 1
        window_z = self.z + self.length 
        window_height = 5
        window_width = window_x + 8
        mc.setBlocks(window_x, window_y, window_z, window_width,window_height,window_z,102)
    
    def left_window(self,mc):
        i = random.randint(1,3)
        window_x = self.x + self.width
        window_y = self.y + random.randint(1,3)
        window_z = self.z + 3
        window_height = window_y + 2
        window_width = window_z + 1
        for x in range(i):
            mc.setBlocks(window_x, window_y, window_z, window_x,window_height,window_width,102)
            window_z = window_z + int(self.length/i) 
            window_width = window_z + 1
            
    
    def right_window(self,mc):
        i = random.randint(1,3)
        window_x = self.x
        window_y = self.y + random.randint(1,3)
        window_z = self.z + 3
        window_height = window_y + 2
        window_width = window_z + 1
        for x in range(i):
            mc.setBlocks(window_x, window_y, window_z, window_x,window_height,window_width,102)
            window_z = window_z + int(self.length/i)
            window_width = window_z + 1

    def door(self,mc):
        create_position = self.x + random.randrange(int(self.width/2) - 1,self.width - 3)
        mc.setBlock(create_position, self.y + 1, self.z, 64, 0)
        mc.setBlock(create_position, self.y + 2, self.z, 64, 0)
        

    def front_window(self,mc):
        window_x = self.x + 3
        window_y = self.y + 3
        window_height = window_x + 2
        window_width = window_y + 2
        mc.setBlocks(window_x, window_y, self.z, window_width,window_height,self.z,102)

    def front(self,mc):
        self.door(mc)
        # self.front_window(mc)

    

    def create_house(self,mc):
        self.create_floor(mc)
        self.create_roof(mc)
        self.create_rooms(mc)
        self.create_walls(mc)
        self.front(mc)
        self.back_window(mc)
        self.left_window(mc)
        self.right_window(mc)


