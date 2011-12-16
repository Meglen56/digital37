import pymel.core as pm
import grid.path
import grid.maya.utils

def replaceProxy():
    if pm.objExists("UWc01_001:UnderwaterChase_C_001_ast") :
        #pm.mel.eval("proxySwitch UWc01_001:HIr01_001RN;")
        pm.mel.eval("proxySwitch UWc01_001:MAr01_001RN;")
        try :
            pm.parent("UWc01_001:HIr01_001:HidingRock_C_001_ast", "Master_C_001_sht")
        except :
            pass
        
        
def isExcluded(assetNode):
    excludedList = list()
    excludedList.append('SCa01_001:StereoCam_C_001_ast')
    excludedList.append("FIr01_001_rig:RockFish_C_001_ast")
    excludedList.append('UWc01_001:MAr01_001:MainRock_C_001_ast')
    excludedList.append('UWc01_001:HIr01_001:HidingRock_C_001_ast')
    #excludedList.append('UWc01_001:UnderwaterChase_C_001_ast')
    
    if str(assetNode) in excludedList :
        return True
    else :
        return False

def main():
    replaceProxy()
    shotNode = pm.PyNode("Master_C_001_sht")
    assetList = shotNode.listRelatives(type="gAsset", ad=True)
    for assetNode in assetList :
        print "EXPORTING :", assetNode
        if assetNode.visibility.get() :
            if not 'layout' in str(assetNode) :
                if not isExcluded(assetNode) :
                    # smooth all mesh
                    if  str(assetNode) == 'UWc01_001:UnderwaterChase_C_001_ast' :
                        geoGrp = pm.PyNode("UWc01_001:Geo_C_001_grp")
                        shapeNodes = geoGrp.listRelatives(type="mesh", ad=True)
                    else :
                        shapeNodes = assetNode.toGeoCache.inputs(shapes=True)
                    for elem in shapeNodes :
                        pm.polySmooth(elem,mth=0,dv=1,bnr=1,c=1,kb=0,ksb=0,khe=0,kt=0,kmb=1,suv=1,peh=0,sl=1,dpe=1,ps=0.1,ro=1,ch=0)
                    pm.select(assetNode)
                    pm.select(shapeNodes, add=True)
                else :
                    pm.select(assetNode)
                    pm.select(assetNode.listRelatives(ad=True), add=True)
            else :
                continue
                    
            #buildName and path
            nameSpaceList = assetNode.split(':')
            if len(nameSpaceList) == 2 :
                assetShortName = nameSpaceList[0]
            elif len(nameSpaceList) == 3 :
                assetShortName = nameSpaceList[1]
            scenePath = grid.path.path(pm.system.sceneName())
            scenePathList = scenePath.split('/')
            baseScenePath = grid.path.path('/'.join(scenePathList[:scenePathList.index('anim')]))
            cacheDirPath = baseScenePath.joinpath('data','alembic')
            pm.sysFile(cacheDirPath, makeDir=True)
            cacheFilePath = cacheDirPath.joinpath('%s.abc'%assetShortName)
            cacheFilePath = cacheFilePath.replace('\\','/')
            start, end = grid.maya.utils.getTimelineFrameRange()
            
            print "ALEMBIC PATH:", cacheFilePath
            pm.mel.eval('AbcExport -j "-fr %s %s -stripNamespaces -writeVisibility -attr focalLength -worldSpace -uv -root %s -sl -file %s";'%(start, end, assetNode, cacheFilePath))
    alembicDir = grid.path.path(cacheFilePath).parent
    pm.newFile(f=True)
    for fileAbc in alembicDir.files() :
        print "IMPORTING :", fileAbc
        fileAbc = fileAbc.replace('\\','/')
        pm.mel.eval('AbcImport -d -m import "%s";'%fileAbc)
