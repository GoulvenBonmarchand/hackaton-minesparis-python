import numpy as np

def barycentre(L):
    Tab = []
    for elt in L:
        Tab.append(np.array(elt))
    Tableau = np.array(Tab)
    return Tableau.sum()/len(Tab)