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
