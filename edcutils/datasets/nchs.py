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
BROAD_DX = ['DIAG13D','DIAG23D','DIAG33D','RFV13D','RFV23D','RFV33D']
SPECIFIC_DX = ['DIAG1','DIAG2','DIAG3','DIAG1R','DIAG2R','DIAG3R']
PATIENT = ['AGER','AGEDAYS','PREGNANT','ETHNIC','RACE','RACER','RACEETH']
VISIT = ['PRIMCARE','REFER','INJDET','INJURY','VMONTH','VDAY','VDAYR','ARRTIME']
VITALS = ['TEMPF','PULSE','RESPR','BPSYS','BPDIAS','PAINSCALE']

DEFAULT_COLS = ['SETTYPE','MAJOR','RFV13D','RFV1','YEAR','REGION','AGE','SEX','DIAG1','DIAG13D']


PUB_DIR = 'pub/Health_Statistics/NCHS'

# NCHS_BASE = 'ftp://ftp.cdc.gov//dataset_documentation/nhamcs/spss/'

def _data_files(survey,file_format):
    remote_dir = '/'.join([PUB_DIR,'dataset_documentation',str(survey).lower(),str(file_format).lower()])
    with FTP('ftp.cdc.gov') as ftp:
        ftp.login()
        contents = ftp.nlst(remote_dir)

    return [f for f in contents if f.endswith('.zip')]

# def _cache_spss_sav(dataset, files=SPSS_FILES):
#     base = 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/dataset_documentation/nhamcs/spss/'
#     fpaths = []
#     for fname in files:
#         path = get_file(fname.lower(),
#                         origin = base + fname,
#                         cache_dir = DEFAULT_CACHE_DIR,
#                         extract=True,
#                         cache_subdir = 'nhamcs')
#         fpaths.append(path)

#     return fpaths

def _cache(files):
    base = 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/dataset_documentation/nhamcs/spss/'
    fpaths = []
    for fname in files:
        path = get_file(fname.lower(),
                        origin = base + fname,
                        cache_dir = DEFAULT_CACHE_DIR,
                        extract=True,
                        cache_subdir = 'nhamcs')
        fpaths.append(path)

    return fpaths

def topn(df,column,query=None,n=5):
    if query is not None:
        results = df.query(query).groupby(column).size().sort_values(ascending=False)
    else:
        results = df.groupby(column).size().sort_values(ascending=False)
        
    return results[:n]