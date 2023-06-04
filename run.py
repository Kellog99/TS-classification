import os
import argparse
import pickle

from configparser import ConfigParser

from data_manipulation.dataset import MyDataset
#from data_manipulation.cloud_points import get_cloud_point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Base model")
    parser.add_argument("-c", "--config", type=str, required = True, help = "Config file")
    parser.add_argument("-d", "--dataset", type=str, required = True, help = "Which dataset it is needed to create")

    parser.add_argument("-md", "--max_dimension", type=str, help = "max_dimension to search")
    parser.add_argument("-vr", "--vietoris_rips", action = 'store_true', help = "tells which dataset it is in creation")
    parser.add_argument("-mp", "--multi_processes", type=str, help = "max_diamter to consider")

    ####### loading the configuration file #####
    args = parser.parse_args()
    config_path = args.config
    config = ConfigParser()
    config.read(config_path)

    
    key = args.dataset
    if key not in ['train','validation', 'test']:
        print(" The dataset cannot be created")
    else:
        ####### creating the cloud point #####
        with open(os.path.join(config['paths']['dataset'], f"cloud_points_{key}.pkl"), "rb") as f:
            cp = pickle.load(f)
            
        with open(os.path.join(config['paths']['dataset'], f"target_label_{key}.pkl"), "rb") as f:
            target_label = pickle.load(f)

        for arg in ["vietoris_rips", "max_dimension", "multi_processes"]:
            tmp = getattr(args, arg)
            print(arg)
            print(tmp)
            if tmp != None:
                if arg == "multi_processes":
                    if int(tmp)==-1:
                        config['multiprocessing'][arg] = f"{os.cpu_count()}"
                    else:
                        config['multiprocessing'][arg] = f"{tmp}"
                else:
                    config['homology'][arg] = f"{tmp}"


            batch_size = config.getint('dataset','batch_size')
        

        if ~os.path.exists(os.path.join(config['paths']['dataset'], f"features_VR_{key}.pkl")):
            vr =  "VR" if config.getboolean('homology', 'vietoris_rips') else "WD"
            print(f" creating the dataset for {args.dataset} with {vr}")
            tmp = MyDataset(cp = cp,
                            label = target_label, 
                            config = config)
            name = f"features_VR_{key}.pkl" if config.getboolean('homology', 'vietoris_rips') else f"features_WD_{key}.pkl"
            with open(os.path.join(config['paths']['dataset'], name),"wb") as f:
                pickle.dump(tmp, f)
