################# QIIME PIPELINE FOR CLINICAL METAGENOMICS ANALYSIS ON CYCTIC FIBROSIS PATIENTS ###############
SCIPTNAME  :	bowtie2_toqiime.sh
VERSION    :	1.1
DATE	    :	November 24th 2015
DEVELOPERS :	Clinical Metagenomics Group
ADVISOR    :	Dr. Fredrik Vannberg
INSTITUTE  :   Georgia Institute of Technology, Atlanta
###############################################################################################################

REQUIREMENTS: 1. Clinical data in fastq format generated from Illumina Hi-Seq placed in a working directory
	      2. Install latest version of Qiime from http://qiime.org/ and create an environmental variable 
		 named "pandaseq"
	      3. Install latest version of Pandaseq from https://github.com/neufeld/pandaseq and add all .py 
		 scripts to the $PATH
              4. Install latest version of bowtie2 and create an environmental variable named "bowtie2" from 
	 	 http://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.2.6/
	      5. Download the latest version of human reference genome with bowtie2 indices from NCBI and pl-
		 ace the files on /human_genome folder in working directory.

ADD-ONS	    : The pipeline is designed to download the fungal ITS database and greengenes bacterial and arch-
	      eal 16S databases and to prepare the mapping and parameter files required by qiime to run.

###############################################################################################################

#WORKFLOW 

STEP1	    : Downloads the fngal ITS database and unzip the folder
STEP2       : Aligns the query data to the human reference and combines the unaligned data into a fastq file
STEP3	    : Preprocesses this unaligned data to remove the chimeric sequences for qiime
STEP4	    : Picks open reference otus using UCLUST algorithm for alignment
STEP5	    : Summarizes the output of the otu picking algorithm and creates plots in .html format
STEP6       : Pickes otus of bacterial and archeal taxa from the sequences failed to align with fungi in step4
STEP7       : Summarizes the output from step6 and creates plots in .html formt

###############################################################################################################
