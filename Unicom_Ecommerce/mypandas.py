import pandas as pd
import numpy as np

data = {}

with pd.ExcelFile(u'D:/Desktop/test_04/test/连伯1.xls') as xls:
    data['Sheet'] = pd.read_excel(xls,sheet_name=0, index_col=None, na_values=[np.nan])
deleted_data = data['Sheet'].dropna(subset=['号码']).copy()
deleted_data.loc[:,'号码'] = '0359'+deleted_data.loc[:,'号码'].str[0:7]

print(deleted_data['号码'])

