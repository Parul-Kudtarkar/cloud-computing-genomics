#!/usr/bin/env python
import sys
import os
#appends environment variables to define path to roundup executables
newpath = os.getcwd() + '/executables/executables'
os.environ['PATH']= newpath + ':' + os.environ['PATH'] 
import os.path
#Run rsd algorithm
for cmd in sys.stdin:
	if (cmd==""):
		sys.stderr.write("reporter:counter:cmd,missing,1\n")
	else:
		sys.stderr.write("reporter:status:%s" %cmd)
		os.system(cmd)
