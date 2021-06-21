import re
import sys
import getopt

def write_list_to_file(fn,tb):
    fp = open(fn,'w+')
    for line in tb:
        fp.write(line+'\n')
    fp.close()


def rm_comments(file_name):
    file = open(file_name, 'r')
    out = []
    try:
        while True:
            line = file.readline()
            if line:
                print(type(line), line)
                try:
                    ind = line.index(";")             
                    if ind >= 0:
                        out.append( line[:ind].strip() )
                    else:
                        out.append(line)
                except ValueError:
                    out.append(line)
            else:
                break
    finally:
        file.close()   
    write_list_to_file("rmc_"+file_name,out)
    
import sys,getopt

if __name__ == '__main__':
    fn=None
    try:
        opts,args=getopt.getopt(sys.argv[1:],"hf:",["help","file_name="]);
    except getopt.GetoptError:
        print("-f xx.svg")
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print("-f xx")
            sys.exit()
        elif opt == '-f':
            fn=arg
    if fn:
        print(fn)
        out=rm_comments(fn)
    else :
        print("no file name assign, please use : -f xx.svg")
