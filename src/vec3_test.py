from src.vec3 import Vec3

import unittest

class Vec3Test(unittest.TestCase):

    def test_cross(self):
        a = Vec3(2.0, 1.0, -1.0)
        b = Vec3(-3.0, 4.0, 1.0)

        axb = a.cross(b)
        self.assertEqual(Vec3(5.0, 1.0, 11.0), axb)

        bxa = b.cross(a)
        self.assertEqual(Vec3(-5.0, -1.0, -11.0), bxa)

    def test_dot(self):
        a = Vec3(2.0, 1.0, -1.0)
        b = Vec3(-3.0, 4.0, 1.0)

        adb = a.dot(b)
        expected = sum((
            a.x * b.x, a.y * b.y, a.z * b.z
        ))
        self.assertEqual(expected, adb)

    def test_itruediv(self):
        a = Vec3(3, 6, 9)
        lowest_terms_a = Vec3(1, 2, 3)
        a /= 3
        self.assertEqual(lowest_terms_a, a)

if __name__ == "__main__":
    unittest.main()
