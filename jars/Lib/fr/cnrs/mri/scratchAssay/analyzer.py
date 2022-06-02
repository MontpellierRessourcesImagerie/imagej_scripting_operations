from ij import IJ
from ij.plugin.frame import RoiManager
from ij.measure import ResultsTable
from fr.cnrs.mri.ijso.commandProxy import IJCP
from fr.cnrs.mri.ijso.operations import Operation
from fr.cnrs.mri.ijso.operations import ChoiceOption
from fr.cnrs.mri.ijso.operations import BoolOption
from fr.cnrs.mri.ijso.operations import IntOption
from fr.cnrs.mri.scratchAssay.masks import CreateMaskFromVariance
from fr.cnrs.mri.scratchAssay.masks import CreateMaskFromFindEdges

ij = IJCP()
 
class ScratchAssayAnalyzer(Operation):
    
    methodOptionLabel = "method"
    measureInPixelUnitsLabel = "measure in pixel units"
    closeIterationsLabel = "radius close"
    minAreaLabel = "min. area"
    
    def __init__(self):
        Operation.__init__(self)
        items = [CreateMaskFromVariance(20, 1), CreateMaskFromFindEdges()]
        self.addOption(ChoiceOption(ScratchAssayAnalyzer.methodOptionLabel, items[0], items))
        self.addOption(BoolOption(ScratchAssayAnalyzer.measureInPixelUnitsLabel, False))
        self.addOption(IntOption(ScratchAssayAnalyzer.closeIterationsLabel, 4))
        self.addOption(IntOption(ScratchAssayAnalyzer.minAreaLabel, 999999))
        
    def getRois(self):
        return self.rois
        
    def setCreateMaskMethod(self, createMaskMethod):
        self.getOption(ScratchAssayAnalyzer.methodOptionLabel).setValue(createMaskMethod)

    def getCreateMaskMethod(self):
        return self.getOption(ScratchAssayAnalyzer.methodOptionLabel).getValue()
    
    def getMeasureInPixelUnits(self):
        return self.getOption(ScratchAssayAnalyzer.measureInPixelUnitsLabel).getValue()
    
    def setMeasureInPixelUnits(self, value):
        self.getOption(ScratchAssayAnalyzer.measureInPixelUnitsLabel).setValue(value)
        
    def setCloseIterations(self, iterations):
        self.getOption(ScratchAssayAnalyzer.closeIterationsLabel).setValue(iterations)

    def getCloseIterations(self):
        return self.getOption(ScratchAssayAnalyzer.closeIterationsLabel).getValue()
        
    def setMinimalArea(self, area):
        self.getOption(ScratchAssayAnalyzer.minAreaLabel).setValue(area)
        
    def getMinimalArea(self):
        return self.getOption(ScratchAssayAnalyzer.minAreaLabel).getValue()
        
    def execute(self):
        self.setStatus("scratch segmentation started...")
        mask = self.createMask()
        self.morphologicalCloseOnTissue(mask)
        self.createRoisOfGaps(mask)
        self.measure()
        self.setStatusAndProgress("...scratch segmentation finished", 1.0)

    def createMask(self):
        self.setStatus("create mask")
        createMaskMethod = self.getCreateMaskMethod()
        createMaskMethod.setInputImage(self.inputImage)
        createMaskMethod.run()
        self.setProgress(0.25)
        return createMaskMethod.getMask()
        
    def morphologicalCloseOnTissue(self, mask):
        self.setStatus("morphological close on tissue")
        ij.options(mask, do="Open", iterations=self.getCloseIterations(), count=1, stack=True, pad=True, black=True)
        ij.options(mask, do="Nothing", iterations=1, count=1, black=True)
        self.setProgress(0.5)

    def createRoisOfGaps(self, mask):
        self.setStatus("create rois of gaps")
        roiManager = RoiManager.getRoiManager()
        roiManager.reset()
        ij.analyzeParticles(mask, size=str(self.getMinimalArea())+"-Infinity", circularity="0.00-1.00", show="Nothing", add=True, stack=True)
        roiManager.runCommand(self.inputImage, "Show All")
        self.rois = list(RoiManager.getInstance().getRoisAsArray())        
        self.setProgress(0.75)
    
    def measure(self):
        self.setStatus("measue")
        ResultsTable.getResultsTable().reset() 
        RoiManager.getInstance().runCommand("measure")
        self.setProgress(1)

