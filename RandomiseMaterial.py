from mcpi.minecraft import Minecraft
from mcpi import block
import random 

# from models.House import *

class RandomiseMaterial:
    def __init__(self) -> None:
         pass
    
    def random_exterior(mc):
       #block ID simplification  
        exterior_blocks = [block.STONE_BRICK.id,
                          block.BRICK_BLOCK.id,
                          block.COBBLESTONE.id,
                          block.MOSS_STONE.id,
                          block.WOOD_PLANKS.withData(0),
                          block.WOOD_PLANKS.withData(1),
                          block.WOOD_PLANKS.withData(2),
                          block.WOOD_PLANKS.withData(3)
                          ]

        
        number = 0
        number = random.randrange(0, len(exterior_blocks))
        randomBlock = block.DIRT.id

        randomBlock = exterior_blocks[number]
        return randomBlock
        
#builds a pyramid roof
    def rooftop(self, mc,x,y,z):

        x_offset = 8
        y_offset = 1
        z_offset = 8
        mc.setBlocks(x,y + y_offset,z, x + x_offset, y + y_offset, z + z_offset, block.WOOD_PLANKS.withData(1))
        mc.setBlocks(x+1,y + y_offset+1,z+1, x + x_offset-1, y + y_offset+1, z + z_offset-1, block.WOOD_PLANKS.withData(2))
        mc.setBlocks(x+2,y + y_offset+2,z+2, x + x_offset-2, y + y_offset+2, z + z_offset-2, block.WOOD_PLANKS.withData(1))
        mc.setBlocks(x+3,y + y_offset+3,z+3, x + x_offset-3, y + y_offset+3, z + z_offset-3, block.WOOD_PLANKS.withData(2))
        
    #TODO colorID + randomize roofs 

