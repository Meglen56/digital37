import pymel.core as pm

class DeformAfterSet(object):
    def __init__(self):
        pass
    
    def getShapeSelection(self):
        self.Shape_Selection = pm.ls(sl=1,dag=1,lf=1,type=['mesh','nurbsSurface','subdiv'])
        if not self.Shape_Selection :
            pm.error('select some objects first.')
            return False
        else :
            return True
        
    def getSourceShape(self):
        self.Source_Deform = list()
        for shape in self.Shape_Selection:
            #check if attribute exists
            try:
                pm.PyNode(shape.tweakLocation)
            except pm.general.MayaAttributeError:
                pm.info('%s has no tweak attribute' % shape.name())
            else:
                # get tweaklocation input
                tweaks = shape.tweakLocation.inputs()
                if tweaks:
                    tweak = tweaks[0]
                    if tweak.connections(d=0):
                        # get transform
                        for transform in tweak.connections(d=0):
                            if transform.inputs() :
                                for t in transform.inputs() :
                                    if str(type(t)) == '<class \'pymel.core.nodetypes.Transform\'>' :
                                        print 'source:\t%s' % t.getShape()
                                        print 'deform:\t%s' % shape
                                        self.Source_Deform.append( (t.getShape(),shape) )
                
    def deformAfterSet(self):
        for source,deform in self.Source_Deform:
            pm.mel.deformerAfterObjectSetMod( source,deform )
        
    def main(self):
        if self.getShapeSelection():
            self.getSourceShape()
            if self.Source_Deform:
                self.deformAfterSet()

def main():
    DeformAfterSet().main()
    
if __name__ == '__main__' :
    pass