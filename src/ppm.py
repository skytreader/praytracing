from src.vec3 import Vec3
from typing import Optional

class PPM(object):
    """
    Stands for "Portable PixMap". Duh.
    """

    def __init__(self, width: int, height: int, default_color: Optional[Vec3]=None):
        self.width = width
        self.height = height
        if default_color is None:
            default_color = Vec3(0.0, 0.0, 0.0)
        self.grid = [[default_color for _ in range(width)] for __ in range(height)]

    def set_pixel(self, row: int, col: int, color: Vec3):
        self.grid[row][col] = color

    def write(self, filename: str):
        if not filename.endswith(".ppm"):
            filename = "%s.ppm" % filename

        with open(filename, "w+") as ppm_file:
            print("P3", file=ppm_file)
            print("%s %s" % (self.width, self.height), file=ppm_file)
            print("255", file=ppm_file)

            for row in self.grid:
                print(
                    " ".join(
                        [" ".join(
                            [str(p) for p in pixel.make_tuple()]
                        ) for pixel in row]
                    ),
                file=ppm_file)
