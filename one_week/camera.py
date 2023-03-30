"""
A pretty hardcoded abstraction for a camera (for now).
"""
from one_week.ray import Ray
from one_week.vec3 import Vec3

import math
import random

class Camera(object):

    def __init__(
        self, lower_left_corner: Vec3, h_movement: Vec3, v_movement: Vec3,
        origin: Vec3
    ):
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
        aspect_ratio: float, aperture: float = 2, focus_dist: float = 1
    ):
        """
        Create a camera automatically positioned relative to the scene such that
        it has a certain vertical field-of-view (vfov, expressed in degrees)
        given the scene's aspect ratio.
        """
        self.lens_radius: float = aperture / 2
        vfov_rad: float = vfov * math.pi / 180
        half_height: float = math.tan(vfov_rad / 2)
        half_width: float = aspect_ratio * half_height
        # The following are just some vectors to define axes. Don't be confused!
        self.__w = (camera_posn - camera_aim).unit_vector()
        self.__u = up_vector.cross(self.__w).unit_vector()
        self.__v = self.__w.cross(self.__u)
        super().__init__(
            camera_posn - focus_dist * (
                (half_width * self.__u) + (half_height * self.__v) + self.__w
            ),
            2 * half_width * focus_dist * self.__u,
            2 * half_height * focus_dist * self.__v,
            camera_posn
        )

    # Minor note: the change in parameter names, because u and v take on a new
    # meaning in this class.
    def get_ray(self, s: float, t: float) -> Ray:
        random_point_in_disc: Vec3 = random_in_unit_disk() * self.lens_radius
        offset: Vec3 = (
            self.__u * random_point_in_disc.x +
            self.__v * random_point_in_disc.y
        )
        return Ray(
            self.origin + offset,
            self.lower_left_corner + (self.h_movement * s) +
            (self.v_movement * t) - self.origin - offset
        )

def irandom_in_unit_disk() -> Vec3:
    point: Vec3 = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), 0)
    
    while point.dot(point) >= 1:
        point = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), 0)

    return point

def random_in_unit_disk() -> Vec3:
    point: Vec3 = 2 * Vec3(random.random(), random.random(), 0) - Vec3(1, 1, 0)

    while point.dot(point) >= 1:
        point = 2 * Vec3(random.random(), random.random(), 0) - Vec3(1, 1, 0)

    return point
