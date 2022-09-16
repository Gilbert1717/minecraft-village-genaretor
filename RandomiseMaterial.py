from mcpi.minecraft import Minecraft
from mcpi import block
import random 

class RandomiseMaterial:
    
    def random_exterior(mc):
        
        exterior_blocks = [block.STONE_BRICK.id,
                          block.BRICK_BLOCK.id,
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
    
    def random_floors(mc):
        
        floor_blocks = [block.COBBLESTONE.id,
                        block.SANDSTONE.id,
                        block.LEAVES.id,
                        block.SANDSTONE.withData(2),
                        block.STONE_BRICK.withData(2)]
        
        number = 0
        number = random.randrange(0, len(floor_blocks))
        
        randomBlock = block.DIRT.id
        randomBlock  = floor_blocks[number]
        
        return randomBlock
    
    #TODO colorID + randomize roofs 