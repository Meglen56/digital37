import pymel.core as pm
import traceback

def main(w,h):
    debug,error = list()
    
    # use '*' as a fill char and center aligned
    debug.append('{0: ^80}'.format('set_render_resolution'))
    error.append('{0: ^80}'.format('set_render_resolution'))
    
    defaultResolution = pm.PyNode('defaultResolution')
    if defaultResolution.w.get() != w :
        try:
            defaultResolution.w.set( int(w) )
        except:
            traceback.print_exc()
            error.append('set defaultResolution.w error')
        else:
            debug.append('set defaultResolution.w success.')
    if defaultResolution.h.get() != h :
        try:
            defaultResolution.h.set( int(h) )
        except:
            traceback.print_exc()
            error.append('set defaultResolution.h error')
        else:
            debug.append('set defaultResolution.h success.')
    return ['\r\n'.join(debug), '\r\n'.join(error)]
