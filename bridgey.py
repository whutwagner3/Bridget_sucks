#!/usr/bin/env python3

##pip install biomart or conda install -c bioconda bioconductor-biomart
import biomart
import sys

def species2dataset():
    '''
    If we want to choose an input species (by name), this gets the available
        species names and datasets. We can use this to populate a drop-down
        box with readable species names and know the dataset name to query.
    Input: none
    Returns: dict of species name: database name
    '''
    srv = biomart.BiomartServer('http://biomart.vectorbase.org/biomart')
    db = srv.databases['vb_gene_mart_1902']
    
    # db.datasets is dict of dataset_name: object
    # object has attribute display_name with the species full name
    return {y.display_name: x for x, y in db.datasets.items()}

def get_go(geneIDs):
    #biomart.list_marts()#This is useless
    server=biomart.BiomartServer('http://biomart.vectorbase.org/biomart')#Erased_Unreasonably_Harsh_Comment
    #server.show_databases()
    #pleaseGodWork = biomart.BiomartDatabase('http://biomart.vectorbase.org/biomart',virtual_schema='vb_mart+1902',name='vb_gene_mart_1902')
    #******THESE DATASET NAMES NEED TO BE GIVEN******
    #print(pleaseGodWork.show_datasets())
    #******THESE DATASET NAMES NEED TO BE GIVEN******
    # dataset_name = species2dataset()['Aedes aegypti (LVP_AGWG) genes (AaegL5.1)'] # for example
    dataset_name = 'alvpagwg_eg_gene'
    inter=server.datasets[dataset_name]


    FOR_BRIDGEY={}
    ##FOR_BRIDGEY['Ensembl_GENE_ID']=[go-term1,go-term2, ...] for all genes in dataset
    resp = inter.search({'attributes':['ensembl_gene_id','go_id','name_1006'],
                        'filters': {'ensembl_gene_id': geneIDs}})
    resp = [x.decode('utf-8').strip() for x in resp.iter_lines()]
    # if we want to write to file:
    # open('geneID_biomart_query.tsv', 'w').write('\n'.join(resp))

    for line in resp:
        # line=line.decode('utf-8')
        text=line.strip().split('\t')

        # add gene ID: go ID to FOR_BRIDGEY
        if text[0] not in FOR_BRIDGEY:
            if len(text)>1:
                FOR_BRIDGEY[text[0]]=[text[1]]
            else:   ### maybe we should ignore these???
                FOR_BRIDGEY[text[0]]=[]
        elif len(text)>1:
            FOR_BRIDGEY[text[0]].append(text[1])
    return [FOR_BRIDGEY, go_id2term]

if __name__ == '__main__':
    id2go, goid2goterm = get_go(['AAEL003439', 'AAEL011411', 'AAEL012522', 'AAEL012774', 'AAEL012864', 'AAEL013263'])
