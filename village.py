# Assignment 1 main file
# Feel free to add additional modules/files as you see fit.

from House import House
from mcpi.minecraft import Minecraft
from mcpi import block
import random 

def get_village_loc(mc):
    """checks for right clicks while holding a sword, returns the coordinate of the right clicked block in vec3"""
    blockevents = mc.events.pollBlockHits()

    while blockevents == []:
        blockevents = mc.events.pollBlockHits()
    

    return blockevents[0].pos

if __name__ == "__main__":
    
    mc = Minecraft.create()
    # loc = get_village_loc(mc)
    
    mc.setBlocks(-200,0,-200,100,200,0)
    mc.setBlocks(-200,-3,-200,0,200,2)
    x = 0
    y = 0
    z = 0
    # house1_location = McPosition(x,y,z)
    # mc.player.setPos(x,y,z)
    # mc.player.getPos()
    # while mc.getBlock(x + 1,y,z + 1) is 0:
    #     y = y - 1
    # print(x,y,z)
    # mc.setBlock(x + 1,y + 1,z + 1, 1) 
    mc.setBlocks(x,y,z,x + 30, y + 30, z + 30, 0)
    house1 = House(x,y,z,2,16,20)
    house1.create_house(mc)
   
