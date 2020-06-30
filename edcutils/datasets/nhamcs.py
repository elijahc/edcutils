"""NHAMCS Dataset
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import numpy as np
import pandas as pd
import glob
from tqdm import tqdm
import pyreadstat

from keras.utils.data_utils import get_file

DEFAULT_CACHE_DIR = os.path.join(os.path.expanduser('~'), 'data')
SPSS_FILES = [
    'ED2017-spss.zip',
    'ed2016-spss.zip',
    'ed2015-spss.zip',
    'ed2014-spss.zip',
    'ed2013-spss.zip',
]

DEFAULT_COLS = [
    'YEAR',
    'VMONTH',
    'VDAY',
    'VDAYR',
    'ARRTIME',
    'AGE',
    'AGER',
    'AGEDAYS',
    'SEX',
    'TEMPF',
    'PULSE',
    'RESPR',
    'REGION',
    'BPSYS',
    'BPDIAS',
    'PAINSCALE',
    'EPISODE',
    'INJURY',
    'RFV1',
    'RFV13D',
#     'RFV2',
#     'RFV3',
    'CAUSE1',
    'CAUSE13D'
#     'CAUSE2',
#     'CAUSE3',
    'PRDIAG1',
    'DIAG1',
    'DIAG13D',
    'DIEDED',
#     'DIAG2',
#     'DIAG3',
#     'DIAG4',
#     'DIAG5'
]

def _cache_spss_sav(files=SPSS_FILES):
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

def _load_savs(base,usecols=None):
    usecols = usecols or DEFAULT_COLS
    sav_files = glob.glob(os.path.join(base,'nhamcs','*.sav'))

    pbar = tqdm(sav_files)
    for fp in pbar:
        pbar.set_description(os.path.split(fp)[-1])
        yield pd.read_spss(fp,usecols=usecols)

def load_ed_data(usecols=None):
    """Loads the NHAMCS ED dataset.

    # Returns
            Pandas Dataframe
    """

    _cache_spss_sav(SPSS_FILES)
    return pd.concat(_load_savs(base=DEFAULT_CACHE_DIR),sort=False)
