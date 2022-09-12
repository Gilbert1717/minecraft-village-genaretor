import imp
from models.Structure import *
from models.House import *
from mcpi.vec3 import Vec3
def create_blocks(mc, start_point, end_point, material = 1, color = 3):
    start_x = start_point.x
    start_y = start_point.y
    start_z = start_point.z
    end_x = end_point.x
    end_y = end_point.y
    end_z = end_point.z
    mc.setBlocks(start_x, start_y, start_z, end_x, end_y, end_z, material ,color)


def create_door(mc,vector1,vector2):
    #  On horizontal wall
    if vector1.x == vector2.x:
        length = abs(vector2.z - vector1.z)
        # print(vector1.x,vector2.x,vector2.z,vector1.z)
        if vector2.z > vector1.z:
            create_z = vector1.z + random.randint(2,length - 2)
            # while mc.getBlock(create_vector + 1, vector1.y, vector1.z) != 0 or mc.getBlock(create_vector - 1, vector1.y, vector1.z) != 0:
            #     create_vector = vector1.z + random.randint(2,length - 2)
        else:
            create_z = vector1.z - random.randint(2,length - 2)
            # while mc.getBlock(create_vector + 1, vector1.y, vector1.z) != 0 or mc.getBlock(create_vector - 1, vector1.y, vector1.z) != 0:
            #     create_vector = vector1.z - random.randint(2,length - 2)
        mc.setBlock(vector1.x, vector1.y + 1, create_z, 0)
        mc.setBlock(vector1.x, vector1.y + 2, create_z, 0)
        mc.setBlock(vector1.x, vector1.y + 2, create_z,64,8)
        mc.setBlock(vector1.x , vector1.y + 1, create_z,64,0)
         
    #  On vertical wall
    elif vector1.z == vector2.z:
        width = abs(vector2.x - vector1.x)
        # print(width)
        if vector2.x > vector1.x:
            create_x = vector1.x + random.randint(2,width - 2)
            # while mc.getBlock(create_vector, vector1.y, vector1.z + 1) == 0 or mc.getBlock(create_vector - 1, vector1.y, vector1.z) == 0:
            #     create_vector = vector1.x + random.randint(2,width - 2)
        else:
            create_x = vector1.x - random.randint(2,width - 2)
            # while mc.getBlock(create_vector, vector1.y, vector1.z + 1) == 0 or mc.getBlock(create_vector - 1, vector1.y, vector1.z) == 0:
            #      create_vector = vector1.x - random.randint(2,width - 2)
        mc.setBlock(create_x, vector1.y + 1, vector1.z, 0)
        mc.setBlock(create_x, vector1.y + 2, vector1.z, 0)
        mc.setBlock(create_x , vector1.y + 2, vector1.z,64,8)
        mc.setBlock(create_x , vector1.y + 1, vector1.z,64,0)
        
        

class Floor:
    def __init__ (self,structure,storey):
        structure.position.y += structure.height * storey
        self.storey = storey
        self.structure = structure
        self.frontleft = Vec3(structure.frontleft.x,
                                structure.position.y,
                                structure.frontleft.z)
        self.frontright = Vec3(structure.frontright.x,
                                structure.position.y,
                                structure.frontright.z)
        self.backleft = Vec3(structure.backleft.x,
                                structure.position.y,
                                structure.backleft.z)
        self.backright = Vec3(structure.backright.x,
                                structure.position.y,
                                structure.backright.z)

    def split_horizontal(self,split_point):
        width = split_point - 1
        structure1 = Structure(self.structure.position, width, self.structure.length)
        structure2_position = create_vector(self.structure.position,split_point,0,0)
        structure2 = Structure(structure2_position, self.structure.width - split_point, self.structure.length)
        floor1 = Floor(structure1,self.storey)
        # print('floor1 x',floor1.frontleft.x,floor1.frontright.x,floor1.backleft.x,floor1.backright.x)
        # print('floor1 z',floor1.frontleft.z,floor1.frontright.z,floor1.backleft.z,floor1.backright.z)
        
        floor2 = Floor(structure2,self.storey)
        # print('floor2 x',floor2.frontleft.x,floor2.frontright.x,floor2.backleft.x,floor2.backright.x)
        return floor1, floor2

    def split_vertical(self,split_point):
        length = split_point - 1
        structure1 = Structure(self.structure.position, self.structure.width, length)
        structure2_position = create_vector(self.structure.position,0,0,split_point)
        structure2 = Structure(structure2_position, self.structure.width, self.structure.length - split_point)
        floor1 = Floor(structure1,self.storey)
        print('floor1 z',floor1.frontleft.z,floor1.frontright.z,floor1.backleft.z,floor1.backright.z)
        floor2 = Floor(structure2,self.storey)
        print('floor2 z',floor2.frontleft.z,floor2.frontright.z,floor2.backleft.z,floor2.backright.z)
        return floor1, floor2

    



    def create_room(self,mc,floor,material = 1,color = 1): 
        min_room_length = 8
        min_room_width = 8
        print('outside',floor.structure.width,floor.structure.length)
        if floor.structure.width > min_room_length and floor.structure.length > min_room_length:
            print('if1',floor.structure.width,floor.structure.length)
            if floor.structure.width >= floor.structure.length:
                # print('if2',floor.structure.width,floor.structure.length)
                split = random.randrange(int(floor.structure.width/2),floor.structure.width - min_room_width//2,1) 
                floor1,floor2 = floor.split_horizontal(split)
                diagonal_point = create_vector(floor1.frontright, 0, floor.structure.height, floor.structure.length)
                create_blocks(mc, floor1.frontright, diagonal_point)
                McPosition1 = floor1.frontright
                McPosition2 = floor1.backright
                create_door(mc,McPosition1,McPosition2)
                stop = 1
                random.randint(0,3)
                if stop != 0:
                    floor1.create_room(mc,floor1)
                    floor2.create_room(mc,floor2)
            else:
                print('else',floor.structure.width,floor.structure.length)
                split = random.randrange(int(floor.structure.length/2),floor.structure.length - min_room_length//2,1)
                floor1,floor2 = floor.split_vertical(split)
                diagonal_point = create_vector(floor1.backleft, floor.structure.width, floor.structure.height, 0)
                create_blocks(mc, floor1.backleft, diagonal_point)
                # print("floorv",floor1.frontleft.x,floor1.frontleft.y,floor1.frontleft.z)
                McPosition1 = floor1.backleft
                McPosition2 = floor1.backright
                create_door(mc,McPosition1,McPosition2)
                stop = random.randint(0,3)
                stop = 1
                if stop != 0:        
                    floor1.create_room(mc,floor1)
                    floor2.create_room(mc,floor2)