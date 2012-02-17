import pymel.core as pm

class SoftModCluster():
    def __init__(self):
        self.Soft_Handles = None
        self.Soft_Mod = None
        self.Pos = None
        self.Vtxs = None
        self.Radius = None
        self.Cluster = None
        
    def soft_to_cluster(self):
        #
        sel = pm.ls(sl=1)
        self.Soft_Handles = pm.ls(sl=1,dag=1,lf=1,type='softModHandle')
        #
        l = pm.spaceLocator()
        pm.select(sel[0],tgl=1)
        pm.mel.eval('align -atl -x Mid -y Mid -z Mid')
        
        pm.select(l,r=1)
        self.Pos = pm.xform(q=1,ws=1,t=1)
        
        if self.Soft_Handles:
            for sh in self.Soft_Handles:
                print sh
                soft_Mods = sh.softModTransforms.connections(p=0,s=1)
                self.Soft_Mod = soft_Mods[0]
                if self.Soft_Mod :
                    sms = self.Soft_Mod.message.connections(p=0,s=1)
                    self.Radius = self.Soft_Mod.falloffRadius.get()
                    #pvt = self.Soft_Mod.falloffCenter.get()
                    print sms
                    if sms:
                        g = sms[0].memberWireframeColor.connections(p=0,s=1)
                        print g
                        pm.select(g[0],r=1)
                        pm.polySelectConstraint(m=3,t=1,d=1,db=(0,self.Radius),dp=self.Pos)
                        #$vtxs[]=`ls -sl -fl`
                        self.Vtxs = pm.ls(sl=1,fl=1)
                        
                        pm.mel.eval('newCluster \" -envelope 1\"')
                        
                        cluster = pm.ls(sl=1)
                        cluster_shape = pm.ls(sl=1,dag=1,lf=1)
                        
                        # Get cluster
                        clusters = cluster_shape[0].clusterTransforms.connections(p=0,d=1)
                        print 'clusters:',clusters
                        self.Cluster = clusters[0]
                        
                        cluster_shape[0].originX.set(0)
                        cluster_shape[0].originY.set(0)
                        cluster_shape[0].originZ.set(0)
                        
                        #vtxs = pm.ls(sl=1,fl=1)
                        pm.polySelectConstraint(m=0)
                        
                        l = pm.spaceLocator()
                        
                        
                        pm.select(cluster[0],r=1)
                        #pm.select(l,tgl=1)
                        #pm.parent()
                        
                        #pm.select(l,r=1)
                        pm.move(self.Pos,r=1)
                        #move -0.192772 0.831059 -0.621647 cluster2Handle.scalePivot cluster2Handle.rotatePivot ;
                        
                        pm.move(cluster[0].scalePivot,self.Pos)
                        pm.move(cluster[0].rotatePivot,self.Pos)
                        
                        cluster[0].tx.set(0)
                        cluster[0].ty.set(0)
                        cluster[0].tz.set(0)
                        
                        cluster_shape[0].originX.set(self.Pos[0])
                        cluster_shape[0].originY.set(self.Pos[1])
                        cluster_shape[0].originZ.set(self.Pos[2])
                        
                        pm.move(cluster[0].scalePivot,self.Pos)
                        pm.move(cluster[0].rotatePivot,self.Pos)
                                
#    def set_cluster_weight(self):
#        print 'self.Cluster:',self.Cluster
#        #pos_softMod = pm.xform(self.Soft_Mod,q=1,ws=1,t=1)
#        for v in self.Vtxs :
#            #$posBY=`xform -q -ws -t $vtxs[$i]`;
#            pos = pm.xform(v,q=1,ws=1,t=1)
#            a = pm.datatypes.Array([self.Pos,pos])
#            l = 1 - pm.datatypes.length(a)/self.Radius*0.5
#            print 'l:',l
#            #percent -v $mag $cluster $vtxs[$i];
#            pm.select(v,r=1)
#            pm.percent(self.Cluster,v=l)
            
    def set_cluster_weight(self):
        n1 = str( pm.PyNode(self.Soft_Mod).name() )
        n2 = str( pm.PyNode(self.Cluster).name() )
        print self.Vtxs
        
        cmd = 'softModCluster (\"' + n1 + '\",\"' + n2 + '\",{'  
        i = 0
        for v in self.Vtxs:
            if i ==0 : 
                cmd += '\"' + v.name() + '\"'
            else:
                cmd += ',\"' + v.name() + '\"'
            i += 1
        cmd += '})'
        print cmd
        pm.mel.eval( cmd )
        
def main():
    a = SoftModCluster()
    a.soft_to_cluster()
    a.set_cluster_weight()

if __name__ == '__main__' :
    main()

