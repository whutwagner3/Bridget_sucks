# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 08:57:41 2019

@author: bnmon
"""
from WebServer import gene_clumper
import pandas as pd

links = gene_clumper.main(save_json=False, save_vars=True)
# %% edge weight distribution

distance_distribution = {}
for link in links:
    distance_distribution[link[2]] = distance_distribution.get(link[2], 0) + 1

# ideas
    # scale edge weights - log?
    # 

nodes = list(set(sum([[x[0], x[1]] for x in links], [])))



dist_m = pd.DataFrame(index=nodes, columns=nodes)
for thing, thingy, blop in links:
    dist_m.loc[thing, thingy] = blop
    dist_m.loc[thingy, thing] = blop
