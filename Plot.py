from mcpi import vec3
from mcpi import minecraft

mc = minecraft.Minecraft.create()

class Plot:
    def __init__(self, central_point, distance_from_path) -> None:
        self.central_point      = central_point
        self.distance_from_path = distance_from_path

        buffer_from_path = 2

        plot_start = vec3.Vec3( self.central_point[0] - int(self.distance_from_path/2) + buffer_from_path,
                                0,
                                self.central_point[1] - int(self.distance_from_path/2) + buffer_from_path)
                                    
        plot_end   = vec3.Vec3( self.central_point[0] - int(self.distance_from_path/2) + buffer_from_path,
                                0,
                                self.central_point[1] - int(self.distance_from_path/2) + buffer_from_path)

        mc.setBlock(    plot_start.x,   plot_start.y,   plot_start.z,
                        plot_end.x,     plot_end.y,     plot_end.z, 17)
        print(plot_start.x,   plot_start.y,   plot_start.z,
                        plot_end.x,     plot_end.y,     plot_end.z, 17)
    
    def make_structure():
        pass