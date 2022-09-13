from random import randrange
from mcpi import vec3
from mcpi import minecraft

mc = minecraft.Minecraft.create()

class Plot:
    def __init__(self, central_point, distance_from_path) -> None:
        self.central_point      = central_point
        self.distance_from_path = distance_from_path

        buffer_from_path = 2

        self.plot_start = vec3.Vec3(self.central_point.x - int(self.distance_from_path/2) + buffer_from_path,
                                    0,
                                    self.central_point.z - int(self.distance_from_path/2) + buffer_from_path)
          
        self.plot_end   = vec3.Vec3(self.central_point.x + int(self.distance_from_path/2) - buffer_from_path,
                                    0,
                                    self.central_point.z + int(self.distance_from_path/2) - buffer_from_path)

        self.plot_length = self.plot_end.x - self.plot_start.x
        
        #TODO set up logic for determining directiond

        print(self.plot_length)
    
    def d_make_structure(self):
        self.structure_length = randrange(10,self.plot_length)
        self.structure_width = randrange(8,self.structure_length)
        print(self.structure_length, self.structure_width)