from Bio.KEGG import REST
import urllib.request
import re
import sys

##### TO DO #############
#### Get Organism ID from organims name #####

result = REST.kegg_list("pathway", "aga").read()
#print(result.split("\t")[0])
pathw_ids=[]
pathw=[]
for item in result.split("\t"):
	#print(item)
	#print("*")
	tmp2=item.split("\n")
	
	if len(tmp2)>1:
		if tmp2[1]!="":
			pathw.append(tmp2[0])
			pathw_ids.append(tmp2[1])
	
#print(pathw)
for pathway in pathw_ids:
#pathway = 'hsa00010' # glycolysis
	url = "http://rest.kegg.jp/get/" + pathway
	with urllib.request.urlopen(url) as f:
		lines = f.read().decode('utf-8').splitlines()
		want = 0
		for line in lines:
			fields = line.split()
        		## The list of genes starts here
			if fields[0] == 'GENE':
				want = 1
            		## The line with GENE is different
				print(fields[2].rstrip(';'))
        		## We reached the next section of the file
			elif want == 1 and re.match('^\S', line):
				sys.exit();
        		## We're still in the list of genes
			if want == 1 and len(fields)>1:
				print(fields[1].rstrip(';'))

# Get genes involved with fatty-acid biosynthesis in Kitasatospora

####Get gene ontology terms#########





result = REST.kegg_link("compound", "map00061").read()
#print(human_pathways)
# Filter all human pathways for repair pathways
####repair_pathways = []
####for line in human_pathways.rstrip().split("n"):
	#entry, description = line.split("\t")
	####print(line)
"""	if "repair" in description:
		repair_pathways.append(entry)
#print(repair_pathways)
# Get the genes for pathways and add them to a list
repair_genes = []
for pathway in repair_pathways:
	pathway_file = REST.kegg_get(pathway).read()  # query and read each pathway
	print(pathway_file)
    # iterate through each KEGG pathway file, keeping track of which section
    # of the file we're in, only read the gene in each pathway
	current_section = None
	for line in pathway_file.rstrip().split("\n"):
		section = line[:12].strip()  # section names are within 12 columns
		if not section == "":
			current_section = section
		if current_section == "GENE":
			gene_identifiers, gene_description = line[12:].split("; ")
			gene_id, gene_symbol = gene_identifiers.split()
			if not gene_symbol in repair_genes:
				repair_genes.append(gene_symbol)
                                    
print("There are %d repair pathways and %d repair genes. The genes are:" % \
      (len(repair_pathways), len(repair_genes)))
print(", ".join(repair_genes))"""
