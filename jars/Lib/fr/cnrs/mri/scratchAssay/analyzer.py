from ij import IJ
from ij.plugin.frame import RoiManager
from ij.measure import ResultsTable
from fr.cnrs.mri.ijso.commandProxy import IJCP
from fr.cnrs.mri.ijso.operations import Operation
from fr.cnrs.mri.scratchAssay.masks import CreateMaskFromVariance

ij = IJCP()
 
class ScratchAssayAnalyzer(Operation):
    
    def __init__(self, image):
        Operation.__init__(self)
        self.measureInPixlUnits = False
        self.inputImage = image
        self.createMaskMethod = None
        self.closeIterations = None
        self.minimalArea = None
        
    def getRois(self):
        return self.rois
        
    def setCreateMaskMethod(self, createMaskMethod):
        self.createMaskMethod = createMaskMethod

    def getCreateMaskMethod(self):
        if not self.createMaskMethod:
            self.createMaskMethod = CreateMaskFromVariance(self.inputImage, 20, 1) 
        return self.createMaskMethod
    
    def setMeasureInPixelUnits(self):
        self.measureInPixlUnits = True

    def setCloseIterations(self, iterations):
        self.closeIterations = iterations

    def getCloseIterations(self):
        if not self.closeIterations:
            self.closeIterations = 4
        return self.closeIterations
        
    def setMinimalArea(self, area):
        self.minimalArea = area
        
    def getMinimalArea(self):
        if not self.minimalArea:
            self.minimalArea = 999999
        return self.minimalArea
        
    def execute(self):
        self.setStatus("scratch segmentation started...")
        self.setProgress(0.0)
        mask = self.createMask()
        self.setProgress(0.25)
        self.morphologicalCloseOnTissue(mask)
        self.setProgress(0.5)
        self.createRoisOfGaps(mask)
        self.setProgress(0.75)
        self.measure()
        self.setProgress(1.0)
        self.setStatus("...scratch segmentation finished")

    def measure(self):
        self.setStatus("measue")
        ResultsTable.getResultsTable().reset() 
        RoiManager.getInstance().runCommand("measure")
    
    def createMask(self):
        self.setStatus("create mask")
        self.getCreateMaskMethod().run()
        return self.getCreateMaskMethod().getMask()
        
    def morphologicalCloseOnTissue(self, mask):
        self.setStatus("morphological close on tissue")
        ij.options(mask, do="Open", iterations=self.getCloseIterations(), count=1, stack=True, pad=True, black=True)
        ij.options(mask, do="Nothing", iterations=1, count=1, black=True)

    def createRoisOfGaps(self, mask):
        self.setStatus("create rois of gaps")
        roiManager = RoiManager.getRoiManager()
        roiManager.reset()
        ij.analyzeParticles(mask, size=str(self.getMinimalArea())+"-Infinity", circularity="0.00-1.00", show="Nothing", add=True, stack=True)
        roiManager.runCommand(self.inputImage, "Show All")
        self.rois = list(RoiManager.getInstance().getRoisAsArray())
