"""
A pretty hardcoded abstraction for a camera (for now).
"""
from src.ray import Ray
from src.vec3 import Vec3

from typing import Optional

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
            self.lower_left_corner + (self.h_movement * u) + (self.v_movement * v)
        )
