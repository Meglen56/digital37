import pymel.core as pm
import traceback

def main(w,h):
    l = list()
    # use '*' as a fill char and center aligned
    l.append('{0: ^80}'.format('set_render_resolution'))
    
    defaultResolution = pm.PyNode('defaultResolution')
    if defaultResolution.w.get() != w :
        try:
            defaultResolution.w.set( int(w) )
        except:
            traceback.print_exc()
            return False
        else:
            l.append('set defaultResolution.w success.')
    if defaultResolution.h.get() != h :
        try:
            defaultResolution.h.set( int(h) )
        except:
            traceback.print_exc()
            return False
        else:
            l.append('set defaultResolution.h success.')
    return '\r\n'.join(l)