#!/usr/bin/env python3

##pip install biomart or conda install -c bioconda bioconductor-biomart
import biomart
import sys
# %%
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
# %%
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


    for_bridgey={}
    go_id2term = {}
    ##for_bridgey['Ensembl_GENE_ID']=[go-term1,go-term2, ...] for all genes in dataset
    resp = inter.search({'attributes':['ensembl_gene_id','go_id','name_1006'],
                        'filters': {'ensembl_gene_id': geneIDs}})
    resp = [x.decode('utf-8').strip() for x in resp.iter_lines()]
    # if we want to write to file:
    # open('geneID_biomart_query.tsv', 'w').write('\n'.join(resp))

    for line in resp:
        # line=line.decode('utf-8')
        text=line.strip().split('\t')

        # add GO ids and terms to dictionary mapping IDs to terms for later
        if len(text) > 1: 
            if text[1] in go_id2term and go_id2term[text[1]] != text[2]:
                print('what fresh torture have I discovered?')
                print(f'{text[1]}: {text[2]} or {go_id2term[text[1]]}?')
                sys.exit()
            else: go_id2term[text[1]] = text[2]

        # add gene ID: go ID to for_bridgey
        if text[0] not in for_bridgey:
            if len(text)>1:
                for_bridgey[text[0]]=[text[1]]
            else:   ### maybe we should ignore these???
                for_bridgey[text[0]]=[]
        elif len(text)>1:
            for_bridgey[text[0]].append(text[1])
    return for_bridgey

if __name__ == '__main__':
#    egen_ids = ['AGAP000322', 'AGAP000433', 'AGAP000812', 'AGAP001133', 'AGAP001435', 'AGAP001953', 'AGAP002036', 'AGAP002109', 'AGAP002120', 'AGAP002288', 'AGAP002550', 'AGAP002644', 'AGAP003192', 'AGAP003207', 'AGAP003208', 'AGAP003844', 'AGAP003925', 'AGAP004092', 'AGAP004353', 'AGAP004494', 'AGAP005113', 'AGAP005160', 'AGAP005435', 'AGAP005845', 'AGAP005981', 'AGAP006243', 'AGAP006474', 'AGAP006715', 'AGAP007377', 'AGAP007532', 'AGAP008046', 'AGAP008137', 'AGAP008646', 'AGAP008705', 'AGAP009181', 'AGAP009510', 'AGAP011570', 'AGAP012008', 'AGAP012020', 'AGAP012097', 'AGAP012118', 'AGAP012186', 'AGAP012258', 'AGAP012606', 'AGAP012632', 'AGAP029337', 'AGAP029474', 'AGAP029655']
#    egen_ids = ['AGAP001296', 'AGAP001330', 'AGAP001481', 'AGAP001681', 'AGAP001905', 'AGAP002280', 'AGAP002344', 'AGAP002513', 'AGAP002567', 'AGAP003018', 'AGAP003023', 'AGAP003090', 'AGAP003114', 'AGAP004215', 'AGAP004288', 'AGAP004989', 'AGAP005088', 'AGAP005362', 'AGAP005545', 'AGAP005796', 'AGAP005897', 'AGAP006606', 'AGAP006994', 'AGAP007585', 'AGAP008134', 'AGAP008185', 'AGAP008708', 'AGAP008942', 'AGAP009631', 'AGAP009765', 'AGAP009780', 'AGAP009809', 'AGAP009864', 'AGAP010413', 'AGAP010673', 'AGAP011234', 'AGAP011351', 'AGAP011888', 'AGAP012090', 'AGAP012194', 'AGAP012932', 'AGAP013375', 'AGAP028466', 'AGAP029190', 'AGAP029390', 'AGAP029760']
    egen_ids = ['AAEL000063', 'AAEL000518', 'AAEL002432', 'AAEL002439', 'AAEL002623', 'AAEL002627', 'AAEL002630', 'AAEL003239', 'AAEL003297', 'AAEL004009', 'AAEL004505', 'AAEL004665', 'AAEL005548', 'AAEL005611', 'AAEL008202', 'AAEL008749', 'AAEL010263', 'AAEL010266', 'AAEL010439', 'AAEL010959', 'AAEL011528', 'AAEL011937', 'AAEL012636', 'AAEL013961', 'AAEL017524', 'AAEL017539', 'AAEL019981', 'AAEL020153', 'AAEL020833', 'AAEL021072', 'AAEL021074', 'AAEL022267', 'AAEL022408', 'AAEL022647', 'AAEL023119', 'AAEL023426', 'AAEL024926', 'AAEL025681', 'AAEL026011', 'AAEL026627', 'AAEL027304']

    id2go = get_go(egen_ids)
