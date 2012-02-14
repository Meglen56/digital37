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
    def __init__(self):
        self.Hairs = None
        
    def get_sel_hair_shapes(self):
        try:
            self.Hairs = pm.ls(sl=1,dag=1,lf=1,l=1,type='hairSystem')
        except:
            traceback.print_exc()
    
    def set_cache_name(self):
        for hair in self.Hairs :
            # get cache node
            cache_shapes = hair.diskCache.connections(p=0,d=1)
            if cache_shapes:
                for cache_shape in cache_shapes:
                    try:
                        nameBefore = cache_shape.cacheName.get()
                    except:
                        traceback.print_exc()
                    else:
                        cache_shape.cacheName.set( self.Scene_Name + '/' + nameBefore )
    
    def del_cache(self):
        for hair in self.Hairs :
            # get cache node
            cache_shapes = hair.diskCache.connections(p=0,d=1)
            if cache_shapes:
                for cache_shape in cache_shapes:
                    try:
                        # delete cache
                        mel.eval('DeleteHairCache')
                    except:
                        traceback.print_exc()
                    else:
                        
                                        
    def set_diskCache_rule(self,dirPath):
        try:
            pm.workspace(fileRule=('diskCache',dirPath) )
        except:
            traceback.print_exc()
        else:
            try:
                pm.workspace(saveWorkspace=True)
            except:
                traceback.print_exc()
            else:
                # create dir if it not exists
                # else cache can not be write to dir
                dirPath = os.path.join( pm.workspace(q=1,rd=1),dirPath )
                self.create_dir(dirPath)
        
    def create_hair_cache(self):
        returnStr = 'create hair cache error'
        # 
        self.get_scene_name()
        # get selection hair shapes
        self.get_sel_hair_shapes()
        # delete hair cache if it has
        self.del_cache()
        # set disk cache file rule
        self.set_diskCache_rule('data/' + self.Scene_Name)
                
        # create hair cache
        try:
            #mel.eval('CreateHairCacheOptions')
            mel.eval('doHairDiskCache 1 { \"2\", 1, 1, 10, 1 } ')
        except:
            traceback.print_exc()
            return returnStr

        # save file
        try:
            pm.system.saveFile(force=True)
        except:
            traceback.print_exc()
            return returnStr
            
        # set hair cache name
        self.set_cache_name()
        # re set disk cache file rule to default
        self.set_diskCache_rule('data')
        
        return 'create hair cache success'
        
if __name__ == '__main__' :
    a = HairCache()
    a.create_hair_cache()
    
#string $p = `file -q -sn -shn`;
#string $buffer[];
#$numTokens = `tokenize $p "." $buffer`;
#$p = "data/" + $buffer[0] ;
#
#//workspace -removeFileRuleEntry "diskCache";
#workspace -fileRule "diskCache" $p;
#workspace -saveWorkspace;
#
#CreateHairCacheOptions;
#
#file -save;
#
#workspace -fileRule "diskCache" "data";
#workspace -saveWorkspace;
    
        