from mcpi.minecraft import Minecraft
from mcpi import block
from mcpi import vec3
import random 
def create_position(position,x,y,z):
    new_position = McPosition(position.x,position.y,position.z)
    new_position.change_position(x,y,z)
    return new_position

def create_wall(mc,start_point,end_point,material = 1,color = 3):
    start_x = start_point.x
    start_y = start_point.y
    start_z = start_point.z
    end_x = end_point.x
    end_y = end_point.y
    end_z = end_point.z
    mc.setBlocks(start_x, start_y, start_z, end_x, end_y, end_z, material ,color)

def create_door(mc,McPosition1,McPosition2):
    if McPosition1.x == McPosition2.x:
        length = abs(McPosition2.z - McPosition1.z)
        # print(McPosition1.x,McPosition2.x,McPosition2.z,McPosition1.z)
        if McPosition2.z > McPosition1.z:
            create_position = McPosition1.z + random.randint(2,length - 2)
            # while mc.getBlock(create_position + 1, McPosition1.y, McPosition1.z) != 0 or mc.getBlock(create_position - 1, McPosition1.y, McPosition1.z) != 0:
            #     create_position = McPosition1.z + random.randint(2,length - 2)
        else:
            create_position = McPosition1.z - random.randint(2,length - 2)
            # while mc.getBlock(create_position + 1, McPosition1.y, McPosition1.z) != 0 or mc.getBlock(create_position - 1, McPosition1.y, McPosition1.z) != 0:
            #     create_position = McPosition1.z - random.randint(2,length - 2)
        mc.setBlock(create_position , McPosition1.y, McPosition1.z, 0)
        mc.setBlock(create_position , McPosition1.y + 1, McPosition1.z, 0)
        mc.setBlock(create_position , McPosition1.y + 1, McPosition1.z,64,8)
        mc.setBlock(create_position , McPosition1.y, McPosition1.z,0)

    elif McPosition1.z == McPosition2.z:
        width = abs(McPosition2.x - McPosition1.x)
        # print(width)
        if McPosition2.x > McPosition1.x:
            create_position = McPosition1.x + random.randint(2,width - 2)
            # while mc.getBlock(create_position, McPosition1.y, McPosition1.z + 1) == 0 or mc.getBlock(create_position - 1, McPosition1.y, McPosition1.z) == 0:
            #     create_position = McPosition1.x + random.randint(2,width - 2)
        else:
            create_position = McPosition1.x - random.randint(2,width - 2)
            # while mc.getBlock(create_position, McPosition1.y, McPosition1.z + 1) == 0 or mc.getBlock(create_position - 1, McPosition1.y, McPosition1.z) == 0:
            #      create_position = McPosition1.x - random.randint(2,width - 2)
        mc.setBlock(create_position , McPosition1.y + 1, McPosition1.z, 0)
        mc.setBlock(create_position , McPosition1.y + 2, McPosition1.z, 0)



class McPosition:
    def __init__ (self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    
    def change_position(self,x,y,z):
        self.x = self.x + x
        self.y = self.y + y
        self.z = self.z + z
        return McPosition(self.x,self.y,self.z)


class Structure:
    def __init__ (self,mcPosition,width = random.randrange(8,16),length = random.randrange(10,20),height = 5,):
        self.height = height
        self.width = width
        self.length = length
        self.position = McPosition(mcPosition.x, mcPosition.y,mcPosition.z)
        self.frontleft = McPosition(mcPosition.x, mcPosition.y, mcPosition.z)
        self.frontright = McPosition(mcPosition.x + self.width, mcPosition.y, mcPosition.z)
        self.backleft = McPosition(mcPosition.x, mcPosition.y, mcPosition.z + self.length)
        self.backright = McPosition(mcPosition.x + self.width, mcPosition.y, mcPosition.z + self.length)

class Floor:
    def __init__ (self,structure,storey):
        structure.position.y += structure.height * storey
        self.storey = storey
        self.structure = structure
        self.frontleft = McPosition(structure.frontleft.x,
                                    structure.position.y,
                                    structure.frontleft.z)
        self.frontright = McPosition(structure.frontright.x,
                                    structure.position.y,
                                    structure.frontright.z)
        self.backleft = McPosition(structure.backleft.x,
                                    structure.position.y,
                                    structure.backleft.z)
        self.backright = McPosition(structure.backright.x,
                                    structure.position.y,
                                    structure.backright.z)

    def split_horizontal(self,split_point):
        width = split_point - 1
        structure1 = Structure(self.structure.position, width, self.structure.length)
        structure2_position = create_position(self.structure.position,split_point,0,0)
        structure2 = Structure(structure2_position, self.structure.width - split_point, self.structure.length)
        floor1 = Floor(structure1,self.storey)
        print('floor1 x',floor1.frontleft.x,floor1.frontright.x,floor1.backleft.x,floor1.backright.x)
        print('floor1 z',floor1.frontleft.z,floor1.frontright.z,floor1.backleft.z,floor1.backright.z)
        
        floor2 = Floor(structure2,self.storey)
        print('floor2 x',floor2.frontleft.x,floor2.frontright.x,floor2.backleft.x,floor2.backright.x)
        return floor1, floor2

    def split_vertical(self,split_point):
        length = split_point - 1
        structure1 = Structure(self.structure.position, self.structure.width, length)
        structure2_position = create_position(self.structure.position,0,0,split_point)
        structure2 = Structure(structure2_position, self.structure.width, self.structure.length - split_point)
        floor1 = Floor(structure1,self.storey)
        print('floor1 z',floor1.frontleft.z,floor1.frontright.z,floor1.backleft.z,floor1.backright.z)
        floor2 = Floor(structure2,self.storey)
        print('floor2 z',floor2.frontleft.z,floor2.frontright.z,floor2.backleft.z,floor2.backright.z)
        return floor1, floor2

    



    def create_room(self,mc,floor,material = 1,color = 1): 
        print('outside',floor.structure.width,floor.structure.length)
        if floor.structure.width > 6 and floor.structure.length > 6:
            print('if1',floor.structure.width,floor.structure.length)
            if floor.structure.width >= floor.structure.length:
                # print('if2',floor.structure.width,floor.structure.length)
                split = random.randrange(int(floor.structure.width/2),floor.structure.width - 4,1) 
                floor1,floor2 = floor.split_horizontal(split)
                print(split)
                create_wall(mc,floor1.frontright,create_position(floor1.frontright,0,floor.structure.height,floor.structure.length))
                # McPosition1 = McPosition(self.structure.x + split, self.structure.y, self.structure.z)
                # McPosition2 = McPosition(self.structure.x + split,self.structure.y,self.structure.z + length)
                # create_door(mc,McPosition1,McPosition2)
                stop = 1
                random.randint(0,3)
                if stop != 0:
                    floor1.create_room(mc,floor1)
                    floor2.create_room(mc,floor2)
            else:
                print('else',floor.structure.width,floor.structure.length)
                split = random.randrange(int(floor.structure.length/2),floor.structure.length - 4,1)
                
                floor1,floor2 = floor.split_vertical(split)
                create_wall(mc,floor1.backleft,create_position(floor1.backleft,floor.structure.width,floor.structure.height,0))
                print("floorv",floor1.frontleft.x,floor1.frontleft.y,floor1.frontleft.z)
                # McPosition1 = McPosition(self.structure.x, self.structure.y, self.structure.z + split)
                # McPosition2 = McPosition(self.structure.x + width,self.structure.y,self.structure.z + split)
                # create_door(mc,McPosition1,McPosition2)
                # stop = random.randint(0,3)
                stop = 1
                if stop != 0:        
                    floor1.create_room(mc,floor1)
                    floor2.create_room(mc,floor2)


        
class House:
    def __init__ (self,structure,stories = random.randint(0,2)):
        self.structure = structure
        self.stories = stories
        self.floors = []
        
    
    def create_floor(self,mc):
        material = random.randint(1,2)
        colour = random.randint(1,3)
        for storey in range(self.stories):
            structure = Structure(self.structure.position,self.structure.width,self.structure.length,self.structure.height)
            floor = Floor(structure,storey)
            create_wall(mc,floor.frontleft,floor.backright,material,colour)
            self.floors.append(floor)

    def create_rooms(self,mc):
        for floor in self.floors:
            floor.create_room(mc,floor)
            

    def create_roof(self,mc):
        start_point = McPosition(self.structure.frontleft.x,
                                self.structure.frontleft.y + self.structure.height * self.stories, 
                                self.structure.frontleft.z)
        end_point = McPosition(self.structure.backright.x,
                                self.structure.backright.y + self.structure.height * self.stories, 
                                self.structure.backright.z)
        create_wall(mc,start_point,end_point)

            
   
        
    def create_walls(self,mc):
        for floor in self.floors:
            endpoint1 = McPosition(floor.backleft.x, floor.backleft.y + self.structure.height, floor.backleft.z)
            endpoint2 = McPosition(floor.frontright.x, floor.frontright.y + self.structure.height, floor.frontright.z)
            create_wall(mc,floor.frontleft,endpoint1)
            create_wall(mc,endpoint1,floor.backright)
            create_wall(mc,floor.backright,endpoint2)
            create_wall(mc,endpoint2,floor.frontleft)
            
    
    def back_window(self,mc):
        window_x = self.structure.x + 3
        window_y = self.structure.y + 1
        window_z = self.structure.z + self.structure.length 
        window_height = 5
        window_width = window_x + 8
        mc.setBlocks(window_x, window_y, window_z, window_width,window_height,window_z,102)
    
    def left_window(self,mc):
        i = random.randint(1,3)
        window_x = self.structure.x + self.structure.width
        window_y = self.structure.y + random.randint(1,3)
        window_z = self.structure.z + 3
        window_height = window_y + 2
        window_width = window_z + 1
        for x in range(i):
            mc.setBlocks(window_x, window_y, window_z, window_x,window_height,window_width,102)
            window_z = window_z + int(self.structure.length/i) 
            window_width = window_z + 1
            
    
    def right_window(self,mc):
        i = random.randint(1,3)
        window_x = self.structure.x
        window_y = self.structure.y + random.randint(1,3)
        window_z = self.structure.z + 3
        window_height = window_y + 2
        window_width = window_z + 1
        for x in range(i):
            mc.setBlocks(window_x, window_y, window_z, window_x,window_height,window_width,102)
            window_z = window_z + int(self.structure.length/i)
            window_width = window_z + 1

    
        

    def front_window(self,mc):
        window_x = self.structure.x + 3
        window_y = self.structure.y + 3
        window_height = window_x + 2
        window_width = window_y + 2
        mc.setBlocks(window_x, window_y, self.structure.z, window_width,window_height,self.structure.z,102)

    def front(self,mc):
        create_door(mc,self.structure.frontleft,self.structure.frontright)
        # self.front_window(mc)

    

    def create_house(self,mc):
        self.create_floor(mc)
        # self.create_roof(mc)
        self.create_rooms(mc)
        # self.create_walls(mc)
        # self.front(mc)
        # self.back_window(mc)
        # self.left_window(mc)
        # self.right_window(mc)


