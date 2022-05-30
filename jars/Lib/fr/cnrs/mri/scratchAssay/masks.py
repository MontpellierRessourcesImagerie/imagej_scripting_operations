from ij import IJ
from ij import Prefs
from fr.cnrs.mri.ijso.operations import Operation
from fr.cnrs.mri.ijso.operations import IntOption
from fr.cnrs.mri.ijso.commandProxy import IJCP

ij = IJCP()

class CreateMask(Operation):

    def __init__(self, image):
        Operation.__init__(self)
        self.inputImage = image
        self.mask = image.duplicate()

    def execute(self):
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
        self.addOption(IntOption("radius", radius))
        self.addOption(IntOption("threshold", threshold))

    def calculateFeature(self):
        ij.variance(self.mask, radius = self.getRadius(), stack = True)
        ij._8__bit(self.mask)

    def getRadius(self):
        return self.getOptions().get('radius').getValue()
        
    def getThreshold(self):
        return self.getOptions().get('threshold').getValue()
        
    def setThresholds(self):
        IJ.setThreshold(self.mask, 0, self.getThreshold())
    
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
