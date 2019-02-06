from src.hittable import HitRecord, Hittable
from src.ray import Ray
from src.vec3 import Vec3
from typing import Optional

import math

class Sphere(Hittable):

    def __init__(self, center: Vec3, radius: float, name: Optional[str]=None):
        self.center: Vec3 = center
        self.radius: float = radius
        self.name: str = "unnamed"
        if name is not None:
            self.name = name

    def __decide_conjugate(
        self, t_min: float, t_max: float, neg_conjugate: float,
        pos_conjugate: float
    ) -> Optional[float]:
        # TODO Experiment: Check for pos_conjugate first. What happens?
        if t_min < neg_conjugate < t_max:
            return neg_conjugate
        elif t_min < pos_conjugate < t_max:
            return pos_conjugate
        else:
            return None

    def hit(self, ray: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        origin_to_center: Vec3 = ray.origin - self.center
        # The following are just "components" of the quadratic formula, derived
        # from vectors and with some redundant 2's canceled out to begin with.
        a: float = ray.direction.dot(ray.direction)
        b: float = origin_to_center.dot(ray.direction)
        c: float = origin_to_center.dot(origin_to_center) - (self.radius ** 2)
        discriminant: float = (b ** 2) - (a * c)

        if discriminant > 0:
            neg_conjugate: float = (-b - math.sqrt(discriminant)) / a
            # The original C++ code, again, saves on stack space by re-using a
            # generic variable `temp`. But heh, I figured can't I skimp a bit on
            # the manual optimization and leave that up to the interpeter?
            pos_conjugate: float = (-b + math.sqrt(discriminant)) / a

            # Also this code was "refactored" from the original C++ to read more
            # Pythonic.
            chosen_conjugate = self.__decide_conjugate(
                t_min, t_max, neg_conjugate, pos_conjugate
            )
            if chosen_conjugate is not None:
                t = chosen_conjugate
                p = ray.point_at_parameter(t)
                normal = (p - self.center) / self.radius
                return HitRecord(t, p, normal, self.name)
        
        return None
