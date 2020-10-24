import os
from ftplib import FTP

import pandas as pd
import numpy as np
from tqdm import tqdm

from keras.utils.data_utils import get_file

from .nchs import _data_files,DEFAULT_COLS,PUB_DIR,_remote_ls

NACMS_DIR = '/'.join([PUB_DIR,'dataset_documentation','namcs'])

PRACTICE_COLS = ['SPEC','SPECR','SPECCAT']
DISPOSITION = ['ADMITHOS','REFERED','REFOTHMD','NOFU','RETPRN','RETAPPT','TELEPHON']


DEFAULT_CACHE_DIR = os.path.join(os.path.expanduser('~'), 'data')

def _remote_spss():
    spss_data_dir = '/'.join([NACMS_DIR,'spss'])
    files = _remote_ls(path=spss_data_dir)
    dat_files = [f for f in files if f.endswith('spss.zip') and 'chc' not in f]
    return dat_files

def _cache_spss(files=None,dataset='namcs'):
    base = 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/dataset_documentation/{}/spss/'.format(dataset)

    for fname in files:
        path = get_file(fname.lower(),
                        origin = base + fname,
                        cache_dir = DEFAULT_CACHE_DIR,
                        extract=True,
                        cache_subdir = dataset)
        yield path

def _remote_sel(dataset=None,**kwargs):
    FILES = _remote_spss()
    if 'year' in kwargs.keys():
        year = kwargs['year']
        if isinstance(year,int):
            year = [year]

        year_is_in = lambda f: True in [str(y) in f for y in year]
        FILES = filter(year_is_in,FILES)

    if dataset is None:
        FILES = filter(lambda f: 'chc' not in f and 'CLAS' not in f,FILES)

    return list(FILES)

def load_data(year=None,usecols=None):
    """Loads the NAMCS Private Practice Health Care Survey Data

    Arguments
        year: None, int, or list

    # Returns
            Pandas Dataframe
    """

    usecols = usecols or DEFAULT_COLS + PRACTICE_COLS
    if year is None:
        # Just load latest year
        sel_files = _remote_sel()[-1:]
    elif isinstance(year,(int,list,np.ndarray)):
        sel_files = _remote_sel(year=year)

    # sav_files = [f.split('.zip')[0]+'.sav' for f in sel_files]
    pbar = tqdm(_cache_spss(sel_files),total=len(sel_files))
    dfs = []
    for f in pbar:
        f = f.split('.zip')[0]+'.sav'
        fp = os.path.join(DEFAULT_CACHE_DIR,'namcs',f)
        pbar.set_description(os.path.split(fp)[-1])
        dfs.append(pd.read_spss(fp,usecols=usecols))

    return pd.concat(dfs,sort=False)