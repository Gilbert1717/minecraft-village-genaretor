from turtle import width
from mcpi.minecraft import Minecraft
from mcpi import block
import random 
def create_wall(mc,McPosition1,McPosition2,material = 1,color = 3):
    start_x = McPosition1.x
    start_y = McPosition1.y
    start_z = McPosition1.z
    end_x = McPosition2.x
    end_y = McPosition2.y
    end_z = McPosition2.z
    mc.setBlocks(start_x, start_y, start_z, end_x, end_y, end_z, material ,color)

def create_door(mc,McPosition1,McPosition2):
    if McPosition1.x == McPosition2.x:
        length = abs(McPosition2.z - McPosition1.z)
        # print(McPosition1.x,McPosition2.x,McPosition2.z,McPosition1.z)
        if McPosition2.z > McPosition1.z:
            create_position = McPosition1.z + random.randint(2,length - 2)
            # while mc.getBlock(create_position + 1, McPosition1.y, McPosition1.z) != 0 or mc.getBlock(create_position - 1, McPosition1.y, McPosition1.z) != 0:
            #     create_position = McPosition1.z + random.randint(2,length - 2)
        else:
            create_position = McPosition1.z - random.randint(2,length - 2)
            # while mc.getBlock(create_position + 1, McPosition1.y, McPosition1.z) != 0 or mc.getBlock(create_position - 1, McPosition1.y, McPosition1.z) != 0:
            #     create_position = McPosition1.z - random.randint(2,length - 2)
        mc.setBlock(create_position , McPosition1.y, McPosition1.z, 0)
        mc.setBlock(create_position , McPosition1.y + 1, McPosition1.z, 0)

    elif McPosition1.z == McPosition2.z:
        width = abs(McPosition2.x - McPosition1.x)
        # print(width)
        if McPosition2.x > McPosition1.x:
            create_position = McPosition1.x + random.randint(2,width - 2)
            # while mc.getBlock(create_position, McPosition1.y, McPosition1.z + 1) == 0 or mc.getBlock(create_position - 1, McPosition1.y, McPosition1.z) == 0:
            #     create_position = McPosition1.x + random.randint(2,width - 2)
        else:
            create_position = McPosition1.x - random.randint(2,width - 2)
            # while mc.getBlock(create_position, McPosition1.y, McPosition1.z + 1) == 0 or mc.getBlock(create_position - 1, McPosition1.y, McPosition1.z) == 0:
            #      create_position = McPosition1.x - random.randint(2,width - 2)
        mc.setBlock(create_position , McPosition1.y + 1, McPosition1.z, 64, 0)
        mc.setBlock(create_position , McPosition1.y + 2, McPosition1.z, 64, 0)

class McPosition:
    def __init__ (self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    
    def move_x(self,x):
        self.x = self.x + x
        return McPosition(self.x,self.y,self.z)

    def move_y(self,y):
        self.y = self.y + y
        return McPosition(self.x,self.y,self.z)

    def move_z(self,z):
         self.z = self.z + z
         return McPosition(self.x,self.y,self.z)

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
        structure.y += structure.height * storey
        self.structure = structure
        self.frontleft = McPosition(structure.frontleft.x,
                                    structure.y,
                                    structure.frontleft.z)
        self.frontright = McPosition(structure.frontright.x,
                                    structure.y,
                                    structure.frontright.z)
        self.backleft = McPosition(structure.backleft.x,
                                    structure.y,
                                    structure.backleft.z)
        self.backright = McPosition(structure.backright.x,
                                    structure.y,
                                    structure.backright.z)
    



    def create_room(self,mc,width,length,material = 1,color = 1): 
        if width > 4 and length > 4:
            if width >= length:
                split = random.randint(int(width/2),width - 3) 
                mc.setBlocks(self.structure.x + split,self.structure.y + 1,self.structure.z,
                    self.structure.x + split,self.structure.y + self.structure.height - 1,self.structure.z + length, 
                    material, color)
                McPosition1 = McPosition(self.structure.x + split, self.structure.y + 1, self.structure.z)
                McPosition2 = McPosition(self.structure.x + split,self.structure.y + 1,self.structure.z + length)
                create_door(mc,McPosition1,McPosition2)
                width = split
                stop = random.randint(0,3)
                if stop != 0:
                    self.create_room(mc,width,length)
            else:
                split = random.randint(int(length/2),length - 3)
                mc.setBlocks(self.structure.x, self.structure.y + 1, self.structure.z + split,
                self.structure.x + width, self.structure.y + self.structure.height - 1, self.structure.z + split, 
                material, color)
                McPosition1 = McPosition(self.structure.x, self.structure.y + 1, self.structure.z + split)
                McPosition2 = McPosition(self.structure.x + width,self.structure.y + 1,self.structure.z + split)
                create_door(mc,McPosition1,McPosition2)
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
        print(1)
        material = random.randint(1,2)
        colour = random.randint(1,3)
        for storey in range(self.stories):
            floor = Floor(self.structure,storey)
            create_wall(mc,floor.frontleft,floor.backright,material,colour)
            self.floors.append(floor)

    def create_rooms(self,mc):
        for floor in self.floors:
            floor.create_room(mc,self.structure.width,self.structure.length)
            

    def create_roof(self,mc):
        start_point = McPosition(self.structure.frontleft.x,
                                self.structure.frontleft.y + self.structure.height * self.stories, 
                                self.structure.frontleft.z)
        end_point = McPosition(self.structure.backright.x,
                                self.structure.backright.y + self.structure.height * self.stories, 
                                self.structure.backright.z)
        create_wall(mc,start_point,end_point)

            
   
        
    def create_walls(self,mc):
        for floor in self.floors:
            endpoint1 = McPosition(floor.backleft.x, floor.backleft.y + self.structure.height, floor.backleft.z)
            endpoint2 = McPosition(floor.frontright.x, floor.frontright.y + self.structure.height, floor.frontright.z)
            create_wall(mc,floor.frontleft,endpoint1)
            create_wall(mc,endpoint1,floor.backright)
            create_wall(mc,floor.backright,endpoint2)
            create_wall(mc,endpoint2,floor.frontleft)
            
    
    def back_window(self,mc):
        window_x = self.structure.x + 3
        window_y = self.structure.y + 1
        window_z = self.structure.z + self.structure.length 
        window_height = 5
        window_width = window_x + 8
        mc.setBlocks(window_x, window_y, window_z, window_width,window_height,window_z,102)
    
    def left_window(self,mc):
        i = random.randint(1,3)
        window_x = self.structure.x + self.structure.width
        window_y = self.structure.y + random.randint(1,3)
        window_z = self.structure.z + 3
        window_height = window_y + 2
        window_width = window_z + 1
        for x in range(i):
            mc.setBlocks(window_x, window_y, window_z, window_x,window_height,window_width,102)
            window_z = window_z + int(self.structure.length/i) 
            window_width = window_z + 1
            
    
    def right_window(self,mc):
        i = random.randint(1,3)
        window_x = self.structure.x
        window_y = self.structure.y + random.randint(1,3)
        window_z = self.structure.z + 3
        window_height = window_y + 2
        window_width = window_z + 1
        for x in range(i):
            mc.setBlocks(window_x, window_y, window_z, window_x,window_height,window_width,102)
            window_z = window_z + int(self.structure.length/i)
            window_width = window_z + 1

    
        

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
        print(1)
        self.create_floor(mc)
        # self.create_roof(mc)
        # self.create_rooms(mc)
        # self.create_walls(mc)
        # self.front(mc)
        # self.back_window(mc)
        # self.left_window(mc)
        # self.right_window(mc)


