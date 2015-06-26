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
    class of the node core...
    '''
    def __init__(self):
        super(Piston, self).__init__()
        
        
    def compute(self, plug, dataBlock):
        sita = dataBlock.inputValue(self.rotate).asFloat() * math.pi / 180.0
        A    = dataBlock.inputValue(self.distanceA).asFloat()
        B    = dataBlock.inputValue(self.distanceB).asFloat()

        H = math.cos(sita) * B + math.sqrt(A**2 - (math.sin(sita) * B)**2)
        
        outAttr = dataBlock.outputValue(self.output)
        outAttr.setFloat(H)
        dataBlock.setClean(plug)



def nodeCreator():
    '''
    Use to create the node...
    '''
    return OpenMayaMPx.asMPxPtr(Piston())



def nodeInitializer():
    '''
    Setup node's attributes...
    '''
    mFnAttr = OpenMaya.MFnNumericAttribute()
    
    for atl, ats in (('distanceA', 'disa'), ('distanceB', 'disb'), ('rotate', 'r')):
        setattr(Piston, atl, mFnAttr.create(atl, ats, OpenMaya.MFnNumericData.kFloat, 0.0))
    
    Piston.output = mFnAttr.create('output',    'o',    OpenMaya.MFnNumericData.kFloat)
    
    
    for attr in (Piston.distanceA, Piston.distanceB, Piston.rotate, Piston.output):
        Piston.addAttribute(attr)

    
    for attr in (Piston.distanceA, Piston.distanceB, Piston.rotate):
        Piston.attributeAffects(attr, Piston.output)




def initializePlugin(MObject):
    '''
    Use to load Plug_in...
    '''
    mplugin = OpenMayaMPx.MFnPlugin(MObject)
    try:
        mplugin.registerNode(PISTON_NODE_NAME, PISTON_NODE_ID, nodeCreator, nodeInitializer)
    except:
        sys.stderr.write('False to load node plug in %s !'%PISTON_NODE_NAME)



def uninitializePlugin(MObject):
    '''
    Use to unload Plug_in...
    '''
    mplugin = OpenMayaMPx.MFnPlugin(MObject)
    try:
        mplugin.deregisterNode(PISTON_NODE_ID)
    except:
        sys.stderr.write('False to unload node plug in %s !'%PISTON_NODE_NAME)
    