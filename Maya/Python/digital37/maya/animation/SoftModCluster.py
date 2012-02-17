import pymel.core as pm

class SoftModCluster():
    def __init__(self):
        self.SoftMod_Handles = None
        self.SoftMod = None
        self.Pos = None
        self.Vtxs = None
        self.Radius = None
        self.Cluster = None
        
    def soft_to_cluster(self):
        #
        sel = pm.ls(sl=1)
        softMod_handle_shapes = pm.ls(sl=1,dag=1,lf=1,type='softModHandle')
        #
        l = pm.spaceLocator()
        pm.select(sel[0],tgl=1)
        pm.mel.eval('align -atl -x Mid -y Mid -z Mid')
        
        pm.select(l,r=1)
        self.Pos = pm.xform(q=1,ws=1,t=1)
        
        if softMod_handle_shapes:
            for softMod_handle_shape in softMod_handle_shapes:
                print softMod_handle_shape
                softMod_handle = softMod_handle_shape.getParent()
                softMods = softMod_handle_shape.softModTransforms.connections(p=0,s=1)
                if softMods:
                    softMod = softMods[0]
                    if softMod :
                        deform_sets = softMod.message.connections(p=0,s=1)
                        self.Radius = softMod.falloffRadius.get()
                        #pvt = softMod.falloffCenter.get()
                        print deform_sets
                        if deform_sets:
                            deform_set = deform_sets[0]
                            geometrys = deform_set.memberWireframeColor.connections(p=0,s=1)
                            print geometrys
                            pm.select(geometrys[0],r=1)
                            pm.polySelectConstraint(m=3,t=1,d=1,db=(0,self.Radius),dp=self.Pos)
                            vtxs = pm.ls(sl=1,fl=1)
                            pm.polySelectConstraint(m=0)
                            
                            pm.mel.eval('newCluster \" -envelope 1\"')
                            
                            cluster_handle = pm.ls(sl=1)[0]
                            cluster_shape = pm.ls(sl=1,dag=1,lf=1)[0]
                            
                            # Get cluster
                            self.Cluster = cluster = cluster_shape.clusterTransforms.connections(p=0,d=1)[0]
                            print 'cluster:',cluster
                            
                            cluster_shape.originX.set(0)
                            cluster_shape.originY.set(0)
                            cluster_shape.originZ.set(0)

                            pm.select(cluster_handle,r=1)
                            pm.move(self.Pos,r=1)
                            
                            pm.move(cluster_handle.scalePivot,self.Pos)
                            pm.move(cluster_handle.rotatePivot,self.Pos)
                            
                            cluster_handle.tx.set(0)
                            cluster_handle.ty.set(0)
                            cluster_handle.tz.set(0)
                            
                            cluster_shape.originX.set(self.Pos[0])
                            cluster_shape.originY.set(self.Pos[1])
                            cluster_shape.originZ.set(self.Pos[2])
                            
                            pm.move(cluster_handle.scalePivot,self.Pos)
                            pm.move(cluster_handle.rotatePivot,self.Pos)
                            
                            # set vtx weight
                            
                            #select $vtxs;
                            #sets -add $deformSet; 
                            pm.select(vtxs,r=1)
                            pm.sets(deform_set,add=1)
                            
                            #$posSoftMod=`xform -q -ws -piv $softModHandle`;
                            #move -r -ws 1 0 0 $softModHandle;
                            print 'softMod_handle:',softMod_handle
                            pos_softMod = pm.xform(softMod_handle,q=1,ws=1,piv=1)
                            pm.move(1,0,0,softMod_handle,r=1,ws=1)
                            print '\na'
                            for vtx in vtxs:
                                #setAttr ($softMod+".envelope") 0;
                                #$posA=`xform -q -ws -t $vtxs[$i]`;
                                #setAttr ($softMod+".envelope") 1;
                                softMod.envelope.set(0)
                                posA = pm.xform(vtx,q=1,ws=1,t=1)
                                softMod.envelope.set(1)
                                
                                xRadius = softMod.falloffRadius.get()
                                yRadius = softMod.falloffRadius.get()
                                
                                posBX=posBY=pm.xform(vtx,q=1,ws=1,t=1)
                                #$vecX=$posA[0]-$posSoftMod[0];
                                #$vecY=$posA[1]-$posSoftMod[1];
                                vecX = posA[0] - pos_softMod[0]
                                vecY = posA[1] - pos_softMod[1]
                                
                                #$magX=$posBX[0]-$posA[0];
                                #$magY=$posBY[0]-$posA[0];
                                magX = posBX[0] - posA[0]
                                magY = posBY[0] - posA[0]
                                mag = ((magX-pm.datatypes.abs(vecY*(1.0/(yRadius*2.0)))) \
                                       + (magY-pm.datatypes.abs(vecX*(1.0/(xRadius*2.0)))))*0.5
                                if mag < 0 :
                                    mag = 0
                                print 'mag: ',mag
                                #percent -v $mag $cluster $vtxs[$i]
                                pm.select(vtx,r=1)
                                pm.percent(cluster,v=mag)
                            
                            print softMod_handle
                            pm.move(-1,0,0,softMod_handle,r=1,ws=1)
            
#    def set_cluster_weight_mel(self):
#        n1 = str( pm.PyNode(self.SoftMod).name() )
#        n2 = str( pm.PyNode(self.Cluster).name() )
#        print self.Vtxs
#        
#        cmd = 'softModCluster (\"' + n1 + '\",\"' + n2 + '\",{'  
#        i = 0
#        for v in self.Vtxs:
#            if i ==0 : 
#                cmd += '\"' + v.name() + '\"'
#            else:
#                cmd += ',\"' + v.name() + '\"'
#            i += 1
#        cmd += '})'
#        print cmd
#        pm.mel.eval( cmd )
        
def main():
    a = SoftModCluster()
    a.soft_to_cluster()

if __name__ == '__main__' :
    main()

