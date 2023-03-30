from abc import ABC, abstractmethod
from one_week.material import Material, Vanta
from one_week.ray import Ray
from one_week.vec3 import Vec3
from typing import List, Optional

class HitRecord(object):
    """
    At this point it's still a bit unclear to me what this class is for. But
    I'll hazard a guess that t is the "time input variable" (also unclear as to
    what that means) and p is the point at which the ray hit our object.
    """

    def __init__(
        self,
        t: float,
        p: Vec3,
        normal: Vec3,
        material: Optional[Material]=None,
        hit_object: Optional[str]=None
    ):
        """
        Note that even if material is set to None, `self.material` will be set
        to the identity material, Vanta. The philosophy of this class is that
        you do not need to have explicit `None` checks in your code.
        """
        self.t: float = t
        self.p: Vec3 = p
        self.normal: Vec3 = normal
        self.material: Material = material or Vanta()
        self.hit_object: str = "unspecified"
        if hit_object is not None:
            self.hit_object = hit_object

class Hittable(ABC):

    def __init__(self, material: Optional[Material]=None):
        self.material: Material = material or Vanta()

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
        """
        Tries to hit each object in self.hittables. The hit record will contain
        the object closest to the source of the Ray.
        """
        hit_attempt: Optional[HitRecord] = None
        # Note how closest_so_far works: it relies on the assumption that the
        # Hittable objects in self.hittables respect t_min and t_max properly.
        closest_so_far: float = t_max

        for hittable in self.hittables:
            hit_attempt = hittable.hit(ray, t_min, closest_so_far) or hit_attempt
            if hit_attempt is not None:
                # At every possible hit, we record the parameter t which gave us
                # the hit. We are sure we can hit this object at this t value
                # and so it is recorded. Then, the t value is set as the t_max
                # for the next possible hit, limiting the propagation of the
                # ray. This process is repeated until all objects have been
                # tested. No sorting needed!
                closest_so_far = hit_attempt.t

        return hit_attempt
