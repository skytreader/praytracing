import math

class Vec3(object):
    """
    **Confusing terminology time!** One of the simplest (and maybe earliest-
    encountered) definition of the term _vector_ is _magnitude with direction_.
    This is in contrast with scalars which are plain magnitudes. But this object
    is more a point in 3D-space with no direction in sight (magnitude can be
    taken as the length, as defined in a method below).

    This represents vectors in the î, ĵ, k-hat sense: they are vectors with the
    origin implied to be at (0, 0, 0). And hence they have magnitude _and_
    direction. This "normalizes" vectors that originate from any point in space.
    """

    def __init__(self, r: float=0.0, g: float=0.0, b: float=0.0):
        self.r: float = r
        self.g: float = g
        self.b: float = b

    @property
    def x(self):
        return self.r

    @property
    def y(self):
        return self.g

    @property
    def z(self):
        return self.b

    def length(self) -> float:
        """
        Would've used the __len__ method, but this could return a float and, by
        convention, __len__ should return an integer.
        """
        return math.sqrt(
            self.r ** 2 + self.g ** 2 + self.b ** 2
        )

    def squared_length(self) -> float:
        return self.r ** 2 + self.g ** 2 + self.b ** 2

    def __add__(self, other) -> "Vec3":
        return Vec3(self.r + other.r, self.g + other.g, self.b + other.b)

    def __sub__(self, other) -> "Vec3":
        return Vec3(self.r - other.r, self.g - other.g, self.b - other.b)

    def __mul__(self, other) -> "Vec3":
        if isinstance(other, Vec3):
            return Vec3(self.r * other.r, self.g * other.g, self.b * other.b)
        else:
            return Vec3(self.r * other, self.g * other, self.b * other)

    def __rmul__(self, other) -> "Vec3":
        return self.__mul__(other)

    def __truediv__(self, other) -> "Vec3":
        if isinstance(other, Vec3):
            return Vec3(self.r / other.r, self.g - other.g, self.b - other.b)
        else:
            return Vec3(self.r / other, self.g / other, self.b / other)

    def make_tuple(self) -> tuple:
        return (self.r, self.g, self.b)

    def dot(self, other) -> float:
        return sum((self * other).make_tuple())

    def cross(self, other) -> "Vec3":
        return Vec3(
            self.g * other.b - self.b * other.g,
            -(self.r * other.b - self.b * other.r),
            self.r * other.g - self.g * other.r
        )

    def __iadd__(self, other) -> "Vec3":
        self.r += other.r
        self.g += other.g
        self.b += other.b
        return self

    def __isub__(self, other) -> "Vec3":
        self.r -= other.r
        self.g -= other.g
        self.b -= other.b
        return self

    def __imul__(self, other) -> "Vec3":
        if isinstance(other, Vec3):
            self.r *= other.r
            self.g *= other.g
            self.b *= other.b
        else:
            self.r *= other
            self.g *= other
            self.b *= other

        return self

    def __itruediv__(self, other) -> "Vec3":
        if isinstance(other, Vec3):
            self.r /= other.r
            self.g /= other.g
            self.b /= other.b
        else:
            self.r /= other
            self.g /= other
            self.b /= other

        return self

    def unit_vector(self) -> "Vec3":
        return self / self.length()

    def __eq__(self, other) -> bool:
        return (
            self.r == other.r and self.g == other.g and self.b == other.b
        )

    def map(self, fn) -> "Vec3":
        self.r = fn(self.r)
        self.g = fn(self.g)
        self.b = fn(self.b)
        return self

    def __str__(self):
        return "(%s, %s, %s)" % (self.r, self.g, self.b)
