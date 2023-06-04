from tqdm import tqdm                          # plotting
import numpy as np                                          # linear algebra
import numpy as np                                          # linear algebra
from multiprocessing import Pool
from functools import partial
from configparser import ConfigParser

from tqdm import tqdm

from scipy.spatial.distance import cdist
from gudhi import WitnessComplex, RipsComplex

############ library for models ###############
from torch.utils.data import Dataset, DataLoader

def get_feat(cp,
            vr_simplexes:bool,
            max_dimension:int):
    
    inf = 0.6
    if vr_simplexes:
        distance = cdist(cp,cp)
        complexes = RipsComplex(distance_matrix = distance, max_edge_length = 0.6)
        simplex_tree = complexes.create_simplex_tree(max_dimension = max_dimension)
        
    else:
        land_ind = np.random.choice(range(len(cp)), len(cp)//3, replace = False)
        landmark = cp[land_ind]

        distance = cdist(cp,landmark)
        nearest_landmark_table = [[] for i in range(len(cp))]
        m = 0.0
        for w in range(len(cp)):
            ind_sort = np.argsort(distance[w])
            m = max(m,distance[w,max_dimension+1])
            nearest_landmark_table[w] = [(ind_sort[i], distance[w,ind_sort[i]]**2) for i in range(max_dimension+1)]
    
        complexes = WitnessComplex(nearest_landmark_table = nearest_landmark_table)
        simplex_tree = complexes.create_simplex_tree(max_alpha_square = 0.5,
                                                     limit_dimension = max_dimension)
        
        inf = m
        
    simplex_tree.compute_persistence()
    simplexes = simplex_tree.persistence()
    bn = simplex_tree.betti_numbers()
    simplexes = np.stack([(*b,a) if b[1] != np.inf else (b[0],inf, a) for a,b in simplexes ])

        
    
    holes = {i: len(simplexes[simplexes[:,2] == i]) for i in range(max_dimension)}
    avg = {}
    sum_lt = {}
    max_lt = {}
    
    for i in range(max_dimension):
        if holes[i]== 0:
            avg[i] = 0
            sum_lt[i] = 0
            max_lt[i] = 0
        else:
            life = simplexes[simplexes[:, 2]== i][:,1] - simplexes[simplexes[:, 2]== i][:,0]
            avg[i] = np.mean(life)
            sum_lt[i] = np.sum(life)
            max_lt[i] = np.max(life)


    tmp = np.concatenate((list(holes.values()), 
                          list(avg.values()), 
                          list(sum_lt.values()), 
                          list(max_lt.values()), 
                          list(bn)), -1)
    
    return np.array(tmp)


class MyDataset(Dataset):
    def __init__(self, 
                 cp: dict, 
                 label: dict,
                 config: ConfigParser):
        
        vr_simplex = config.getboolean('homology', 'vietoris_rips')
        max_dimension = config.getint('homology', 'max_dimension')
        step = config.getint('multiprocessing', 'multi_processes')
        self.dataset = []
        self.label = list(label.values())
        
        cps = []
        print("the number of process at the same time is ", step)
        
        np.random.seed(1234)
        
        with tqdm(total=len(cp)) as progress_bar: 
            for idx in range(0, len(cp), step):
                cps = [cp[j] for j in range(idx, min(idx+step, len(cp)))]
                with Pool(processes=step) as pool:
                    async_result = pool.map(partial(get_feat,
                                                    vr_simplexes = vr_simplex,
                                                    max_dimension = max_dimension), cps)
                    self.dataset.extend(async_result)
                progress_bar.update(step)
                
    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idxs):
        return self.dataset[idxs], self.label[idxs]