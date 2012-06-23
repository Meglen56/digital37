import maya.OpenMaya as OpenMaya

ref = list()
OpenMaya.MFileIO.getReferences(ref,True)
print ref
OpenMaya.MFileIO.loadReference(ref[0])