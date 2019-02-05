from abc import ABC, abstractmethod
from src.ray import Ray
from src.vec3 import Vec3
from typing import List

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
    def hit(self, ray: Ray, t_min: float, t_max: float, record: HitRecord) -> bool:
        pass

class HittableList(Hittable):

    def __init__(self, hittables: List[Hittable]):
        self.hittables: List[Hittable] = hittables

    def hit(self, ray: Ray, t_min: float, t_max: float, record: HitRecord) -> bool:
        # Just a sentinel variable, we don't really care what this is initialized
        # to since it will just be repeatedly overwritten as it is used.
        rover_record: HitRecord = HitRecord(
            0.0, Vec3(0, 0, 0), Vec3(1, 1, 1)
        )
        hit_anything: bool = False
        closest_so_far: float = t_max

        for hittable in self.hittables:
            if hittable.hit(ray, t_min, t_max, rover_record):
                hit_anything = True
                closest_so_far = rover_record.t
                record = rover_record

        return hit_anything
