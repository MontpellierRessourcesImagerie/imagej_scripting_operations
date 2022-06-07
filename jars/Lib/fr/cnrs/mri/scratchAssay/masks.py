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
        self.calculateFeature()
        self.setThresholds()
        self.convertToMask()

    def calculateFeature(self):
        pass

    def setThresholds(self):
        pass

    def convertToMask(self):
        ij.convertToMask(self.getResultImage(), method="Default", background="Dark", black=True)    
        
    
class CreateMaskFromVariance(CreateMask):

    radiusLabel = "radius"
    thresholdLabel = "threshold"
    
    def __init__(self, radius, threshold):
        CreateMask.__init__(self)
        self.addOption(IntOption(CreateMaskFromVariance.radiusLabel, radius))
        self.addOption(IntOption(CreateMaskFromVariance.thresholdLabel, threshold))

    def calculateFeature(self):
        ij.variance(self.getResultImage(), radius = self.getRadius(), stack = True)
        ij._8__bit(self.getResultImage())

    def getRadius(self):
        return self.getOption(CreateMaskFromVariance.radiusLabel).getValue()
        
    def getThreshold(self):
        return self.getOption(CreateMaskFromVariance.thresholdLabel).getValue()
        
    def setThresholds(self):
        IJ.setThreshold(self.getResultImage(), 0, self.getThreshold())
    
class CreateMaskFromFindEdges(CreateMask):

    def __init__(self):
        CreateMask.__init__(self)

    def calculateFeature(self):
        mask = self.getResultImage()
        ij.findEdges(mask, stack = True)
        ij.invert(mask, stack = True)
        if mask.bitDepth==24:
            ij._8__bit(mask)

    def setThresholds(self):
        IJ.setAutoThreshold(self.getResultImage(), "Percentile dark");
