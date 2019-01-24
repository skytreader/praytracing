class Vec3(object):

    def __init__(self, r: float=0.0, g: float=0.0, b: float=0.0):
        self.r = r
        self.g = g
        self.b = b

    @property
    def x(self):
        return self.r

    @property
    def y(self):
        return self.g

    @property
    def z(self):
        return self.b

    def __add__(self, other):
        return Vec3(self.r + other.r, self.g + other.g, self.b + other.b)

    def __sub__(self, other):
        return Vec3(self.r - other.r, self.g - other.g, self.b - other.b)

    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.r * other.r, self.g - other.g, self.b - other.b)
        else:
            return Vec3(self.r * other, self.g * other, self.b * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.r / other.r, self.g - other.g, self.b - other.b)
        else:
            return Vec3(self.r / other, self.g / other, self.b / other)

    def make_tuple(self):
        return (self.r, self.g, self.b)

    def dot(self, other):
        return sum((self * other).make_tuple())

    def cross(self, other):
        return Vec3(
            self.g * other.b - self.b * other.g,
            -(self.r * other.b - self.b * other.r),
            self.r * other.g - self.g * other.r
        )

    def __iadd__(self, other):
        self.r += other.r
        self.g += other.g
        self.b += other.b
        return self

    def __isub__(self, other):
        self.r -= other.r
        self.g -= other.g
        self.b -= other.b
        return self

    def __imul__(self, other):
        if type(other) is type(self):
            self.r *= other.r
            self.g *= other.g
            self.b *= other.b
        else:
            self.r *= other
            self.g *= other
            self.b *= other

        return self

    def __idiv__(self, other):
        if type(other) is type(self):
            self.r /= other.r
            self.g /= other.g
            self.b /= other.b
        else:
            self.r /= other
            self.g /= other.g
            self.b /= other.b

        return self

    def unit_vector(self):
        return self / 3.0

    def __eq__(self, other):
        return (
            self.r == other.r and self.g == other.g and self.b and other.b
        )

    def map(self, fn):
        self.r = fn(self.r)
        self.g = fn(self.g)
        self.b = fn(self.b)
        return self
