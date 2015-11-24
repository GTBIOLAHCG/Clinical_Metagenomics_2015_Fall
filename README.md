# Clinical_Metagenomics_2015_Fall

To deliver innovative, simple, flexible, and scalable solutions for comprehensive and rapid identification of fungal pathogens in clinical samples.

**1. Kraken Pipeline**:

A general Kraken pipeline that can be used for any metagenomics sample. This pipeline focus on fungi detection part and also involved a self defined fungal Kraken database. Input of this pipeline should be pair end fastq metagenomics reads. Output of this pipeline includes both Kraken report and Krona html report page of detected fungal reads.

Kraken:
`https://ccb.jhu.edu/software/kraken/`

**2. Qiime Pipeline**:





**2. MongoDB Pipeline**:

Easy to use pipeline for querrying input fastqs for fungal reads.

Dependencies :

1. Python3

2. MongoDB : https://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/

3. PyMongo : pip install pymongo

4. Install anaconda to get additional libraries which are used : https://www.continuum.io/downloads

5. KAnalyze : http://sourceforge.net/projects/kanalyze/


Note : Currently unaligned fastqs are required to run the program, these can be generated using the Kraken Pipeline

Usage : run the shell script mongodb_wrapper.sh inside the bin folder

        <path to mongodb_wrapper.sh> <input_folder containing unaligned fastqs> 


Output : Will create a folder with name as input_folder.outputs containing :

         1. A folder MongoDB containing the output html file, out.html
         
         2. json result file
         
         3. kc file
         
         4. Fasta files containing kmers for the top 10 species hit in the database
         
         5. A bar graph png 
