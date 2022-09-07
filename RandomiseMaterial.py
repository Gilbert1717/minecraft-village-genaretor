from mcpi.minecraft import Minecraft
from mcpi import block
import random 

class RandomiseMaterial:
    
    def random_exterior(self,block):

        exteriorBlocks = [block.STONE_BRICK.id,
                          block.BRICK_BLOCK.id,
                          block.NETHER_BRICK.id,
                          block.WOOD_PLANKS.id,
                          block.COBBLESTONE.id,
                          block.MOSS_STONE.id,
                          block.SANDSTONE.id
                          ]

        number = 0
        number = random.randrange(0, len(exteriorBlocks))
        randomBlock = block.DIRT.id

        randomBlock = exteriorBlocks[number]
        return randomBlock