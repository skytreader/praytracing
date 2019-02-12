from abc import ABC, abstractmethod
from src.ray import Ray
from src.vec3 import Vec3

class Material(ABC):
    from src.hittable import HitRecord

    @abstractmethod
    def scatter(
        self,
        incident_ray: Ray,
        record: HitRecord,
        attenuation: Vec3, 
        scattered_ray: Ray
    ) -> bool:
        pass
