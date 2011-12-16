import os
import fnmatch

def listOrTuple(obj):
    '''
    Return if obj is list or a tuple
    
    Param :
    obj = obj
    
    Return :
    listOrTuple = Boolean
    '''
    return isinstance(obj, (list,tuple))

def iterableNotString(obj):
    '''
    Return if obj is iterable but not a string
    
    Param :
    obj = obj
    
    Return :
    iterableNotString = boolean
    '''
    try : iter(obj)
    except TypeError : return False
    else : return not isinstance(obj, basestring)
    
def flatenList(sequence, aExpanser = listOrTuple):
    '''
    Flaten nested list.
    
    Param :
    sequence = iterable object
    aExpanser = fonction
    
    Return :
    list = generator
    '''
    
    for elem in sequence :
        if aExpanser(elem):
            for under_elem in flatenList(elem, aExpanser):
                yield under_elem
        else :
            yield elem
            
def listAllFiles (root,pattern='*',oneLevel = False, directory = False):
    pattern = pattern.split(';')
    for path, underDirectory, files in os.walk(root) :
        if directory :
            files.extend(underDirectory)
        files.sort()
        for name in files :
            for pat in pattern :
                if fnmatch.fnmatch(name, pat):
                    yield path, name
                    break
        if oneLevel :
            break
        
def str2bool(bool):
    '''
    Convert a string to a boolean if needed.
    
    param :
    str = string
    '''
    if type(bool) != 'bool' and isinstance(bool, basestring) :
        if bool.lower() == 'true' :
            return True
        elif bool.lower() == 'false' :
            return False
        else :
            raise ValueError
    elif type(bool) == 'bool' :
        return bool
    
    
def listIntersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

def listUnion(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

def listDifference(a, b):
    """ show whats in list b which isn't in list a """
    return list(set(b).difference(set(a)))


class Singleton(object):
    
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
    
    
## {{{ http://code.activestate.com/recipes/66531/ (r2)
class Borg:
    """ A borg singleton """
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state




