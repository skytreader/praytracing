"""
A pretty hardcoded abstraction for a camera (for now).
"""
from src.ray import Ray
from src.vec3 import Vec3

import math

class Camera(object):

    def __init__(
        self, lower_left_corner: Vec3, h_movement: Vec3, v_movement: Vec3,
        origin: Vec3
    ):
        """
        Actually, all these parameters should not be Optional but are tagged as
        so for backwards compatibility.
        """
        self.lower_left_corner: Vec3 = lower_left_corner
        self.h_movement: Vec3 = h_movement
        self.v_movement: Vec3 = v_movement
        self.origin: Vec3 = origin

    def get_ray(self, u: float, v: float) -> Ray:
        return Ray(
            self.origin,
            self.lower_left_corner + (self.h_movement * u) + (self.v_movement * v) - self.origin
        )

class PositionableCamera(Camera):

    # TODO Specify camera_aim as a direction, which just feels more natural.
    # Even the text says "Later...you could define a direction to look in
    # instead of a point to look at".
    # TODO Maybe check that the up_vector is indeed valid wrt to the camera_posn
    def __init__(
        self, camera_posn: Vec3, camera_aim: Vec3, up_vector: Vec3, vfov: float,
        aspect_ratio: float
    ):
        """
        Create a camera automatically positioned relative to the scene such that
        it has a certain vertical field-of-view (vfov, expressed in degrees)
        given the scene's aspect ration.
        """
        vfov_rad: float = vfov * math.pi / 180
        half_height = math.tan(vfov_rad / 2)
        half_width = aspect_ratio * half_height
        # The following are just some vectors to define axes. Don't be confused!
        w = (camera_posn - camera_aim).unit_vector()
        u = up_vector.cross(w).unit_vector()
        v = w.cross(u)
        super().__init__(
            camera_posn - (half_width * u) - (half_height * v) - w,
            2 * half_width * u,
            2 * half_height * v,
            camera_posn
        )
