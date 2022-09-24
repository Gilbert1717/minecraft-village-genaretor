from mcpi import block

class Path_Objects:

    def lampPost(mc, x_coord, y_coord, z_coord): # Create lampPost for path_gen
        
        lamp_height = 4
        
        # Initialising trap door block and trap_door positions that aren't in the API.
        
        trapdoor = 96
        trapdoor_north = 4
        trapdoor_south = 5
        trapdoor_west = 6        
        trapdoor_east = 7   

        # Placing base of lamp post
        mc.setBlock(x_coord, y_coord, z_coord, block.MOSS_STONE.id)

        # Placing fence till lamp_height
        for i in range(1, lamp_height):
            
            mc.setBlock(x_coord, y_coord + i, z_coord, block.FENCE.id)


        # Setting down the trapdoors for the lamp post.
        mc.setBlock(x_coord, y_coord + lamp_height, z_coord - 1, trapdoor, trapdoor_north)
        mc.setBlock(x_coord, y_coord + lamp_height, z_coord + 1, trapdoor, trapdoor_south)

        mc.setBlock(x_coord - 1, y_coord + lamp_height, z_coord, trapdoor, trapdoor_west)
        mc.setBlock(x_coord + 1, y_coord + lamp_height, z_coord, trapdoor, trapdoor_east)

        mc.setBlock(x_coord,y_coord + lamp_height, z_coord, block.GLOWSTONE_BLOCK.id)
        mc.setBlock(x_coord,y_coord + lamp_height + 1, z_coord, trapdoor)
        

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