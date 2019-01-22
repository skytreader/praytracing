from src.ppm import PPM

if __name__ == "__main__":
    hello_world = PPM(300, 200)
    for ri in range(hello_world.height):
        for ci in range(hello_world.width):
            r = ri / hello_world.width
            g = ci / hello_world.height
            b = 0.2
            color = (
                int(r * 255.99), int(g * 255.9), int(b * 255.9)
            )
            hello_world.set_pixel(ri, ci, color)
    hello_world.write("/tmp/prt_hello_world.ppm")
