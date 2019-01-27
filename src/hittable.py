from abc import ABC, abstractmethod
from src.ray import Ray
from src.vec3 import Vec3

class HitRecord(object):

    def __init__(self, t: float, p: Vec3, normal: Vec3):
        self.t = t
        self.p = p
        self.normal = normal

class Hittable(ABC):

    @abstractmethod
    def hit(self, ray: Ray, t_min: float, t_max: float, record: HitRecord) -> bool:
        pass
