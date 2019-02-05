from abc import ABC, abstractmethod
from src.ray import Ray
from src.vec3 import Vec3
from typing import List, Optional

class HitRecord(object):
    """
    At this point it's still a bit unclear to me what this class is for. But
    I'll hazard a guess that t is the "time input variable" (also unclear as to
    what that means) and p is the point at which the ray hit our object.
    """

    def __init__(self, t: float, p: Vec3, normal: Vec3):
        self.t = t
        self.p = p
        self.normal = normal

class Hittable(ABC):

    @abstractmethod
    def hit(self, ray: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        """
        Check whether the given Ray hits this object. Return a HitRecord if it
        does, otherwise None.

        Note that this deviates from the C++ code since the C++ code makes use
        of side-effects to "return" the HitRecord. I find this signature more
        Pythonic than relying on side-effects like that.
        """
        pass

class HittableList(Hittable):

    def __init__(self, hittables: List[Hittable]):
        self.hittables: List[Hittable] = hittables

    def hit(self, ray: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        hit_attempt: Optional[HitRecord] = None
        closest_so_far: float = t_max

        for hittable in self.hittables:
            hit_attempt = hittable.hit(ray, t_min, closest_so_far)
            if hit_attempt is not None:
                closest_so_far = hit_attempt.t

        return hit_attempt
