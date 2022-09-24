
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
        #TEMPORARY CODE to test village.py without creating a house
        #self.house_door = Vec3(central_point.x, 0, central_point.z + 5)
        ############################################################
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
            redo = set() # used set instead of list because query_blocks returns duplicated results for some reason
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

                if block_id == 0: #prevents an infinite loop when the block is a seagrass
                    self.height_dict[(x,z)] = y
                    self.block_dict[(x,z)] = block.WATER.id
                    
                elif block_id not in ground:
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
                structure = Structure(structure_start, self.structure_width, self.structure_length)

            elif self.direction =='x+':
                structure_start = Vec3(randrange(self.plot_end.x, self.plot_start.x + self.structure_length, -1) -self.structure_width,
                                            self.central_point.y,
                                            randrange(self.plot_end.z, self.plot_start.z + self.structure_width, -1))
                structure = Structure(structure_start, self.structure_width, - self.structure_length)
                   
            elif self.direction =='z-':
                structure_start = Vec3(randrange(self.plot_end.x, self.plot_start.x + self.structure_width, -1) - self.structure_width,
                                            self.central_point.y,
                                            randrange(self.plot_start.z, self.plot_end.z - self.structure_length))
                structure = Structure(structure_start, self.structure_width, self.structure_length)

            elif self.direction =='z+':
                structure_start = Vec3(randrange(self.plot_start.x, self.plot_end.x - self.structure_width),
                                            self.central_point.y,
                                            randrange(self.plot_end.z, self.plot_start.z + self.structure_length, -1))
                structure = Structure(structure_start, self.structure_width, - self.structure_length)
            
            self.structure = structure

            self.structure_corners = []
            self.structure_corners.extend([ structure.frontleft,
                                            structure.frontright,
                                            structure.backleft,
                                            structure.backright])
            return structure
                

    def flatten_plot(self):
        #clears the space above the plot
        mc.setBlocks(   self.plot_start.x, self.plot_start.y + 1, self.plot_start.z,
                        self.plot_end.x, self.plot_end.y + 30, self.plot_end.z, block.AIR.id)
        
        #places floor
        for x in range(self.plot_start.x, self.plot_end.x +1):
            for z in range(self.plot_start.z, self.plot_end.z +1):
                y = self.central_point.y
                Plot.place_terraformed_block(x,y,z,self.block_dict[(x,z)])
                
    
    
                
    def terraform(self):
        self.flatten_plot()
        ###### most of the code blocks here are very similar,
        ###### but different enough so that there isnt an obvious and elegant way to condense them into repeating calls of one function with different parameters

        # terraforms the "-x" side of the plot
        x = self.plot_start.x
        for z in range(self.plot_start.z , self.plot_end.z + 1):
            y_diff = self.height_dict[(x-5,z)] - self.central_point.y
            
            interpolated = scale_sigmoid(0.5, 0.3, 6, y_diff, self.central_point.y)
        
            for x_interp in range(self.plot_start.x, self.plot_start.x - 5, -1):
                y = interpolated.pop(0)
                Plot.place_terraformed_block(x_interp,y,z,self.block_dict[(x_interp,z)])
                
                
        # terraforms the "+z" side of the plot
        z = self.plot_end.z
        for x in range(self.plot_start.x , self.plot_end.x + 1):
            y_diff = self.height_dict[(x,z + 5)] - self.central_point.y
            
            interpolated = scale_sigmoid(0.5, 0.3, 6, y_diff, self.central_point.y)
            
            for z_interp in range(self.plot_end.z, self.plot_end.z + 6):
                y = interpolated.pop(0)
                Plot.place_terraformed_block(x,y,z_interp,self.block_dict[(x,z_interp)])
        
        # terraforms the "+x" side of the plot
        x = self.plot_end.x
        for z in reversed(range(self.plot_start.z , self.plot_end.z + 1)):
            y_diff = self.height_dict[(x+5,z)] - self.central_point.y
            
            interpolated = scale_sigmoid(0.5, 0.3, 6, y_diff, self.central_point.y)
            
            for x_interp in range(self.plot_end.x, self.plot_end.x + 6):
                y = interpolated.pop(0)
                Plot.place_terraformed_block(x_interp,y,z,self.block_dict[(x_interp,z)])
        
        # terraforms the "-z" side of the plot
        z = self.plot_start.z
        for x in reversed(range(self.plot_start.x , self.plot_end.x + 1)):
            y_diff = self.height_dict[(x,z - 5)] - self.central_point.y
            
            interpolated = scale_sigmoid(0.5, 0.3, 6, y_diff, self.central_point.y)
            
            for z_interp in range(self.plot_start.z, self.plot_start.z - 6, -1):
                y = interpolated.pop(0)
                Plot.place_terraformed_block(x,y,z_interp,self.block_dict[(x,z_interp)])
        
        #interpolate corners
        #corner1
        #########
            ########## interpolate diagonally from plot corner to outer corner 
        xs = [x for x in reversed(range(self.plot_start.x - 3, self.plot_start.x + 2))] # shifted the range a little bit towards the plot
        zs = [z for z in reversed(range(self.plot_start.z - 3, self.plot_start.z + 2))] # to achieve rounded corners
        corner_coords  = [(xs[i],zs[i]) for i in range(5)]

        y_diff = self.height_dict[corner_coords[-1]] - self.central_point.y
        
        interpolated = scale_sigmoid(0.5, 0.5, 6, y_diff, self.central_point.y) # higher slope value to counteract diagonal length looking longer
        ybase_1, ybase_2 = interpolated[1], interpolated[2] # used for interpolating the rest of the corner
        
        for x,z in corner_coords:
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x,y,z,self.block_dict[(x,z)])
            ##########


        #interpolate from the corner diagonal to the plot buffer border
        x,z = corner_coords[1]
            #########
        y_diff = self.height_dict[x,z-3] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5, y_diff, ybase_1)

        for z_interp in range(z, z - 4, -1):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x,y,z_interp,self.block_dict[(x,z_interp)])

        y_diff = self.height_dict[x-3,z] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5    , y_diff, ybase_1)

        for x_interp in range(x, x - 4, -1):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x_interp,y,z,self.block_dict[(x_interp,z)])
            ########
        x,z = corner_coords[2]

        y_diff = self.height_dict[x,z-2] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for z_interp in range(z, z - 3, -1):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x,y,z_interp,self.block_dict[(x,z_interp)])

        y_diff = self.height_dict[x-2,z] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for x_interp in range(x, x - 3, -1):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x_interp,y,z,self.block_dict[(x_interp,z)])
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
            Plot.place_terraformed_block(x,y,z,self.block_dict[(x,z)])
            ##########


        #interpolate from the corner diagonal to the plot buffer border
        x,z = corner_coords[1]
            #########
        y_diff = self.height_dict[x,z-3] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5, y_diff, ybase_1)

        for z_interp in range(z, z - 4, -1):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x,y,z_interp,self.block_dict[(x,z_interp)])

        y_diff = self.height_dict[x+3,z] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5    , y_diff, ybase_1)

        for x_interp in range(x, x + 4):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x_interp,y,z,self.block_dict[(x_interp,z)])
            ########
        x,z = corner_coords[2]

        y_diff = self.height_dict[x,z-2] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for z_interp in range(z, z - 3, -1):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x,y,z_interp,self.block_dict[(x,z_interp)])

        y_diff = self.height_dict[x+2,z] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for x_interp in range(x, x + 3):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x_interp,y,z,self.block_dict[(x_interp,z)])
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
            Plot.place_terraformed_block(x,y,z,self.block_dict[(x,z)])
            ##########


        #interpolate from the corner diagonal to the plot buffer border
        x,z = corner_coords[1]
            #########
        y_diff = self.height_dict[x,z+3] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5, y_diff, ybase_1)

        for z_interp in range(z, z + 4):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x,y,z_interp,self.block_dict[(x,z_interp)])

        y_diff = self.height_dict[x+3,z] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5    , y_diff, ybase_1)

        for x_interp in range(x, x + 4):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x_interp,y,z,self.block_dict[(x_interp,z)])
            ########
        x,z = corner_coords[2]

        y_diff = self.height_dict[x,z+2] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for z_interp in range(z, z + 3):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x,y,z_interp,self.block_dict[(x,z_interp)])

        y_diff = self.height_dict[x+2,z] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for x_interp in range(x, x + 3):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x_interp,y,z,self.block_dict[(x_interp,z)])
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
            Plot.place_terraformed_block(x,y,z,self.block_dict[(x,z)])
            ##########


        #interpolate from the corner diagonal to the plot buffer border
        x,z = corner_coords[1]
            #########
        y_diff = self.height_dict[x,z+3] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5, y_diff, ybase_1)

        for z_interp in range(z, z + 4):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x,y,z_interp,self.block_dict[(x,z_interp)])

        y_diff = self.height_dict[x-3,z] - ybase_1

        interpolated = scale_sigmoid(0.5, 0.3, 5    , y_diff, ybase_1)

        for x_interp in range(x, x - 4, -1):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x_interp,y,z,self.block_dict[(x_interp,z)])
            ########
        x,z = corner_coords[2]

        y_diff = self.height_dict[x,z+2] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for z_interp in range(z, z + 3):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x,y,z_interp,self.block_dict[(x,z_interp)])

        y_diff = self.height_dict[x-2,z] - ybase_2

        interpolated = scale_sigmoid(0.5, 0.3, 4, y_diff, ybase_2)

        for x_interp in range(x, x - 3, -1):
            y = interpolated.pop(0)
            Plot.place_terraformed_block(x_interp,y,z,self.block_dict[(x_interp,z)])
            ##########
        ########

    def place_terraformed_block(x,y,z,block_id):
        water_blocks = [block.WATER.id, block.WATER_FLOWING.id, block.WATER_STATIONARY.id]
        mc.setBlocks(       x, y + 1,   z,
                            x, y + 21,  z, block.AIR.id)

        if block_id in water_blocks:
            mc.setBlock(   x, y,       z, block.WATER_STATIONARY.id)
        else:
            mc.setBlocks(   x, y - 20,  z,
                            x, y,       z, block_id)

    def place_house(self, structure):
        house = House(structure)
        house.create_house(mc)
        self.house_door = house.front_door
        return house.front_door

    def connect_with_paths(self,path_coords, intersection_coords, bordering_paths, vil_start, vil_end):
        # starting from 2 blocks after the front door, travel facing self.direction until it connects to a path block. 
        # add the connection as an intersection, then add the new path connection to the path blocks list
        # if the front door is outside of the village area, connect to the nearest block in bordering_paths in terms of the self.direction axis.
        connection = []
        if self.direction == 'x-':
            new_path = Vec3(self.house_door.x, 0, self.house_door.z -2) # starting point
            front_door_path = Vec3(self.house_door.x, 0, self.house_door.z -2)
            connection.append(new_path)
            intersection_coords.append(new_path)

            loop_counter = 0
            temp_new_path = Vec3(self.house_door.x, 0, self.house_door.z -2)
            no_path_ahead = False
            while temp_new_path not in path_coords: #checks if theres a path ahead
                temp_new_path = Vec3(temp_new_path.x - 1, 0,  temp_new_path.z)
                loop_counter+= 1
                if loop_counter == 200:
                    no_path_ahead = True
                    break

            if Plot.out_of_range(new_path, vil_start, vil_end) or no_path_ahead:
                nearest = Plot.find_nearest_bordering_paths(new_path,
                                    [coord for coord in bordering_paths if coord.z == vil_end.z or coord.z == vil_start.z])
                                    # makes sure that nearest is on the same side of the border

                if new_path.x < nearest.x:
                    dir = 1
                else:
                    dir = -1

                while new_path.x != nearest.x:
                    new_path = Vec3(new_path.x + dir, 0, new_path.z)
                    connection.append(new_path)

                if nearest.z > new_path.z:
                    for z in range(new_path.z, nearest.z + 1):
                        connection.append(Vec3(new_path.x, 0, z))
        
                else:
                    for z in range(nearest.z, new_path.z + 1):
                        connection.append(Vec3(new_path.x, 0, z))
                intersection_coords.append(nearest)

            else:
                while new_path not in path_coords:
                    new_path = Vec3(new_path.x - 1, 0,  new_path.z)
                    connection.append(new_path)
                else:
                    while new_path in path_coords:
                        intersection_coords.append(new_path)
                        new_path = Vec3(new_path.x - 1, 0,  new_path.z)
                    

        elif self.direction =='x+':
            new_path = Vec3(self.house_door.x, 0, self.house_door.z +2) # starting point
            front_door_path = Vec3(self.house_door.x, 0, self.house_door.z +2)
            connection.append(new_path)
            intersection_coords.append(new_path)

            loop_counter = 0
            temp_new_path = Vec3(self.house_door.x, 0, self.house_door.z +2)
            no_path_ahead = False
            while temp_new_path not in path_coords: #checks if theres a path ahead
                temp_new_path = Vec3(temp_new_path.x + 1, 0,  temp_new_path.z)
                loop_counter+= 1
                if loop_counter == 200:
                    no_path_ahead = True
                    break

            if Plot.out_of_range(new_path, vil_start, vil_end) or no_path_ahead:
                nearest = Plot.find_nearest_bordering_paths(new_path,
                                    [coord for coord in bordering_paths if coord.z == vil_end.z or coord.z == vil_start.z])

                if new_path.x < nearest.x:
                    dir = 1
                else:
                    dir = -1

                while new_path.x != nearest.x:
                    new_path = Vec3(new_path.x + dir, 0, new_path.z)
                    connection.append(new_path)

                if nearest.z > new_path.z:
                    for z in range(new_path.z, nearest.z + 1):
                        connection.append(Vec3(new_path.x, 0, z))
    
                else:
                    for z in range(nearest.z, new_path.z + 1):
                        connection.append(Vec3(new_path.x, 0, z))
                intersection_coords.append(nearest)


            else:
                while new_path not in path_coords: # infinite loops here very frequently
                    new_path = Vec3(new_path.x + 1, 0,  new_path.z)
                    connection.append(new_path)
                else:
                    while new_path in path_coords:
                        intersection_coords.append(new_path)
                        new_path = Vec3(new_path.x + 1, 0,  new_path.z)


        elif self.direction =='z-':
            new_path = Vec3(self.house_door.x, 0, self.house_door.z -2) # starting point
            front_door_path = Vec3(self.house_door.x, 0, self.house_door.z -2)
            connection.append(new_path)
            intersection_coords.append(new_path)

            loop_counter = 0
            temp_new_path = Vec3(self.house_door.x, 0, self.house_door.z -2)
            no_path_ahead = False
            while temp_new_path not in path_coords: #checks if theres a path ahead
                temp_new_path = Vec3(temp_new_path.x, 0,  temp_new_path.z - 1)
                loop_counter+= 1
                if loop_counter == 200:
                    no_path_ahead = True
                    break

            if Plot.out_of_range(new_path, vil_start, vil_end) or no_path_ahead:
                nearest = Plot.find_nearest_bordering_paths(new_path,
                                    [coord for coord in bordering_paths if coord.x == vil_end.x or coord.x == vil_start.x])

                if new_path.z < nearest.z:
                    dir = 1
                else:
                    dir = -1

                while new_path.z != nearest.z:
                    new_path = Vec3(new_path.x, 0, new_path.z + dir)
                    connection.append(new_path)

                if nearest.x > new_path.x:
                    for x in range(new_path.x, nearest.x + 1):
                        connection.append(Vec3(x, 0, new_path.z))
            
                else:
                    for x in range(nearest.x, new_path.x + 1):
                        connection.append(Vec3(x, 0, new_path.z))
                intersection_coords.append(nearest)
            else:
                while new_path not in path_coords:
                    new_path = Vec3(new_path.x, 0,  new_path.z - 1)
                    connection.append(new_path)
                else:
                    while new_path in path_coords:
                        intersection_coords.append(new_path)
                        new_path = Vec3(new_path.x, 0,  new_path.z - 1)


        elif self.direction =='z+':
            new_path = Vec3(self.house_door.x, 0, self.house_door.z +2) # starting point
            front_door_path = Vec3(self.house_door.x, 0, self.house_door.z +2)
            connection.append(new_path)
            intersection_coords.append(new_path)
            
            loop_counter = 0
            temp_new_path = Vec3(self.house_door.x, 0, self.house_door.z +2)
            no_path_ahead = False
            while temp_new_path not in path_coords: #checks if theres a path ahead
                temp_new_path = Vec3(temp_new_path.x, 0,  temp_new_path.z + 1)
                loop_counter+= 1
                if loop_counter == 200:
                    no_path_ahead = True
                    break

            if Plot.out_of_range(new_path, vil_start, vil_end) or no_path_ahead:
                nearest = Plot.find_nearest_bordering_paths(new_path,
                                    [coord for coord in bordering_paths if coord.x == vil_end.x or coord.x == vil_start.x])

                if new_path.z < nearest.z:
                    dir = 1
                else:
                    dir = -1
                
                while new_path.z != nearest.z:
    
                    new_path = Vec3(new_path.x, 0, new_path.z + dir)
                    connection.append(new_path)

                if nearest.x > new_path.x:
                    for x in range(new_path.x, nearest.x + 1):
                        connection.append(Vec3(x, 0, new_path.z))

                else:
                    for x in range(nearest.x, new_path.x + 1):
                        connection.append(Vec3(x, 0, new_path.z))
                intersection_coords.append(nearest)
                
    
            else:
                while new_path not in path_coords:
                    new_path = Vec3(new_path.x, 0,  new_path.z + 1)
                    connection.append(new_path)
                else:
                    while new_path in path_coords:
                        intersection_coords.append(new_path)
                        new_path = Vec3(new_path.x, 0,  new_path.z + 1)

        path_coords.extend(connection)
        intersection_coords.extend(connection)

        front_door_path = Vec3(front_door_path.x, self.central_point.y, front_door_path.z)
        return front_door_path


    def out_of_range(starting_point, vil_start, vil_end):
        """function for connect_with_paths()"""
        x_out_of_range = starting_point.x <= vil_start.x or starting_point.x >= vil_end.x
        z_out_of_range = starting_point.z <= vil_start.z or starting_point.z >= vil_end.z

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
    test_plot.place_house(test_plot.get_structure())