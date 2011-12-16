import pymel.core as pm

joints = pm.ls(dag=1,sl=1,type='joint')
for joint in joints :
    
    plane = pm.polyPlane(sh=0,ax=[1,0,0],w=10,h=10,sx=1,sy=1)
    pm.select(joint,r=1)
    pm.select(plane,tgl=1)
    pm.pointConstraint(offset=[0.5,0,0],weight=1)
    pm.orientConstraint(offset=[0,0,0],weight=1)
    
    plane = pm.polyPlane(sh=0,ax=[1,0,0],w=10,h=10,sx=1,sy=1)
    pm.select(joint,r=1)
    pm.select(plane,tgl=1)
    pm.pointConstraint(offset=[-0.5,0,0],weight=1)
    pm.orientConstraint(offset=[0,0,0],weight=1)  
    
    