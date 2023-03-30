from one_week.vec3 import Vec3

class Ray(object):
    
    def __init__(self, a: Vec3, b: Vec3):
        self.a = a
        self.b = b

    @property
    def origin(self):
        return self.a

    @property
    def direction(self):
        return self.b

    def point_at_parameter(self, t: float) -> Vec3:
        """
        Get a particular point in the 3D line represented by this Ray.
        """
        return self.a + (t * self.b)
