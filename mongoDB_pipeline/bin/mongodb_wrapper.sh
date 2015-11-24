#!/bin/bash

###############################################################################  
##           WRAPPER TO RUN MONGODB QUERRYING ON INPUT FASTQ DATA            ##
###############################################################################
exec &> $(date +%y%m%d).error.txt

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
cmd="cd $script_directory"
echo $cmd
eval $cmd
 
## Run kanalyze
cmd="./count -f fastq -o $sample_name.1.out.kc $original_directory/$sample_name/unaligned_1.fastq"
echo $cmd
eval $cmd
cmd="./count -f fastq -o $sample_name.2.out.kc $original_directory/$sample_name/unaligned_2.fastq"
echo $cmd
eval $cmd
## Merge the two kc files
cmd="cat $sample_name.1.out.kc > $sample_name.out.kc"
echo $cmd
eval $cmd
cmd="cat $sample_name.2.out.kc >> $sample_name.out.kc"
echo $cmd
eval $cmd
## Remove the old kc files
cmd="rm $sample_name.1.out.kc"
echo $cmd
eval $cmd
cmd="rm $sample_name.2.out.kc"
echo $cmd
eval $cmd 
## Filter the result
#awk '{if($2>7){print $0}}' $sample_name.out.kc > $sample_name.filtered.out.kc
head -50000 $sample_name.out.kc > $sample_name.filtered.out.kc
## Rename the file back to the original name
cmd="mv $sample_name.filtered.out.kc $sample_name.out.kc"
echo $cmd
eval $cmd
## Run the MongoDB query 
cmd="python create_db.py $sample_name.out.kc $sample_name"
echo $cmd
eval $cmd 

## Run the visualization script
cmd="python html_page.py $sample_name.result.json > ./MongoDB/out.html"
echo $cmd
eval $cmd

## Move the output files to a new directory with the same name as the sample in the original directory from where the script was called
cmd="cd $original_directory"
echo $cmd
eval $cmd 
cmd="mkdir $sample_name.outputs"
echo $cmd
eval $cmd
cmd="mv $script_directory/*.fa $sample_name.outputs"
echo $cmd
eval $cmd
cmd="mv $script_directory/*.json $sample_name.outputs"
echo $cmd
eval $cmd
cmd="mv $script_directory/*.kc $sample_name.outputs"
echo $cmd
eval $cmd
cmd="mv $script_directory/*.png $sample_name.outputs"
echo $cmd
eval $cmd
cmd="cp $script_directory/MongoDB -r $sample_name.outputs"
echo $cmd
eval $cmd
cmd="cp $script_directory/styles  -r $sample_name.outputs"
echo $cmd
eval $cmd

## Delete the output html page from bin
cmd="rm $script_directory/MongoDB/out.html"
echo $cmd
eval $cmd

