from mcpi.minecraft import Minecraft
from mcpi import block
import random 

class McPosition:
    def __init__ (self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    

        
class House:
    def __init__ (self,x,y,z,stories = random.randint(1,2),width = random.randrange(8,16),length = random.randrange(10,20),hight = 6):
        self.stories = stories
        self.width = width
        self.length = length
        self.hight = hight
        self.x = x
        self.y = y
        self.z = z
        self.ground_frontleft = McPosition(x, y, z)
        self.ground_frontright = McPosition(x + width, y, z)
        self.ground_backleft = McPosition(x, y, z + length)
        self.ground_backright = McPosition(x + width, y, z + length)
        self.roof_frontleft = McPosition(x, y + hight, z)
        self.roof_frontright = McPosition(x + width, y + hight, z)
        self.roof_backleft = McPosition(x, y + hight, z + length)
        self.roof_backright = McPosition(x + width, y + hight, z + length)

    # def frame(self,mc):
    #     # frame_materials = []
    #     # assign start point
    #     Start_width_point = self.StartPoint.width
    #     Start_hight_point = self.StartPoint.hight
    #     Start_length_point = self.StartPoint.length

    #     # calculate size of the frame
    #     frame_width = Start_width_point + self.width
    #     frame_hight = Start_hight_point + self.hight
    #     frame_length = Start_length_point + self.length

    #     # create frame
    #     colour = random.randint(1,10)
    #     # material = frame_materials[random.randint(1,10)]
    #     mc.setBlocks(Start_width_point, Start_hight_point, Start_length_point, frame_width, frame_hight, frame_length,1,colour)
    #     mc.setBlocks(Start_width_point + 1, Start_hight_point + 1, Start_length_point + 1, frame_width - 2, frame_hight - 2, frame_length - 2,0)
    def create_roof(self,mc):
        for i in range(self.stories):
            self.roof_frontleft.y += self.hight * i 
            self.roof_backright.y += self.hight * i 
            print(self.roof_frontleft.y,
            self.roof_backright.y)
            self.create_wall(mc,self.roof_frontleft,self.roof_backright)

    def create_ground(self,mc):
        self.create_wall(mc,self.ground_frontleft,self.ground_backright)
            

    def create_walls(self,mc):
        for i in range(self.stories):
            self.roof_frontleft.y += self.hight * i 
            self.roof_backright.y += self.hight * i 
            print(self.roof_frontleft.y,self.roof_backright.y)
            self.create_wall(mc,self.roof_frontleft,self.ground_backleft)
            self.create_wall(mc,self.ground_backleft,self.roof_backright)
            self.create_wall(mc,self.roof_backright,self.ground_frontright)
            self.create_wall(mc,self.ground_frontright,self.roof_frontleft)

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


