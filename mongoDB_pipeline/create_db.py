import pymongo
from pymongo import MongoClient
import glob
import re
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import sys
import json

def insert_data(fungal_db):
    """ Inserts k-mer information into database
    """
            
    species_matcher = re.compile('.*\/(.*)_whole\.fa\.kc\.filtered')
    
    for file in glob.glob('./filtered_kc/*'):
        match = re.match(species_matcher,file)
        species = match.group(1)
        print (species)
        TEMP_HANDLE = open(file,'r')
        for line in TEMP_HANDLE:
            line = line.rstrip('\n')
            kmer = line.split('\t')[0]
            count = line.split('\t')[1]
            data = {"kmer":kmer,"Species":species,"Count":count}
            fungal_db.taxa.insert_one(data)

    ## Keep Unique K-mers only in the database
    #fungal_db.taxa.ensure_index([("kmer", pymongo.ASCENDING)])

def run_query(fungal_db,flag=0,FASTA_HANDLE={},fasta_seq_counter={}):
    """ Run the query
    fungal_db => mongodb connection object
    flag => to specify if fastas need to be created (by default is 0)
    FASTA_HANDLE => a dict to store the file handles for the fastas, is an empty dict by default
    fasta_seq_counter => a dict to store fasta sequence numbers
    returns an array containing the names of the species found (taking counts into account)
    """
    ## List to store the species which have kmer hits in the database
    result = []

    with open(sys.argv[1],'r') as INPUT_HANDLE:  ## First argument is the name of the kc file
        for line in INPUT_HANDLE:
            line = line.rstrip('\n')
            kmer_query = line.split('\t')[0]
            count = line.split('\t')[1]
            q = fungal_db.taxa.find({"kmer" : kmer_query})
            
            if(q.count()>0):  ## The query has a hit in the database
                for doc in q: ## Iterate over the cursor
                    i = 0
                    if(flag == 1): ## Fastas are to be created
                        if doc['Species'] in FASTA_HANDLE.keys():
                            species_key = doc['Species']
                            seq_num = fasta_seq_counter[species_key]
                            FASTA_HANDLE[species_key].write(">kmer"+str(seq_num)+"\n")
                            FASTA_HANDLE[species_key].write(doc['kmer']+"\n")
                            fasta_seq_counter[species_key] = fasta_seq_counter[species_key]+1
                    while(i<len(count)): ## take into account the kmer counts 
                        result.append(doc['Species'])
                        i+=1
            else: ## No hit in the database
                i = 0
                while(i<len(count)):  ## take into account the kmer counts
                    result.append("None")
                    i+=1
    if(flag == 0):
        return result

def create_fastas(fungal_db,result,sample_name):
    """ Creates Fastas for the top 10 fungal species
    """

    c = return_result_hash(result)
    FASTA_HANDLE = {}
    fasta_seq_counter = {}

    for i in range(0,10):
        species = c[i+1][0]
        FASTA_HANDLE[species] = open(sample_name+"_"+species+"_kmers.fa",'w')
        fasta_seq_counter[species] = 1

    ## Call the query function with flag = 1 and FASTA_HANDLE as input
    run_query(fungal_db,1,FASTA_HANDLE,fasta_seq_counter)

    ## Close the file handles
    for key in FASTA_HANDLE.keys():
        FASTA_HANDLE[key].close()

def output_json(result,sample_name):
    """ Create a json output of the result
    """
    c = return_result_hash(result)
    with open(sample_name+'_result.json','w') as  JSON_HANDLE:
        json.dump(c,JSON_HANDLE)

def return_result_hash(result):
    """ Result is an array of species names
    """
    ## Create a counter dictionary from the result array 
    c = Counter(result)

    #sorted_c = sorted(c.items(),key=operator.itemgetter(1))
    sorted_c = c.most_common()
    
    return sorted_c

def plot_result(result,sample_name):
    """ Plots a bar graph of the result
    """

    sorted_c = return_result_hash(result)
    #### SIMPLE PLOTTING ####
    temp = []
    labels = []
    width = 1

    for i in range(0,len(sorted_c)):    
        temp.append(sorted_c[i][1])
        labels.append(sorted_c[i][0])

        indexes = np.arange(len(temp[1:10]))
        plt.bar(indexes,temp[1:10],0.2)
        plt.xticks(indexes+width*0.1,labels[1:10],rotation=20,fontsize=9)
        fig = plt.gcf()
        fig.set_size_inches(18.5,10.5)
        fig.savefig(sample_name+".png")


def main():
    ## Get the name of the sample
    if(sys.argv[1][-1] == "/"):
        sample_name = sys.argv[1].split("/")[-2]
    else:
        sample_name = sys.argv[1].split("/")[-1]


    ## Create a connection
    client = MongoClient()
    ## Switch to the database 
    fungal_db = client.Fungal_DB_v3

    ## Create the database
    #insert_data(fungal_db)

    ## Query the database
    result = run_query(fungal_db)

    ## Create the fastas
    
    ## Output the json
    output_json(result,sample_name)

    ## Output the plot
    plot_result(result,sample_name)

    ## Create fastas for the top results (query would need to be run again)
    create_fastas(fungal_db,result,sample_name)

if __name__ == "__main__":
    main()

