from src.ppm import PPM
from src.vec3 import Vec3

if __name__ == "__main__":
    hello_world = PPM(300, 200)
    for ri in range(hello_world.height):
        for ci in range(hello_world.width):
            v = Vec3(
                ri / hello_world.width,
                ci / hello_world.height,
                0.2
            )
            color = v * 255.99
            color.map(int)
            hello_world.set_pixel(ri, ci, color)
    hello_world.write("/tmp/prt_hello_world.ppm")
