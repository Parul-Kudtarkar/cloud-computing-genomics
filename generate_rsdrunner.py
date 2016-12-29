#this will generate rsdrunner which consist of python command-lines to run rsd algorithm
import re
import string
import sys
from optparse import OptionParser
def create_cmd(glist):
    s = glist[0]
    q = glist[1]
    out = ('%s_%s')%(s,q)
    path = "./genomes/genomes/"
    path1 = "./blastinput/blastinput/"
    cmd1 = "python ./RSD_standalone/RSD_standalone/RSD.py --thresh=1e-20 --div=0.2 -q %s -s %s -o ./result/result/%s --fbh=%s --revbh=%s"%(path+s+'/'+s, path+q+'/'+q, out+'_0.2_1e-20',path1+s+'_'+q+'_blast_hits_f',path1+s+'_'+q+'_blast_hits_r')
    cmd2 = "python ./RSD_standalone/RSD_standalone/RSD.py --thresh=1e-20 --div=0.5 -q %s -s %s -o ./result/result/%s --fbh=%s --revbh=%s"%(path+s+'/'+s, path+q+'/'+q, out+'_0.5_1e-20',path1+s+'_'+q+'_blast_hits_f',path1+s+'_'+q+'_blast_hits_r')
    cmd3 = "python ./RSD_standalone/RSD_standalone/RSD.py --thresh=1e-20 --div=0.8 -q %s -s %s -o ./result/result/%s --fbh=%s --revbh=%s"%(path+s+'/'+s, path+q+'/'+q, out+'_0.8_1e-20',path1+s+'_'+q+'_blast_hits_f',path1+s+'_'+q+'_blast_hits_r')
    cmd4 = "python ./RSD_standalone/RSD_standalone/RSD.py --thresh=1e-15 --div=0.2 -q %s -s %s -o ./result/result/%s --fbh=%s --revbh=%s"%(path+s+'/'+s, path+q+'/'+q, out+'_0.2_1e-15',path1+s+'_'+q+'_blast_hits_f',path1+s+'_'+q+'_blast_hits_r')
    cmd5 = "python ./RSD_standalone/RSD_standalone/RSD.py --thresh=1e-15 --div=0.5 -q %s -s %s -o ./result/result/%s --fbh=%s --revbh=%s"%(path+s+'/'+s, path+q+'/'+q, out+'_0.5_1e-15',path1+s+'_'+q+'_blast_hits_f',path1+s+'_'+q+'_blast_hits_r')
    cmd6 = "python ./RSD_standalone/RSD_standalone/RSD.py --thresh=1e-15 --div=0.8 -q %s -s %s -o ./result/result/%s --fbh=%s --revbh=%s"%(path+s+'/'+s, path+q+'/'+q, out+'_0.8_1e-15',path1+s+'_'+q+'_blast_hits_f',path1+s+'_'+q+'_blast_hits_r')
    cmd7 = "python ./RSD_standalone/RSD_standalone/RSD.py --thresh=1e-10 --div=0.2 -q %s -s %s -o ./result/result/%s --fbh=%s --revbh=%s"%(path+s+'/'+s, path+q+'/'+q, out+'_0.2_1e-10',path1+s+'_'+q+'_blast_hits_f',path1+s+'_'+q+'_blast_hits_r')
    cmd8 = "python ./RSD_standalone/RSD_standalone/RSD.py --thresh=1e-10 --div=0.5 -q %s -s %s -o ./result/result/%s --fbh=%s --revbh=%s"%(path+s+'/'+s, path+q+'/'+q, out+'_0.5_1e-10',path1+s+'_'+q+'_blast_hits_f',path1+s+'_'+q+'_blast_hits_r')
    cmd9 = "python ./RSD_standalone/RSD_standalone/RSD.py --thresh=1e-10 --div=0.8 -q %s -s %s -o ./result/result/%s --fbh=%s --revbh=%s"%(path+s+'/'+s, path+q+'/'+q, out+'_0.8_1e-10',path1+s+'_'+q+'_blast_hits_f',path1+s+'_'+q+'_blast_hits_r')
    cmd10 = "python ./RSD_standalone/RSD_standalone/RSD.py --thresh=1e-5 --div=0.2 -q %s -s %s -o ./result/result/%s --fbh=%s --revbh=%s"%(path+s+'/'+s, path+q+'/'+q, out+'_0.2_1e-5',path1+s+'_'+q+'_blast_hits_f',path1+s+'_'+q+'_blast_hits_r')
    cmd11 = "python ./RSD_standalone/RSD_standalone/RSD.py --thresh=1e-5 --div=0.5 -q %s -s %s -o ./result/result/%s --fbh=%s --revbh=%s"%(path+s+'/'+s, path+q+'/'+q, out+'_0.5_1e-5',path1+s+'_'+q+'_blast_hits_f',path1+s+'_'+q+'_blast_hits_r')
    cmd12 = "python ./RSD_standalone/RSD_standalone/RSD.py --thresh=1e-5 --div=0.8 -q %s -s %s -o ./result/result/%s --fbh=%s --revbh=%s"%(path+s+'/'+s, path+q+'/'+q, out+'_0.8_1e-5',path1+s+'_'+q+'_blast_hits_f',path1+s+'_'+q+'_blast_hits_r')
    return (cmd1,cmd2,cmd3,cmd4,cmd5,cmd6,cmd7,cmd8,cmd9,cmd10,cmd11,cmd12)
def pairing(j):
    cmds1 = ""
    count = len(j)
    ex_dic = {}
    for a in range(count):
        elsewhere = range(0, a) + range(a + 1, count)
        for b in elsewhere:
            combo=[j[a],j[b]]
            mirror_1 = j[b]+j[a]                                                           
            mirror_2 = j[a]+j[b]
            if ex_dic.has_key(mirror_2):
                continue
            if not ex_dic.has_key(mirror_1):
                ex_dic[mirror_1]=""
            combo.sort()    
            cmds1 += "%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n"%create_cmd(combo)    
            print "List of query and subject genomes:",combo        
    return cmds1                                                                                                                                                                     
def main():
    #opens file as a long string,every genome is seperated by a newline character(\n)
    import optparse
    parser = optparse.OptionParser(usage='%prog [options] [arg]...')
    parser.add_option('--source',help='Required. Path to the genomeslist file')
    parser.add_option('--destination',help='Required.Path to the rsdruner file')
    options, args = parser.parse_args()
    f1=options.source
    f2=options.destination
    print f1
    print f2
    tocompute=open(f1,'r').read()
    #print j
    j=string.split(tocompute,'\n')
    outf= open(f2,'w')
    cmds=pairing(j)
    output="%s\n"%(cmds)
    outf.write(output)
if __name__ == '__main__':
    main()
