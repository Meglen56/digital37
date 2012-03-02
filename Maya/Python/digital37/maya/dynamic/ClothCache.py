import os
import traceback
import pymel.core as pm
            
class General():
    def __init__(self):
        pass
    
    def get_scene_name(self):
        self.Scene_Name = os.path.splitext( os.path.basename( pm.system.sceneName() ) )[0]
    
    def create_dir(self,dirPath):
        if not os.path.exists( dirPath ):
            try:
                os.makedirs( dirPath )
            except:
                traceback.print_exc()
                print 'create dirs error'
                
        
class ClothCache(General):
    '''
    create cloth cache:
    add scenes name before maya default cloth cache
    '''
    def __init__(self):
        self.Cloths = None
        self.Nucleus = set()
        
    def get_sel_cloth_shapes(self):
        self.Cloths = pm.ls(sl=1,dag=1,lf=1,l=1,type='nCloth')
        if not self.Cloths:
            pm.warning('select some cloth system first.')
        print self.Cloths
                    
    def get_sel_nucleus(self):
        print 'get_sel_nuclues'
        cmd = 'ls -sl -dag -lf -l -type nucleus'
        self.Nucleus = pm.mel.eval(cmd)
        if not self.Nucleus:
            pm.warning('select some nuclues first.')
        print self.Nucleus
        
    def set_nucleus_attr(self,isEnable):
        if isEnable :
            minTime = pm.playbackOptions(q=1,min=1)
            for n in self.Nucleus:
                #n.enable.set(True)
                #n.startFrame.set(minTime)
                pm.mel.setAttr(( n +'.enable'),1)
                pm.mel.setAttr(( n +'.startFrame'),minTime)
        else:
            for n in self.Nucleus:
                #n.enable.set(False)
                #n.startFrame.set(9999)
                pm.mel.setAttr(( n +'.enable'),0)
        
    def set_cloth_attr(self):
        for cloth in self.Cloths:
            try:
                cloth.isDynamic.set(True)
            except:
                traceback.print_exc()
                            
    def get_diskCache_rule(self):
        try:
            #workspace -q -fileRuleEntry "diskCache"
            # get file rule entry
            self.DiskCache = pm.workspace('diskCache',fileRuleEntry=1,q=1 )
        except:
            traceback.print_exc()
    
    def save_file(self):
        returnStr = 'create cloth cache error'
        # save file
        try:
            pm.system.saveFile(force=True)
        except:
            traceback.print_exc()
            return returnStr
                
    def create_cloth_cache(self):
        returnStr = 'create cloth cache error'
        # get selection cloth shapes
        self.get_sel_cloth_shapes()
        self.get_sel_nucleus()
        if self.Cloths and self.Nucleus:
            self.get_scene_name()
            if self.Scene_Name :
                
                # create cache folder if not exists
                
#                dirPath = os.path.join( pm.workspace(q=1,rd=1),\
#                                        self.DiskCache,\
#                                        self.Scene_Name )
#                try:
#                    self.create_dir(dirPath)
#                except:
#                    traceback.print_exc()
#                    return returnStr
                
                # for disk cache is Q:\data
                self.get_diskCache_rule()
                dirPath = os.path.join( self.DiskCache,\
                                        self.Scene_Name )
                dirPath = dirPath.replace('\\','/')
                try:
                    self.create_dir(dirPath)
                except:
                    traceback.print_exc()
                    return returnStr
                
                # enable nuclues
                self.set_nucleus_attr(True)
                self.set_cloth_attr()
                
                #doCreateNclothCache 4 { "2", "1", "10", "OneFilePerFrame", "1", "","0","","0", "0", "0", "1", "1","0","1" }
                # create cache
                pm.select(self.Cloths,r=1)
                cmd = 'catch(`deleteNclothCache`);'
                cmd += 'doCreateNclothCache 4 { "2", "1", "10", "OneFilePerFrame", "1", ' 
                cmd += '"' + dirPath + '"' 
                cmd += ',"0","","0", "add", "0", "1", "1","0","1" } ;'
                print cmd
                try:
                    pm.mel.eval(cmd)
                except:
                    traceback.print_exc()
                    return returnStr
                
                # re set nucleus to disable
                self.set_nucleus_attr(False)
                #save file
                #self.save_file()
                    
                return 'create cloth cache success'
                
def main():
    ClothCache().create_cloth_cache()
    
if __name__ == '__main__' :
    pass
    #main()
        