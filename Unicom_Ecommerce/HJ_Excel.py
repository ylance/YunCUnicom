import os,winreg
import pandas as pd
import numpy as np




class DivideProfit(object):
    def __init__(self,old,new,file,out):
        # self.old_dir_path = old
        # self.new_dir_path = new
        # self.file_path = file
        # self.out_path = out

        self.old_dir_path = r'D:\Desktop\test_04'
        self.new_dir_path = r'D:\Desktop\test_05'
        self.file_path = r'D:\Desktop\出账明细201805账期宽带.xls'
        self.out_path = r'D:\Desktop'
        self.stop = False

    def read_dir(self,dirpath):
        for company in os.listdir(dirpath):
            if os.path.isdir(os.path.join(dirpath,company)):
                company_path = os.path.join(dirpath, company)
                file_list = os.listdir(os.path.join(dirpath, company))
                path_generator = map(lambda x: os.path.join(company_path, x), file_list)
                key = company
            else:
                path_generator = map(lambda x:os.path.join(dirpath,x),os.listdir(dirpath))
                company = dirpath.split('\\')[-1]
                key = company
        return self.process_data(path_generator,key)

    def process_data(self, path_gener, key):
        result={}
        df_list = []
        for path in path_gener:
            # print(path)
            with pd.ExcelFile(path) as xls:
                data = pd.read_excel(xls, sheet_name=0, index_col=None, na_values=['NaN'])
                deleted_data = data.dropna(subset=['号码']).drop(
                    columns=['分光器设备', '上连OLT端口', 'OLT端口类型', '分光器端子', '端子业务状态', '语音IP', 'ONU MAC地址或SN码', '逻辑ID',
                             'SN串码'])
                left_list = [number for number in deleted_data['号码'] if len(number) > 7]
                deleted_data = deleted_data[deleted_data['号码'].isin(left_list)].copy()
                if deleted_data.empty:
                    continue
                deleted_data.loc[:, '号码'] = '0359' + deleted_data['号码'].str[0:8]
                df_list.append(deleted_data)
        result[key] = pd.concat(df_list,ignore_index=True)
        return result

    def read_file(self):
        with pd.ExcelFile(self.file_path) as xls:
            data = pd.read_excel(xls, 0, index_col=None, na_values=['NaN'])
            result = pd.concat([data['SERIAL_NUMBER'], data['FEE']], axis=1, ignore_index=True).rename(
                columns={0: '号码', 1: '出账收入'}).fillna(0)
        return result

    def profit(self, users, profit_data):
        merged_data = pd.merge(users, profit_data, how='left', on='号码')
        merged_data['分成金额'] = np.where(merged_data['出账收入'] >= 16.66, 16.66, 0)
        merged_data['出账收入'] = merged_data['出账收入'].fillna('未在出账收入表里匹配到相应的号码')
        return merged_data

    def process(self):
        add_columns = ['新老用户', '用户到达', '分成金额']
        old_data_dict = self.read_dir(self.old_dir_path)
        new_data_dict = self.read_dir(self.new_dir_path)
        for company, dataform in old_data_dict.items():
            new_data = new_data_dict[company]
            old_data = old_data_dict[company]
            old_user = new_data[new_data['号码'].isin(old_data['号码'])].reindex(columns=list(old_data.columns) + add_columns)
            old_user.loc[:, '新老用户'] = '老用户'
            old_user.loc[:, '用户到达'] = '1'
            left_numbers = [number for number in list(new_data['号码']) if number not in list(old_data['号码'])]
            new_user = new_data[new_data['号码'].isin(left_numbers)].reindex(columns=list(old_data.columns) + add_columns)
            new_user.loc[:, '新老用户'] = '新用户'
            new_user.loc[:, '用户到达'] = '1'
            users = old_user.append(new_user, ignore_index=True)
            profit_data = self.read_file()
            result_data = self.profit(users,profit_data)
            # print(self.out_path)
            result_data.to_excel(os.path.join(self.out_path,company)+'初算表.xlsx')
        self.stop = True
