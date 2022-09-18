# Assignment 1 main file
# Feel free to add additional modules/files as you see fit.


from mcpi.minecraft import Minecraft
from mcpi import block
from mcpi import vec3
import random
from RandomiseMaterial import RandomiseMaterial


from models.House import House
from models.Structure import Structure


import path_gen


def get_village_coords(mc):
    """checks for right clicks while holding a sword, returns the coordinate of the right clicked block in vec3"""
    blockevents = mc.events.pollBlockHits()

    mc.postToChat('right click on a block while holdling a sword to set village location')
    while blockevents == []:
        blockevents = mc.events.pollBlockHits()
    
    mc.postToChat('location set to ' + str(blockevents[0].pos))
    return blockevents[0].pos


if __name__ == "__main__":
    mc = Minecraft.create()

    # vil_length = 100

    # vil_start = get_village_coords(mc)
    # vil_end = vec3.Vec3(vil_start.x + vil_length, 
    #                     vil_start.y,
    #                     vil_start.z + vil_length)

    # path_gen.generate_path(vil_start,vil_end, 8)

    # print("made it here!")

    # mc.setBlocks(-200,0,-200,100,200,0)
    # mc.setBlocks(-200,-3,-200,0,200,2)
    # house1_location = McPosition(x,y,z)
    # mc.player.setPos(x,y,z)

    # while mc.getBlock(x + 1,y,z + 1) is 0:
    #     y = y - 1
    # print(x,y,z)
    # mc.setBlock(x + 1,y + 1,z + 1, 1) 
    x = 0
    y = 0
    z = 0
    position = mc.player.getPos()
    #position = vec3.Vec3(0,0,0)
    mc.setBlocks(x,y - 1,z,x + 30, y + 20, z + 30, 0)
    mc.setBlocks(x + 10,y -1,z + 10,x - 30, y + 20, z - 30, 0)
    structure1 = Structure(position,16,18)
    # print(structure1.frontleft.x,structure1.frontleft.z,structure1.frontright.x,structure1.frontright.z)
    # house1 = House(structure1,1)
    # house1.create_house(mc)
    ran = RandomiseMaterial()
    ran.rooftop(mc,position.x,position.y,position.z)
    
    
    
    
    
    
   
   
