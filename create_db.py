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

## Create a connection
client = MongoClient()
## Switch to the database 
fungal_db = client.Fungal_DB_v3

## Populate the database
#insert_data(fungal_db)

## Keep Unique K-mers only in the database
#fungal_db.taxa.ensure_index([("kmer", pymongo.ASCENDING)])


## List to store the species which have kmer hits in the database
result = []

RHIZ_STOL_HANDLE  = open(sys.argv[1]+'_Rhizopus_stolonifer_kmers.fa','w')
PARA_BRAS_HANDLE = open(sys.argv[1]+'Paracoccidioides_brasiliensis_kmers.fa','w')
RHIZ_ORYZ_HANDLE = open(sys.argv[1]+'Rhizopus_oryzae_kmers.fa','w')
RHIZ_IRRE_HANDLE = open(sys.argv[1]+'Rhizophagus_irregularis_kmers.fa','w')
HIST_CAPS_HANDLE = open(sys.argv[1]+'Histoplasma_capsulatum_kmers.fa','w')
MYCE_THER_HANDLE = open(sys.argv[1]+'Myceliophthora_thermophila_kmers.fa','w')

## kmer counters for the fasta file headers
rhiz_stol_counter = 1
para_bras_counter = 1
rhiz_oryz_counter = 1
rhiz_irre_counter = 1 
hist_caps_counter = 1 
myce_ther_counter = 1 

with open(sys.argv[1],'r') as INPUT_HANDLE:  ## First argument is the name of the kc file
    for line in INPUT_HANDLE:
        line = line.rstrip('\n')
        kmer_query = line.split('\t')[0]
        count = line.split('\t')[1]
        q = fungal_db.taxa.find({"kmer" : kmer_query})

        if(q.count()>0):  ## The query has a hit in the database
            for doc in q: ## Iterate over the cursor
                i = 0
                if(doc['Species'] == 'Rhizopus_stolonifer'):
                    RHIZ_STOL_HANDLE.write(">kmer"+str(rhiz_stol_counter)+"\n")
                    RHIZ_STOL_HANDLE.write(doc["kmer"]+"\n")
                    rhiz_stol_counter = rhiz_stol_counter + 1 

                elif(doc['Species'] == 'Paracoccidioides_brasiliensis'):
                    PARA_BRAS_HANDLE.write(">kmer"+str(para_bras_counter)+"\n")
                    PARA_BRAS_HANDLE.write(doc["kmer"]+"\n")
                    para_bras_counter = para_bras_counter + 1

                elif(doc['Species'] == 'Rhizopus_oryzae'):
                    RHIZ_ORYZ_HANDLE.write(">kmer"+str(rhiz_oryz_counter)+"\n")
                    RHIZ_ORYZ_HANDLE.write(doc["kmer"]+"\n")
                    rhiz_oryz_counter = rhiz_oryz_counter + 1

                elif(doc['Species'] == 'Rhizophagus_irregularis'):
                    RHIZ_IRRE_HANDLE.write(">kmer"+str(rhiz_irre_counter)+"\n")
                    RHIZ_IRRE_HANDLE.write(doc["kmer"]+"\n")
                    rhiz_irre_counter = rhiz_irre_counter + 1

                elif(doc['Species'] == 'Histoplasma_capsulatum'):
                    HIST_CAPS_HANDLE.write(">kmer"+str(hist_caps_counter)+"\n")
                    HIST_CAPS_HANDLE.write(doc["kmer"]+"\n")
                    hist_caps_counter = hist_caps_counter + 1

                elif(doc['Species'] == 'Myceliophthora_thermophila'):
                    MYCE_THER_HANDLE.write(">kmer"+str(myce_ther_counter)+"\n")
                    MYCE_THER_HANDLE.write(doc["kmer"]+"\n")
                    myce_ther_counter = myce_ther_counter + 1

                while(i<len(count)): ## take into account the kmer counts 
                    result.append(doc['Species'])
                    i+=1

        else: ## No hit in the database
            i = 0
            while(i<len(count)):  ## take into account the kmer counts
                result.append("None")
                i+=1

RHIZO_STOL_HANDLE.close()
PARA_BRAS_HANDLE.close()
RHIZ_ORYZ_HANDLE.close()
RHIZ_IRRE_HANDLE.close()
HIST_CAPS_HANDLE.close() 
MYCE_THERM_HANDLE.close()

## Create a counter dictionary from the result array 
c = Counter(result)

#### OUTPUT A JSON FILE ####
with open(sys.argv[1]+'_result.json','w') as  JSON_HANDLE:
    json.dump(c,JSON_HANDLE)

#sorted_c = sorted(c.items(),key=operator.itemgetter(1))
sorted_c = c.most_common()

    
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
fig.savefig(sys.argv[1].split('.')[0]+".png")



