from mcpi.minecraft import Minecraft
from mcpi import block
import random 
class House:
    def __init__ (self,x,y,z,stories = random.randint(1,2),width = random.randrange(8,16),length = random.randrange(10,20)):
        self.x = x
        self.y = y
        self.z = z
        self.stories = stories
        self.width = width
        self.length = length
        
    def random_exterior(self,block):
        
        exteriorBlocks = [block.STONE_BRICK.id,
                          block.BRICK_BLOCK.id,
                          block.NETHER_BRICK.id,
                          block.WOOD_PLANKS.id,
                          block.COBBLESTONE.id,
                          block.MOSS_STONE.id,
                          block.SANDSTONE.id
                          ]
        
        number = 0
        number = random.randrange(0, len(exteriorBlocks))
        randomBlock = block.DIRT.id
        
        randomBlock = exteriorBlocks[number]
        return randomBlock
    
    def frame(self,mc):
        mc.setBlocks(self.x,self.y,self.z,self.x + self.width,self.y + 6,self.z + self.length, self.random_exterior(block))
        mc.setBlocks(self.x + 1,self.y + 1,self.z + 1,self.x + self.width - 1,self.y + 5,self.z + self.length - 1,0)

    # def wall(self,mc):

    def door(self,mc):
        x = random.randrange(int(self.width/2) - 1,self.width - 3)
        door_height = 3
        door_width = 2
        mc.setBlocks(self.x + x, self.y + 1, self.z, self.x + x + door_width,self.y + door_height,self.z,0)

    def window(self,mc):
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
            print(window_z)
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
            print(window_z)
            mc.setBlocks(window_x, window_y, window_z, window_x,window_height,window_width,102)
            window_z = window_z + int(self.length/i)
            window_width = window_z + 1
            
    def front(self,mc):
        self.door()
        self.window()

    def ground(self,mc):
        mc.setBlocks(self.x,self.y,self.z,self.x + self.width,self.y,self.z + self.length,5)

    def roof(self,mc):
        mc.setBlocks(self.x,self.y + 6 * self.stories,self.z,self.x + self.width,self.y + 6 * self.stories,self.z + self.length,2)

