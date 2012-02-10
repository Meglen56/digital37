import traceback
import maya.cmds as cmds

class test(object):
    def __init__(self):
        self.a_Num = '000'
        self.SelectGrp = ""
        self.g_Num = '000'
        self.SkeletonGrp = []
        self.RenameLinesPermanent = []
        self.NumPermanent = []
        self.NumberPermanent = []
        self.RenameLines = ''
        self.Len = 0
        self.NumSpan = 0
        self.lines2 = []
        self.s = ''
        self.DesmondSkeleton('XXXX','G','Hair','Skeleton','Grp') 
        
        
    def BaseDigital(self,i):
        loopSize = len(str(i))
        numSize = len(self.g_Num)
        subString = self.a_Num[0 : numSize - loopSize]
        return subString
    
    def SegmentDigital(self,i):
        loopSize = len(str(i))
        numSize = len(self.g_Num)
        subString = self.g_Num[0 : numSize - loopSize]
        return subString
    
    def DesmondSkeleton(self,Character,Position,Part,Category,Function):
        self.sel = cmds.ls(sl = True)
        self.Len = len(self.sel)
        for s in range(0, len(self.sel)):
            self.RenameLines = cmds.rename (self.sel[s], Character + '_' + Position + '_' + self.BaseDigital(s) + str(s)+ '_' )
            self.RenameLinesPermanent.append(self.RenameLines)
            #self.RenameLinesPermanent += RenameLines 
            
            shape = cmds.listRelatives(self.RenameLines, s = True)
            
            Num = cmds.getAttr( shape[0] +'.spans')

            self.NumPermanent.append(Num)
            
            Number = Num + 1
            self.NumberPermanent.append(Number)
            print 'self.RenameLines:%s',self.RenameLines
            line = self.RenameLines + Part + '_' + self.SegmentDigital(0) + str(0) + '_' + 'Line'
            self.lines2.append(line)
            print 'self.lines2:%s', self.lines2
            finalLine = cmds.rename (self.RenameLines, line )
            for g in range(0, Number):
                cmds.select(d = True)
                SelectSkeleton = cmds.joint( p=(0, 0, 0),n = self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + Category )
                self.SkeletonGrp.append(SelectSkeleton)
                CV = cmds.select (finalLine + '.cv[%d]'%(g),r =True)
                print CV
                cmds.cluster( rel= False )
                Cluste = cmds.ls(sl = True)           
                SelectCluster = cmds.rename (Cluste,self.RenameLines + Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'Cluster')
                cmds.setAttr (SelectCluster + '.visibility',0)
                print SelectCluster
                print 'g:',g
                sphereName = self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'SpherePoly'
                print 'sphereName:',sphereName
                SelectSpherePoly = cmds.polySphere (r = 0.2, n = sphereName )
                
                SelectSphereZero = cmds.group (em = True , n = self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'SphereZero')
                cmds.addAttr (self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'SpherePoly', ln='up' , defaultValue= 0, minValue= -360, maxValue= 360 )
                cmds.setAttr (self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'SpherePoly'+'.up',e=True ,keyable=True  )
                
    
                cmds.parent (SelectSphereZero,SelectSpherePoly)
                print '********************'
                SelectSphereAim = cmds.group (em = True , n = self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'SphereAim')
                cmds.parent (SelectSphereAim,SelectSphereZero)
                print '====================='
                SelectSphere = cmds.group (em = True , n = self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'Sphere')
                cmds.parent (SelectSphere,SelectSphereAim)
                
        
                
           
                cmds.select(d = True)
                SelectFKZero = cmds.joint( p=(0, 0, 0),n = self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'FKZero' )
                cmds.parent (SelectFKZero,SelectSphere)
                cmds.select(d = True)
                SelectFKFix = cmds.joint( p=(0, 0, 0),n = self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'FKFix' )
                cmds.parent (SelectFKFix,SelectFKZero)
                cmds.select(d = True)
                SelectFKExp = cmds.joint( p=(0, 0, 0),n = self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'FKExp' )
                cmds.parent (SelectFKExp,SelectFKFix)
                cmds.select(d = True)
                SelectFKSDK = cmds.joint( p=(0, 0, 0),n = self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'FKSDK' )
                cmds.parent (SelectFKSDK,SelectFKExp)
                cmds.select(d = True)
                SelectFK = cmds.joint( p=(0, 0, 0),n = self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'FK' )
                cmds.parent (SelectFK,SelectFKSDK)
                
                
                
                cmds.select(d = True)
                SelectIKZero = cmds.joint( p=(0, 0, 0),n = self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'IKZero' )
                cmds.parent (SelectIKZero,SelectSphere)
                cmds.select(d = True)
                SelectIKFix = cmds.joint( p=(0, 0, 0),n = self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'IKFix' )
                cmds.parent (SelectIKFix,SelectIKZero)
                cmds.select(d = True)
                SelectIKExp = cmds.joint( p=(0, 0, 0),n = self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'IKExp' )
                cmds.parent (SelectIKExp,SelectIKFix)
                cmds.select(d = True)
                SelectIKSDK = cmds.joint( p=(0, 0, 0),n = self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'IKSDK' )
                cmds.parent (SelectIKSDK,SelectIKExp)
                cmds.select(d = True)
                SelectIK = cmds.joint( p=(0, 0, 0),n = self.RenameLines +  Part + '_' + self.SegmentDigital(g) + str(g) + '_' + 'IK' )
                #
                self.s = SelectIK
                cmds.parent (SelectIK,SelectIKSDK)
                
                
                
                
                
                cmds.parentConstraint( SelectCluster, SelectSpherePoly[0] )
                cmds.delete (SelectSpherePoly[0] + '_parentConstraint1')
                cmds.parentConstraint( SelectSpherePoly, SelectCluster )
                
                
                cmds.connectAttr( SelectSpherePoly[0] + '.up', SelectSphere + '.rotateX' )
            for pg in range(0, Num): 
                #n = self.RenameLines +  Part + '_' + self.SegmentDigital(pg) + str(pg + 1) + '_' + 'SpherePoly'
                n = self.RenameLines +  Part + '_' + self.SegmentDigital(pg +1) + str(pg + 1) + '_' + 'SpherePoly'
                print 'n:',n
                cmds.aimConstraint(n, self.RenameLines +  Part + '_' + self.SegmentDigital(pg) + str(pg) + '_' + 'SphereAim' )
                print '+++++++++++++++++++++'
                
                
                
                    
    
                           
    
        self.SelectGrp = cmds.group(self.SkeletonGrp, n= Character + '_' + Position + '_' + self.BaseDigital(0) + str(0) + '_' + Part + '_' + self.SegmentDigital(0) + str(0) + '_' + Category + Function)       
    
    
        DesmondOrientJointWindow = cmds.window(title = 'OrientJoint', wh=(100,30))
        cmds.columnLayout()
        cmds.button(label = 'OK',command = self.xsj)
        #cmds.button(label = 'OK')
        cmds.showWindow(DesmondOrientJointWindow)
        
        
    
    def xsj(self,Character='XXXX',Position='G',Part='Hair',Category='Skeleton',Function='Grp'):
        s=e=''
        ns=ne=''
        print '*****************'
        print self.RenameLinesPermanent
        for l,i in zip(self.RenameLinesPermanent,range(len(self.RenameLinesPermanent))):
            
            for tt in xrange(self.NumPermanent[i]):
                print 'self.NumPermanent:%s',self.NumPermanent
                print 'tt%s',tt
                print 'self.SegmentDigital(tt):',self.SegmentDigital(tt)
                #cmds.parent (l+  Part + '_' + self.SegmentDigital(tt) + str(tt + 1) + '_' + 'FKZero', l +  Part + '_' + self.SegmentDigital(tt) + str(tt) + '_' + 'FK' )
                cmds.parent (l+  Part + '_' + self.SegmentDigital(tt+1) + str(tt + 1) + '_' + 'FKZero', l +  Part + '_' + self.SegmentDigital(tt) + str(tt) + '_' + 'FK' )
                #cmds.parent (l+  Part + '_' + self.SegmentDigital(tt) + str(tt + 1) + '_' + 'IKZero', l +  Part + '_' + self.SegmentDigital(tt) + str(tt) + '_' + 'IK' )
                cmds.parent (l+  Part + '_' + self.SegmentDigital(tt+1) + str(tt + 1) + '_' + 'IKZero', l +  Part + '_' + self.SegmentDigital(tt) + str(tt) + '_' + 'IK' )
                    
                
                #e = l +  Part + '_' + self.SegmentDigital(tt) + str(tt + i) + '_' + 'IK'
                ne = self.SegmentDigital(tt) + str(tt+1 )
                e = l +  Part + '_' + self.SegmentDigital(tt) + str(tt+1 ) + '_' + 'IK'
                    #try:
                    #cmds.parent (a, b )
                    #except:
                        #traceback.print_exc()
                
            if tt==0:
                ns = self.SegmentDigital(tt) + str(tt)
                s = l +  Part + '_' + self.SegmentDigital(tt) + str(tt) + '_' + 'IKZero'
                
            print 's:%s',s 
            print 'e:%e',e
                
            print 'iiiiiiiiiiiiiiii:%s',i
            cmds.ikHandle(n = l + '_' + Part + '_' + '_IKSplineH', sj = s, ee=e,\
                            ccv = False , c = self.lines2[i],sol = 'ikSplineSolver')
                
def main():
    test()
        
if __name__ == "__main__":
    main()
    




