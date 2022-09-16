from mcpi.minecraft import Minecraft
from mcpi import block
import random 

class RandomiseMaterial:
    
    def random_exterior(mc): #Returns a block material to use for the exterior parts of the house
        
        exterior_blocks = [block.STONE_BRICK.withData(0),
                          block.BRICK_BLOCK.id,
                          block.WOOD_PLANKS.withData(0),
                          block.WOOD_PLANKS.withData(1), # Creates a list of blocks, for the house exterior.
                          block.WOOD_PLANKS.withData(2),
                          block.WOOD_PLANKS.withData(3)
                          ]

        # Returns random block in the list
        number = 0
        number = random.randrange(0, len(exterior_blocks)) 
        randomBlock = block.DIRT.id

        randomBlock = exterior_blocks[number]
        
        # print(f"exterior block: {randomBlock}")
        return randomBlock
    
    def random_floors(mc): #Returns a block material to use for the floors of the house
        
        floor_blocks = [block.COBBLESTONE.id,
                        block.SANDSTONE.id,
                        block.WOOL.withData(0),
                        block.WOOL.withData(14), # Creates a list of blocks for the house floors.
                        block.WOOL.withData(15),
                        block.SANDSTONE.withData(2),
                        block.STONE_BRICK.withData(3)]
        
        # Returns random block in the list
        number = 0
        number = random.randrange(0, len(floor_blocks))
        
        randomBlock = block.DIRT.id
        randomBlock  = floor_blocks[number]
        
        return randomBlock
    
    def random_furniture(mc): # Returns furniture blocks to randomly place in the house.
        
        furniture_blocks = [block.BOOKSHELF.id,
                            block.CHEST.id, 
                            block.FURNACE_ACTIVE.id, # Creates a list of blocks for the furnitures in house.
                            block.CRAFTING_TABLE.id,
                            block.COBWEB.id
                            ]
        
        # Returns random block in the list
        number = 0
        number = random.randrange(0, len(furniture_blocks))
        
        randomBlock = block.DIRT.id
        randomBlock = furniture_blocks[number]
        
        return randomBlock
    
    def outline_blocks(mc): # Returns blocks to use for the outline of the house.
        
        outline_blocks = [block.WOOD.withData(0), # WOOD OAK, DIRECTIONALLY UP/DOWN
                          block.WOOD.withData(1), # SPRUCE OAK, DIRECTIONALLY UP/DOWN
                          block.WOOD.withData(2), # BIRCH OAK, DIRECTIONALLY UP/DOWN
                          ]
        
    #TODO create roof structures + randomize roofs
    #TODO create wall outer layer to add more aesthetic
    #TODO place a form of lighting, whether that be patterned glowstone floors or torches.
    #TODO room decorations/furniture