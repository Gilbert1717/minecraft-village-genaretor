from models.Structure import *
from mcpi.vec3 import Vec3
from mcpi import block

from RandomiseMaterial import RandomiseMaterial
import random
import math

rm = RandomiseMaterial()

def create_blocks(mc, start_point, end_point, material = rm.random_exterior(), color = 3):
    start_x = start_point.x
    start_y = start_point.y
    start_z = start_point.z
    end_x = end_point.x
    end_y = end_point.y
    end_z = end_point.z
    mc.setBlocks(start_x, start_y, start_z, end_x, end_y, end_z, material ,color)


def create_door(mc,vector1,vector2):
    Air = 0
    window_block = 95
    door = 64
    #  On horizontal wall
    if vector1.x == vector2.x:
        length = abs(vector2.z - vector1.z)
        if vector2.z > vector1.z:
            create_z = vector1.z + random.randint(3,length - 3)
            # check if the randomised coordinate is suitable for placing a door
            while (mc.getBlock(vector1.x + 1, vector1.y + 2, create_z) != Air or
                    mc.getBlock(vector1.x - 1, vector1.y + 2, create_z ) != Air or
                    mc.getBlock(vector1.x, vector1.y + 2, create_z) == window_block):
                create_z = vector1.z + random.randint(3,length - 3)
            
        else:
            create_z = vector1.z - random.randint(3,length - 3)
            # check if the randomised coordinate is suitable for placing a door
            while (mc.getBlock(vector1.x + 1, vector1.y + 2, create_z) != Air or
                    mc.getBlock(vector1.x - 1, vector1.y + 2, create_z) != Air or
                    mc.getBlock(vector1.x, vector1.y + 2, create_z) == window_block):
                create_z = vector1.z - random.randint(3,length - 3)
        # Place the door on room's wall
        mc.setBlock(vector1.x, vector1.y + 1, create_z, block.AIR)
        mc.setBlock(vector1.x, vector1.y + 2, create_z, block.AIR)
        mc.setBlock(vector1.x, vector1.y + 2, create_z,door,8)
        mc.setBlock(vector1.x , vector1.y + 1, create_z,door,0)
        return Vec3(vector1.x,vector1.y,create_z)
         
    #  On vertical wall
    elif vector1.z == vector2.z:
        width = abs(vector2.x - vector1.x)
        if vector2.x > vector1.x:
            create_x = vector1.x + random.randint(2,width - 2)
            while (mc.getBlock(create_x, vector1.y + 2, vector1.z + 1) != Air or
                    mc.getBlock(create_x, vector1.y + 2, vector1.z - 1) != Air or 
                    mc.getBlock(create_x, vector1.y + 2, vector1.z) == window_block):
                create_x = vector1.x + random.randint(2,width - 2)
                
               
            
        else:
            create_x = vector1.x - random.randint(2,width - 2)
            while (mc.getBlock(create_x, vector1.y + 2, vector1.z + 1) != Air or
                    mc.getBlock(create_x, vector1.y + 2, vector1.z - 1) != Air or
                    mc.getBlock(create_x, vector1.y + 2, vector1.z) != window_block):
                create_x = vector1.x - random.randint(2,width - 2)
               
                
        mc.setBlock(create_x, vector1.y + 1, vector1.z, block.AIR)
        mc.setBlock(create_x, vector1.y + 2, vector1.z, block.AIR)
        mc.setBlock(create_x , vector1.y + 2, vector1.z,door,8)
        mc.setBlock(create_x , vector1.y + 1, vector1.z,door,0)
        return Vec3(create_x,vector1.y,vector1.z)
        
        

class Floor:
    def __init__ (self, structure,storey):
        y = structure.position.y + structure.height * storey
        self.storey = storey
        self.structure = structure
        # Room list restore all the floor instance created in the create_rooms function
        self.rooms = []
        self.frontleft = Vec3(structure.frontleft.x,
                                y,
                                structure.frontleft.z)
        self.frontright = Vec3(structure.frontright.x,
                                y,
                                structure.frontright.z)
        self.backleft = Vec3(structure.backleft.x,
                                y,
                                structure.backleft.z)
        self.backright = Vec3(structure.backright.x,
                                y,
                                structure.backright.z)

    # split the floor into 2 small floors by choosing a position on x-axis
    def split_horizontal(self,split_point):
        """
        Use this method to ...
        """
        width = split_point - 1
        structure1 = Structure(self.structure.position, width, self.structure.length)
        structure2_position = create_vector(self.structure.position,split_point,0,0)
        structure2 = Structure(structure2_position, self.structure.width - split_point, self.structure.length)
        floor1 = Floor(structure1,self.storey)
        floor2 = Floor(structure2,self.storey)
        return floor1, floor2

    # split the floor into 2 small floors by choosing a position on z-axis
    def split_vertical(self,split_point):
        if self.structure.length < 0:
            length = split_point + 1
        else:
            length = split_point - 1
        structure1 = Structure(self.structure.position, self.structure.width, length)
        structure2_position = create_vector(self.structure.position,0,0,split_point)
        structure2 = Structure(structure2_position, self.structure.width, self.structure.length - split_point)
        floor1 = Floor(structure1,self.storey)
        floor2 = Floor(structure2,self.storey)
        return floor1, floor2

    


    # waiting to fix --- could not add room into self.rooms properly
    def create_room(self,mc,floor,rooms = None, material = 1,color = 1): 
        """
           keep spliting the floor until room length or width less than 6(or random stop number == 0 to stop the function) 
            add the small floors into the list self.rooms
        """
        min_room_length = 6
        min_room_width = 6
        if rooms is None:
            rooms = self.rooms
        if abs(floor.structure.width) > min_room_width and abs(floor.structure.length) > min_room_length:           
            if abs(floor.structure.width) >= abs(floor.structure.length):
                split = random.randrange(math.floor(floor.structure.width/2),floor.structure.width - min_room_width//2,1) 
                floor1,floor2 = floor.split_horizontal(split)
                diagonal_point = create_vector(floor1.frontright, 0, floor.structure.height - 1, floor.structure.length)
                create_blocks(mc, floor1.frontright, diagonal_point)
                McPosition1 = floor1.frontright
                McPosition2 = floor1.backright
                # resurion will randomly stop if stop equals 0 so house will contain some big rooms
                stop = random.randint(0,3)
                if stop != 0:
                    floor1.create_room(mc,floor1,rooms)
                    floor2.create_room(mc,floor2,rooms)
                else:
                    rooms.append(floor1)
                    rooms.append(floor2)
                create_door(mc,McPosition1,McPosition2)
            else:
                if floor.structure.length < 0:
                    split = random.randint(floor.structure.length + min_room_length//2, math.ceil(floor.structure.length/2))
                else:
                    split = random.randrange(int(floor.structure.length/2),floor.structure.length - min_room_length//2)
                floor1,floor2 = floor.split_vertical(split)
                diagonal_point = create_vector(floor1.backleft, floor.structure.width, floor.structure.height - 1, 0)
                create_blocks(mc, floor1.backleft, diagonal_point)
                McPosition1 = floor1.backleft
                McPosition2 = floor1.backright
                # resurion will randomly stop if stop equals 0 so house will contain some big rooms
                stop = random.randint(0,3)
                if stop != 0:        
                    floor1.create_room(mc,floor1,rooms)
                    floor2.create_room(mc,floor2,rooms)
                else:
                    rooms.append(floor1)
                    rooms.append(floor2)
                create_door(mc,McPosition1,McPosition2)
        else:
            rooms.append(floor)
            
        
    
    def create_window(self,mc,floor):
        # create window on front wall
        window = 95
        if floor.frontleft.z == self.frontleft.z:
            wall_width = abs(floor.frontright.x - floor.frontleft.x)
            
            if floor.structure.length < 0:
                x_offset = math.floor(wall_width/2)
            else:
                x_offset = math.ceil(wall_width/2)
            
            window_x = floor.frontleft.x + x_offset
            window_y = floor.frontleft.y + 2
            window_z = floor.frontleft.z
            
            # validate the width 
            if abs(wall_width) <= 3:
                # if the width is not long enough, window_width will be 1 block
                window_width = window_x
            else:
                # if the width is long enough, window_width will be 2 blocks
                window_width = window_x + 1
            window_height = window_y + 1
            mc.setBlocks (window_x,window_y,window_z,
                        window_width,window_height,window_z,
                        window)

        # create window on back wall
        if floor.backleft.z == self.backleft.z:
            wall_width = abs(floor.backleft.x - floor.backright.x)
            x_offset = math.ceil(wall_width/2)
            window_x = floor.frontleft.x + x_offset
            window_y = floor.backleft.y + 2
            window_z = floor.backleft.z   
            if wall_width <= 3:
                # if the width is not long enought, window_width will be 1 block
                window_width = window_x
            else:
                # if the width is enought, window_width will be 2 blocks
                window_width = window_x + 1
            window_height = window_y + 1
            mc.setBlocks (window_x,window_y,window_z,
                        window_width,window_height,window_z,
                        window)
        
        # create window on left-side wall
        if floor.frontleft.x == self.frontleft.x:
            wall_width = abs(floor.frontright.z - floor.backright.z)/2
            if floor.structure.length < 0:
                z_offset = -math.ceil(wall_width/2)
            else:
                z_offset = math.floor(wall_width/2)

            window_x = floor.frontleft.x
            window_y = floor.frontleft.y + 2
            window_z = floor.frontleft.z + z_offset
            
            if wall_width <= 3:
                # if the width is not long enought, window_width will be 1 block
                 window_width = window_z
            else:
                # if the width is enought, window_width will be 2 blocks
                window_width = window_z + 1
           
            window_height = window_y + 1
            mc.setBlocks (window_x,window_y,window_z,
                            window_x,window_height,window_width,
                            window)

        # create window on right-side wall
        if floor.frontright.x == self.frontright.x:
            wall_width = abs(floor.frontright.z - floor.backright.z)/2
            if floor.structure.length < 0:
                z_offset = -math.ceil(wall_width/2)
            else:
                z_offset = math.floor(wall_width/2)
            window_x = floor.frontright.x
            window_y = floor.frontright.y + 2
            window_z = floor.frontright.z + z_offset
            if wall_width <= 3:
                # if the width is not long enought, window_width will be 1 block
                 window_width = window_z
            else:
                # if the width is enought, window_width will be 2 blocks
                window_width = window_z + 1
            window_height = window_y + 1
            mc.setBlocks (window_x,window_y,window_z,
                            window_x,window_height,window_width,
                            window)


       

    def create_stair(self,mc):
        stairs = block.STAIRS_WOOD.id
        support = block.WOOD.id
        if self.structure.length > 0:
            

            # clear the blocks right in front of stairs
            start_vector = create_vector(self.backleft, self.structure.height + 2,  1, -1)
            end_vector = create_vector(start_vector, 0, self.structure.height - 2, -1)
            create_blocks(mc,start_vector,end_vector,block.AIR)

            # create stairs
            for x in range(self.structure.height):
                vector1 = create_vector(self.backleft,self.structure.height - x + 1, x + 1 , -1)
                vector2 = create_vector(self.backleft,self.structure.height - x + 1, x + 1, -2)
                mc.setBlock(vector1.x,vector1.y,vector1.z,stairs,1)
                mc.setBlock(vector1.x,vector1.y - 1,vector1.z,support,1)
                mc.setBlock(vector2.x,vector2.y,vector2.z,stairs,1)
                mc.setBlock(vector2.x,vector2.y - 1,vector2.z,support,1)
        else:

            # clear the blocks right in front of stairs
            start_vector = create_vector(self.backleft, self.structure.height + 2,  1, 1)
            end_vector = create_vector(start_vector, 0, self.structure.height - 2, 1)
            create_blocks(mc,start_vector,end_vector,block.AIR)
            

            for x in range(self.structure.height):
                vector1 = create_vector(self.backleft,self.structure.height - x + 1, x + 1 , 1)
                vector2 = create_vector(self.backleft,self.structure.height - x + 1, x + 1, 2)
                mc.setBlock(vector1.x,vector1.y,vector1.z,stairs,1)
                mc.setBlock(vector1.x,vector1.y - 1,vector1.z,support,1)
                mc.setBlock(vector2.x,vector2.y,vector2.z,stairs,1)
                mc.setBlock(vector2.x,vector2.y - 1,vector2.z,support,1)
                
                
    def place_furniture(self, mc, floor):
        
        # Choosing furniture material
        furniture = rm.random_furniture()
        
        # Initialising door block.
        door = 64
        
        # Grabbing the coordinates of the block facing the negative z-direction.
        negative_z = Vec3(self.structure.frontleft.x, self.structure.frontleft.y + self.structure.height, self.structure.frontleft.z - 1)
        check_negativeBlock= mc.getBlock(negative_z)
        
        
        # If the block is facing the -z direction, place furniture blocks accordingly
        if check_negativeBlock == block.AIR.id:
            
            if floor.frontleft.x + 1 == floor.frontright.x - 1:
                
                place_frontwall = floor.frontleft.x
                check_door = mc.getBlock(place_frontwall, floor.frontleft.y + 1, floor.frontleft.z - 1, furniture)
                
                if check_door == door:
                    mc.setBlock(place_frontwall, floor.frontleft.y + 1, floor.frontleft.z - 2, furniture)
                
                else:
                    mc.setBlock(place_frontwall, floor.frontleft.y + 1, floor.frontleft.z - 1, furniture)
                    
            else:
                
                #Pick a block in between the length of the walls
                place_frontwall = random.randrange(floor.frontleft.x + 1, floor.frontright.x - 1)
                check_door = mc.getBlock(place_frontwall, floor.frontleft.y + 1, floor.frontleft.z + 1, furniture)
                
                
                if check_door == door:
                    mc.setBlock(place_frontwall, floor.frontleft.y + 1, floor.frontleft.z + 2, furniture)
                    
                else:
                    mc.setBlock(place_frontwall, floor.frontleft.y + 1, floor.frontleft.z + 1, furniture)
                print("placing furniture for negative z direction")


        # Else the block is facing the +z direction, place furniture blocks accordingly
        else:
            
            #Pick a block in between the length of the walls
            if floor.frontleft.x + 1 == floor.frontright.x - 1:
                place_frontwall = floor.frontleft.x
                check_door = mc.getBlock(place_frontwall, floor.frontleft.y + 1, floor.frontleft.z - 1, furniture)
                
                if check_door == door:
                    mc.setBlock(place_frontwall, floor.frontleft.y + 1, floor.frontleft.z - 2, furniture)
                
                else:
                    mc.setBlock(place_frontwall, floor.frontleft.y + 1, floor.frontleft.z - 1, furniture)
                    
            
            else:
                
                place_frontwall = random.randrange(floor.frontleft.x + 1, floor.frontright.x - 1)
                check_door = mc.getBlock(place_frontwall, floor.frontleft.y + 1, floor.frontleft.z - 1, furniture)
                
                
                if check_door == door:
                    mc.setBlock(place_frontwall, floor.frontleft.y + 1, floor.frontleft.z - 2, furniture)
                    
                else:
                    mc.setBlock(place_frontwall, floor.frontleft.y + 1, floor.frontleft.z - 1, furniture)
                    
                print("placing furniture for positive z direction")
            
            
                
            
            

