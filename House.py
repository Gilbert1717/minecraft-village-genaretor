from mcpi.minecraft import Minecraft
from mcpi import block
import random 

class McPosition:
    def __init__ (self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

class Floor:
    def __init__ (self,mc,house,storey):
        x = house.x
        y = house.y
        z = house.z
        height = house.height
        width = house.width
        length = house.length
        self.floor_frontleft = McPosition(x, y + height * storey , z)
        self.floor_frontright = McPosition(x + width, y + height * storey, z)
        self.floor_backleft = McPosition(x, y + height * storey, z + length)
        self.floor_backright = McPosition(x + width, y + height * storey, z + length)

    def create(self,mc,material = 1,color = 3):
        start_x = self.floor_frontleft.x
        start_y = self.floor_frontleft.y
        start_z = self.floor_frontleft.z
        end_x = self.floor_backright.x
        end_y = self.floor_backright.y
        end_z = self.floor_backright.z
        mc.setBlocks(start_x, start_y, start_z, end_x, end_y, end_z, material ,color)

    def measure(self,position1,position2):
        x = abs(position1.x - position2.x)
        z = abs(position1.z - position2.z)
        if x != 0:
            return x
        else:
            return z

    # to do: create rooms using recursion
    def create_rooms(self,mc,floor):
        width = self.measure(self.floor_frontleft,self.floor_frontright)
        length = self.measure(self.floor_frontleft,self.floor_backleft)
        if width < 3 or length <3:
            return floor

        
class House:
    def __init__ (self,x,y,z,stories = random.randint(0,2),width = random.randrange(8,16),length = random.randrange(10,20),height = 4):
        self.stories = stories
        self.width = width
        self.length = length
        self.height = height
        x = x - width//2
        z = z - length//2
        self.x = x 
        self.y = y
        self.z = z
        self.roof_frontleft = McPosition(x, y + self.height * self.stories, z)
        self.roof_frontright = McPosition(x + width, y + self.height * self.stories, z)
        self.roof_backleft = McPosition(x, y + self.height * self.stories, z + length)
        self.roof_backright = McPosition(x + width, y + self.height * self.stories, z + length)
        self.floors = []
        
    
    def create_floor(self,mc):
        material = random.randint(1,2)
        colour = random.randint(1,3)
        for storey in range(self.stories):
            floor = Floor(mc,self,storey)
            floor.create(mc,material,colour)
            self.floors.append(floor)
            

    def create_roof(self,mc):
        self.create_wall(mc,self.roof_frontleft,self.roof_backright)


            
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
            endpoint1 = McPosition(floor.floor_backleft.x,floor.floor_backleft.y + self.height,floor.floor_backleft.z)
            endpoint2 = McPosition(floor.floor_frontright.x,floor.floor_frontright.y + self.height,floor.floor_frontright.z)
            self.create_wall(mc,floor.floor_frontleft,endpoint1)
            self.create_wall(mc,endpoint1,floor.floor_backright)
            self.create_wall(mc,floor.floor_backright,endpoint2)
            self.create_wall(mc,endpoint2,floor.floor_frontleft)
            
    
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
        door_height = 3
        door_width = 2
        mc.setBlocks(create_position, self.y + 1, self.z, create_position + door_width, self.y + 1 + door_height,self.z,0)

    def front_window(self,mc):
        window_x = self.x + 3
        window_y = self.y + 3
        window_height = window_x + 2
        window_width = window_y + 2
        mc.setBlocks(window_x, window_y, self.z, window_width,window_height,self.z,102)

    def front(self,mc):
        self.door(mc)
        self.front_window(mc)

    

    def create_house(self,mc):
        self.create_floor(mc)
        self.create_roof(mc)
        self.create_walls(mc)
        self.front(mc)
        self.back_window(mc)
        self.left_window(mc)
        self.right_window(mc)


