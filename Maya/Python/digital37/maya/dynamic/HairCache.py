import os
import traceback
import pymel.core as pm
from pymel.all import mel
            
class General():
    def __init__(self):
        pass
    
    def get_scene_name(self):
        self.Scene_Name = os.path.splitext( os.path.basename( pm.system.sceneName() ) )[0]
    
    def create_dir(self,dirPath):
        if not os.path.exists( dirPath ):
            os.makedirs( dirPath )
        
class HairCache(General):
    '''
    create hair cache:
    add scenes name before maya default hair cache
    '''
    def __init__(self):
        self.Hairs = None
        self.DiskCache_Before = None
        
    # if user select no hair system,then select all hair system in scene    
    def get_sel_hair_shapes(self):
        self.Hairs = pm.ls(sl=1,dag=1,lf=1,l=1,type='hairSystem')
        if not self.Hairs:
            # select all hair system in scenes
            self.Hairs = pm.ls(dag=1,lf=1,l=1,type='hairSystem')
        if not self.Hairs:
            pm.warning('select some hair system first.')
        else:
            pm.select(self.Hairs,r=1)
            
    def set_cache_name(self):
        for hair in self.Hairs :
            # get cache node
            cache_shapes = hair.diskCache.connections(p=0,d=1)
            if cache_shapes:
                for cache_shape in cache_shapes:
                    try:
                        nameBefore = cache_shape.cacheName.get()
                        print 'nameBefore:',nameBefore
                    except:
                        traceback.print_exc()
                        self.set_diskCache_rule()
                    else:
                        print 'self.Scene_Name:',self.Scene_Name
                        cache_shape.cacheName.set( (self.Scene_Name + '/' + nameBefore),type='string' )
                        print 'nameAfter:',cache_shape.cacheName.get()
                        cache_shape.cacheName.set(lock=1)
    
            
    def lock_cache_name(self):
        for hair in self.Hairs :
            # get cache node
            cache_shapes = hair.diskCache.connections(p=0,d=1)
            if cache_shapes:
                for cache_shape in cache_shapes:
                    try:
                        cache_shape.cacheName.set(lock=1)
                    except:
                        traceback.print_exc()
                        self.set_diskCache_rule()
                            
    def del_cache(self):
        try:
            # delete cache
            mel.eval('DeleteHairCache')
        except:
            traceback.print_exc()
                                        
    def get_diskCache_rule(self):
        try:
            #workspace -q -fileRuleEntry "diskCache"
            # get file rule entry
            self.DiskCache_Before = pm.workspace('diskCache',fileRuleEntry=1,q=1 )
        except:
            traceback.print_exc()
    
    def set_diskCache_rule(self,dirPath=None):
        if not dirPath:
            dirPath = self.DiskCache_Before
        try:
            pm.workspace(fileRule=('diskCache',dirPath) )
        except:
            traceback.print_exc()
        else:
            try:
                pm.workspace(saveWorkspace=True)
            except:
                traceback.print_exc()
                
    def save_file(self):
        returnStr = 'create hair cache error'
        # save file
        try:
            #pm.system.saveFile(force=True)
            #TODO 2011 error
            mel.eval('file -s -f')
        except:
            self.set_diskCache_rule()
            traceback.print_exc()
            return returnStr
                
    def create_hair_cache(self):
        returnStr = 'create hair cache error'
        # get selection hair shapes
        self.get_sel_hair_shapes()
        
        if self.Hairs :            
            self.get_scene_name()
            if self.Scene_Name :
                # delete cache first
                self.del_cache()
                
                # 
                self.get_diskCache_rule()
                
                # set disk cache file rule
                self.set_diskCache_rule(self.DiskCache_Before + '/' + self.Scene_Name)
                
                # create dir if it not exists
                # else cache can not be write to dir
                dirPath = os.path.join( pm.workspace(q=1,rd=1),\
                                        self.DiskCache_Before,\
                                        self.Scene_Name )
                try:
                    self.create_dir(dirPath)
                except KeyboardInterrupt:
                    print 'user cancel create dir'
                    self.set_diskCache_rule()
                    return returnStr
                except:
                    self.set_diskCache_rule()
                    traceback.print_exc()
                    return returnStr
                        
                # create hair cache
                try:
                    #mel.eval('CreateHairCacheOptions')
                    mel.eval('doHairDiskCache 1 { \"2\", 1, 1, 10, 1 } ')
                except KeyboardInterrupt:
                    print 'user cancel'
                    self.set_diskCache_rule()
                    return returnStr
                except:
                    self.set_diskCache_rule()
                    traceback.print_exc()
                    return returnStr
        
                #save file
                self.save_file()
                    
                # set hair cache name
                self.set_cache_name()
                # re set disk cache file rule to default
                self.set_diskCache_rule()
                
                self.lock_cache_name()
                #save file
                self.save_file()
                
                return 'create hair cache success'
        # lock hair cache name attribute
        
            
def main():
    HairCache().create_hair_cache()
    
if __name__ == '__main__' :
    pass
        