import time

def main():
    start_time = time.time()
    f0 = open('D:/temp2/mb2ma/shot035.ma','r')
    f1 = open('D:/temp2/mb2ma/shot035_.ma','w')
    f1.write(''.join(f0.readlines()))
    f0.close()
    f1.close()
    
    print (time.time()-start_time)

if __name__ == '__main__' :
    main()