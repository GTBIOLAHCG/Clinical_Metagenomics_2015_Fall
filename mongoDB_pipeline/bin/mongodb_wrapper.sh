#!/bin/bash

###############################################################################  
##           WRAPPER TO RUN MONGODB QUERRYING ON INPUT FASTQ DATA            ##
###############################################################################


## CL Argument 1 - Specifies the folder containing fastq location 
## The Folder should have the following two files : unaligned_1.fastq and unaligned_2.fastq)

## Setup Directory Names for Use ##
original_directory=$(pwd)
input_directory=$1
script_location=$0
script_directory=$(dirname "${script_location}")
 
## Get the sample name from the input_directory 
sample_name=$(basename "${input_directory}")

## Change into the script_directory
cd $script_directory 
 
## Run kanalyze 
./count -f fastq -o $sample_name.1.out.kc unaligned_1.fastq
./count -f fastq -o $sample_name.2.out.kc unaligned_2.fastq
## Merge the two kc files
cat $sample_name.1.out.kc > $sample_name.out.kc
cat $sample_name.2.out.kc >> $sample_name.out.kc
## Remove the old kc files
rm $sample_name.1.out.kc
rm $sample_name.2.out.kc 

## Run the MongoDB query 
python create_db.py $sample_name.out.kc $sample_name 

## Move the output files to a new directory with the same name as the sample in the original directory from where the script was called
cd $original_directory 
mkdir $sample_name.outputs
mv $script_directory/*.fa $sample_name.outputs
mv $script_directory/*.json $sample_name.outputs
mv $script_directory/*.kc $sample_name.outputs
mv $script_directory/*.png $sample_name.outputs
 

