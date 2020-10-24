"""NHAMCS Dataset
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from ftplib import FTP

import numpy as np
import pandas as pd
import glob
from tqdm import tqdm
import pyreadstat

from keras.utils.data_utils import get_file

from .nchs import DEFAULT_COLS

HOSP_INFO = ['MSA','OWNER','HOSPCODE']

DEFAULT_CACHE_DIR = os.path.join(os.path.expanduser('~'), 'data')

SPSS_FILES = [
    'ED2017-spss.zip',
    'ed2016-spss.zip',
    'ed2015-spss.zip',
    'ed2014-spss.zip',
    'ed2013-spss.zip',
    'ed2011-spss.zip',
    'ed2010-spss.zip',
]

OPD_SPSS = [
    'opd2011-spss.zip',
    'opd2010-spss.zip',
]

def _cache_spss_sav(files=SPSS_FILES):
    base = 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/dataset_documentation/nhamcs/spss/'

    # with FTP('ftp.cdc.gov') as ftp:
    #     ftp.login()
    #     ftp.cwd('pub/Health_Statistics/NCHS/dataset_documentation/nhamcs/spss/')
    #     contents = []
    #     ftp.dir(contents.append
    fpaths = []
    for fname in files:
        path = get_file(fname.lower(),
                        origin = base + fname,
                        cache_dir = DEFAULT_CACHE_DIR,
                        extract=True,
                        cache_subdir = 'nhamcs')
        fpaths.append(path)

    return fpaths

def _load_spss(spss_files,usecols=None):
    usecols = usecols or DEFAULT_COLS

    pbar = tqdm(sorted(spss_files))
    for fp in pbar:
        pbar.set_description(os.path.split(fp)[-1])
        yield pd.read_spss(fp,usecols=usecols)


def load_ed(year=None,usecols=None):
    """Loads the NHAMCS ED dataset.

    Arguments
        year: None, int, or list

    # Returns
            Pandas Dataframe
    """

    is_in_year = lambda f: True in [str(y) in f for y in year]
    if isinstance(year,int):
        year = [year]

    if year is None:
        # Just load latest year
        sel_files = [SPSS_FILES[0]]
    elif isinstance(year,(list,np.ndarray)):
        sel_files = filter(is_in_year,SPSS_FILES)

    cached_files = _cache_spss_sav(sel_files)

    # sav_files = glob.glob(os.path.join(base,'nhamcs','*.sav'))
    sav_files = [f.split('.zip')[0]+'.sav' for f in cached_files]
    load_fps = [os.path.join(DEFAULT_CACHE_DIR,'nhamcs',f) for f in sav_files]

    dataset = pd.concat(_load_spss(load_fps),sort=False)
    dataset['SPECCAT'] = 'Emergency Medicine'

    return dataset

def load_opd(year=None,usecols=None):
    """Loads the National Hospital Outpatient dataset.

    Arguments
        year: None, int, or list

    # Returns
            Pandas Dataframe
    """
    is_in_year = lambda f: True in [str(y) in f for y in year]
    if isinstance(year,int):
        year = [year]

    if year is None:
        # Just load latest year
        sel_files = [OPD_SPSS[0]]
    elif isinstance(year,(list,np.ndarray)):
        sel_files = filter(is_in_year,OPD_SPSS)

    cached_files = _cache_spss_sav(sel_files)

    # sav_files = glob.glob(os.path.join(base,'nhamcs','*.sav'))
    sav_files = [f.split('.zip')[0]+'.sav' for f in cached_files]
    load_fps = [os.path.join(DEFAULT_CACHE_DIR,'nhamcs',f) for f in sav_files]

    dataset = pd.concat(_load_spss(load_fps,usecols=DEFAULT_COLS+['CLINTYPE']),sort=False)

    return dataset