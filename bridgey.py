#!/usr/bin/env python3

##pip install biomart or conda install -c bioconda bioconductor-biomart
import biomart

#biomart.list_marts()#This is useless
server=biomart.BiomartServer('http://biomart.vectorbase.org/biomart')#Erased_Unreasonably_Harsh_Comment
#server.show_databases()
#pleaseGodWork = biomart.BiomartDatabase('http://biomart.vectorbase.org/biomart',virtual_schema='vb_mart+1902',name='vb_gene_mart_1902')
#******THESE DATASET NAMES NEED TO BE GIVEN******
#print(pleaseGodWork.show_datasets())
#******THESE DATASET NAMES NEED TO BE GIVEN******
inter=server.datasets['alvpagwg_eg_gene']


FOR_BRIDGEY={}
##FOR_BRIDGEY['Ensembl_GENE_ID']=[go-term1,go-term2, ...] for all genes in dataset
#a lot are empty. But I didn't check our actual genes were using as examples
resp = inter.search({'attributes':['ensembl_gene_id','name_1006']})
for line in resp.iter_lines():
    line=line.decode('utf-8')
    text=line.strip().split(None,1)
    if text[0] not in FOR_BRIDGEY:
        if len(text)>1:
            FOR_BRIDGEY[text[0]]=[text[1]]
        else:
            FOR_BRIDGEY[text[0]]=[]
    elif len(text)>1:
        FOR_BRIDGEY[text[0]].append(text[1])
