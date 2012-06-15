import digital37.maya.modeling.doubleDisplay as dd
reload(dd)
import digital37.maya.modeling.fiveFace as ff
reload(ff)
import digital37.maya.modeling.normalizeUV as nu
reload(nu)
import digital37.maya.modeling.deleteCamera as dc
reload(dc)

import digital37.maya.general.zeroObject as zo
reload(zo)
import digital37.maya.general.deleteDisplayLayer as ddl
reload(ddl)
import digital37.maya.general.deleteEmptyGroup as deg
reload(deg)
import digital37.maya.general.deleteHistory as dh
reload(dh)
import digital37.maya.general.deleteRenderLayer as drl
reload(drl)

import digital37.maya.lighting.deleteLight as dl
reload(dl)

def main():
    
    dd.main()
    ff.main()
    nu.main()
    dc.main()
    
    zo.main()
    ddl.main()
    deg.main()
    dh.main()
    drl.main()
    
    dl.main()