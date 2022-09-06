# Assignment 1 main file
# Feel free to add additional modules/files as you see fit.

from House import House
from mcpi.minecraft import Minecraft
from mcpi import block
from mcpi import vec3
import random 

def get_village_coords(mc):
    """checks for right clicks while holding a sword, returns the coordinate of the right clicked block in vec3"""
    blockevents = mc.events.pollBlockHits()

    mc.postToChat('right click on a block while holdling a sword to set village location')
    while blockevents == []:
        blockevents = mc.events.pollBlockHits()
    
    mc.postToChat('location set to ' + str(blockevents[0].pos))
    return blockevents[0].pos

def generate_house_coords(start, end, amount):
    """returns random coordinates within the values of start and end parameters in a list x,z tuples"""
    #TODO add restrictions to limit how close each coordinates can be
    coords = []

    for i in range(amount):
        x = random.randint(start.x, end.x)
        z = random.randint(start.z, end.z)
        coords.append((x, z))

    print(coords)
    return coords

if __name__ == "__main__":
    mc = Minecraft.create()

    vil_length = 200
    

    vil_start = get_village_coords(mc)
    vil_end = vec3.Vec3(vil_start.x + vil_length             , vil_start.y,               vil_start.z + vil_length)

    house_coords = generate_house_coords(vil_start,vil_end, 5)

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
