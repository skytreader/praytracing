from src.ppm import PPM
from src.ray import Ray
from src.vec3 import Vec3

"""
We have an abstract, static camera at (0, 0, 0).
"""

UNIT_VEC3: Vec3 = Vec3(1.0, 1.0, 1.0)

def color(ray: Ray) -> Vec3:
    """
    Linear interpolation of color based on the y direction.
    """
    unit_direction: Vec3 = ray.direction.unit_vector()
    # WOW lots of magic numbers!
    t: float = 0.5 * (unit_direction.y + 1)
    return (UNIT_VEC3 * (1.0 - t)) + (Vec3(0.5, 0.7, 1.0) * t)

if __name__ == "__main__":
    width = 400
    height = 200
    ppm: PPM = PPM(width, height)
    lower_left_corner: Vec3 = Vec3(-2, -1, -1)
    h_movement: Vec3 = Vec3(4, 0, 0)
    v_movement: Vec3 = Vec3(0, 2, 0)
    origin: Vec3 = Vec3(0, 0, 0)

    for j in range(height - 1, -1, -1):
        for i in range(width):
            # Get the ratio of how far are we from the "edges".
            u = i / width
            v = j / height
            # And use those ratios to "move" the ray away from the origin. Note:
            #  - (h_ * u) + (v_ * v) is scaled movement
            #  - the movement scales differently depending on dimension:
            #    horizontal movement is increasing towards the vector (4, 0, 0)
            #    while vertical movement is decreasing from the vector (0, 2, 0)
            r: Ray = Ray(origin, lower_left_corner + (h_movement * u) + (v_movement * v))
            _color: Vec3 = color(r)
            _color *= 255.9
            _color.map(int)

            # Note the translation for the row: we want the white part of the
            # gradient at the bottom so we do this.
            ppm.set_pixel((height - 1) - j, i, _color)

    ppm.write("/tmp/simple_camera.ppm")
