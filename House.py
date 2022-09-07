from mcpi.minecraft import Minecraft
from mcpi import block
import random 

class McPosition:
    def __init__ (self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

class Roof:
    def __init__ (self,mc,house,storey):
        x = house.x
        y = house.y
        z = house.z
        height = house.height
        width = house.width
        length = house.length
        self.roof_frontleft = McPosition(x, y + height * storey, z)
        self.roof_frontright = McPosition(x + width, y + height * storey, z)
        self.roof_backleft = McPosition(x, y + height * storey, z + length)
        self.roof_backright = McPosition(x + width, y + height * storey, z + length)

    def create(self,mc,material = 1,color = 3):
        start_x = self.roof_frontleft.x
        start_y = self.roof_frontleft.y
        start_z = self.roof_frontleft.z
        end_x = self.roof_backright.x
        end_y = self.roof_backright.y
        end_z = self.roof_backright.z
        mc.setBlocks(start_x, start_y, start_z, end_x, end_y, end_z, material ,color)

        
class House:
    def __init__ (self,x,y,z,stories = random.randint(1,2),width = random.randrange(8,16),length = random.randrange(10,20),height = 6):
        self.stories = stories
        self.width = width
        self.length = length
        self.height = height
        self.x = x
        self.y = y
        self.z = z
        self.ground_frontleft = McPosition(x, y, z)
        self.ground_frontright = McPosition(x + width, y, z)
        self.ground_backleft = McPosition(x, y, z + length)
        self.ground_backright = McPosition(x + width, y, z + length)
        self.roofs = []
        
    
    def create_roof(self,mc):
        material = random.randint(1,2)
        colour = random.randint(1,3)
        for storey in range(self.stories):
            roof = Roof(mc,self,storey + 1)
            roof.create(mc,material,colour)
            self.roofs.append(roof)
            

    def create_ground(self,mc):
        self.create_wall(mc,self.ground_frontleft,self.ground_backright)
            
    def create_wall(self,mc,start_point,end_point,material = 1,color = 3):
        start_x = start_point.x
        start_y = start_point.y
        start_z = start_point.z
        end_x = end_point.x
        end_y = end_point.y
        end_z = end_point.z
        mc.setBlocks(start_x, start_y, start_z, end_x, end_y, end_z, material ,color)
        
    def create_walls(self,mc):
        for roof in self.roofs:
            endpoint1 = McPosition(roof.roof_backleft.x,roof.roof_backleft.y - self.height,roof.roof_backleft.z)
            endpoint2 = McPosition(roof.roof_frontright.x,roof.roof_frontright.y - self.height,roof.roof_frontright.z)
            self.create_wall(mc,roof.roof_frontleft,endpoint1)
            self.create_wall(mc,endpoint1,roof.roof_backright)
            self.create_wall(mc,roof.roof_backright,endpoint2)
            self.create_wall(mc,endpoint2,roof.roof_frontleft)
            

    def door(self,mc):
        create_position = self.x + random.randrange(int(self.width/2) - 1,self.width - 3)
        door_height = 3
        door_width = 2
        mc.setBlocks(create_position, self.y + 1, self.z, create_position + door_width, self.y + 1 + door_height,self.z,0)

    def front_window(self,mc):
        window_x = self.x + 3
        window_y = self.y + 3
        window_height = window_x + 2
        window_width = window_y + 2
        mc.setBlocks(window_x, window_y, self.z, window_width,window_height,self.z,102)
    
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
            
    def front(self,mc):
        self.door(mc)
        self.front_window(mc)

    

    def create_house(self,mc):
        self.create_ground(mc)
        self.create_roof(mc)
        self.create_walls(mc)
        self.front(mc)
        self.back_window(mc)
        self.left_window(mc)
        self.right_window(mc)


