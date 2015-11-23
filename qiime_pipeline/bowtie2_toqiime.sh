exec &> $(date +%y%m%d).error.txt
time
library="null"
touch map.txt
touch params.txt

for i in *.fastq
do
    name=$(echo $i|cut -d "_" -f 1)
    temp=$(echo $i|cut -d "_" -f 3)    
    s=$(echo $i|cut -d "_" -f 2)
    
    if [[ $temp != $library ]]; then
      output=$name_$temp
      	
      read1=$name"_"$s"_L001_R1_001.fastq"
      read2=$name"_"$s"_L001_R2_001.fastq"
      cmd="/home/ketienne3/bin/bowtie2-2.2.6/bowtie2 -p 16 -q -t --un-conc $output  -x human_genome/genome -1 $read1 -2 $read2 -S $name.sam"
      echo $cmd
      eval $cmd
      library=$temp
    fi;
done
rm -- -x.*
rm *.sam
rm L00*

#Preparing the mapping file for qiime pipeline
echo "#SampleID BarcodeSequence LinkerPrimerSequence    SampleType      Description" > map.txt
echo "$name     AGCTGT  ILBC_17 CysticFibrosis  CysticFibrosis_MetagenomicAnalysis_of_$name" >> map.txt

#Preparing the parameters file for picking open reference otus
echo "pick_otus:enable_rev_strand_match True" > params.txt
echo "assign_taxonomy:assignment_method uclust" >> params.txt
echo "assign_taxonomy:id_to_taxonomy_fp its_12_11_otus/taxonomy/99_otu_taxonomy.txt" >> params.txt
echo "assign_taxonomy:reference_seqs_fp its_12_11_otus/rep_set/99_otus.fasta" >> params.txt

#Merging the unaligned sequences
cat *.1 >> unaligned_1.fastq
cat *.2 >> unaligned_2.fastq

#this command will take the unaligned reads from the bowtie2 alignment against the human genomes and output the fasta sequences with removed chimeric reads from the data. The maximum length of each read is set to 255bps which is optimum for picking otus by qiime. 
cmd="pandaseq -f unaligned_1.fastq -r unaligned_2.fastq -L 255 -w unaligned_pandaseq.fasta -g unaligned_pandaseq.log -L 255"
echo $cmd
eval $cmd

#Downloading the fungal ITS reference database
wget ftp://ftp.microbio.me/qiime/tutorial_files/its_12_11_otus.tgz
tar -xvf its_12_11_otus.tgz

#this command will take the preprocessed data from pandaseq output and gives out the biom table with otus picked and taxa assigned. The algorithm chooses open_reference method of picking otus and we are passing --suppress_align_and_tree because the trees generated from ITS sequences are generally not phylogenetically informative. 
cmd="pick_open_reference_otus.py -i unaligned_pandaseq.fasta -r its_12_11_otus/rep_set/99_otus.fasta -o fungal_unaligned_pick_open_otus_uclust/ -p params.txt --supress_align_and_tree"
echo $cmd
eval $cmd

#this command will take the picked otus and summarizes the taxa through plots
cmd="summarize_taxa_through_plots.py -i fungal_unaligned_pick_open_otus_uclust/otu_table_mc2_w_tax.biom -o plots_charts/ -m map.txt"
echo $cmd
eval $cmd

#Download the greengenes baterial and archeal 16S refernce database
wget ftp://greengenes.microbio.me/greengenes_release/gg_13_5/gg_13_8_otus.tar.gz
tar -xvf gg_13_8_otus.tar.gz

#Preparing parameters file for bacterial and archeal identification
echo "assign_taxonomy:assignment_method uclust" > params1.txt
echo "assign_taxonomy:id_to_taxonomy_fp gg_13_8_otus/taxonomy/97_otu_taxonomy.txt" >> params1.txt
echo "assign_taxonomy:reference_seqs_fp gg_13_8_otus/rep_set/97_otus.fasta" >> params1.txt

#this command will pick open reference otus from failed reads from fungal_otu picking step
cmd="pick_open_reference_otus.py -i fungal_unaligned_pick_open_otus_uclust/step3_otus/failures_failures.fasta -r gg_13_8_otus/rep_set/97_otus.fasta -o bac_arc_otu_picking/ -p params1.txt --supress_align_and_tree"
echo $cmd
eval $cmd

#this command will summarize the bacterial and archeal taxa through plots
cmd="summarize_taxa_through_plots.py -i bac_arc_otu_picking/otu_table_mc2_w_tax.biom -o bac_arc_otu_picking/plots_charts/ -m map.txt"
echo $cmd
eval $cmd
