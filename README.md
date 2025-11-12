# Cloud Computing for Comparative Genomics

> Scalable ortholog computation using Amazon's Elastic MapReduce (EMR) and the Reciprocal Smallest Distance (RSD) algorithm

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Cloud](https://img.shields.io/badge/platform-AWS%20EMR-orange.svg)](https://aws.amazon.com/emr/)

##  Publications

This repository contains the implementation described in:

- Wall, D.P., Kudtarkar, P., Fusaro, V., Pivovarov, R., Patil, P., & Tonellato, P. (2010). [Cloud computing for comparative genomics](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-11-259). *BMC Bioinformatics*, 11(1), 259.

- Kudtarkar, P., DeLuca, T.F., Fusaro, V.A., Tonellato, P.J., & Wall, D.P. (2010). [Cost‐effective cloud computing: a case study using the comparative genomics tool Roundup](http://www.la-press.com/cost-effective-cloud-computing-a-case-study-using-the-comparative-geno-article-a2422). *Evolutionary Bioinformatics*, 6, 197–203.

##  Overview

This package enables distributed computation of orthologous genes across multiple genomes using Amazon's cloud infrastructure. By leveraging MapReduce, it significantly reduces the computational time required for large-scale comparative genomics analyses.

### Key Features

- **Scalable**: Process multiple genomes in parallel using cloud resources
- **Cost-effective**: Pay-as-you-go cloud computing model
- **Distributed**: Leverages Hadoop MapReduce for efficient computation
- **Comprehensive**: Includes BLAST pre-computation and RSD ortholog estimation

##  Repository Structure

```
cloud-computing-genomics/
├── Scripts/
│   ├── blastmapper.py         # Mapper for BLAST estimation
│   ├── rsdmapper.py           # Mapper for ortholog estimation
│   ├── generate_blastrunner.py # Generate BLAST runner commands
│   └── generate_rsdrunner.py   # Generate RSD runner commands
├── RSD_standalone/            # RSD algorithm implementation
├── executables.tar.gz        # Required binaries (PAML, ClustalW)
├── blastout.sh               # Setup BLAST output directories
├── example/                  # Example genomes and runner files
├── log/                      # EMR logs directory
├── blast_result/             # BLAST results placeholder
└── ortholog_result/          # Ortholog results placeholder
```

##  Prerequisites

### Software Requirements

- Python 2.7+
- [Amazon S3 Tools](http://s3tools.org/s3cmd) (s3cmd)
- [Elastic MapReduce Ruby CLI](http://developer.amazonwebservices.com/connect/entry.jspa?externalID=2264)
- Active AWS account with S3 and EMR access

### Required Binaries

 **Important**: Washington University BLAST 2.0 requires a [license agreement](http://blast.wustl.edu/licensing) before downloading.

You'll need:
- `blastp` (protein BLAST tool)
- `xdget`
- `xdformat`
- BLAST matrix folder
- ClustalW (included)
- PAML codeml (included)

##  Installation & Setup

### Step 1: Prepare Genomes

Format your FASTA genomes with unique prefix identifiers:

```bash
# Each FASTA entry should have a unique prefix
# Strip problematic characters from name fields
# Format for blastp using xdformat
```

See `example/genomes/` for properly formatted examples.

### Step 2: Configure Executables

1. Download BLAST binaries (after licensing)
2. Set permissions:
   ```bash
   chmod 777 blastp xdget xdformat
   ```
3. Package executables:
   ```bash
   tar czf executables.tar executables/
   ```

### Step 3: Generate Runner Files

Create a `genomeslist` file containing genome names, then:

```bash
# Generate BLAST runner
python generate_blastrunner.py \
    --source /path/to/genomeslist \
    --destination /path/to/blastrunner

# Generate RSD runner
python generate_rsdrunner.py \
    --source /path/to/genomeslist \
    --destination /path/to/rsdrunner
```

### Step 4: Configure S3 Bucket

Update S3 bucket references in:
- `RSD_standalone/Blast_compute.py` (line 101)
- `RSD_standalone/RSD.py` (line 845)

Replace `<s3bucketname>` with your actual bucket name.

### Step 5: Upload to S3

```bash
# Package genomes and RSD standalone
tar czf genomes.tar genomes/
tar czf RSD_standalone.tar RSD_standalone/

# Upload all required files
s3cmd put *.py *.tar.gz *.sh s3://your-bucket-name/
```

##  Running on AWS EMR

### 1. Create EMR Cluster

```bash
./elastic-mapreduce --create --alive \
    --name "ortholog-computation" \
    --num-instances 4 \
    --instance-type c1.xlarge \
    --log-uri s3n://your-bucket/log
```

### 2. Setup HDFS Directories

```bash
# Get job flow ID
./elastic-mapreduce --list --active

# Create placeholders
./elastic-mapreduce --jobflow YOUR_JOB_ID \
    --jar s3://elasticmapreduce/libs/script-runner/script-runner.jar \
    --args s3://your-bucket/blastout.sh
```

### 3. Run BLAST Pre-computation

```bash
# Copy input files
./elastic-mapreduce --jobflow YOUR_JOB_ID \
    --jar s3://elasticmapreduce/samples/distcp/distcp.jar \
    --args s3://your-bucket/blastrunner,hdfs:///home/hadoop/blastrunner

# Run BLAST mapper
./elastic-mapreduce -j YOUR_JOB_ID --stream \
    --input hdfs:///home/hadoop/blastrunner \
    --mapper s3n://your-bucket/blastmapper.py \
    --reducer NONE \
    --cache-archive s3n://your-bucket/executables.tar.gz#executables \
    --cache-archive s3n://your-bucket/genomes.tar.gz#genomes \
    --jobconf mapred.map.tasks=10 \
    --jobconf mapred.task.timeout=604800000
```

### 4. Run Ortholog Estimation

```bash
# Copy RSD runner
./elastic-mapreduce --jobflow YOUR_JOB_ID \
    --jar s3://elasticmapreduce/samples/distcp/distcp.jar \
    --args s3://your-bucket/rsdrunner,hdfs:///home/hadoop/rsdrunner

# Run RSD mapper
./elastic-mapreduce -j YOUR_JOB_ID --stream \
    --input hdfs:///home/hadoop/rsdrunner \
    --mapper s3n://your-bucket/rsdmapper.py \
    --reducer NONE \
    --cache-archive s3n://your-bucket/executables.tar.gz#executables \
    --cache-archive s3n://your-bucket/genomes.tar.gz#genomes \
    --output hdfs:///home/hadoop/output
```

##  Monitoring

Monitor job progress using FoxyProxy with SSH tunnel:

1. Establish SOCKS proxy on local machine
2. Create SSH tunnel to master node
3. Access Hadoop UI through browser

##  Retrieving Results

```bash
# Terminate cluster
./elastic-mapreduce --terminate -j YOUR_JOB_ID

# Download results
s3cmd get -r s3://your-bucket/ortholog_result/ ./results/
```

##  Configuration Options

### MapReduce Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `mapred.map.tasks` | 10 | Number of map tasks |
| `mapred.task.timeout` | 604800000 | Task timeout (ms) |
| `mapred.tasktracker.map.tasks.maximum` | 7-8 | Max tasks per node |
| `mapred.map.tasks.speculative.execution` | false | Disable speculation |

## Notes

- Ensure all FASTA headers are unique and properly formatted
- Monitor S3 costs as intermediate results are stored there
- Consider using spot instances for cost savings
- Results are stored in tab-delimited format

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Contact

For questions or support, please open an issue on GitHub.

## Acknowledgments

- Amazon Web Services for cloud infrastructure
- Washington University for BLAST tools
- Contributors to PAML and ClustalW

---

*For detailed methodology and performance benchmarks, please refer to our [publications](#-publications).*
