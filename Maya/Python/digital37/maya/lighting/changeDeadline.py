import maya.cmds as cmds
import maya.mel as mm

pool = "tony_pool"
gp = "none"
outputPath = "z:\D031SEER\sequence"
projectPath = "z:\D031SEER\MayaProject"

def delLayer():
        
    temp = cmds.ls("*:" + "defaultRenderLayer" + "*")
    for t in temp:
        print t
        if(t != "defaultRenderLayer"):
            cmds.select(t, r = True)
            mm.eval("doDelete")
            
def getOutputPath():
    
    fallName = cmds.file(q = True, l = True, sceneName = True)
    temp = fallName[0].split("/")
    print temp
    returnName = temp[len(temp) - 4] + "\\" + temp[len(temp) - 3] + "\\" + temp[len(temp) - 2]
    return outputPath + "\\" + returnName
    
def getFileName():
    
    fallName = cmds.file(q = True, l = True, sceneName = True)
    temp = fallName[0].split("/")
    print temp
    returnName = temp[len(temp) - 1].split(".")[0]
    return returnName


def initDeadline():
    
    mm.eval("source \"InitDeadlineSubmitter.mel\";")
    mm.eval("source \"SubmitMayaToDeadline.mel\";")

def changeDeadline():
    
    mm.eval("global string $JobNameGrp;")
    mm.eval("global string $ImageOutputPathGrp;")
    mm.eval("global string $ProjectPathGrp;")

    gJobName = mm.eval("string $temp = $JobNameGrp")
    gImage = mm.eval("string $temp = $ImageOutputPathGrp")
    gProject = mm.eval("string $temp = $ProjectPathGrp")
    print cmds.textFieldButtonGrp(gJobName, e = True, text = getFileName())
    cmds.optionMenuGrp("frw_deadlinePool", e = True, v = pool)
    cmds.optionMenuGrp("frw_Group", e = True, v = gp)
    cmds.intSliderGrp("frw_FrameGroup", e = True, v = 5)
    cmds.checkBox("frw_submitEachRenderLayer", e = True, v = 0)
    print cmds.textFieldButtonGrp(gImage, e = True, text = getOutputPath())
    print cmds.textFieldButtonGrp(gProject, e = True, text = projectPath)
    
def main():
    delLayer()
    initDeadline()
    changeDeadline()
    
if __name__ == "__main__":
    main()