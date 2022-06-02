from ij import IJ
from ij import Prefs
from fr.cnrs.mri.ijso.operations import Operation
from fr.cnrs.mri.ijso.operations import IntOption
from fr.cnrs.mri.ijso.commandProxy import IJCP

ij = IJCP()

class CreateMask(Operation):

    def __init__(self):
        Operation.__init__(self)

    def execute(self):
        self.mask = self.inputImage.duplicate()
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

    radiusLabel = "radius"
    thresholdLabel = "threshold"
    
    def __init__(self, radius, threshold):
        CreateMask.__init__(self)
        self.addOption(IntOption(CreateMaskFromVariance.radiusLabel, radius))
        self.addOption(IntOption(CreateMaskFromVariance.thresholdLabel, threshold))

    def calculateFeature(self):
        ij.variance(self.mask, radius = self.getRadius(), stack = True)
        ij._8__bit(self.mask)

    def getRadius(self):
        return self.getOption(CreateMaskFromVariance.radiusLabel).getValue()
        
    def getThreshold(self):
        return self.getOption(CreateMaskFromVariance.thresholdLabel).getValue()
        
    def setThresholds(self):
        IJ.setThreshold(self.mask, 0, self.getThreshold())
    
class CreateMaskFromFindEdges(CreateMask):

    def __init__(self):
        CreateMask.__init__(self)

    def calculateFeature(self):
        ij.findEdges(self.mask, stack = True)
        ij.invert(self.mask, stack = True)
        if self.mask.bitDepth==24:
            ij._8__bit(self.mask)

    def setThresholds(self):
        IJ.setAutoThreshold(self.mask, "Percentile dark");
