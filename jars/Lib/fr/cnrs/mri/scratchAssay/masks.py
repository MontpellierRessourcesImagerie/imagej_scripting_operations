from ij import IJ
from fr.cnrs.mri.commandProxy import IJCP
from ij import Prefs

ij = IJCP()

class CreateMask(object):

    def __init__(self, image):
        self.inputImage = image
        self.mask = image.duplicate()

    def run(self):
        self.calculateFeature()
        self.setThresholds()
        self.convertToMask()

    def calculateFeature(self):
        pass

    def setThresholds(self):
        pass

    def convertToMask(self):
        ij.convertToMask(self.mask, method="Default", background="Dark", black=True)    
        
    def getMask(self):
        return self.mask
    
class CreateMaskFromVariance(CreateMask):

    def __init__(self, image, radius, threshold):
        CreateMask.__init__(self, image)
        self.radius = radius
        self.threshold = threshold

    def calculateFeature(self):
        ij.variance(self.mask, radius = self.radius, stack = True)
        ij._8__bit(self.mask)

    def setThresholds(self):
        IJ.setThreshold(self.mask, 0, self.threshold);   
    
class CreateMaskFromFindEdges(CreateMask):

    def __init__(self, image):
        CreateMask.__init__(self, image)

    def calculateFeature(self):
        ij.findEdges(self.mask, stack = True)
        ij.invert(self.mask, stack = True)
        if self.mask.bitDepth==24:
            ij._8__bit(self.mask)

    def setThresholds(self):
        IJ.setAutoThreshold(self.mask, "Percentile dark");
