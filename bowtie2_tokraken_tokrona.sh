exec &> $(date +%y%m%d).error.txt
time

library="null"
for i in *.fastq
do
    name=$(echo $i|cut -d "_" -f 1)
    temp=$(echo $i|cut -d "_" -f 3)    
    s=$(echo $i|cut -d "_" -f 2) 
    
    if [[ $temp != $library ]]; then
      output=$name_$temp
      	
      read1=$name"_"$s"_L001_R1_001.fastq"
      read2=$name"_"$s"_L001_R2_001.fastq"
      cmd="/home/ketienne3/bin/bowtie2-2.2.6/bowtie2 -p 16 -q -t --un-conc $output  -x /storage/AHCG/clinicalmetagenomics/2015Fall/genome -1 $read1 -2 $read2 -S $name.sam"
      echo $cmd
      eval $cmd
      library=$temp
    fi;
done

cat *.1 >> unaligned_1.fastq
cat *.2 >> unaligned_2.fastq

#this command will take the unaligned reads from the bowtie2 alignment against the human genomes and output the classified and unclassified fastq reads against minikrakendb and the classified output for krona 
cmd="/home/ketienne3/kraken/kraken --db /class/ahcg/2015/clinicalmetagenomics/2015Fall/minikraken_20141208 --paired unaligned_1.fastq unaligned_2.fastq --classified-out minikrakenclass.fastq --unclassified-out otherunclass_minikraken.fastq --output minikraken.out"
echo $cmd
eval $cmd


#this command will taken the unaligned reads from the bowtie2 alignment against the human genome and output the classified and unclassified reads against the fungal_v2_db and output the classified kraken fungal output 
cmd="/home/ketienne3/kraken/kraken --db /class/ahcg/2015/clinicalmetagenomics/2015Fall/fungi_db_v2 --paired unaligned_1.fastq unaligned_2.fastq --classified-out fungiclass_v2.fastq --unclassified-out otherunclass_fungaldb_v2.fastq --output kraken_fungal_v2.output"
echo $cmd
eval $cmd

#this command will take the classified fungal output from the command above and create a fungal kraken report
cmd="/home/ketienne3/kraken/kraken-report --db /class/ahcg/2015/clinicalmetagenomics/2015Fall/fungi_db_v2 kraken_fungal_v2.output > fungal_kraken_report_krona_v2.in"
echo $cmd
eval $cmd

#this command will cut the 2,3, and 6 column for input into krona
cmd="cut -f2,3,6 fungal_kraken_report_krona_v2.in > fungal_kraken_report_krona_v2.out"
echo $cmd
eval $cmd

#this command will cut the 2,3 and 6 column for input into krona
cmd="cut -f2,3,6 minikraken.in > minikraken_report_krona.out"
echo $cmd
eval $cmd


#this command will create a krona output
cmd="/home/ketienne3/bin/KronaTools-2.6/scripts/ImportText.pl ./fungal_kraken_report_krona_v2.out -o fungal_krona.out_v2.html"
echo $cmd
eval $cmd

#this command will create a krona output
cmd="/home/ketienne3/bin/KronaTools-2.6/scripts/ImportText.pl ./minikraken_report_krona.out -o minikraken.out.html"
echo $cmd
eval $cmd

time 

