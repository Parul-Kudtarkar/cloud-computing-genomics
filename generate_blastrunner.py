#this will generate blastrunner which consist of python command-lines to run blast
import re
import string
import sys
from optparse import OptionParser
def create_cmd(glist):
    s=glist[0]
    q=glist[1]
    out=('%s_%s')%(s,q)
    path="./genomes/genomes/"
    cmd1= "python ./RSD_standalone/RSD_standalone/Blast_compute.py -q %s -s %s -o ./blastinput/blastinput/%s"%(path+s+'/'+s, path+q+'/'+q, out+'_blast_hits_f')
    cmd2= "python ./RSD_standalone/RSD_standalone/Blast_compute.py -q %s -s %s -o ./blastinput/blastinput/%s"%(path+q+'/'+q,path+s+'/'+s,out+'_blast_hits_r')
    return(cmd1,cmd2)
def pairing(j):
    cmds1=""
    count =len(j)
    ex_dic = {}
    for a in range(count):
        elsewhere=range(0,a)+range(a+1,count)
        for b in elsewhere:
            combo=[j[a],j[b]]
            mirror_1= j[b]+j[a]
            mirror_2=j[a]+j[b]
            if ex_dic.has_key(mirror_2):
                continue
            if not ex_dic.has_key(mirror_1):
                ex_dic[mirror_1]=""
                combo.sort()
                print "this is combo1",combo
            cmds1 += "%s\n%s\n"%create_cmd(combo)
    return cmds1      
def main():
    #opens file as a long string,every genome is seperated by a newline character(\n)
    import optparse
    parser = optparse.OptionParser(usage='%prog [options] [arg]...')
    parser.add_option('--source',help='Required. Path to the genomeslist file')
    parser.add_option('--destination',help='Required.Path to the blastrunner file')
    options, args = parser.parse_args()
    f1=options.source
    f2=options.destination
    tocompute=open(f1,'r').read()
    j=string.split(tocompute,'\n')
    outf=open(f2,'w')
    cmds=pairing(j)
    output="%s\n"%(cmds)
    outf.write(output)
if __name__ == '__main__':
    main()
