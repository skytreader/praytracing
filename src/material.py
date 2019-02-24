from abc import ABC, abstractmethod
from src.hittable import *
from src.ray import Ray
from src.vec3 import Vec3

import random

class ReflectionRecord(object):
    """
    Records the details of a reflection.

    Attenuation is how much flux/intensity was lost by the incident ray once it
    is reflected.

    Scattering is just the Ray that resulted from the relfection.
    """

    def __init__(self, attenuation: Vec3, scattering: Ray):
        self.attenuation: Vec3 = attenuation
        self.scattering: Ray = scattering

class Material(ABC):

    @abstractmethod
    def scatter(self, incident_ray: Ray, record: "HitRecord") -> ReflectionRecord:
        """
        Computes the resulting reflection when the given incident_ray bounces
        off this material. The details of the hit is recorded in the record
        parameter.
        """
        pass

class Vanta(Material):
    """
    This material reflects nothing. This can be used as an "identity" material
    for when you are not really after a reflection in your code (e.g., previous
    chapters in the text).

    So, really, this is just for backwards compatibility. :)
    """

    def scatter(self, incident_ray: Ray, record: "HitRecord") -> ReflectionRecord:
        return ReflectionRecord(Vec3(0, 0, 0), incident_ray)

class Lambertian(Material):
    
    def __init__(self, albedo: Vec3):
        self.albedo: Vec3 = albedo

    def scatter(self, incident_ray: Ray, record: "HitRecord") -> ReflectionRecord:
        # Lots of Physics I don't understand :\
        target: Vec3 = record.p + record.normal + random_unit_sphere_point()
        scattered: Ray = Ray(record.p, target - record.p)
        attenuation: Vec3 = self.albedo
        reflecord: ReflectionRecord = ReflectionRecord(attenuation, scattered)
        return reflecord

class Metal(Material):

    def __init__(self, albedo: Vec3):
        self.albedo: Vec3  = albedo

    def __reflect(self, v: Vec3, n: Vec3) -> Vec3:
        return v - 2 * v.dot(n) * n

    def scatter(self, incident_ray: Ray, record: "HitRecord") -> ReflectionRecord:
        reflected: Vec3 = self.__reflect(
            incident_ray.direction.unit_vector(), record.normal
        )
        scattered: Ray = Ray(record.p, reflected)
        return ReflectionRecord(self.albedo, scattered)


def random_unit_sphere_point() -> Vec3:
    """
    Pick a random point inside a unit sphere. To do this, we use a "rejection
    method":

    1. Pick a random point inside a cube with edges in the [-1, 1] range of all
    axes. Note that the unit sphere is inside this cube and this cube is "easy"
    to construct programmatically.
    2. Check whether the point is inside the unit sphere. If it is not, generate
    again. Do this until we get a point inside the unit sphere.

    The time complexity of this procedure is left as an exercise to the reader.
    """
    # Shirley uses the following formula to generate a random point in the
    # constraints specified:
    #   2 * rand_vector - unit_vector
    # Where rand_vector has components that range from [0, 1). While this is
    # understandable enough, I'm experimenting with random.uniform instead.
    rand_point: Vec3 = Vec3(
        random.uniform(-1, 1),
        random.uniform(-1, 1),
        random.uniform(-1, 1)
    )

    while rand_point.squared_length() >= 1:
        rand_point = Vec3(
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        )

    return rand_point
