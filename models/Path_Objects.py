from mcpi import block

class Path_Objects:
    
    def lampPost(mc, x_coord, y_coord, z_coord): # Create lampPost for path_gen
        #TODO: Use getheight function, to ensure that it doesnt place into the ground, but ontop.
        lamp_height = 4
        one_unit = 1
        # Initialising trap door block and trap_door positions that aren't in the API.
        trapdoor = 96
        trapdoor_north = 4
        trapdoor_south = 5
        trapdoor_west = 6        
        trapdoor_east = 7
        
        mc.setBlock(x_coord, y_coord, z_coord, block.MOSS_STONE.id)
        
        for i in range(one_unit, lamp_height):
            mc.setBlock(x_coord, y_coord + i, z_coord, block.FENCE.id)
            
        mc.setBlock(x_coord, y_coord + lamp_height, z_coord - one_unit, trapdoor, trapdoor_north)
        mc.setBlock(x_coord, y_coord + lamp_height, z_coord + one_unit, trapdoor, trapdoor_south)
        
        mc.setBlock(x_coord - one_unit, y_coord + lamp_height, z_coord, trapdoor, trapdoor_west)
        mc.setBlock(x_coord + one_unit, y_coord + lamp_height, z_coord, trapdoor, trapdoor_east)
        
    def setFlowers(): # Lay out flowers near path_gen
        pass 
    
    def setBench(): # Lay out chairs/benches near path_gen
        pass
    
        