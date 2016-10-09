cloud-computing-genomics
manuscript->Dennis P. Wall, Parul Kudtarkar, Vincent Fusaro, Rimma Pivovarov, Prasad Patil, and Peter Tonellato. Cloud computing for comparative genomics. BMC Bioinformatics, Vol. 11, No. 1. (2010), 259.
Parul Kudtarkar, Todd F. DeLuca, Vincent A. Fusaro, Peter J. Tonellato and Dennis P. Wall, Cost‐effective cloud computing: a case study using the comparative genomics tool Roundup. Evolutionary Bioinformatics , (2010) 6: 197–203
manuscript link:https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-11-259
http://www.la-press.com/cost-effective-cloud-computing-a-case-study-using-the-comparative-geno-article-a2422
This file explains ortholog computation using Amazon's Elastic MapReduce cloud
---------------------------------------------
The Cloud_RSD package contains the following:
---------------------------------------------
blastmapper.py -> mapper script for blast estimation step
rsdmapper.py -> mapper script for ortholog estimation
generate_blastrunner.py -> this script generates blastrunner file(file containing set of commands to run blast)
generate_rsdrunner.py -> this script generates rsdrunner file(file containing set of commands to run ortholog estimation)
exectuables.tar.gz -> this  gzipped tar folder consist of paml, clustalw executables required by the RSD algorithm in order to estimate orthologs
RSD_standalone -> consist of scripts to compute orthologs using RSD algorithm
blastout.sh -> script to generate place-holder/folder to hold pre-computed blast results
blastinput.tar.gz -> place holder for blast results in hadoop distributed file system
result.tar.gz -> place holder for rsd results in hadoop distributed file system
blast_result -> place holder for blast results 
ortholog_result -> place holder for rsd(orthology estimation)
log - > stores Amazon's Elastic MapReduce specific logs
example -> contains example of genome and runner files
-----------------------------------------------------------------------------------------------------------------------------------------------
Steps to run RSD algorithm on Amazon's Elastic MapReduce cloud(Refer to the manuscript Cloud Computing for Comparative Genomics by Wall et al.)
-----------------------------------------------------------------------------------------------------------------------------------------------
Step1: get your FASTA formatted Genomes that you care to analyze and ensure that each fasta entry of the query has a unique prefix identifier,pre-formatted using a program designed to strip out offending characters from the name field and formatted for blastp using xdformat(refer the genomes folder within the example folder)

Step2: executables
The Washington University BLAST 2.0 executables require that a license agreement be established at the following website http://blast.wustl.edu/licensing before downloading.The programs blastp (the protein based blast tool), xdget, matrix folder within the wublast package and xdformat are required to run RSD. Also ensure that the blastp (the protein based blast tool), xdget and xdformat binary files have execute, write and read permission( chmod 777 blastp). We have already made the codeml and clustalw binaries available in the executable folder. Insert blastp,xdget,xdformat binaries and matrix folder within the executables folder and create a gzipped tar ball i.e.
commands:tar cvf executables.tar executables/
         gzip executables.tar

Step3: Generate blast and rsd runner file
create a flat file genomeslist within the Cloud_RSD folder which contains genome names for which we desire to compute orthologs(refer the flat file genomeslist in the examples folder)
Run generate_blastrunner.py(python generate_blastrunner.py --source <Path to the genomeslist file> --destination <Path to store the blastrunner file>) to generate blastrunner file
Run generate_rsdrunner.py(python generate_rsdrunner.py --source<Path to the genomeslist file> --destination <Path to store rsdrunner file>) to generate rsdrunner file

Step4: within RSD_standalone package in, 
Blast_compute.py(line 101) replace os.system("/home/hadoop/bin/hadoop fs -copyFromLocal %s s3n://<s3bucketname>/blastresult/"%outputDbName) "<s3bucketname>" with the actual name of your s3 bucket
RSD.py(line 845) replace os.system("/home/hadoop/bin/hadoop fs -copyFromLocal %s s3n://<s3bucketname>/out/"%outfile)  "<s3bucketname>" with the actual name of your s3 bucket

Step5:Create gzipped tar ball of genomes and RSD_standalone
example:pk76@orchestra:~/dev/trunk/Cloud_RSD$ tar cvf genomes.tar  genomes/
        pk76@orchestra:~/dev/trunk/Cloud_RSD$ gzip genomes.tar

Step6: Transfer contents of Cloud_RSD folder i.e. blastmapper.py,rsdmapper.py,executables.tar.gz,RSD_standalone.tar.gz,genomes.tar.gz,blastout.sh,blastinput.tar.gz,result.tar.gz,blast_result,ortholog_result,log,blastrunner,rsdrunner to your s3 bucket using s3cmd tool(http://s3tools.org/s3cmd)
example:s3cmd put ~/dev/trunk/Cloud_RSD/RSD_standalone.tar.gz s3://<s3bucketname>/
Where <s3bucketname> is the actual name of your s3 bucket

Step7:Run RSD on cloud(using elastic mapreduce ruby command line interface:http://developer.amazonwebservices.com/connect/entry.jspa?externalID=2264)
Example of a test rsd run on emr
Creating EMR job flow
~/Desktop/elastic-mapreduce-ruby CBI$ ./elastic-mapreduce --create --alive --name "roundup" --num-instances 4 --instance-type c1.xlarge --log-uri s3n://testingrsd/log

To list job id and DNS of master
~/Desktop/elastic-mapreduce-ruby CBI$ ./elastic-mapreduce --list --active
j-2I5DFUCGWDEYS     RUNNING        ec2-174-129-109-40.compute-1.amazonaws.com   roundup
 
Create place-holder/folder to hold pre-computed results in hdfs
~/Desktop/elastic-mapreduce-ruby CBI$ ./elastic-mapreduce --jobflow j-2I5DFUCGWDEYS --jar s3://elasticmapreduce/libs/script-runner/script-runner.jar --args s3://rounduptest/blastout.sh

Distcp input to blast mapper script
~/Desktop/elastic-mapreduce-ruby CBI$ ./elastic-mapreduce --jobflow j-2I5DFUCGWDEYS --jar s3://elasticmapreduce/samples/distcp/distcp.jar --args s3://testingrsd/blastrunner,hdfs:///home/hadoop/blastrunner

Run Blast mapper script ( Blast pre-computation)
~/Desktop/elastic-mapreduce-ruby CBI$ ./elastic-mapreduce -j j-2I5DFUCGWDEYS --stream --input hdfs:///home/hadoop/blastrunner  --mapper s3n://testingrsd/blastmapper.py --reducer NONE --cache-archive s3n://testingrsd/executables.tar.gz#executables --cache-archive s3n://testingrsd/genomes.tar.gz#genomes --cache-archive s3n://testingrsd/blastinput.tar.gz#blastinput 
--cache-archive s3n://testingrsd/RSD_standalone.tar.gz#RSD_--jobconf mapred.map.tasks=10 --jobconf mapred.task.timeout=604800000 --jobconf mapred.tasktracker.map.tasks.maximum=7 --jobconf mapred.task.tracker.expiry.interval=3600000 --jobconf mapred.map.tasks.speculative.execution=false

Distcp input to roundup mapper script
~/Desktop/elastic-mapreduce-ruby CBI$ ./elastic-mapreduce --jobflow j-2I5DFUCGWDEYS --jar s3://elasticmapreduce/samples/distcp/distcp.jar --args s3://testingrsd/rsdrunner,hdfs:///home/hadoop/rsdrunner

Run Roundup mapper script:
~/Desktop/elastic-mapreduce-ruby CBI$ ./elastic-mapreduce -j j-2I5DFUCGWDEYS --stream --input hdfs:///home/hadoop/rsdrunner --mapper s3n://testingrsd/rsdmapper.py --reducer NONE --cache-archive s3n://testingrsd/executables.tar.gz#executables --cache-archive s3n://testingrsd/genomes.tar.gz#genomes --cache-archive s3n://testingrsd/result.tar.gz#result --cache-archive s3n://testingrsd/RSD_standalone.tar.gz#RSD_standalone --cache-archive s3n://testingrsd/blastinput.tar.gz#blastinput --output hdfs:///home/hadoop/--jobconf mapred.tasktracker.map.tasks.maximum=8 --jobconf mapred.task.timeout=604800000 --jobconf mapred.tasktracker.expiry.interval=3600000 --jobconf mapred.map.tasks.speculative.execution=false

Step8: Monitor the job flow 
With the web address of the master node, monitor the status of the cluster through a user interface called FoxyProxy.To access this UI, it is necessary to establish SOCKS server on the local machine and an SSH tunnel between local machine and master node,  This UI shows general health of the cluster, including how many jobs were launched, how many are currently running, the number in queue, etc

Step9:Termiate the cluster upon completion of rsd computation and transfer the results to local system!!!
Termiate cluster 
~/Desktop/elastic-mapreduce-ruby CBI$ ./elastic-mapreduce --termiate -j j-2I5DFUCGWDEYS

Transfer result to local cluster using s3cmd
s3cmd get s3://<s3bucketname>/ortholog_result <destination directory in home folder>

