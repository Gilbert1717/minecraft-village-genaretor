from mcpi.minecraft import Minecraft
from mcpi import block
import random 

class RandomiseMaterial:
    
    def random_exterior():
        
        exterior_blocks = [block.STONE_BRICK.id,
                          block.BRICK_BLOCK.id,
                          block.COBBLESTONE.id,
                          block.MOSS_STONE.id,
                          block.WOOD_PLANKS.withData(0),
                          block.WOOD_PLANKS.withData(1),
                          block.WOOD_PLANKS.withData(2),
                          block.WOOD_PLANKS.withData(3)
                          ]

        
        blockValue = random.randRange(0, len(exterior_blocks))
        
        return exterior_blocks[blockValue]
    
    #TODO colorID + randomize roofs 