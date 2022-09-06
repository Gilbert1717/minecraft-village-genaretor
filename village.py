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
    loc = get_village_loc(mc)
    
    mc.setBlocks(-200,0,-200,100,200,0)
    mc.setBlocks(-200,-3,-200,0,200,2)
    x = 0
    y = 0
    z = 0
    # mc.player.setPos(x,y,z)
    # mc.player.getPos()
    # while mc.getBlock(x + 1,y,z + 1) is 0:
    #     y = y - 1
    # print(x,y,z)
    # mc.setBlock(x + 1,y + 1,z + 1, 1)
    house1 = House(x,y,z,1,16,20)
    house1.frame(mc)
    house1.ground(mc)
    house1.roof(mc)
    house1.door(mc)
    house1.window(mc)
    house1.back_window(mc)
    house1.left_window(mc)
    house1.right_window(mc)
