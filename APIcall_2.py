from Bio import Entrez
import ensembl_rest
import sys


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = sys.argv[0]
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

organism='aedes aegypti'
geneIDs=['AAEL003439', 'AAEL011411', 'AAEL012522', 'AAEL012774', 'AAEL012864', 'AAEL013263']
ied = ",".join(geneIDs)

#print(ied[:-1])
Entrez.email=sys.argv[0]
handle = Entrez.esearch(db="pubmed",retmax=13,id=ied,term=organism)
record = Entrez.read(handle)
handle.close()
print(record['IdList'])
id_list = record['IdList']
papers = fetch_details(id_list)
print(papers)
'''for i, paper in enumerate(papers):
	print()'''
final={}
final['ids']=[]
final['seq']=[]
final['papers_id']=record['IdList']
client = ensembl_rest.EnsemblClient()
for genes in geneIDs:
    temp = client.sequence_id(genes)
    final['ids'].append(genes)
    final['seq'].append(temp['seq'])
