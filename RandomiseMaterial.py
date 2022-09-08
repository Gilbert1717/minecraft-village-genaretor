from mcpi.minecraft import Minecraft
import random 

class RandomiseMaterial:
    
    def random_exterior():
        
        exterior_blocks = {'STONE_BRICK': 98,
                           'BRICK_BLOCK': 45,
                           'COBBLESTONE': 4,
                           'SANDSTONE': 24, 
                           'NETHER_BRICK': 112,
                           'WOOD PLANK': 17
                        }
        
        materialID = random.choice(list(exterior_blocks.values()))
        
        return materialID
    
    #TODO colorID + randomize roofs 