from mcpi.minecraft import Minecraft
from mcpi import block
from models.Floor import *
from mcpi import vec3
from RandomiseMaterial import RandomiseMaterial
import random 
import math

rm = RandomiseMaterial()

         


class House:
    def __init__ (self,structure):
        self.structure = structure
        self.stories = 5
        # random.randint(0,10)
        self.height = structure.height * self.stories
        # Floor list restore all the floor instance in the house
        self.floors = []
        self.front_door = None

        
    
    def create_floor(self, mc: Minecraft):
        material = rm.random_floors()
        colour = random.randint(1,3)
        if self.structure.length > 0 :
            lightBlock_offset_z = random.randint(2, 3)
        else:
            lightBlock_offset_z = random.randint(-3, -2)
        lightBlock_offset_x = random.randint(2, 3)
        
        
        for storey in range(self.stories):
            structure = self.structure
            floor = Floor(structure, storey)
            create_blocks(mc, floor.frontleft, floor.backright, material, colour)
            
            """ADDING LIGHTING BY INCORPORATING IT INTO THE FLOOR BY ITERATING THROUGH ROWS AND COLUMNS"""
            for i in range(floor.frontleft.x, floor.backright.x, lightBlock_offset_x): 
                block_difference_x = i - floor.frontleft.x # Setting the offset position to place glowstone on the row
                for z in range(floor.frontleft.z, floor.backright.z, lightBlock_offset_z): 
                    block_difference_z = z - floor.frontleft.z # Setting the offset position to place glowstone on column
                    mc.setBlock(floor.frontleft.x + block_difference_x, floor.frontleft.y + self.structure.height + 1,
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
        
        # Creates the ceiling for the final floor of the house and initialises the two opposite corners.
        start_point = vec3.Vec3(self.structure.frontleft.x,
                                self.structure.frontleft.y + self.structure.height * self.stories, 
                                self.structure.frontleft.z)
        end_point = vec3.Vec3(self.structure.backright.x,
                                self.structure.backright.y + self.structure.height * self.stories, 
                                self.structure.backright.z)
        create_blocks(mc, start_point, end_point)
        
        """CREATE TWO TYPES OF ROOF. ONE WITH BLOCKS AND ONE WITH STAIRS."""
        # Creating the base of the roof
        start_point.y += 1
        
        create_blocks(mc, start_point, end_point, block.COBBLESTONE.id)
        
        #mc.setBlock(self.structure.frontleft.x, self.structure.frontleft.y + self.structure.height * self.stories + 1, self.structure.frontleft.z, block.GLOWSTONE_BLOCK)
        #mc.setBlock(self.structure.backright.x, self.structure.backright.y + self.structure.height * self.stories + 1, self.structure.backright.z, block.GLOWSTONE_BLOCK)
        
        mc.postToChat(f"frontleft.x = {self.structure.frontleft.x}, frontleft.y = {self.structure.frontleft.y + self.structure.height * self.stories + 1}, frontleft.z = {self.structure.frontleft.z}")
        mc.postToChat(f"backright.x = {self.structure.backright.x}, backright.y = {self.structure.backright.y + self.structure.height * self.stories + 1}, backright.z = {self.structure.backright.z}")
        
        
        # Grabbing the coordinates of the block facing the negative z-direction.
        negative_z = Vec3(self.structure.frontleft.x, self.structure.frontleft.y + self.structure.height * self.stories + 1, self.structure.frontleft.z - 1)
        check_negativeBlock= mc.getBlock(negative_z)
        
        # Creating the roof top on top of the house, placing the blocks accordingly depending on if it is facing -z or +z direction.
        if check_negativeBlock == block.AIR.id:
            
            for minus in range(0, 5):
                    
                start_point.x += 1
                start_point.y += 1
                start_point.z += 1
        
                end_point.x -= 1
                end_point.y += 1
                end_point.z -= 1
            
                create_blocks(mc, start_point, end_point, block.COBBLESTONE.id)
                print("minus direction")               
                    
        else:
            
            for positive in range(0, 5):
            
                start_point.x += 1
                start_point.y += 1
                start_point.z -= 1
            
                end_point.x -= 1
                end_point.y += 1
                end_point.z += 1
            
                create_blocks(mc, start_point, end_point, block.COBBLESTONE.id)
                print("positive direction")
                print(self.structure.frontleft.z + 1) 
   
        
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
                # print(floor.frontleft.x,floor.frontleft.y,floor.frontleft.z)
                # print(room.frontleft.x,room.frontleft.y,room.frontleft.z)  
    

    def front_side(self,mc):
        self.front_door = create_door(mc,self.structure.frontleft,self.structure.frontright)
        

    def create_furniture(self, mc):
        
        for floor in self.floors:
            for room in floor.rooms:
                floor.place_furniture(mc, room)
                # print("placing furniture")

    def create_house(self,mc):
        self.create_floor(mc)
        self.create_roof(mc)
        self.create_rooms(mc)
        self.create_stairs(mc)
        self.create_walls(mc)
        self.create_windows(mc)
        self.front_side(mc)
        self.create_furniture(mc)
        # self.back_window(mc)
        # self.side_window(mc,self.structure.frontleft)
        # self.side_window(mc,self.structure.frontright)
        


