from src.ppm import PPM
from src.ray import Ray
from src.vec3 import Vec3

"""
We have an abstract, static camera at (0, 0, 0).
"""

UNIT_VEC3: Vec3 = Vec3(1.0, 1.0, 1.0)

def color(ray: Ray) -> Vec3:
    unit_direction: Vec3 = ray.direction.unit_vector()
    # WOW lots of magic numbers!
    t: float = 0.5 * (unit_direction.y + 1)
    return (UNIT_VEC3 * (1.0 - t)) + (Vec3(0.5, 0.7, 1.0) * t)

if __name__ == "__main__":
    width = 200
    height = 100
    ppm: PPM = PPM(width, height)
    lower_left_corner: Vec3 = Vec3(-2, -1, -1)
    h_movement: Vec3 = Vec3(4, 0, 0)
    v_movement: Vec3 = Vec3(0, 2, 0)
    origin: Vec3 = Vec3(0, 0, 0)

    for j in range(height - 1, 0, -1):
        for i in range(width):
            u = i / width
            v = j / height
            r: Ray = Ray(origin, lower_left_corner + (h_movement * u) + (v_movement * v))
            _color: Vec3 = color(r)
            _color *= 255.9
            _color.map(int)

            ppm.set_pixel(j, i, _color)

    ppm.write("/tmp/simple_camera.ppm")
