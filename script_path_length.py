import pandas as pd
import sys
"""The below script is an implementation of floyd's algorithm
Input: A edge list with each line representing (child node tab parent node) as geberated from biomart
Output:It provides number of nodes between any two gene pairs as distance
"""
def Create_Adjacency_Matrix(fil):
    dict_interaction={}
    with open(fil,"r") as sf:
        for line in sf:
            l=line.strip("\n").split("\t")
            #print(l)
            if len(l)>1:
                l[0]=l[0].strip("\n").strip(" ")
                l[1]=l[1].strip("\n").strip(" ")
                dict_interaction[l[1],l[0]]=1

    #getting the list of proteins interacting with other proteins
    prot= dict_interaction.keys()
    lst_x=[]
    for i in prot:
        lst_x.append(i[0])
        lst_x.append(i[1])
        
    lst_xy=[]
    for i in lst_x:
        if i not in lst_xy:
            lst_xy.append(i)

    n=len(lst_xy)
    a=[] #adjacency matrix
    a=[0]*n
    for i in range(0,n):
        a[i]=[0]*n
    for i in range(0,len(lst_xy)):
        for j in range(0,len(lst_xy)):
            if i==j:
                a[i][j]=0
            elif (lst_xy[i],lst_xy[j]) in prot:
                a[i][j]=dict_interaction[lst_xy[i],lst_xy[j]]
            elif (lst_xy[j],lst_xy[i]) in prot:
                a[i][j]=dict_interaction[lst_xy[j],lst_xy[i]]
    return a,lst_xy
#Function to reconstruct the path
def reconstruct_path(u,v,next_1):
    path=[]
    if next_1[u][v]=="NA":
        return []
    path = [u]
    while u!=v:
        u=next_1[u][v]
        path.append(u)
    return path

def main_2():
    #a_mat,lst_x_y= Create_Adjacency_Matrix(input("Type the name of the file with the edge lists: "))
    ad_mat,lst_x_y= Create_Adjacency_Matrix("edge_list.txt") #sys.argv[1]
    a_mat=ad_mat
    #print(a_mat)
    for i in range(0,len(lst_x_y)):
        for j in range(0,len(lst_x_y)):
            if i!=j and a_mat[i][j]!=1:
                a_mat[i][j]=10000
                
    next_1=['NA']*len(lst_x_y)
    for j in range(0,len(lst_x_y)):
        next_1[j]=['NA']*(len(lst_x_y))
 
    for i in range(0,len(lst_x_y)):
        for j in range(0,len(lst_x_y)):
            if a_mat[i][j]!=1000 and a_mat[i][j]!=0:
                next_1[i][j]=j
            
    for k in range(0,len(lst_x_y)):
        for i in range(0,len(lst_x_y)):
            for j in range(0,len(lst_x_y)):
                if a_mat[i][j] > ((a_mat[i][k]) + (a_mat[k][j])):
                    a_mat[i][j]= a_mat[i][k] + a_mat[k][j]
                    next_1[i][j]=next_1[i][k]

    dict_pair={}
    for item1 in lst_x_y:
        for item2 in lst_x_y:
            if not item1.startswith("GO:") and not item2.startswith("GO:"):
                if item1==item2:
                    dict_pair[(item1,item2)]=0
                elif (item1,item2) not in dict_pair:
                    u=lst_x_y.index(item1)
                    v=lst_x_y.index(item2)
                    lst_path=reconstruct_path(u,v,next_1)
                    lst_path.remove(u)
                    lst_path.remove(v)
                    tmp=len(lst_path)
                    dict_pair[(item1,item2)]=tmp
                    dict_pair[(item2,item1)]=tmp
    lst_mat=[]
    for i in lst_x_y:
        if not i.startswith("GO:"):
            lst_mat.append(i)
    df=pd.DataFrame(0,columns= lst_mat, index= lst_mat)
    for val in dict_pair:
        df.loc[val[0],val[1]]=dict_pair[val]
        df.loc[val[1],val[0]]=dict_pair[val]
    df.to_csv("distance_matrix.csv")
    
if __name__=="__main__":
    main_2()


