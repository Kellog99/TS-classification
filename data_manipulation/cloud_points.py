import pandas as pd                                         # data processing, CSV file I/O (e.g. pd.read_csv)
import pickle                                               # saving and loading compress files
import os
from configparser import ConfigParser
import tqdm
from gtda.time_series import SingleTakensEmbedding

def get_cloud_point(config: ConfigParser,
                    key: str, 
                    ds):

    embedder_periodic = SingleTakensEmbedding(
        parameters_type = "fixed",
        n_jobs = os.cpu_count(),
        time_delay = config.getint('homology', 'step'),
        dimension = config.getint('homology', 'embedding'),
        stride = config.getint('homology', 'stride'),
    )

    dataset_cloud_points = {}
    label = {}
    for j in tqdm(range(len(ds)), desc = f" cloud point for {key} "):
        dataset_cloud_points[j] = embedder_periodic.fit_transform(ds.values[j,:-1])
        label[j] = ds.values[j][-1]

    with open(os.path.join(config['paths']['dataset'], f"cloud_points_{key}.pkl"), "wb") as f:
        pickle.dump(dataset_cloud_points, f)

    with open(os.path.join(config['paths']['dataset'], f"target_label_{key}.pkl"), "wb") as f:
        pickle.dump(label, f)

    return dataset_cloud_points, label