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

        mc.setBlock(x_coord,y_coord + lamp_height, z_coord, block.GLOWSTONE_BLOCK.id)
        mc.setBlock(x_coord,y_coord + lamp_height + 1, z_coord, trapdoor)

    def setFlowers(): # Lay out flowers near path_gen
        pass 

    def setBench(): # Lay out chairs/benches near path_gen
        pass

    def construction_blockade(mc,x,y,z,axis):
        if axis == 'x':
            
            mc.setBlocks(   x,  y+1,    z-1,
                            x,  y+1,    z+1,block.FENCE.id)
            mc.setBlock(x,y+2,z-1,block.WOOL.id,15) #15 is the data id for black wool
            mc.setBlock(x,y+2,z,block.WOOL.id,4) # 4 is the data id for yellow wool
            mc.setBlock(x,y+2,z+1,block.WOOL.id,15)
            print(axis, x,z)
        else:
            
            mc.setBlocks(   x-1,  y+1,    z,
                            x+1,  y+1,    z,block.FENCE.id)
            mc.setBlock(x-1,y+2,z,block.WOOL.id,15) 
            mc.setBlock(x,y+2,z,block.WOOL.id,4)
            mc.setBlock(x+1,y+2,z,block.WOOL.id,15)
            print(axis,x,z)