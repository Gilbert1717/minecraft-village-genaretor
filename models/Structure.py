from mcpi.vec3 import Vec3
import random

def create_vector(vector,x,y,z):
    new_vector = Vector(vector.x,vector.y,vector.z)
    new_vector.change_vector(x,y,z)
    return new_vector

class Structure:
    def __init__ (self,vector,direction,width = random.randrange(8,16),length = random.randrange(10,20),height = 5,):
        self.height = height
        self.width = width
        self.length = length * direction
        self.direction = direction
        self.position = Vec3(vector.x, vector.y,vector.z)
        self.frontleft = Vec3(vector.x, vector.y, vector.z)
        self.frontright = Vec3(vector.x + self.width, vector.y, vector.z)
        self.backleft = Vec3(vector.x, vector.y, vector.z + self.length)
        self.backright = Vec3(vector.x + self.width, vector.y, vector.z + self.length)


class Vector(Vec3):
    def change_vector(self, x, y, z):
        self.x = self.x + x
        self.y = self.y + y
        self.z = self.z + z
        return Vec3(self.x, self.y, self.z)