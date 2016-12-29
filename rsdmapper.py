#!/usr/bin/env python

import sys
import os
import re
import os.path
import string
#appends environment variables to define path to roundup executables
newpath = os.getcwd() + '/executables/executables'
os.environ['PATH']= newpath + ':' + os.environ['PATH'] 
import os.path
#copy the pre-computed blast result file from hdfs to local file system
for rsdcmd in sys.stdin:
	try:
		if (rsdcmd=='END\n'):
			sys.exit(0)
		elif (rsdcmd=='\n'):
			pass
		else:
			fwdseq=rsdcmd[rsdcmd.index('--fbh=./blastinput/blastinput/'):rsdcmd.index(' --revbh=')]
	                fwdseq1=re.sub('--fbh=./blastinput/blastinput/','',fwdseq)
	                revseq=rsdcmd[rsdcmd.index('--revbh=./blastinput/blastinput/'):]
	                revseq1=re.sub('--revbh=./blastinput/blastinput/','',revseq)
	                revseq2=re.sub(' ','',revseq1)
			revseq3=re.sub('\n','',revseq2)
		        hadoopf=[os.getcwd()+'/blastinput/blastinput']
	                hadoopf.append(fwdseq1)
	                hadoopf1=''.join(hadoopf)
	                hadoopr=[os.getcwd()+'/blastinput/blastinput']
	                hadoopr.append(revseq3)
	                hadoopr1=''.join(hadoopr)
	                #for forward blast hit extract file related to rsd command running
	                inpath =os.getcwd()+'/blastinput/blastinput/'
	                if os.path.exists(hadoopf1):
				pass
		        else:
				cmd1="hadoop dfs -copyToLocal hdfs:///home/hadoop/blastoutput/%s %s"%(fwdseq1,inpath)
		                os.system(cmd1)
		        if os.path.exists(hadoopr1):
				pass
		        else:
				cmd2="hadoop dfs -copyToLocal hdfs:///home/hadoop/blastoutput/%s %s"%(revseq3,inpath)
		                os.system(cmd2)
        finally:
	        if (rsdcmd==""):
			sys.stderr.write("reporter:counter:cmd,missing,1\n")
	        else:
			sys.stderr.write("reporter:status:%s"%rsdcmd)
		        os.system(rsdcmd)
