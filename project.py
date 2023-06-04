from configparser import ConfigParser
from tqdm import tqdm
import matplotlib.pyplot as plt                             # plotting
import numpy as np                                          # linear algebra
import os                                                   # accessing directory structure
import sys
from multiprocessing import Pool
from functools import partial

import pandas as pd                                         # data processing, CSV file I/O (e.g. pd.read_csv)
import argparse
from configparser import ConfigParser
import pickle                                               # saving and loading compress files

############ library for GTDA #################
import gudhi as gd
from gudhi import RipsComplex

############ library for models ###############
from torch.utils.data import DataLoader
from data_manipulation import MyDataset
from model import classifier


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Base model")
    parser.add_argument("-c", "--config", type=str, required = True, help="Config file")

    ####### loading the configuration file #####
    args = parser.parse_args()
    config_path = args.config
    config = ConfigParser()
    config.read(config_path)

    dataset = {}
    for key in ['train','validation', 'test']:
        dataset[key] = pd.read_csv(os.path.join(config['paths']['dataset'],f"dataset_{key}.csv"), header=None)
        nRow, nCol = dataset[key].shape
        print(f'There are {nRow} rows and {nCol} columns for the {key} dataset')
    
    m = 3
    step = 50

    if os.path.exists(os.path.join(config['paths']['dataset'], "cloud_points.pkl")):
        with open(os.path.join(config['paths']['dataset'], "cloud_points.pkl"), "rb") as f:
            cp = pickle.load(f)
        with open(os.path.join(config['paths']['dataset'], "target_label.pkl"), "rb") as f:
            target_label = pickle.load(f)    
    else:
        dataset_cloud_points ={}
        label = {}
        for key in dataset.keys():
            dataset_cloud_points[key] = {}
            label[key] = {}
            for j in tqdm(range(len(dataset[key]))):
                cp = []
                for i in range(step):
                    tmp = dataset[key].values[j][:-1]
                    cp.append(tmp[i::step][:m])
                dataset_cloud_points[key][j]=np.stack(cp)
                label[key][j] = dataset[key].values[j][-1]

        with open(os.path.join(config['paths']['dataset'], "cloud_points.pkl"), "wb") as f:
            pickle.dump(dataset_cloud_points, f)
        with open(os.path.join(config['paths']['dataset'], "target_label.pkl"), "wb") as f:
            pickle.dump(label, f)
        cp = dataset_cloud_points
        target_label = label

    max_dimension = config.getint('homology','max_dimension')
    max_diameter = config.getfloat('homology','max_diameter')

    batch_size = config.getint('dataset','batch_size')
    mydatasets = {}
    dl = {}
    for key in cp.keys():
        if os.path.exists(os.path.join(config['paths']['dataset'], f"features_{key}.pkl")):
            with open(os.path.join(config['paths']['dataset'], f"features_{key}.pkl"),"rb") as f:
                mydatasets[key] = pickle.load(f)
        else:
            print(f"extracting the features for the {key}")
            tmp = MyDataset(cp = cp['train'], 
                        label = target_label['train'], 
                        max_dimension = max_dimension, 
                        max_diameter = max_diameter)
            mydatasets[key] = tmp
            with open(os.path.join(config['paths']['dataset'], f"features_{key}.pkl"),"wb") as f:
                pickle.dump(tmp, f)
        
        dl[key] = DataLoader(mydatasets[key], 
                            shuffle = True, 
                            batch_size = batch_size)
    
    batch = next(iter(dl['train']))
    batch[0]
    model = classifier(nfeat_in = batch[0].shape[1], 
                   nclass = 5)
    model(batch[0])
    #model(torch.randn(15))