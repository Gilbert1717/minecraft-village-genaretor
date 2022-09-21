# Assignment 1 main file
# Feel free to add additional modules/files as you see fit.


from mcpi.minecraft import Minecraft

from mcpi import block
from mcpi import vec3
from RandomiseMaterial import RandomiseMaterial

import random

from models.House import House
from models.Structure import Structure, Vector


import path_gen


def get_village_coords(mc):
    """checks for right clicks while holding a sword, returns the coordinate of the right clicked block in vec3
        checks does not work with netherite sword"""
    blockevents = mc.events.pollBlockHits()

    mc.postToChat('right click on a block while holdling a sword to set village location')
    while blockevents == []:
        blockevents = mc.events.pollBlockHits()
    
    mc.postToChat('location set to ' + str(blockevents[0].pos))
    return blockevents[0].pos


if __name__ == "__main__":
    mc = Minecraft.create()

    vil_length = 85
    num_points = 5

    vil_start = get_village_coords(mc)
    vil_end = vec3.Vec3(vil_start.x + vil_length, 
                        vil_start.y,
                        vil_start.z + vil_length)
    
    #vil_center = vec3.Vec3( vil_start.x + (vil_end.x - vil_start.x)//2,
    #                        0,
    #                        vil_start.z + (vil_end.z - vil_start.z)//2)

    
    #paths,intersections, bordering_paths, plots = path_gen.generate_path_and_plots(vil_start, vil_end, vil_center, num_points)
    
    #front_doors = []
    #for plot in plots:
    #    plot.terraform()
    #    plot.place_house(plot.get_structure())
    #    plot.connect_with_paths(paths,intersections,bordering_paths,vil_start, vil_end)
    #    front_doors.append((plot.front_door.x, plot.front_door.z))
        
    #height_dict = path_gen.get_path_height(paths)
    #path_gen.alternateCheckSteepPath(height_dict,front_doors)
    #for path in paths:
    #    mc.setBlock(path.x, path.y, path.z, block.COAL_ORE)

    #for blocks in intersections:
    #    mc.setBlock(blocks.x, 100, blocks.z, block.BRICK_BLOCK.id)
    
    print(vil_start, vil_end)
    #mc.setBlocks(-200,0,-200,100,200,0)
    #mc.setBlocks(-200,-3,-200,0,200,2)
    #house1_location = McPosition(x,y,z)
    #mc.player.setPos(x,y,z)

     #while mc.getBlock(x + 1,y,z + 1) is 0:
       # y = y - 1
    # print(x,y,z)
    # mc.setBlock(x + 1,y + 1,z + 1, 1) 
    # x = 0
    # y = 0
    # z = 0
    # position = vec3.Vec3(0,0,0)
    # mc.setBlocks(x,y - 1,z,x + 30, y + 50, z + 30, 0)
    # mc.setBlocks(x + 10,y -1,z + 10,x - 30, y + 50, z - 30, 0)
    position = mc.player.getTilePos()
    # vecPos = vec3.Vec3(position)
    width = random.randint(8,12)
    length = random.randint(-16,-12)
    structure1 = Structure(position,width,length)
    # print(structure1.frontleft.x,structure1.frontleft.z,structure1.frontright.x,structure1.frontright.z)
    house1 = House(structure1,3)
    house1.create_house(mc)
    #ran = RandomiseMaterial()
    #ran.rooftop(mc,position .x,position.y,position.z)
    
    #stories = random.randint(1,3)
    #house1 = House(structure1,3)
    #house1.create_house(mc)
    
    #material = ran.random_furniture()
    
    #mc.setBlock(position.x, position.y, position.z, material)
    # mc.setBlock(vector1.x + 1, vector1.y + 2, vector1.z,64,8)
    # mc.setBlock(vector1.x + 1, vector1.y + 1, vector1.z,64,0)
    
    # quit = False
    
    # while not quit:
    #     chatEvents = mc.events.pollChatPosts()
        
    #     for chatEvent in chatEvents:
            
    #         if chatEvent.message.upper() == "QUIT":
    #             quit = True
                
    #         elif chatEvent.message.upper() == "HOUSE":
                
    #             position = mc.player.getTilePos()
    #             # vecPos = vec3.Vec3(position)
    #             vecPos = position
    #             weith = random.randint(8,12)
    #             length = random.randint(12,16)
    #             structure1 = Structure(position,weith,length)
    #             print(structure1.frontleft.x,structure1.frontleft.z,structure1.frontright.x,structure1.frontright.z)
    #             house1 = House(structure1,3)
    #             house1.create_house(mc)
    
    

    
    
   
   
