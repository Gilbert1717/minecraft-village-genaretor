
from mcpi.vec3 import Vec3
from mcpi import minecraft
from mcpi import block
from fast_query_and_interpolation.mcpi_query_performance import query_blocks

from random import randrange

from models.Structure import Structure
from models.House import House
from fast_query_and_interpolation.interpolation import sigmoid
from fast_query_and_interpolation.interpolation import scale_sigmoid

mc = minecraft.Minecraft.create()

### copy pasted from path_gen.py to circumvent circular dependency issues
def getBlockHeight(block_x, block_z):
    """DOES NOT WORK IF SETWORLDSPAWN HEIGHT IS NOT SET TO 0"""
    
    y = mc.getHeight(block_x,block_z)
    ground_block = mc.getBlock(block_x, y, block_z)
    
    while (ground_block != block.GRASS.id and ground_block != block.DIRT.id and
            ground_block !=block.WATER_STATIONARY.id and ground_block != block.WATER_FLOWING.id 
            and ground_block != block.SAND.id and ground_block != block.STONE.id):
        
        y = y - 1
        ground_block = mc.getBlock(block_x, y, block_z)
        #print(block_x, y, block_z, ground_block)

    return y, ground_block


mc = minecraft.Minecraft.create()

class Plot:
   
    def __init__(self, central_point, distance_from_path, direction, away) -> None:
        """takes voronoi points in a village as its central point."""
        self.central_point      = central_point
        self.distance_from_path = distance_from_path
        self.direction          = direction
        self.away               = away
        buffer_from_path        = 2

        self.plot_start = Vec3(self.central_point.x - int(self.distance_from_path/2) + buffer_from_path,
                                    self.central_point.y,
                                    self.central_point.z - int(self.distance_from_path/2) + buffer_from_path)
          
        self.plot_end   = Vec3(self.central_point.x + int(self.distance_from_path/2) - buffer_from_path,
                                    self.central_point.y,
                                    self.central_point.z + int(self.distance_from_path/2) - buffer_from_path)


        self.plot_length = self.plot_end.x - self.plot_start.x
        
        
        length_lower_bound = 12 if self.plot_length // 2 < 12 else self.plot_length // 2

        self.structure_length = randrange(length_lower_bound,   self.plot_length)
        self.structure_width  = randrange(9,                    self.structure_length)
        
        self.create_terrain_dict()

        if self.direction == 'x-':
            mc.setBlock(self.central_point.x, 100, self.central_point.z, block.CHEST.id)
        elif self.direction == 'x+':
            mc.setBlock(self.central_point.x, 100, self.central_point.z, block.CRAFTING_TABLE.id)
        elif self.direction == 'z-':
            mc.setBlock(self.central_point.x, 100, self.central_point.z, block.DIAMOND_BLOCK.id)
        elif self.direction == 'z+':
            mc.setBlock(self.central_point.x, 100, self.central_point.z, block.END_STONE.id)


    def create_terrain_dict(self):
        self.height_dict = dict()
        self.block_dict = dict()
        terrain_coords = []
        ground =  [ block.GRASS.id, block.DIRT.id, block.WATER_STATIONARY.id, block.SAND.id, block.WATER_FLOWING.id,
                    block.STONE.id, block.CLAY.id, block.MYCELIUM.id, block.SANDSTONE.id]
        
        for x in range(self.plot_start.x - 5, self.plot_end.x + 6): # extra 5 blocks of buffer/padding/margin for use in terraforming
            for z in range(self.plot_start.z - 5, self.plot_end.z + 6):
                terrain_coords.append((x,z))
        
        Done = False

        while not Done:
            Done = True
            redo = set() # used set instead of list because query_blocks returns duplicate results for some reason
            ground_blocks = set()
            
            terrain_height = query_blocks(terrain_coords,'world.getHeight(%d,%d)',int)

            for query_result in terrain_height:
                x = query_result[0][0]
                z = query_result[0][1]
                y = query_result[1]
                
                self.height_dict[(x,z)] = y
                ground_blocks.add((x,y,z))
            
            del terrain_height

            ground_block_queries = query_blocks(ground_blocks,'world.getBlock(%d,%d,%d)',int)
        
            for query_result in ground_block_queries:
                x,y,z = query_result[0]
                block_id = query_result[1]

                if block_id == 0: #then the block is a seagrass
                    self.height_dict[(x,z)] = y
                    self.block_dict[(x,z)] = block.WATER.id
                    
                elif block_id not in ground: # block_id != to prevent Done being set to false at seagrass
                    Done = False
                    redo.add((x,y,z))
                
                


                self.height_dict[(x,z)] = y

                self.block_dict[(x,z)] = block_id

            del ground_block_queries
            del ground_blocks
            
            if Done:
                break
            else:
                for x,y,z in redo:
                    mc.setBlock(x,y,z,block.AIR.id)

                #re-assign terrain cords for the next iteration
                terrain_coords = []
                for x,y,z in redo:
                    terrain_coords.append((x,z))
            
            
    def get_structure(self):
            """contains complicated logic to determine direction and the "frontleft" of a structure inside a plot"""
            #TODO: redo this, houses can still sometimes go beyond the plot
            if self.direction == 'x-':
                structure_start = Vec3(randrange(self.plot_start.x, self.plot_end.x - self.structure_length),
                                            self.central_point.y,
                                            randrange(self.plot_start.z, self.plot_end.z - self.structure_width))
                structure = Structure(structure_start, 1, self.structure_width, self.structure_length)

            elif self.direction =='x+':
                structure_start = Vec3(randrange(self.plot_end.x, self.plot_start.x + self.structure_length, -1) -self.structure_width,
                                            self.central_point.y,
                                            randrange(self.plot_end.z, self.plot_start.z + self.structure_width, -1))
                structure = Structure(structure_start, -1, self.structure_width, self.structure_length)
                   
            elif self.direction =='z-':
                structure_start = Vec3(randrange(self.plot_end.x, self.plot_start.x + self.structure_width, -1) - self.structure_width,
                                            self.central_point.y,
                                            randrange(self.plot_start.z, self.plot_end.z - self.structure_length))
                structure = Structure(structure_start, 1, self.structure_width, self.structure_length)

            elif self.direction =='z+':
                structure_start = Vec3(randrange(self.plot_start.x, self.plot_end.x - self.structure_width),
                                            self.central_point.y,
                                            randrange(self.plot_end.z, self.plot_start.z + self.structure_length, -1))
                structure = Structure(structure_start, -1, self.structure_width, self.structure_length)
            
            self.structure = structure

            return structure
                

    def place_land(self):
        #clears the space above the plot
        mc.setBlocks(   self.plot_start.x, self.plot_start.y, self.plot_start.z,
                        self.plot_end.x, self.plot_end.y + 30, self.plot_end.z, block.AIR.id)
        
        #places floor
        for x in range(self.plot_start.x, self.plot_end.x +1):
            for z in range(self.plot_start.z, self.plot_end.z +1):
                y = self.central_point.y
                mc.setBlocks(   x,y-20,z,
                                x,y,z, self.block_dict[(x,z)])
    
    
                
    def terraform(self):
        self.place_land()

        ###### most of the code blocks here are very similar,
        ###### but different enough so that there isnt an obvious and elegant way to condense them into one function

        # terraforms the "-x" side of the plot
        x = self.plot_start.x
        for z in range(self.plot_start.z , self.plot_end.z + 1):
            y_diff = self.height_dict[(x-5,z)] - self.central_point.y
            
            interpolated = scale_sigmoid(0.5, 0.3, 6, y_diff, self.central_point.y)
        
            for x_interp in range(self.plot_start.x, self.plot_start.x - 5, -1):
                y = interpolated.pop(0)
                
                mc.setBlocks(   x_interp, y - 20,z,
                                x_interp, y, z, self.block_dict[(x_interp,z)])
                mc.setBlocks(   x_interp, y + 1, z,
                                x_interp, y + 21, z, block.AIR.id)
                
        # terraforms the "+z" side of the plot
        z = self.plot_end.z
        for x in range(self.plot_start.x , self.plot_end.x + 1):
            y_diff = self.height_dict[(x,z + 5)] - self.central_point.y
            
            interpolated = scale_sigmoid(0.5, 0.3, 6, y_diff, self.central_point.y)
            
            for z_interp in range(self.plot_end.z, self.plot_end.z + 6):
                y = interpolated.pop(0)
                
                mc.setBlocks(   x, y - 20,z_interp,
                                x, y, z_interp, self.block_dict[(x,z_interp)])
                mc.setBlocks(   x, y + 1,z_interp,
                                x, y + 21, z_interp, block.AIR.id)
        
        # terraforms the "+x" side of the plot
        x = self.plot_end.x
        for z in reversed(range(self.plot_start.z , self.plot_end.z + 1)):
            y_diff = self.height_dict[(x+5,z)] - self.central_point.y
            
            interpolated = scale_sigmoid(0.5, 0.3, 6, y_diff, self.central_point.y)
            
            for x_interp in range(self.plot_end.x, self.plot_end.x + 6):
                y = interpolated.pop(0)
                mc.setBlocks(   x_interp, y - 20,z,
                                x_interp, y, z, self.block_dict[(x_interp,z)])
                mc.setBlocks(   x_interp, y + 1, z,
                                x_interp, y + 21, z, block.AIR.id)
        
        # terraforms the "-z" side of the plot
        z = self.plot_start.z
        for x in reversed(range(self.plot_start.x , self.plot_end.x + 1)):
            y_diff = self.height_dict[(x,z - 5)] - self.central_point.y
            
            interpolated = scale_sigmoid(0.5, 0.3, 6, y_diff, self.central_point.y)
            
            for z_interp in range(self.plot_start.z, self.plot_start.z - 6, -1):
                y = interpolated.pop(0)
                mc.setBlocks(   x, y - 20,z_interp,
                                x, y, z_interp, self.block_dict[(x,z_interp)])
                mc.setBlocks(   x, y + 1,z_interp,
                                x, y + 21, z_interp, block.AIR.id)
        
        #interpolate corners
        #corner1
        #########
            ########## interpolate diagonally from plot corner to outer corner 
        xs = [x for x in reversed(range(self.plot_start.x - 3, self.plot_start.x + 2))]
        zs = [z for z in reversed(range(self.plot_start.z - 3, self.plot_start.z + 2))]
        corner_coords  = [(xs[i],zs[i]) for i in range(5)]

        y_diff = self.height_dict[corner_coords[-1]] - self.central_point.y
        
        interpolated = scale_sigmoid(0.5, 0.5, 6, y_diff, self.central_point.y)
        
        ybase_1, ybase_2 = interpolated[1], interpolated[2] # used for interpolating the rest of the corner
        
        for x,z in corner_coords:
            y = interpolated.pop(0)
            mc.setBlocks(   x, y - 20,z,
                            x, y, z, self.block_dict[(x,z_interp)])
            mc.setBlocks(   x, y + 1,z,
                            x, y + 21, z, block.AIR.id)
            ##########


        #interpolate from the corner diagonal to the corner sides
        x,z = corner_coords[1]
            #########
        y_diff = self.height_dict[x,z-3] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5, y_diff, ybase_1)

        for z_interp in range(z, z - 4, -1):
            y = interpolated.pop(0)
            mc.setBlocks(   x, y - 20,z_interp,
                            x, y, z_interp, self.block_dict[(x,z_interp)])
            mc.setBlocks(   x, y + 1,z_interp,
                            x, y + 21, z_interp, block.AIR.id)

        y_diff = self.height_dict[x-3,z] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5    , y_diff, ybase_1)

        for x_interp in range(x, x - 4, -1):
            y = interpolated.pop(0)
            mc.setBlocks(   x_interp, y - 20,z,
                            x_interp, y, z, self.block_dict[(x_interp,z)])
            mc.setBlocks(   x_interp, y + 1,z,
                            x_interp, y + 21, z, block.AIR.id)
            ########
        x,z = corner_coords[2]

        y_diff = self.height_dict[x,z-2] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for z_interp in range(z, z - 3, -1):
            y = interpolated.pop(0)
            mc.setBlocks(   x, y - 20,z_interp,
                            x, y, z_interp, self.block_dict[(x,z_interp)])
            mc.setBlocks(   x, y + 1,z_interp,
                            x, y + 21, z_interp, block.AIR.id)

        y_diff = self.height_dict[x-2,z] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for x_interp in range(x, x - 3, -1):
            y = interpolated.pop(0)
            mc.setBlocks(   x_interp, y - 20,z,
                            x_interp, y, z, self.block_dict[(x_interp,z)])
            mc.setBlocks(   x_interp, y + 1,z,
                            x_interp, y + 21, z, block.AIR.id)
            ##########
        ########

        #corner2
        #########
            ########## interpolate diagonally from plot corner to outer corner 
        xs = [x for x in range(self.plot_end.x - 1, self.plot_end.x + 4)]
        zs = [z for z in reversed(range(self.plot_start.z - 3, self.plot_start.z + 2))]
        corner_coords  = [(xs[i],zs[i]) for i in range(5)]

        y_diff = self.height_dict[corner_coords[-1]] - self.central_point.y
        
        interpolated = scale_sigmoid(0.5, 0.5, 6, y_diff, self.central_point.y)
        
        ybase_1, ybase_2 = interpolated[1], interpolated[2] # used for interpolating the rest of the corner
        
        for x,z in corner_coords:
            y = interpolated.pop(0)
            mc.setBlocks(   x, y - 20,z,
                            x, y, z, self.block_dict[(x,z_interp)])
            mc.setBlocks(   x, y + 1,z,
                            x, y + 21, z, block.AIR.id)
            ##########


        #interpolate from the corner diagonal to the corner sides
        x,z = corner_coords[1]
            #########
        y_diff = self.height_dict[x,z-3] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5, y_diff, ybase_1)

        for z_interp in range(z, z - 4, -1):
            y = interpolated.pop(0)
            mc.setBlocks(   x, y - 20,z_interp,
                            x, y, z_interp, self.block_dict[(x,z_interp)])
            mc.setBlocks(   x, y + 1,z_interp,
                            x, y + 21, z_interp, block.AIR.id)

        y_diff = self.height_dict[x+3,z] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5    , y_diff, ybase_1)

        for x_interp in range(x, x + 4):
            y = interpolated.pop(0)
            mc.setBlocks(   x_interp, y - 20,z,
                            x_interp, y, z, self.block_dict[(x_interp,z)])
            mc.setBlocks(   x_interp, y + 1,z,
                            x_interp, y + 21, z, block.AIR.id)
            ########
        x,z = corner_coords[2]

        y_diff = self.height_dict[x,z-2] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for z_interp in range(z, z - 3, -1):
            y = interpolated.pop(0)
            mc.setBlocks(   x, y - 20,z_interp,
                            x, y, z_interp, self.block_dict[(x,z_interp)])
            mc.setBlocks(   x, y + 1,z_interp,
                            x, y + 21, z_interp, block.AIR.id)

        y_diff = self.height_dict[x+2,z] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for x_interp in range(x, x + 3):
            y = interpolated.pop(0)
            mc.setBlocks(   x_interp, y - 20,z,
                            x_interp, y, z, self.block_dict[(x_interp,z)])
            mc.setBlocks(   x_interp, y + 1,z,
                            x_interp, y + 21, z, block.AIR.id)
            ##########
        ########
    
        #corner3
        #########
            ########## interpolate diagonally from plot corner to outer corner 
        xs = [x for x in range(self.plot_end.x - 1, self.plot_end.x + 4)]
        zs = [z for z in range(self.plot_end.z - 1, self.plot_end.z + 4)]
        corner_coords  = [(xs[i],zs[i]) for i in range(5)]

        y_diff = self.height_dict[corner_coords[-1]] - self.central_point.y
        
        interpolated = scale_sigmoid(0.5, 0.5, 6, y_diff, self.central_point.y)
        
        ybase_1, ybase_2 = interpolated[1], interpolated[2] # used for interpolating the rest of the corner
        
        for x,z in corner_coords:
            y = interpolated.pop(0)
            mc.setBlocks(   x, y - 20,z,
                            x, y, z, self.block_dict[(x,z_interp)])
            mc.setBlocks(   x, y + 1,z,
                            x, y + 21, z, block.AIR.id)
            ##########


        #interpolate from the corner diagonal to the corner sides
        x,z = corner_coords[1]
            #########
        y_diff = self.height_dict[x,z+3] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5, y_diff, ybase_1)

        for z_interp in range(z, z + 4):
            y = interpolated.pop(0)
            mc.setBlocks(   x, y - 20,z_interp,
                            x, y, z_interp, self.block_dict[(x,z_interp)])
            mc.setBlocks(   x, y + 1,z_interp,
                            x, y + 21, z_interp, block.AIR.id)

        y_diff = self.height_dict[x+3,z] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5    , y_diff, ybase_1)

        for x_interp in range(x, x + 4):
            y = interpolated.pop(0)
            mc.setBlocks(   x_interp, y - 20,z,
                            x_interp, y, z, self.block_dict[(x_interp,z)])
            mc.setBlocks(   x_interp, y + 1,z,
                            x_interp, y + 21, z, block.AIR.id)
            ########
        x,z = corner_coords[2]

        y_diff = self.height_dict[x,z+2] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for z_interp in range(z, z + 3):
            y = interpolated.pop(0)
            mc.setBlocks(   x, y - 20,z_interp,
                            x, y, z_interp, self.block_dict[(x,z_interp)])
            mc.setBlocks(   x, y + 1,z_interp,
                            x, y + 21, z_interp, block.AIR.id)

        y_diff = self.height_dict[x+2,z] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for x_interp in range(x, x + 3):
            y = interpolated.pop(0)
            mc.setBlocks(   x_interp, y - 20,z,
                            x_interp, y, z, self.block_dict[(x_interp,z)])
            mc.setBlocks(   x_interp, y + 1,z,
                            x_interp, y + 21, z, block.AIR.id)
            ##########
        ########

        #corner4
        #########
            ########## interpolate diagonally from plot corner to outer corner 
        xs = [x for x in reversed(range(self.plot_start.x - 3, self.plot_start.x + 2))]
        zs = [z for z in range(self.plot_end.z - 1, self.plot_end.z + 4)]
        corner_coords  = [(xs[i],zs[i]) for i in range(5)]

        y_diff = self.height_dict[corner_coords[-1]] - self.central_point.y
        
        interpolated = scale_sigmoid(0.5, 0.5, 6, y_diff, self.central_point.y)
        
        ybase_1, ybase_2 = interpolated[1], interpolated[2] # used for interpolating the rest of the corner
        
        for x,z in corner_coords:
            y = interpolated.pop(0)
            mc.setBlocks(   x, y - 20,z,
                            x, y, z, self.block_dict[(x,z_interp)])
            mc.setBlocks(   x, y + 1,z,
                            x, y + 21, z, block.AIR.id)
            ##########


        #interpolate from the corner diagonal to the corner sides
        x,z = corner_coords[1]
            #########
        y_diff = self.height_dict[x,z+3] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5, y_diff, ybase_1)

        for z_interp in range(z, z + 4):
            y = interpolated.pop(0)
            mc.setBlocks(   x, y - 20,z_interp,
                            x, y, z_interp, self.block_dict[(x,z_interp)])
            mc.setBlocks(   x, y + 1,z_interp,
                            x, y + 21, z_interp, block.AIR.id)

        y_diff = self.height_dict[x-3,z] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5    , y_diff, ybase_1)

        for x_interp in range(x, x - 4, -1):
            y = interpolated.pop(0)
            mc.setBlocks(   x_interp, y - 20,z,
                            x_interp, y, z, self.block_dict[(x_interp,z)])
            mc.setBlocks(   x_interp, y + 1,z,
                            x_interp, y + 21, z, block.AIR.id)
            ########
        x,z = corner_coords[2]

        y_diff = self.height_dict[x,z+2] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for z_interp in range(z, z + 3):
            y = interpolated.pop(0)
            mc.setBlocks(   x, y - 20,z_interp,
                            x, y, z_interp, self.block_dict[(x,z_interp)])
            mc.setBlocks(   x, y + 1,z_interp,
                            x, y + 21, z_interp, block.AIR.id)

        y_diff = self.height_dict[x-2,z] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for x_interp in range(x, x - 3, -1):
            y = interpolated.pop(0)
            mc.setBlocks(   x_interp, y - 20,z,
                            x_interp, y, z, self.block_dict[(x_interp,z)])
            mc.setBlocks(   x_interp, y + 1,z,
                            x_interp, y + 21, z, block.AIR.id)
            ##########
        ########


    def place_house(self, structure):
        house = House(structure)
        house.create_house(mc)
        self.house_door = house.front_door
        return house.front_door

    def connect_with_paths(self,path_coords, intersection_coords, bordering_paths, vil_start, vil_end):
        # staring from one block away from the front door, travel facing self.direction until it connects to a path block. 
        # traverse the path away from the centre of the village in the perpendicular direction, and delete that section if there is no intersection.
        # add the connection as an intersection, then add the new path connection to the path blocks list
        # if the front door is outside of the village area, connect to the nearest block in bordering_paths in terms of the self.direction axis.
        connection = []
        if self.direction == 'x-':
            new_path = Vec3(self.house_door.x, 0, self.house_door.z -2) # starting point
            connection.append(new_path)
            if Plot.out_of_range(new_path, vil_start, vil_end):
                nearest = Plot.find_nearest_bordering_paths(new_path,
                                    [coord for coord in bordering_paths if coord.z == vil_end.z or coord.z == vil_start.z])

                while new_path.x != nearest.x:
                    new_path = Vec3(new_path.x - 1, 0, new_path.z)
                    connection.append(new_path)

                if nearest.z > new_path.z:
                    for z in range(new_path.z, nearest.z):
                        connection.append(Vec3(new_path.x, 0, z))
                    intersection_coords.append(new_path.x,0,z+ 1)

                else:
                    for z in range(nearest.z, new_path.z):
                        connection.append(Vec3(new_path.x, 0, z))
                    intersection_coords.append(new_path.x,0,z + 1)
                
                print(connection)
            else:
                while new_path not in path_coords:
                    new_path = Vec3(new_path.x - 1, 0,  new_path.z)
                    connection.append(new_path)
                else:
                    append_to_intersection_coords_later = new_path # to prevent it from intervering with the next while loop

                    #traverse the path away from the village centre
                    traversed = []

                    if self.away == 'z-':
                        n = -1
                    else:
                        n = 1
                    
                    curr_block = new_path

                    while curr_block not in intersection_coords:
                        blocks_in_path_coords = False
                        potential_next_blocks = [   Vec3(curr_block.x + 1, 0, curr_block.z + n),
                                                    Vec3(curr_block.x    , 0, curr_block.z + n),
                                                    Vec3(curr_block.x - 1, 0, curr_block.z + n),]

                        for block in potential_next_blocks:
                            if block in path_coords:
                                curr_block = block
                                traversed.append(curr_block)
                                blocks_in_path_coords = True
                                continue
                        
                        if not blocks_in_path_coords:
                            for block in traversed:
                                if block in path_coords:
                                    path_coords.remove(block)
                            break
                    
                    intersection_coords.append(append_to_intersection_coords_later)
                    

        elif self.direction =='x+':
            new_path = Vec3(self.house_door.x, 0, self.house_door.z + 2) # starting point
            connection.append(new_path)
            if Plot.out_of_range(new_path, vil_start, vil_end):
                nearest = Plot.find_nearest_bordering_paths(new_path,
                                    [coord for coord in bordering_paths if coord.z == vil_end.z or coord.z == vil_start.z])

                while new_path.x != nearest.x:
                    new_path = Vec3(new_path.x + 1, 0, new_path.z)
                    connection.append(new_path)

                if nearest.z > new_path.z:
                    for z in range(new_path.z, nearest.z):
                        connection.append(Vec3(new_path.x, 0, z))
                    intersection_coords.append(new_path.x,0,z+ 1)

                else:
                    for z in range(nearest.z, new_path.z):
                        connection.append(Vec3(new_path.x, 0, z))
                    intersection_coords.append(new_path.x,0,z + 1)
                
                print(connection)
            else:
                while new_path not in path_coords:
                    new_path = Vec3(new_path.x + 1, 0,  new_path.z)
                    connection.append(new_path)
                else:
                    append_to_intersection_coords_later = new_path # to prevent it from intervering with the next while loop

                    #traverse the path away from the village centre
                    traversed = []

                    if self.away == 'z-':
                        n = -1
                    else:
                        n = 1
                    
                    curr_block = new_path

                    while curr_block not in intersection_coords:
                        blocks_in_path_coords = False
                        potential_next_blocks = [   Vec3(curr_block.x + 1, 0, curr_block.z + n),
                                                    Vec3(curr_block.x    , 0, curr_block.z + n),
                                                    Vec3(curr_block.x - 1, 0, curr_block.z + n),]

                        for block in potential_next_blocks:
                            if block in path_coords:
                                curr_block = block
                                traversed.append(curr_block)
                                blocks_in_path_coords = True
                                continue
                        
                        if not blocks_in_path_coords:
                            for block in traversed:
                                if block in path_coords:
                                    path_coords.remove(block)
                            break
                    
                    intersection_coords.append(append_to_intersection_coords_later)
        elif self.direction =='z-':
            pass
        elif self.direction =='z+':
            pass

        path_coords.extend(connection)
        return path_coords


    def out_of_range(starting_point, vil_start, vil_end):
        """function for connect_with_paths()"""
        x_out_of_range = starting_point.x <= vil_start.x - 3 or starting_point.x >= vil_end.x + 3 #3 block buffer to protect from false negatives
        z_out_of_range = starting_point.z <= vil_start.z - 3 or starting_point.z >= vil_end.z + 3

        if x_out_of_range or z_out_of_range:
            return True
        else:
            return False
    
    def find_nearest_bordering_paths(new_path,bordering_paths):
        """function for connect_with_paths()"""
        distances = [] 

        for coord in bordering_paths:
            distances.append((coord, abs(coord.x - new_path.x) + abs(coord.z - new_path.z)))
            
        distances.sort(key = lambda list : list[1]) 
        print(distances)
        print(bordering_paths)
        return distances[0][0]

    
    
if __name__ == '__main__':
    test_plot = Plot(mc.player.getTilePos(),20,'z+', 'x+')
    test_plot.terraform()
    #test_plot.place_house(test_plot.get_structure())