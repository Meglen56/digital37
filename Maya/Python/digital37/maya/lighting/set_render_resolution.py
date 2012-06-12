import pymel.core as pm
import traceback

def main(w,h,log=None):
    if not log:
        import logging
        log = logging.getLogger()
    # use ' ' as a fill char and center aligned
    log.debug('{0:-<40}'.format('set_render_resolution'))

    defaultResolution = pm.PyNode('defaultResolution')
    if defaultResolution.w.get() != w :
        try:
            defaultResolution.w.set( int(w) )
        except:
            log.error('set defaultResolution.w error')
            log.error( traceback.format_exc() )
        else:
            log.debug('set defaultResolution.w success.')
    if defaultResolution.h.get() != h :
        try:
            defaultResolution.h.set( int(h) )
        except:
            log.error('set defaultResolution.h error')
            log.error( traceback.format_exc() )
        else:
            log.debug('set defaultResolution.h success.')
