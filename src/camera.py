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

    def __init__(self, vfov: float, aspect_ratio: float):
        """
        Create a camera automatically positioned relative to the scene such that
        it has a certain vertical field-of-view (vfov, expressed in degrees)
        given the scene's aspect ration.
        """
        vfov_rad: float = vfov * math.pi / 180
        half_height = math.tan(vfov_rad / 2)
        half_width = aspect_ratio * half_height
        super().__init__(
            Vec3(-half_width, -half_height, -1.0),
            Vec3(2 * half_width, 0, 0),
            Vec3(0, 2 * half_height, 0),
            Vec3(0, 0, 0)
        )
