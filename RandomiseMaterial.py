from mcpi.minecraft import Minecraft
from mcpi import block
import random 

class RandomiseMaterial:
    
    def random_exterior(mc):
        
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
    
    #TODO colorID + randomize roofs 