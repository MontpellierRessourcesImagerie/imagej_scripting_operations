import unittest, math, sys, pprint
from fr.cnrs.mri.scratchAssay.masks import CreateMaskFromVariance
from ij.macro import Interpreter 
from ij import IJ

class CreateMaskFromVarianceTest(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        IJ.run("Close All");
        self.image =  IJ.createImage("Untitled", "8-bit ramp", 16, 16, 1)
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        IJ.run("Close All");
        self.image.close()
        
    def testConstructor(self):
        createMask = CreateMaskFromVariance(self.image, 20, 1)
        self.assertEquals(createMask.inputImage, self.image)
        self.assertEquals(createMask.getMask().getWidth(), self.image.getWidth())
        self.assertEquals(createMask.radius, 20)
        self.assertEquals(createMask.threshold, 1)

    def testSetThresholds(self):
        createMask = CreateMaskFromVariance(self.image, 20, 3)
        createMask.setThresholds()
        self.assertEquals(createMask.getMask().getProcessor().getMinThreshold(), 0)
        self.assertEquals(createMask.getMask().getProcessor().getMaxThreshold(), 3)
    
def suite():
    suite = unittest.TestSuite()

    suite.addTest(CreateMaskFromVarianceTest('testConstructor'))
    suite.addTest(CreateMaskFromVarianceTest('testSetThresholds'))
    return suite

runner = unittest.TextTestRunner(sys.stdout, verbosity=1)
runner.run(suite())