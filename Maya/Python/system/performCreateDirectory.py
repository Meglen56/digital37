import os
import traceback
import itertools
import pickle

class PerformCreateDirectory():
    def __init__(self):
        self.Dir_Root = ''
        self.Dir_Framework = list()
        self.Dir_Name = dict()
        self.Dir_Acture = list()
        self.V = None
        
    #self.Dir_Framework: [{['a']: ['1', '']}, {['b']: [{'2': ['I', 'II']}]}, ['c']]                                                                                 
    def create_directory(self,dir_root,dir_list):
        # create ep directory
        for f in dir_list:
            if type(f) is type('') :
                if f:
                    self.make_dir(dir_root,f)
                else:
                    # skip for ''
                    pass
            if type(f) is type(list()) :
                #
                for l in f:
                    if type(l) is type(dict()) :
                        for k,v in l.iteritems() :
                            for x in k.split() :
                                root_dir = os.path.join(dir_root,x)
                                print 'root_dir:\t%s' % root_dir
                                print 'v:\t%s' % v
                                self.create_directory(root_dir,v)
                    else:
                        print 'l:\t%s' % l
                        if l:
                            self.make_dir(dir_root, l)
            else:
                print 'type error in dir_list'

    # make folders and files
    def make_dir(self,root,name):
        root = root.replace('\\','/')
        # TODO 
        # root = ../sc010/sc010_shot0020/light
        # root_list = ['sc010_shot0020', 'light']
        #root_list = root.split('/')[-2:]
        #print root_list
        d = os.path.join(root,name).replace('\\','/')
        print 'd:%s' % d
        if not os.path.exists(d):
            if os.path.dirname(d) == d :
                # create folder
                try:
                    os.makedirs(d)
                except:
                    traceback.print_exc()
            else :
                # create file
                # create folder first
                if not os.path.exists(os.path.dirname(d)):
                    try:
                        os.makedirs(os.path.dirname(d))
                    except:
                        traceback.print_exc()
                    else:
                        # create file
                        try:
                            fd = open(d,'w')
                        except:
                            traceback.print_exc()
                        else:
                            fd.close()
                else:
                    # create file
                    try:
                        fd = open(d,'w')
                    except:
                        traceback.print_exc()
                    else:
                        fd.close()

    def get_acture_name(self,sourceList,pattern=None):
        targetList = sourceList
        #targetList = list()
        # self.Dir_Framework 
        # self.Dir_Name 
        # self.Dir_Framework: [{'sc': [{'sc+x+shot': [{'type': ['sc+x+shot+x+type+.mb']}]}]}]
        for l,i in zip(sourceList,xrange(len(sourceList))):
            targetList[i] = list()
            #targetList.append(list())
            if type(l) is type(dict()) :
                print 'l:\t%s' % l
                for k,self.V in l.iteritems():
                    # k: 'sc'
                    # v: [{'sc+x+shot': [{'type': ['sc+x+shot+x+type+.mb']}]}]
                    
                    # k = 'a' with no '+'
                    print 'k:%s' % k
                    a = self.get_mapped_name( k )
                    print 'a:',a
                    returnList = self.get_acture_name(self.V)

                    # rerurnList: {'type': ['sc+x+shot+x+type+.mb']}
                    for x in a:
                        print 'x:\t%s' % x
                        print 'self.V:\t%s' % self.V
                        #returnList = self.get_mapped_name(self.V,x)
                        print 'self.V:\t%s' % self.V
                        print 'returnList:\t%s' % returnList
                    
                        targetList[i].append( {x:returnList} )
            else :       
                print '*l:\t%s' % l
                print '*pattern:\t%s' % pattern
                targetList[i] = self.get_mapped_name(l,pattern)
            print 'targetList\t%s' % targetList
            print 'sourceList\t%s' % sourceList
        return targetList

    def get_mapped_name(self,l,pattern=None):
        t = list()
        if l.find('+') == -1 :
            # l = 'c'
            if l in self.Dir_Name:# l in self.Dir_Name
                for x in self.Dir_Name[l].split() :
                    print 'x:\t%s' % x
                    t.append(x)
            else:# l not in self.Dir_Name
                # use l for value 
                t.append(l)
        else:
            # l = 'c+d'
            # split '+'
            t1 = list()
            for x in l.split('+') :
                tmp = list()
                if x in self.Dir_Name:# x in self.Dir_Name
                    for y in self.Dir_Name[x].split() :
                        tmp.append(y)
                    t1.append(tmp)
                else:# x not in self.Dir_Name
                    tmp.append(x)
                    t1.append(tmp)
            print 't1:\t%s' % t1
            
            print 'pattern:\t%s' % pattern
            # t1 = {'a': ['aa', 'bb'], 'b': ['bb', 'cc']}
            
            # use pattern replace item in t1
            t1_repl = list()
            tmp_pattern = list()
            tmp_pattern.append(pattern)
            for x in t1:
                if pattern in x:
                    t1_repl.append(tmp_pattern)
                else:
                    t1_repl.append(x)
            print t1_repl
            t1_product = list( self.product(t1_repl) )
            print t1_product
            # t = [('aa', 'bb'), ('aa', 'cc'), ('bb', 'bb'), ('bb', 'cc')]
            for x in t1_product:
                t.append( ''.join(x) )
        #t = ' '.join(t)
        print 't:\t%s' % t
        return t
                
    # from itertools's product function
    def product(self,inputList):
        # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
        # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
        #pools = map(tuple, args) * kwds.get('repeat', 1)
        #pools = map(tuple, args) * kwds.get('repeat', 1)
        pools = list(x for x in inputList)
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        for prod in result:
            yield list(prod)
            
    def perform_create_directory(self):
        print 'self.Dir_Root\t%s' % self.Dir_Root
        print 'self.Dir_Framework\t%s' % self.Dir_Framework
        print 'self.Dir_Name\t%s' % self.Dir_Name

        self.Dir_Acture = self.get_acture_name( self.Dir_Framework )
        print 'self.Dir_Acture\t%s' % self.Dir_Acture
        self.create_directory(self.Dir_Root, self.Dir_Acture)
                                    
def main():
    a = PerformCreateDirectory()
    a.Dir_Root='D:/Autodesk'
    a.Dir_Framework=[{'sc':[{'sc+_+shot': [{'type':['sc+_+shot+_+type+.mb']}]}]}]
    a.Dir_Name={'sc': 'sc010', 'shot': 'shot0010 shot0020', 'type': 'anim light'}
    a.perform_create_directory()
    
if __name__ == '__main__' :
    main()
    #pass
    
#    #self.Dir_Framework: [{['a']: ['1', '']}, {['b']: [{'2': ['I', 'II']}]}, ['c']]                                                                                 
#    def create_directory(self,dir_root,dir_list):
#        # create ep directory
#        for f in dir_list:
#            if type(f) is type('') :
#                if f:
#                    f = f.split() 
#                    # for 'some name'
#                    # create folder
#                    for x in f :
#                        print 'x:%s' %x
#                        print 'dir_root:%s' % dir_root                
#                        self.make_dir(dir_root,x)
#                else:
#                    # skip for ''
#                    pass
#            elif type(f) is type(dict()) :
#                #
#                for k,v in f.iteritems() :
#                    for x in k.split() :
#                        root_dir = os.path.join(dir_root,x)
#                        print 'root_dir:\t%s' % root_dir
#                        print 'v:\t%s' % v
#                        self.create_directory(root_dir,v)
#            else:
#                print 'type error in dir_list'