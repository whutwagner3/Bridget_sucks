# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 11:11:02 2019

@author: bnmon
"""
import biomart
import json
import sys
import time
import pickle

def main(gene_ids, organism, save_vars=False):
    if gene_ids == '':
        # 195 genes (74 with GO terms)
        gene_ids = ['AAEL000243', 'AAEL000853', 'AAEL000964', 'AAEL001015', 'AAEL001076', 'AAEL001118', 'AAEL001199', 'AAEL001208', 'AAEL001682', 'AAEL001714', 'AAEL001821', 'AAEL002024', 'AAEL002303', 'AAEL002380', 'AAEL002641', 'AAEL003265', 'AAEL003436', 'AAEL003755', 'AAEL003982', 'AAEL004037', 'AAEL004648', 'AAEL004717', 'AAEL004991', 'AAEL005133', 'AAEL005164', 'AAEL005287', 'AAEL005399', 'AAEL005420', 'AAEL005759', 'AAEL006137', 'AAEL006335', 'AAEL006365', 'AAEL006690', 'AAEL007005', 'AAEL007110', 'AAEL007437', 'AAEL007598', 'AAEL007604', 'AAEL007719', 'AAEL007951', 'AAEL008266', 'AAEL008282', 'AAEL008360', 'AAEL008409', 'AAEL009517', 'AAEL009724', 'AAEL010140', 'AAEL010424', 'AAEL010749', 'AAEL010915', 'AAEL010987', 'AAEL011112', 'AAEL011160', 'AAEL011757', 'AAEL011777', 'AAEL011808', 'AAEL011926', 'AAEL011966', 'AAEL011987', 'AAEL012139', 'AAEL012356', 'AAEL012703', 'AAEL012713', 'AAEL012887', 'AAEL013024', 'AAEL013054', 'AAEL013216', 'AAEL013232', 'AAEL013856', 'AAEL014334', 'AAEL014579', 'AAEL015201', 'AAEL015457', 'AAEL015526', 'AAEL017095', 'AAEL017557', 'AAEL018061', 'AAEL019417', 'AAEL019494', 'AAEL019498', 'AAEL019587', 'AAEL019675', 'AAEL019676', 'AAEL019960', 'AAEL020084', 'AAEL020179', 'AAEL020315', 'AAEL020404', 'AAEL020424', 'AAEL020504', 'AAEL020630', 'AAEL020683', 'AAEL020691', 'AAEL021030', 'AAEL021152', 'AAEL021364', 'AAEL021379', 'AAEL021408', 'AAEL021504', 'AAEL021521', 'AAEL021559', 'AAEL021712', 'AAEL021769', 'AAEL021772', 'AAEL021808', 'AAEL021934', 'AAEL022018', 'AAEL022176', 'AAEL022448', 'AAEL022473', 'AAEL022536', 'AAEL022592', 'AAEL022672', 'AAEL022676', 'AAEL022688', 'AAEL022767', 'AAEL022871', 'AAEL022975', 'AAEL023049', 'AAEL023054', 'AAEL023067', 'AAEL023079', 'AAEL023139', 'AAEL023140', 'AAEL023170', 'AAEL023447', 'AAEL023573', 'AAEL023607', 'AAEL023725', 'AAEL023771', 'AAEL023775', 'AAEL023878', 'AAEL023890', 'AAEL024058', 'AAEL024096', 'AAEL024122', 'AAEL024457', 'AAEL024648', 'AAEL024680', 'AAEL024689', 'AAEL024903', 'AAEL024944', 'AAEL025159', 'AAEL025251', 'AAEL025255', 'AAEL025387', 'AAEL025442', 'AAEL025454', 'AAEL025488', 'AAEL025633', 'AAEL025707', 'AAEL025713', 'AAEL025860', 'AAEL025928', 'AAEL025932', 'AAEL025971', 'AAEL026268', 'AAEL026400', 'AAEL026451', 'AAEL026530', 'AAEL026547', 'AAEL026586', 'AAEL026611', 'AAEL026692', 'AAEL026747', 'AAEL026756', 'AAEL026766', 'AAEL026850', 'AAEL027013', 'AAEL027061', 'AAEL027139', 'AAEL027200', 'AAEL027220', 'AAEL027224', 'AAEL027235', 'AAEL027273', 'AAEL027312', 'AAEL027356', 'AAEL027505', 'AAEL027692', 'AAEL027814', 'AAEL027820', 'AAEL027849', 'AAEL027889', 'AAEL027904', 'AAEL027925', 'AAEL028054', 'AAEL028067', 'AAEL028074', 'AAEL028093', 'AAEL028094', 'AAEL028122', 'AAEL028210', 'AAEL028219', 'AAEL028242']
        
#        # 50 genes (19 with GO terms)
#        gene_ids = ['AAEL002099', 'AAEL002354', 'AAEL002972', 'AAEL004770', 'AAEL005622', 'AAEL005924', 'AAEL006122', 'AAEL008986', 'AAEL008989', 'AAEL010531', 'AAEL010623', 'AAEL011440', 'AAEL012575', 'AAEL013792', 'AAEL013853', 'AAEL014655', 'AAEL014770', 'AAEL017015', 'AAEL017397', 'AAEL017464', 'AAEL019994', 'AAEL020248', 'AAEL020397', 'AAEL020561', 'AAEL021042', 'AAEL021122', 'AAEL021127', 'AAEL021285', 'AAEL021588', 'AAEL021590', 'AAEL021685', 'AAEL021691', 'AAEL022746', 'AAEL022796', 'AAEL023785', 'AAEL024028', 'AAEL024299', 'AAEL024556', 'AAEL024875', 'AAEL025155', 'AAEL025269', 'AAEL025555', 'AAEL026233', 'AAEL026315', 'AAEL026845', 'AAEL027155', 'AAEL027432', 'AAEL027675', 'AAEL029008', 'AAEL029011']
        
#        # 11 genes (6 with GO terms) 
#        gene_ids = ['AAEL003318', 'AAEL006381', 'AAEL010338', 'AAEL010398', 'AAEL011756', 'AAEL022994', 'AAEL023879', 'AAEL026304', 'AAEL026602', 'AAEL027637', 'AAEL027839']
    else:
        gene_ids = gene_ids.split(',')
    if save_vars:
        with open('./variables/gene_ids.pkl') as f:
            pickle.dump(gene_ids, f)

    dataset = species2dataset()[organism]
    gene2go_list = get_go(gene_ids, dataset)
    if save_vars: 
        with open('./variables/gene2go.pkl') as f:
            pickle.dump(gene2go_list, f)

    distances, base2gene, genealogy = build_ontologies(gene2go_list)
    if save_vars: 
        with open('./variables/distances.pkl') as f:
            pickle.dump(distances, f)
        with open('./variables/base2gene.pkl') as f:
            pickle.dump(base2gene, f)
        with open('./variables/genealogy.pkl') as f:
            pickle.dump(genealogy, f)
    
    real_genealogy = {}
    for ont, thing in genealogy.items():
        genes = base2gene[ont]
        for gn in genes:
            real_genealogy[gn] = thing
    
    go_edges = get_edges(distances)

    real_edges = []
    pylinks = []
    for edge in go_edges:
        sources = base2gene[edge['source']]
        targets = base2gene[edge['target']]
        value = edge['value']
        for src in sources:
            for tgt in targets:
                pylinks.append((src, tgt, value))
                real_edges.append({'source': src,
                                   'target': tgt,
                                   'value': value})

    if save_vars:
        with open('./variables/real_genealogy.pkl') as f:
            pickle.dump(real_genealogy, f)
        with open('./variables/go_edges.pkl') as f:
            pickle.dump(go_edges, f)
        with open('./variables/real_edges.pkl') as f:
            pickle.dump(real_edges, f)
        with open('./variables/pylinks.pkl') as f:
            pickle.dump(pylinks, f)

    with open('./static/genealogy.json', 'w') as f:
        json.dump(real_genealogy, f)

    with open('./static/links.json', 'w') as f:
        json.dump(real_edges, f)

    return pylinks

def print_time(sec, message='', to_print=True):
    if message != '': message += ': '
    if sec > 3600: output = f'{message}{round(sec//3600,0)}h {round((sec%3600)/60,1)}m'
    else: output = f'{message}{round(sec//60,0)}m {round(sec%60,1)}s'
    if to_print: print(output)
    return output

def get_edges(distances):
    '''
    Gets a list of links for the graph from input dict
    Input: dict of base onts: list of (dist from base, parent ID)s
    Output: JSON object list with 'source', 'target', and 'value'
    '''
    links = []
    for ont1 in distances:
        for ont2 in distances:
            if ont1 == ont2: continue
            match_found = False
            for dist1, term1 in sorted(distances[ont1]):
                for dist2, term2 in sorted(distances[ont2]):
                    if term1 != term2: continue
                    match_found = True
                    links.append({'source': ont1,
                                  'target': ont2,
                                  'value': dist1 + dist2})
                    break
                if match_found: break
            if match_found: break
    return links

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

def build_ontologies(gene2go):
    '''
    Queries the GO database for all parent GO IDs
    Input: dictionary of gene ID: list of relevant GO IDs
    Returns: [dist (dict of childGO: list of (parent to child distance, parentID)),
              basegos2gene (dict of GO IDs to genes with this base GO),
              genealogy (JSON-like object for output to file)]
    '''

    # make paths (multiples included)
        # dict gene ID: [paths]

    go_db = biomart.BiomartServer('http://biomart.vectorbase.org/biomart'
                                 ).datasets['closure_GO']
    atts = ['accession_305', 'name_305', 'accession_305_r1',
            'name_305_r1', 'accession_305_r2', 'distance_301']
    
    gos_to_query = sum(gene2go.values(), [])  # flat list of all GO gene hits
    basegos2gene = {}
    for gene, go_list in gene2go.items():
        for go in go_list:
            basegos2gene[go] = basegos2gene.get(go, []) + [gene]
    
    response = go_db.search({'attributes': atts, 'filters': {'accession_305': gos_to_query}}, header=1)
    response = [x.decode('utf-8').strip() for x in response.iter_lines()]

#    # to write to file:
#    head = response[0]
#    with open('test.tsv', 'w') as f: f.write('\n'.join(response))

    parent_to_term = []
    genealogy = {}
    dist = {}
    for line in response[1:]:
        fields = line.strip("\n").strip(" ").split("\t")
        child = fields[0]
        distance = int(fields[5])
        parent = fields[2]
        term_name = fields[3]
        parent_to_term.append({'ID': parent, 'Term': term_name})
    
        if distance > 0:
            # to get distances, we just need parents and levels of all child
                # so: gene -> parent, dist
            dist[child] = dist.get(child, []) + [(distance, parent)]
            genealogy[child] = genealogy.get(child, []) + [{'Distance': distance,
                                                            'ParentID': parent,
                                                            'Term': term_name}]

    return dist, basegos2gene, genealogy

def species2dataset():
    '''
    If we want to choose an input species (by name), this gets the available
        species names and datasets. We can use this to populate a drop-down
        box with readable species names and know the dataset name to query.
    Input: none
    Returns: dict of species name: database name
    '''
    srv = biomart.BiomartServer('http://biomart.vectorbase.org/biomart')
    db = srv.databases['vb_gene_mart_1904']

    # db.datasets is dict of dataset_name: object
    # object has attribute display_name with the species full name
    return {y.display_name: x for x, y in db.datasets.items()}

def get_go(geneIDs, dataset_name):

    server=biomart.BiomartServer('http://biomart.vectorbase.org/biomart')
    inter=server.datasets[dataset_name]

    for_bridgey={}
    go_id2term = {}

    ##for_bridgey['Ensembl_GENE_ID']=[go-term1,go-term2, ...] for all genes in dataset
    resp = inter.search({'attributes':['ensembl_gene_id','go_id','name_1006'],
                        'filters': {'ensembl_gene_id': geneIDs}})
    resp = [x.decode('utf-8').strip() for x in resp.iter_lines()]

    # if we want to write to file:
    # with open('geneID_biomart_query.tsv', 'w') as f: f.write('\n'.join(resp))

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
            else:
                for_bridgey[text[0]]=[]
        elif len(text)>1:
            for_bridgey[text[0]].append(text[1])
    return for_bridgey


if __name__ == '__main__':
    lap = time.time()
    if len(sys.argv) < 3:
        main()
    else:
        main(sys.argv[1], sys.argv[2])
#    print_time(time.time() - lap, 'Completed in')
    print_time(time.time() - lap, to_print=False)


