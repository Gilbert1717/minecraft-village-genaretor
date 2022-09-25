from tracemalloc import start
from mcpi.minecraft import Minecraft
from mcpi import block
from models.Floor import *
from mcpi import vec3
from RandomiseMaterial import RandomiseMaterial
import random 
import math
from fast_query_and_interpolation.mcpi_query_performance import query_blocks

rm = RandomiseMaterial()



class House:
    def __init__ (self,structure):
        self.structure = structure
        # randomly make the stories of the house between 1 to 6
        self.stories = random.randint(1,5)
        self.height = structure.height * self.stories
        # Floor list restore all the floor instance in the house
        self.floors = []
        self.front_door = None

        
    
    def create_floor(self, mc: Minecraft):
        material = rm.random_floors()
        colour = random.randint(1,3)
        
        for storey in range(self.stories):
            structure = self.structure
            floor = Floor(structure, storey)
            create_blocks(mc, floor.frontleft, floor.backright, material, colour)
            
        self.create_lighting(mc)
        
        
    def create_lighting(self, mc: Minecraft):
        
        if self.structure.length > 0 :
            lightBlock_offset_z = random.randint(2, 3)
            
        else:
            lightBlock_offset_z = random.randint(-3, -2)
        lightBlock_offset_x = random.randint(2, 3)


        for storey in range(self.stories):
            
            structure = self.structure
            floor = Floor(structure, storey)
            
            
            #CREATING LIGHTING FOR BASE FLOOR BY ITERATING THROUGH ROW AND COLUMN
            for i in range(floor.frontleft.x, floor.backright.x, lightBlock_offset_x): 
                block_difference_x = i - floor.frontleft.x # Setting the offset position to place glowstone on the row
                for z in range(floor.frontleft.z, floor.backright.z, lightBlock_offset_z): 
                    block_difference_z = z - floor.frontleft.z # Setting the offset position to place glowstone on column
                    mc.setBlock(floor.frontleft.x + block_difference_x, floor.frontleft.y,
                                floor.frontleft.z + block_difference_z, block.GLOWSTONE_BLOCK.id)
                    
                    
            # CREATING LIGHTING FOR OTHER STORIES, ITERATING THROUGH ROWS AND COLUMNS
            for i in range(floor.frontleft.x, floor.backright.x, lightBlock_offset_x): 
                block_difference_x = i - floor.frontleft.x # Setting the offset position to place glowstone on the row
                for z in range(floor.frontleft.z, floor.backright.z, lightBlock_offset_z): 
                    block_difference_z = z - floor.frontleft.z # Setting the offset position to place glowstone on column
                    mc.setBlock(floor.frontleft.x + block_difference_x, floor.frontleft.y + self.structure.height,
                                floor.frontleft.z + block_difference_z, block.GLOWSTONE_BLOCK.id)
                    
            self.floors.append(floor)


    def create_rooms(self,mc):
        for floor in self.floors:
            floor.create_room(mc,floor)
    
    def create_stairs(self,mc):
        if self.structure.length < 0:
            start_vector = create_vector(self.structure.backleft, 2,  1, 1)
            end_vector = create_vector(self.structure.backleft,self.structure.height + 1, self.height - 1, 2)
            create_blocks(mc,start_vector, end_vector, block.AIR)
        else:
            start_vector = create_vector(self.structure.backleft, 2,  1, -1)
            end_vector = create_vector(self.structure.backleft,self.structure.height + 1, self.height - 1, -2)
            create_blocks(mc,start_vector, end_vector, block.AIR)
        for floor in self.floors:
            if self.stories > 1 and floor.storey < self.stories - 1:
                floor.create_stair(mc)
            

    def create_roof(self,mc):
        
        # Creates the ceiling of the house
        start_point = vec3.Vec3(self.structure.frontleft.x,
                                self.structure.frontleft.y + self.structure.height * self.stories, 
                                self.structure.frontleft.z)
        end_point = vec3.Vec3(self.structure.backright.x,
                                self.structure.backright.y + self.structure.height * self.stories, 
                                self.structure.backright.z)
        create_blocks(mc, start_point, end_point)
        

        # Grabbing the coordinates of the block facing the negative z-direction.
        negative_z = Vec3(self.structure.frontleft.x, self.structure.frontleft.y + self.structure.height * self.stories + 1, self.structure.frontleft.z - 1)
        check_negativeBlock = mc.getBlock(negative_z)
        
        
        # Choosing which rooftype to give the house
        roofType = random.randint(0, 1)
        
        
        # If roofType = 0, create a rooftop with stairs.
        if roofType == 0:
            
            # Initialises the start point and end point for roofType 0. For Right and Left.
            start_pointLeft = vec3.Vec3(self.structure.frontleft.x,
                                self.structure.frontleft.y + self.structure.height * self.stories, 
                                self.structure.frontleft.z)
            end_pointLeft = vec3.Vec3(self.structure.backleft.x,
                                self.structure.backleft.y + self.structure.height * self.stories, 
                                self.structure.backleft.z)


            start_pointRight = vec3.Vec3(self.structure.frontright.x,
                                self.structure.frontright.y + self.structure.height * self.stories, 
                                self.structure.frontright.z)
            
            end_pointRight = vec3.Vec3(self.structure.backright.x,
                                self.structure.backright.y + self.structure.height * self.stories, 
                                self.structure.backright.z)
            
            
            
            # Creating the blocks placed underneath stairs for Right and Left.
            block_startLeft = vec3.Vec3(self.structure.frontleft.x,
                                self.structure.frontleft.y + self.structure.height * self.stories, 
                                self.structure.frontleft.z)
            block_endLeft = vec3.Vec3(self.structure.backleft.x,
                                self.structure.backleft.y + self.structure.height * self.stories, 
                                self.structure.backleft.z)
            
            
            block_startRight = vec3.Vec3(self.structure.frontright.x,
                                self.structure.frontright.y + self.structure.height * self.stories, 
                                self.structure.frontright.z)
            
            block_endRight = vec3.Vec3(self.structure.backright.x,
                                self.structure.backright.y + self.structure.height * self.stories, 
                                self.structure.backright.z)
            
            

            # Raising the height to be above the ceiling for proper stair placement.
            start_pointLeft.y += 1
            end_pointLeft.y += 1
            
            start_pointRight.y += 1
            end_pointRight.y += 1

            
            # Implements house facing the -z direction.
            if check_negativeBlock == block.AIR.id:
                
                # Creating roof structure at the base
                create_blocks(mc, start_pointLeft, end_pointLeft, block.STAIRS_COBBLESTONE.withData(0))
                create_blocks(mc, start_pointRight, end_pointRight, block.STAIRS_COBBLESTONE.withData(1))
                
                
                # Find the midpoint to see how many times we need to iterate to complete the roof.
                midpoint = math.ceil(self.structure.width / 2)
                
                
                # If the width is even, the middle will be empty. So we will fill it with blocks.
                if (self.structure.width % 2) == 0:
                    roof_midpoint = self.structure.frontleft.x + midpoint
                    
                    mc.setBlocks(roof_midpoint, self.structure.frontleft.y + self.structure.height * self.stories, self.structure.frontleft.z,
                                roof_midpoint, self.structure.backleft.y + self.structure.height * self.stories + midpoint, self.structure.backleft.z,
                                block.STONE_BRICK.withData(2))
                    
                    
                # Creating stairs facing east for the left half of the house.
                for minusEast in range(1, midpoint):
                    
                    start_pointLeft.x += 1
                    start_pointLeft.y += 1
                    
                    end_pointLeft.x += 1
                    end_pointLeft.y += 1
                    
                    block_startLeft.x += 1
                    
                    block_endLeft.x += 1
                    block_endLeft.y += 1
                    
                    create_blocks(mc, start_pointLeft, end_pointLeft, block.STAIRS_COBBLESTONE.withData(0))
                    create_blocks(mc, block_startLeft, block_endLeft, block.STONE_BRICK.withData(2))
                    
                    
                # Creating stairs facing west for the right half of the house.
                for minusWest in range(1, midpoint):
                    
                    start_pointRight.x -= 1
                    start_pointRight.y += 1
                    
                    end_pointRight.x -= 1
                    end_pointRight.y += 1
                    
                    block_startRight.x -= 1
                    
                    block_endRight.x -= 1
                    block_endRight.y += 1
                    
                    create_blocks(mc, start_pointRight, end_pointRight, block.STAIRS_COBBLESTONE.withData(1))
                    create_blocks(mc, block_startRight, block_endRight, block.STONE_BRICK.withData(2))
            
            
            # Else implement house correctly, if it is facing the positive z direction.
            else:
                 
                 # Creating roof structure at the base
                create_blocks(mc, start_pointLeft, end_pointLeft, block.STAIRS_COBBLESTONE.withData(0))
                create_blocks(mc, start_pointRight, end_pointRight, block.STAIRS_COBBLESTONE.withData(1))
                
                
                # Find midpoint to see how many iterations are required to fill in the roof.
                midpoint = math.ceil(self.structure.width / 2)
                
                
                # If the width is even, the middle will be empty. So we will fill it with blocks.
                if (self.structure.width % 2) == 0:
                    roof_midpoint = self.structure.frontleft.x + midpoint
                    
                    mc.setBlocks(roof_midpoint, self.structure.frontleft.y + self.structure.height * self.stories, self.structure.frontleft.z,
                                roof_midpoint, self.structure.backleft.y + self.structure.height * self.stories + midpoint, self.structure.backleft.z,
                                block.STONE_BRICK.withData(2))
                
                
                # Create stairs facing the east direction
                for positiveEast in range(1, midpoint):
                    
                    start_pointLeft.x -= 1
                    start_pointLeft.y += 1
                    
                    end_pointLeft.x -= 1
                    end_pointLeft.y += 1
                    
                    block_startLeft.x -= 1
                    
                    block_endLeft.x -= 1
                    block_endLeft.y += 1

                    create_blocks(mc, start_pointLeft, end_pointLeft, block.STAIRS_COBBLESTONE.withData(0))
                    create_blocks(mc, block_startLeft, block_endLeft, block.STONE_BRICK.withData(2))
                    
                    
                # Create stairs facing the west direction
                for positiveWest in range(1, midpoint):
                    
                    start_pointLeft.x += 1
                    start_pointRight.y += 1
                    
                    end_pointLeft.x += 1
                    end_pointLeft.y += 1
                    
                    block_startLeft.x += 1
                    
                    block_endLeft.x += 1
                    block_endLeft.y += 1

                    create_blocks(mc, start_pointLeft, end_pointLeft, block.STAIRS_COBBLESTONE.withData(0))
                    create_blocks(mc, block_startLeft, block_endLeft, block.STONE_BRICK.withData(2))
                
                
                
        # Creating block roof
        elif roofType == 1:
            
            # Setting the foundation and raising blocks from the ceiling to the surface.
            start_point.y += 1
            create_blocks(mc, start_point, end_point, block.COBBLESTONE.id)
            
            
            # Grabbing the coordinates of the block facing the negative z-direction.
            negative_z = Vec3(self.structure.frontleft.x, self.structure.frontleft.y + self.structure.height * self.stories + 1, self.structure.frontleft.z - 1)
            check_negativeBlock = mc.getBlock(negative_z)
        
        
            # Creating the roof structure on top of the house, placing the blocks accordingly depending on if it is facing -z or +z direction.
            if check_negativeBlock == block.AIR.id:
            
                # Find the midpoint to see how many iterations we need to complete the roof.
                midpoint = math.ceil(self.structure.width / 2)
 
                    
                # Creating the roof structure.
                for minus in range(1, midpoint):
                    
                    start_point.x += 1
                    start_point.y += 1
                    start_point.z += 1
        
                    end_point.x -= 1
                    end_point.y += 1
                    end_point.z -= 1
                    
                    # Placing the roof structure
                    create_blocks(mc, start_point, end_point, block.COBBLESTONE.id) 
                               
                    
            else:
                
                # Find the midpoint to see how many iterations we need to complete the roof.
                midpoint = math.ceil(self.structure.width / 2) 
                
                # Creating the roof structure.
                for positive in range(1, midpoint):
                    
                    start_point.x += 1
                    start_point.y += 1
                    start_point.z -= 1
        
                    end_point.x -= 1
                    end_point.y += 1
                    end_point.z += 1

                    # Placing the roof structure 
                    create_blocks(mc, start_point, end_point, block.COBBLESTONE.id)  
   
        
    def create_walls(self,mc):
        
        #initialises the randomised outline blocks to place down for the house.
        corner_block = rm.vertical_outline_blocks() 
        east_block = rm.east_outline_blocks(corner_block) # passes wood type as a parameter, to get the horizontal version
        north_block = rm.north_outline_blocks(corner_block) # passes wood type as a parameter, to get the horizontal version
        
        #initialises the randomised exterior block to place down for the walls
        exterior_block = rm.random_exterior()
        
        
        for floor in self.floors:
            endpoint1 = vec3.Vec3(floor.backleft.x, floor.backleft.y + self.structure.height, floor.backleft.z)
            endpoint2 = vec3.Vec3(floor.frontright.x, floor.frontright.y + self.structure.height, floor.frontright.z)
            create_blocks(mc, floor.frontleft, endpoint1, exterior_block)
            create_blocks(mc, endpoint1, floor.backright, exterior_block)
            create_blocks(mc, floor.backright, endpoint2, exterior_block)
            create_blocks(mc, endpoint2, floor.frontleft, exterior_block)
        

            """PLACES HORIZONTAL OUTLINE BLOCKS OF THE HOUSE"""
            # finds the endpoint of the opposite side of the house, to place outline block material
            horizontal_one = vec3.Vec3(floor.frontright.x, floor.frontleft.y, floor.frontleft.z)
            create_blocks(mc, floor.frontleft, horizontal_one, east_block)
            
            # finds the endpoint of the opposite side of the house, to place outline block material
            horizontal_two = vec3.Vec3(floor.frontleft.x, floor.frontleft.y, floor.frontleft.z)
            create_blocks(mc, floor.backleft, horizontal_two, north_block)
            
            # finds the endpoint of the opposite side of the house, to place outline block material
            horizontal_three = vec3.Vec3(floor.frontright.x, floor.frontright.y, floor.frontright.z)
            create_blocks(mc, floor.backright, horizontal_three, north_block)
            
            # finds the endpoint of the opposite side of the house, to place outline block material
            horizontal_four = vec3.Vec3(floor.backright.x, floor.frontright.y, floor.backleft.z)
            create_blocks(mc, floor.backleft, horizontal_four, east_block)
            
            """PLACES VERITCAL OUTLINE BLOCKS OF THE HOUSE"""
            # finds the corner of the frontleft and places the outline block material in the frontleft corner.
            corner_one = vec3.Vec3(floor.frontleft.x, floor.frontleft.y + self.structure.height, floor.frontleft.z)
            create_blocks(mc, floor.frontleft, corner_one, corner_block)
            
            # finds the corner of the frontright and places the outline block material in the frontright corner.
            corner_two = vec3.Vec3(floor.frontright.x, floor.frontright.y + self.structure.height, floor.frontright.z)
            create_blocks(mc, floor.frontright, corner_two, corner_block)
            
            # finds the corner of the backleft and places the outline block material in the backleft corner.
            corner_three = vec3.Vec3(floor.backleft.x, floor.backleft.y + self.structure.height, floor.backleft.z)
            create_blocks(mc, floor.backleft, corner_three, corner_block)
            
            # finds the corner of the backright and places the outline block material in the backright corner.
            corner_four = vec3.Vec3(floor.backright.x, floor.backright.y + self.structure.height, floor.backright.z)
            create_blocks(mc, floor.backright, corner_four, corner_block)
            
    def create_windows(self,mc):
        for floor in self.floors:
            for room in floor.rooms:
                floor.create_window(mc,room)   
               
    
    
    def creating_front_door(self,mc):
        Air = 0
        window_block = 95
        door = 64
        # assign a variable to make the code easier to read
        create_x = random.randint(self.structure.frontleft.x, self.structure.frontright.x)
        create_y = self.structure.frontleft.y
        create_z = self.structure.frontleft.z
        # check if the randomised coordinate is suitable for placing a door
        while (mc.getBlock(create_x, create_y + 2, create_z + 1) != Air or
                mc.getBlock(create_x, create_y + 2, create_z - 1) != Air or 
                mc.getBlock(create_x, create_y + 2, create_z) == window_block):
            create_x = random.randint(self.structure.frontleft.x, self.structure.frontright.x)
        
        # placing the door
        mc.setBlock(create_x, create_y + 1, create_z, block.AIR)
        mc.setBlock(create_x, create_y + 2, create_z, block.AIR)
        mc.setBlock(create_x , create_y + 2, create_z,door,8)
        mc.setBlock(create_x , create_y + 1, create_z,door,0)
        self.front_door = Vec3(create_x, create_y, create_z)
        

    def create_furniture(self, mc):
        
        for floor in self.floors:
            for room in floor.rooms:
                floor.place_furniture(mc, room)
                

    def create_house(self,mc):
        self.create_floor(mc)
        self.create_roof(mc)
        self.create_rooms(mc)
        self.create_stairs(mc)
        self.create_walls(mc)
        self.create_windows(mc)
        self.creating_front_door(mc)
        # self.create_furniture(mc)
         
       


