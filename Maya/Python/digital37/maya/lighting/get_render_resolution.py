import pymel.core as pm

def main():
    defaultResolution = pm.PyNode('defaultResolution')
    return (defaultResolution.w.get(),defaultResolution.h.get())
