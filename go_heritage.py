# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 13:01:22 2019

@author: bnmon
"""
# %%
import biomart
import sys

# %% setup
def main():
    '''
    This is added just for demonstration purposes. The build_ontologies() function works by itself,
    and it can be called from other scripts. Here is an example:
    '''
    resp = [x.decode('utf-8').strip().split('\t') for x in biomart.BiomartServer(
            'http://biomart.vectorbase.org/biomart').datasets['alvpagwg_eg_gene'
            ].search({'attributes':['ensembl_gene_id', 'go_id', 'name_1006'],
                      'filters': {'ensembl_gene_id': ['AAEL003439', 'AAEL011411', 'AAEL012522',
                                   'AAEL012774', 'AAEL012864', 'AAEL013263']}}).iter_lines()]
    gene2go = {x[0]: [y[1] for y in resp if len(y) > 1 and y[0] == x[0]] for x in resp}
    
    edge_list, goid2goterm = build_ontologies(gene2go)
    return [edge_list, goid2goterm]       # in case you want to look at the variables in Spyder

# %%
def add_entry(key, value, dic):
    '''
    Checks for duplicate keys with different values. Just in case...
    Input: the key and value to add and dictionary
    Returns: nothing
    '''
    if key in dic:
        if dic[key] != value:
            print('Nooooo')
            print(f'{key}: {value} or {dic[key]}?')
            sys.exit()
    else:
        dic[key] = value

# %%
def build_ontologies(gene2go):
    '''
    Queries the GO database for all parent GO IDs
    Input: dictionary of gene ID: list of relevant GO IDs
    Returns: [edge_list (list of tuples: (child GO ID, parent GO ID)),
              goid2goterm (dict of GO IDs to GO terms)]
    '''

    # make paths (multiples included)
        # dict gene ID: [paths]

    go_db = biomart.BiomartServer('http://biomart.vectorbase.org/biomart'
                                 ).datasets['closure_GO']
    atts = ['accession_305', 'name_305', 'accession_305_r1',
            'name_305_r1', 'accession_305_r2', 'distance_301']
    gos_to_query = sum(gene2go.values(), [])  # flat list of all GO gene hits
    
    response = go_db.search({'attributes': atts, 'filters': {'accession_305': gos_to_query}}, header=1)
    response = [x.decode('utf-8').strip() for x in response.iter_lines()]

#    # to write to file:
#    head = response[0]
#    open('test.tsv', 'w').write('\n'.join(response))

####### MANI EDIT BELOW #########
    edge_list = []
    for gene, goIDs in gene2go.items():
        for go_id in goIDs:
            edge_list.append((gene, go_id))
    goid2goterm = {}
    for line in [x.split('\t') for x in response[1:]]:
        add_entry(line[0], line[1], goid2goterm)
        add_entry(line[2], line[3], goid2goterm)
        if line[-1] == '0': continue
        edge_list.append((line[4], line[2]))
    return [edge_list, goid2goterm]

# %%
if __name__ == '__main__':
    edges, go_id2term = main()