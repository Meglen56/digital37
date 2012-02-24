import pymel.core as pm

class SoftModCluster():
    def __init__(self):
        self.SoftMod_Handles = None
        self.SoftMod = None
        self.Vtxs = None
        self.Radius = None
        self.Cluster = None
        
    def add_fallOff_attr(self):
        sels = pm.ls(sl=1,l=1)
        if sels:
            for sel in sels:
                try :
                    pm.PyNode(sel.falloffRadius)
                except :
                    pm.addAttr(sel,ln='falloffRadius',at='double')
                    sel.falloffRadius.set(keyable=True)
                sel.falloffRadius.set(1)
                
                try :
                    pm.PyNode(sel.falloffMode)
                except :
                    pm.addAttr(sel,ln='falloffMode',at='enum',en='volume:surface')
                    sel.falloffMode.set(keyable=True)
                sel.falloffMode.set('volume')
        
    def softMod_to_cluster(self):
        #
        sels = pm.ls(sl=1)
        #
        if sels:
            for sel in sels :
                l = pm.spaceLocator()
                pm.select(sel,tgl=1)
                pm.mel.eval('align -atl -x Mid -y Mid -z Mid')
                
                pm.select(l,r=1)
                pos_locator = pm.xform(q=1,ws=1,t=1)
            
                softMod_handle = sel.connections(p=0,d=1)[0].constraintTranslateX.connections(p=0,d=1)[0]
                print softMod_handle
                # get handle shape
                softMod_handle_shape = pm.PyNode(softMod_handle).getShape()
                
                if softMod_handle_shape:
                    print softMod_handle_shape
                    softMod_handle = softMod_handle_shape.getParent()
                    softMods = softMod_handle_shape.softModTransforms.connections(p=0,s=1)
                    if softMods:
                        softMod = softMods[0]
                        if softMod :
                            deform_sets = softMod.message.connections(p=0,s=1)
                            #TODO radius*0.5
                            self.Radius = softMod.falloffRadius.get()
                            #pvt = softMod.falloffCenter.get()
                            print deform_sets
                            if deform_sets:
                                deform_set = deform_sets[0]
                                geometrys = deform_set.memberWireframeColor.connections(p=0,s=1)
                                print geometrys
                                pm.select(geometrys[0],r=1)
                                pm.polySelectConstraint(m=3,t=1,d=1,db=(0,self.Radius),dp=pos_locator)
                                vtxs = pm.ls(sl=1,fl=1)
                                pm.polySelectConstraint(m=0)
                                
                                #
                                mags = []
                                pos_0_list = []
                                pos_1_list = []
                                pm.move(1,0,0,softMod_handle,r=1,ws=1)
                                for vtx in vtxs:
                                    pos = pm.xform(vtx,q=1,ws=1,t=1)
                                    pos_0_list.append( pos )
                                    
                                pm.move(-1,0,0,softMod_handle,r=1,ws=1)
                                for vtx in vtxs:
                                    pos = pm.xform(vtx,q=1,ws=1,t=1)
                                    pos_1_list.append( pos )
                                    
                                for (p0,p1) in zip(pos_0_list,pos_1_list):
                                    print 'p0:',p0
                                    print 'p1:',p1
                                    length = self.get_length(p0,p1)
                                    print 'length:',length
                                    mags.append(length)
                                
                                pm.mel.eval('newCluster \" -envelope 1\"')
                                
                                cluster_handle = pm.ls(sl=1)[0]
                                cluster_shape = pm.ls(sl=1,dag=1,lf=1)[0]
                                
                                # Get cluster
                                self.Cluster = cluster = cluster_shape.clusterTransforms.connections(p=0,d=1)[0]
                                print 'cluster:',cluster
                                cluster.relative.set(1)
                                
                                cluster_shape.originX.set(0)
                                cluster_shape.originY.set(0)
                                cluster_shape.originZ.set(0)
    
                                pm.select(cluster_handle,r=1)
                                pm.move(pos_locator,r=1)
                                
                                pm.move(cluster_handle.scalePivot,pos_locator)
                                pm.move(cluster_handle.rotatePivot,pos_locator)
                                
                                cluster_handle.tx.set(0)
                                cluster_handle.ty.set(0)
                                cluster_handle.tz.set(0)
                                
                                cluster_shape.originX.set(pos_locator[0])
                                cluster_shape.originY.set(pos_locator[1])
                                cluster_shape.originZ.set(pos_locator[2])
                                
                                pm.move(cluster_handle.scalePivot,pos_locator)
                                pm.move(cluster_handle.rotatePivot,pos_locator)
                                
                                #select $vtxs;
                                #sets -add $deformSet; 
                                pm.select(vtxs,r=1)
                                pm.sets(deform_set,add=1)
                                
                                #$posSoftMod=`xform -q -ws -piv $softModHandle`;
                                #move -r -ws 1 0 0 $softModHandle;
                                print 'softMod_handle:',softMod_handle
                                pos_softMod = pm.xform(softMod_handle,q=1,ws=1,piv=1)
                                #pm.move(1,0,0,softMod_handle,r=1,ws=1)
                                print '\na'
    
                                min = pm.datatypes.min(mags)
                                max = pm.datatypes.max(mags)
                                print 'min:',min
                                print 'max:',max
                                
                                for (vtx,m) in zip(vtxs,mags):
                                    try:
                                        mag = pm.datatypes.smoothstep(min,max,m)
                                    except:
                                        mag = 1
                                    #print 'mags[i]:],',mags[i]
                                    #mag = 0.1
                                    #print 'mag: ',mag
                                    pm.select(vtx,r=1)
                                    # set vtx weight
                                    pm.percent(cluster,v=mag)

                                pm.select(sel,r=1)
                                pm.select(cluster_handle,add=1)
                                pm.parentConstraint(mo=1,weight=1)
    
                                sel_parent = sel.getParent()
                                print type(sel_parent)
                                sel_parent = pm.PyNode( sel_parent ).getParent()
                                sel_parent = pm.PyNode( sel_parent ).getParent()
                                sel_parent = pm.PyNode( sel_parent ).getParent()
                                sel_parent = pm.PyNode( sel_parent ).getParent()
                                print 'sel_parent:',sel_parent
                
                                pm.select(cluster_handle,r=1)
                                pm.select( cluster_handle,sel_parent )
                                pm.parent()
                                
                                try:
                                    pm.delete(softMod_handle)
                                except:
                                    pm.error('can not delete softMod handle')
                pm.delete(l)
                #pm.select(vtxs,r=1)
        
    def get_length(self,posA,posB):
        mag = pm.datatypes.sqrt( (posA[0]-posB[0])**2 + (posA[1]-posB[1])**2  + (posA[2]-posB[2])**2 )
        return mag
    
    def control_to_softMod(self):
        sels = pm.ls(sl=1)
        if len(sels) == 2 :
            control = sels[0]
            geometry = sels[1]
            falloff_radius = control.falloffRadius.get()
            falloff_mode = control.falloffMode.get()
            
            pos = t = pm.xform(control,q=1,ws=1,t=1)
            r = pm.xform(control,q=1,ws=1,ro=1)
            s = pm.xform(control,q=1,r=1,s=1)
            
            pm.select(geometry,r=1)
            #softMod -falloffMode 1 -falloffAroundSelection 0
            (softMod,softMod_handle) = pm.softMod(falloffMode=1, falloffAroundSelection=0)
            #rename $tempString[0] ("convertedSoftMod_"+$sel[0])
            pm.rename(softMod, ( 'convertedSoftMod_'+control.name() ) )
            pm.rename(softMod_handle, ( 'convertedSoftModHandle_'+control.name() ) )
            
            softMod.falloffRadius.set( falloff_radius )
            softMod.falloffMode.set( falloff_mode )
            #setAttr -type float3 ($softModHandle+"Shape.origin") ($pos[0]) $pos[1] $pos[2];
            softMod_handle.getShape().origin.set(pos)
            #setAttr ($softMod+".falloffCenter") ($pos[0]) $pos[1] $pos[2];
            softMod.falloffCenter.set(pos)
            
            #xform -piv ($pos[0]) $pos[1] $pos[2] $softModHandle;
            pm.xform(softMod_handle,piv=pos)
            #xform -ws -t ($t[0]-$pos[0]) ($t[1]-$pos[1]) ($t[2]-$pos[2]) -ro $r[0] $r[1] $r[2] -s $s[0] $s[1] $s[2] $softModHandle;
            pm.xform(softMod_handle,ws=1,t=((t[0]-pos[0]),(t[1]-pos[1]),(t[2]-pos[2])),ro=r,s=s)
            
            pm.select(softMod_handle)
            
        else:
            pm.warning('control_to_softMod:please select one control and one geometry first')
        
def main():
    a = SoftModCluster()
    a.softMod_to_cluster()
    #a.add_fallOff_attr()
    #a.control_to_softMod()

if __name__ == '__main__' :
    main()

