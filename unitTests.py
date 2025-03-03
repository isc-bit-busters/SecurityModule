import unittest
import numpy as np
from unittest.mock import patch

from workingAreaChecking import Sphere


class unitTests(unittest.TestCase):
    
    def setUp(self):
        self.sphere = Sphere(0, 0, 0, 500)
        
    def test_isPointInHalfOfSphere(self):   
        # Test if the point is in the upper hemisphere
        self.assertFalse(self.sphere.isPointInHalfOfSphere((-100, -100, 100)))
        
        # Test if the point is within the sphere's radius
        self.assertTrue(self.sphere.isPointInHalfOfSphere((0, 0, 500)))
        
        # Test if the point is in the upper hemisphere and within the sphere's radius
        self.assertFalse(self.sphere.isPointInHalfOfSphere((0, 0, -500)))
        
        self.assertFalse(self.sphere.isPointInHalfOfSphere((0, -500, 0)))
        
        self.assertTrue(self.sphere.isPointInHalfOfSphere((0, 0, 0)))
        
        self.assertFalse(self.sphere.isPointInHalfOfSphere((500, 500, 0)))
        
        self.assertTrue(self.sphere.isPointInHalfOfSphere((500, 0, 0)))
        
        self.assertTrue(self.sphere.isPointInHalfOfSphere((450, 0, 50)))
        
        self.assertFalse(self.sphere.isPointInHalfOfSphere((450,250,50)))
    
    def test_areInHalfOfSphere(self):
        # Test if the points are in the upper hemisphere
        self.assertEqual(self.sphere.areInHalfOfSphere([(-100, -100, 100), (0, 0, 500), (0, 0, -500)]), [False, True, False])
        
    def test_areAllInHalfOfSphere(self):
        # Test if all points are in the upper hemisphere
        self.assertFalse(self.sphere.areAllInHalfOfSphere([(-100, -100, 100), (0, 0, 500), (0, 0, -500)]))
    
    
    
if __name__ == '__main__':
    unittest.main()