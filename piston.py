#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Fri, 26 Jun 2015 14:04:27
#========================================
import sys, math
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

PISTON_NODE_NAME = 'piston'
PISTON_NODE_ID   = OpenMaya.MTypeId(0x100ffff)


class Piston(OpenMayaMPx.MPxNode):
    '''
    '''
    def __init__(self):
        super(Piston, self).__init__()
        
        
    def compute(self, plug, dataBlock):
        sita = dataBlock.inputValue(self.inRotate).asFloat() * math.pi / 180.0
        A    = dataBlock.inputValue(self.inLengthA).asFloat()
        B    = dataBlock.inputValue(self.inLengthB).asFloat()

        H = math.cos(sita) * B + math.sqrt(A**2 - (math.sin(sita) * B)**2)
        
        outAttr = dataBlock.outputValue(self.output)
        outAttr.setFloat(H)
        dataBlock.setClean(plug)



def nodeCreator():
    return OpenMayaMPx.asMPxPtr(Piston())



def nodeInitializer():
    mFnAttr = OpenMaya.MFnNumericAttribute()
    
    Piston.inLengthA = mFnAttr.create('distanceA', 'disa', OpenMaya.MFnNumericData.kFloat, 0.0)
    Piston.inLengthB = mFnAttr.create('distanceB', 'disb', OpenMaya.MFnNumericData.kFloat, 0.0)
    Piston.inRotate  = mFnAttr.create('rotate',    'r',    OpenMaya.MFnNumericData.kFloat, 0.0)
    Piston.output    = mFnAttr.create('output',    'o',    OpenMaya.MFnNumericData.kFloat)
    
    
    Piston.addAttribute(Piston.inLengthA)
    Piston.addAttribute(Piston.inLengthB)
    Piston.addAttribute(Piston.inRotate)
    Piston.addAttribute(Piston.output)
    
    
    Piston.attributeAffects(Piston.inLengthA, Piston.output)
    Piston.attributeAffects(Piston.inLengthB, Piston.output)
    Piston.attributeAffects(Piston.inRotate,  Piston.output)



def initializePlugin(MObject):
    mplugin = OpenMayaMPx.MFnPlugin(MObject)
    try:
        mplugin.registerNode(PISTON_NODE_NAME, PISTON_NODE_ID, nodeCreator, nodeInitializer)
    except:
        sys.stderr.write('False to load node plug in %s !'%PISTON_NODE_NAME)



def uninitializePlugin(MObject):
    mplugin = OpenMayaMPx.MFnPlugin(MObject)
    try:
        mplugin.deregisterNode(PISTON_NODE_ID)
    except:
        sys.stderr.write('False to unload node plug in %s !'%PISTON_NODE_NAME)
    