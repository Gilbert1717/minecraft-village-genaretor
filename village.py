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
    
    vil_center = vec3.Vec3( vil_start.x + (vil_end.x - vil_start.x)//2,
                            0,
                            vil_start.z + (vil_end.z - vil_start.z)//2)

    
    paths,intersections, bordering_paths, plots = path_gen.generate_path_and_plots(vil_start, vil_end, vil_center, num_points)
    
    #sort the plots by distance from village center. in descending order.
    plots.sort( key = lambda plot: ((plot.central_point.x - vil_center.x)**2 + (plot.central_point.z - vil_center.z)**2)** 0.5,
                reverse= True) #IMPORTANT!!! OR ELSE ROADS MAY BE DISCONNECTED
    
    for plot in plots:
        plot.terraform()
        plot.place_house(plot.get_structure())

    #sort the plots by distance from village center. in descending order.
    plots.sort( key = lambda plot: ((plot.house_door.x - vil_center.x)**2 + (plot.house_door.z - vil_center.z)**2)** 0.5,
                reverse= True) #IMPORTANT!!! OR ELSE ROADS MAY BE DISCONNECTED
    
    for plot in plots:
        plot.connect_with_paths(paths,intersections,bordering_paths,vil_start, vil_end)
    
    
    path_gen.get_path_height(paths)
    

    for blocks in intersections:
        mc.setBlock(blocks.x, 100, blocks.z, block.BRICK_BLOCK.id)
    
    
    
    #material = ran.random_furniture()
    
    
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
    
    

    
    
   
   
