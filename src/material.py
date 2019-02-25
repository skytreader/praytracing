from abc import ABC, abstractmethod
from src.hittable import *
from src.ray import Ray
from src.vec3 import Vec3
from typing import Optional

import math
import random

# FIXME Rename this to ScatteringRecord. I'm just too lazy right now.
class ReflectionRecord(object):
    """
    Records how a ray scatters after it hits a material. Inaccurately named as
    that can be either reflection or refraction.

    Attenuation is how much flux/intensity was lost by the incident ray once it
    is reflected.

    Scattering is just the Ray that resulted from the reflection.
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
    This material reflects nothing.

    See also: https://www.surreynanosystems.com/vantablack
    """

    def scatter(self, incident_ray: Ray, record: "HitRecord") -> ReflectionRecord:
        return ReflectionRecord(Vec3(0, 0, 0), incident_ray)

class Identity(Material):
    """
    This material reflects everything.
    """

    def scatter(self, incident_ray: Ray, record: "HitRecord") -> ReflectionRecord:
        return ReflectionRecord(Vec3(1, 1, 1), incident_ray)

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

    def __init__(self, albedo: Vec3, fuzz: float):
        self.albedo: Vec3  = albedo
        self.fuzz: float = fuzz if fuzz < 1 else 1

    def scatter(self, incident_ray: Ray, record: "HitRecord") -> ReflectionRecord:
        reflected: Vec3 = reflect(
            incident_ray.direction.unit_vector(), record.normal
        )
        scattered: Ray = Ray(
            record.p, reflected + self.fuzz * random_unit_sphere_point()
        )
        return ReflectionRecord(self.albedo, scattered)

class Dielectric(Material):

    def __init__(self, refractive_index: float):
        self.refractive_index: float = refractive_index

    def __schlick_approximation(self, cosine: float):
        r0 : float = (1 - self.refractive_index) / (1 + self.refractive_index) ** 2
        return r0 + (1 - r0) * (1 - cosine) ** 5

    def scatter(self, incident_ray: Ray, record: "HitRecord") -> ReflectionRecord:
        reflected: Vec3 = reflect(incident_ray.direction, record.normal)
        attenuation: Vec3 = Vec3(1, 1, 0)

        # These are just placeholders; the following conditional block is their
        # actual "initial values".
        outward_normal: Vec3 = Vec3(1, 1, 1)
        nint: float = 0
        cosine: float = 0

        if incident_ray.direction.dot(record.normal) > 0:
            outward_normal = -1 * record.normal
            nint = self.refractive_index
            cosine = (
                self.refractive_index * incident_ray.direction.dot(record.normal) /
                incident_ray.direction.length()
            )
        else:
            outward_normal = record.normal
            nint = 1 / self.refractive_index
            cosine = -(
                incident_ray.direction.dot(record.normal) / incident_ray.direction.length()
            )

        refracted: Optional[Vec3] = refract(
            incident_ray.direction, outward_normal, nint
        )
        reflection_probability: float = 1
        if refracted is not None:
            reflection_probability = self.__schlick_approximation(cosine)

        if reflection_probability == 1:
            return ReflectionRecord(attenuation, Ray(record.p, reflected))
        else:
            return ReflectionRecord(attenuation, Ray(record.p, refracted))


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

# TODO What is the n parameter in reflect and refract?
def reflect(v: Vec3, n: Vec3) -> Vec3:
    return v - 2 * v.dot(n) * n

# TODO Will nint be the ratio of refractive indices? --> VERIFY!
def refract(v: Vec3, n: Vec3, nint: float) -> Optional[Vec3]:
    """
    Return the refracting ray if the conditions are good for refraction. If it
    does not describe a refracting scenario, return None.
    """
    uv: Vec3 = v.unit_vector()
    dt: float = uv.dot(n)
    discriminant: float = 1 - (nint ** 2) * (1 - dt ** 2)

    if discriminant > 0:
        return (
            nint * (uv - n * dt) - n * math.sqrt(discriminant)
        )

    return None
