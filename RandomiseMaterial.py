from mcpi.minecraft import Minecraft
from mcpi import block
import random 

class RandomiseMaterial:
    
    def random_exterior(mc): #Returns a block material to use for the exterior parts of the house
        
        # ADDING BLOCKS THAT ARE NOT INCLUDED IN MCPI BLOCK MODULE
        NETHER_BRICK = 112
        
        exterior_blocks = [block.STONE_BRICK.withData(0),
                           block.STONE_BRICK.withData(3),
                           block.BRICK_BLOCK.id,
                           block.WOOD_PLANKS.withData(0),
                           block.WOOD_PLANKS.withData(1), # Creates a list of blocks, for the house exterior.
                           block.WOOD_PLANKS.withData(2),
                           NETHER_BRICK
                           ]

        # Returns random block in the list
        number = 0
        number = random.randrange(0, len(exterior_blocks)) 
        randomBlock = block.DIRT.id

        randomBlock = exterior_blocks[number]
        
        # print(f"exterior block: {randomBlock}")
        return randomBlock
    
    def random_floors(mc): #Returns a block material to use for the floors of the house
        
        # ADDING A BLOCK THAT ISNT IN THE MCPI BLOCK MODULE
        floor_blocks = [block.COBBLESTONE.id,
                        block.SANDSTONE.id,
                        block.WOOL.withData(0),
                        block.WOOL.withData(14), # Creates a list of blocks for the house floors.
                        block.WOOL.withData(15),
                        block.SANDSTONE.withData(2),
                        block.STONE_BRICK.withData(2)]
        
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
    
    def vertical_outline_blocks(mc): # Returns blocks to use for the outline of the house.
        
        outline_blocks = [block.WOOD.withData(0), # WOOD OAK, DIRECTIONALLY UP/DOWN
                          block.WOOD.withData(1), # SPRUCE OAK, DIRECTIONALLY UP/DOWN
                          block.WOOD.withData(2), # BIRCH OAK, DIRECTIONALLY UP/DOWN
                          ]
        
        number = 0
        number = random.randrange(0, len(outline_blocks))
        
        randomBlock = block.DIRT.id
        randomBlock = outline_blocks[number]
        
        return randomBlock
    
    def east_outline_blocks(mc, wood_block): # Returns the horizontal (east/west) version of vertical_outline_blocks
        
        if wood_block == block.WOOD.withData(0):
            return block.WOOD.withData(4) # WOOD OAK, EAST/WEST
        
        elif wood_block == block.WOOD.withData(1):
            return block.WOOD.withData(5) # SPRUCE OAK, EAST/WEST
        
        elif wood_block == block.WOOD.withData(2):
            return block.WOOD.withData(6) # BIRCH OAK, EAST/WEST
    
    def north_outline_blocks(mc, wood_block): # Returns the horizontal (north/west) version of vertical_outline_blocks
        
        if wood_block == block.WOOD.withData(0):
            return block.WOOD.withData(8) # WOOD OAK, NORTH/WEST
        
        elif wood_block == block.WOOD.withData(1):
            return block.WOOD.withData(9) # SPRUCE OAK, NORTH/WEST
        
        elif wood_block == block.WOOD.withData(2):
            return block.WOOD.withData(10) # BIRCH OAK, NORTH/WEST
        
    #TODO create roof structures + randomize roofs
    #TODO create wall outer layer to add more aesthetic
    #TODO place a form of lighting, whether that be patterned glowstone floors or torches.
    #TODO room decorations/furniture