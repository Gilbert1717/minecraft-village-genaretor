# Assignment 1 main file
# Feel free to add additional modules/files as you see fit.


from mcpi.minecraft import Minecraft

from mcpi import block
from mcpi import vec3
from RandomiseMaterial import RandomiseMaterial

import random

from models.House import House
from models.Structure import *

import path_gen


def get_village_coords(mc):
    """checks for right clicks while holding a sword, returns the coordinate of the right clicked block in vec3
        checks does not work with netherite sword"""
    blockevents = mc.events.pollBlockHits()

    mc.postToChat('right click on a block while holdling a wooden sword to set the village location. ')
    mc.postToChat('the village will generate towards postive x & z away from the block')
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
    
    front_doors = []
    for plot in plots:
        plot.terraform()
        #plot.get_structure()
        plot.place_house(plot.get_structure())
        front_door_path = plot.connect_with_paths(paths,intersections,bordering_paths,vil_start, vil_end)
        front_doors.append(front_door_path)
        
        
    height_dict = path_gen.get_path_height(paths)
    
    paths, raised_paths,final_height_dict = path_gen.alternateCheckSteepPath(height_dict,front_doors)

    blocks_to_add_support_to = []
    blocks_to_add_support_to.extend(paths)

    for plot in plots:
        blocks_to_add_support_to.extend(plot.structure_corners)
    
    path_gen.add_support_blocks(blocks_to_add_support_to)
    
    for path in paths:
        mc.setBlocks(path.x-1, path.y, path.z-1, 
                     path.x+1, path.y, path.z+1,block.COBBLESTONE.id)
    
    for plot in plots: # clears out the doorway
        mc.setBlock(plot.house_door.x, plot.house_door.y + 1, plot.house_door.z -1, block.AIR.id)
        mc.setBlock(plot.house_door.x, plot.house_door.y + 1, plot.house_door.z +1, block.AIR.id)

    path_gen.add_construction_blockades(bordering_paths,intersections,final_height_dict, vil_start, vil_end)
    path_gen.add_lamp_posts(intersections,height_dict)






    
   

    
    
    

    
    
   
   
