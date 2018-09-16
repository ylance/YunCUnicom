import os
import requests

from pyexcel_io import iget_data
from pyexcel_xlsx import get_data, save_data
from collections import OrderedDict

import lxml
from lxml import etree


def read_xlsx(path, sheet_index, start_row):
    dict_data, _ = iget_data(afile=path, sheet_index=sheet_index, start_row=start_row)
    for value in dict_data.values():
        first_row = next(value)
        name_index = first_row.index('姓名')
        id_index = first_row.index('身份证号')
        number_index = first_row.index('号码')
        for row in value:
            name = row[name_index]
            id = row[id_index]
            number = row[number_index]
            yield name, id, number


def write(name, id, number, result, record_path):
    if not os.path.exists(record_path):
        data = OrderedDict()
        data.update({'Sheet 1': [['姓名', '身份证号', '号码', '缴费结果']]})
        save_data(record_path, data)
    else:
        data = get_data(afile=record_path)
    rows = data["Sheet 1"]
    if [name, id, number, result] not in rows:
        rows.append([name, id, number, result])
    data.update({"Sheet 1": rows})
    save_data(record_path, data)


class PayMent(object):
    def __init__(self):
        self.url = 'http://133.128.6.186:8080/acctmanm'
        self.path = 'D:/Desktop/xueyuan_2.xlsx'
        self.record_path = 'D:/Desktop/xueyuan_2_reord.xlsx'
        self.fee = '50.00'
        self.submit = ' 收 费 '.encode('gbk')
        self.query = ' 查 询 '.encode('gbk')
        self.headers = {
            'Accept': 'image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*',
            'Referer': 'http://133.128.6.186:8080/acctmanm',
            'Accept-Language': 'zh-CN',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate',
            'Host': '133.128.6.186:8080',
            'Connection': 'Keep-Alive',
            'Pragma': 'no-cache',
           'Cookie': '__guid=221721176.840067343969089200.1536318815165.4204; LOGIN_SUBSYS_CODEBSS=CRM; LOGIN_STAFF_IDBSS=YCZY0451; BSS_BSS_JSESSIONID=nzCPbbsLBkxWFxxGLmd47pTdHJ0S17qPBqfrhfr9wtqGsQFNYkPK!-178863608!1551878969; BSS_BSS_STATSERV_JSESSIONID=20cWbbsLzppKTHsdZpj914QV4Z7MKwpdv0FjJhP3Hhz8npzP6713!-2127903152!-1715235729; BSS_SYSMANM_JSESSIONID=L8f7bbsLjPhnGyJL9YhYzgYCDklFqHlhN6w5QRtPrZbVDSNTBysJ!-1433269564!-269914159; BSS_BSS_CUSTMANM_JSESSIONID=2kl6bbsLtHhvK9jrgwyYDBKTKWmSGwv74JQGQQQwFT7n2HMz7sm8!-355411734!-245996366; BSS_RESMANM_JSESSIONID=h5sNbbsLJJ35TDyBCgND472GNT3wMXpJpGpPCpQbyv4wCB0JqMQW!1672713234!1101795391; BSS_BSS_SALEMANM_JSESSIONID=ZZSgbbsLZJxdv2YgGPZvchRSd9cYMNG76lRhdy8sCjF0QTlLNpsk!2061263565!159647921; BSS_CHNLMANM_JSESSIONID=dLjTbbsLh1dcMwyYNH17Rgw6VmhtxTdlD510kWr8VJQydthCjKLb!-798000933!112363500; BSS_BSS_CUSTSERV_JSESSIONID=SYLbbbsZVW6lSYg5gPJdj7bhcBTMnkXB72KnrRPvJJhbnN8L8g1h!1301866683!-243533903; BSS_BSS_ACCTMANM_JSESSIONID=9NJsbbsJY1mY1LHvbpkpG8T92w0nNJsTbbn6TkKqfNWh1nzWyx3K!1192800156!-1652137237'
        }
        # cookies 需要在登陆BSS后进行修改
        # self.cookies = {
        #     'LOGIN_STAFF_IDBSS': 'YCZY0884',
        #     'LOGIN_SUBSYS_CODEBSS': 'CRM',
        #     'BSS_BSS_STATSERV_JSESSIONID': '5416bQ1R6hkrSYG8XRkThMDx6QMxPnVGLlypTThJb2B2X2vj3GH8!-2127903152!-1715235729',
        #     'BSS_CHNLMANM_JSESSIONID': 'Lh7FbQ1RmPLkG41ZrKD1fmj03v8Fm2tjYHc6LQqNP1tFtrhwTkZt!112363500!-798000933',
        #     'BSS_SYSMANM_JSESSIONID': 'l2PSbQ1R7SSR1YzGz16Y1J7nBP58x2hSLJ5J1W2VvCQ7Lfp9WkJn!1981237768!2034334691',
        #     'BSS_RESMANM_JSESSIONID': 'xGFBbQ1Rx66PTfhwmyXHFyLb32QgRzgC4DNdqcC0HpZFyLv2GZGB!1672713234!1101795391',
        #     'BSS_BSS_SALEMANM_JSESSIONID': 'f7zTbQ1R6jTT8pQZ9RGzqYL6hxyf4wc6n9V3120D9JbkFTNwDV0G!159647921!2061263565',
        #     'BSS_BSS_CUSTMANM_JSESSIONID': '1ThpbQ1RTqHgHyT3LRdXd0bW8DnhX3ph8hwLQjsXZBh5TQ1n25kn!-705794729!-1850198033',
        #     'BSS_BSS_CUSTSERV_JSESSIONID': 'lyL6bQ1fKMHTfzFymzdJmnrXyJyQSWvJCxdPw1VNnfrVYBLYLMmG!2096993900!-870654650',
        #     'BSS_BSS_ACCTMANM_JSESSIONID': 'WCHCbQ1XK0Bd18h8wlMKLhJ16rXyTPsn7fP3Vsp6ffGpX9hZ4WpD!-1569386235!704896381',
        #     'BSS_BSS_JSESSIONID': 'F4MlbQJNfHmLfMyCX21fyhN1LhylYnhtJPy7NMM1rfq4Cd80hNY2!56405278!-476549662',
        # }

        self.data = {
            "service": "direct/1/amcharge.payfee.PayFee/$Form".encode('gbk'),
            "sp": "S0",
            "Form0": 'cond_WRITEOFF_MODE,cond_DESIGNATE_PAY,cond_CUST_COMMEND,cond_PUBLIC_TAG,cond_PRIVATE_TAG,cond_STOP_TAG,bquerytopwithfee,cond_NO_ROUND,cond_PAY_MODE,cond_SPAY_FEE,cond_TRADE_FEE,btnXml,cond_REMARK,bsubmit'.encode(
                'gbk'),
            "cond_ACCT_ID": "",
            "cond_USER_ID": "",
            "cond_CREDIT_OWEFEE": "",
            "cond_ISCREDIT_PAY": "",
            "cond_EPARCHY_CODE2": "",
            "cond_MIN_CYCLE_ID": "201809",
            "cond_LOG_IN_STAFFID": "YCZY0451",
            "TIME_FLAG": "",
            'AGENT_FLAG': '',
            "cond_NET_TYPE_CODE": "",
            "cond_ID_TYPE": "0",
            "cond_SERIAL_NUMBER": "18635985316",  # 17635292945   业务号码
            "cond_REMOVE_TAG": "0",
            "cond_CUST_COMMEND": "on",
            "cond_PUBLIC_TAG": "on",
            'bquerytopwithfee': ' 查 询 '.encode('gbk'),  # 验证号码是否存在的时候要用， 缴费的时候不用
            "cond_X_USER_COUNT": "",
            "sches": "on",
            "cond_NO_ROUND": "2",
            "cond_PAY_MODE": "0",
            "cond_SPAY_FEE": "0.00",
            "cond_TRADE_STAFF_ID": "",
            "cond_TRADE_DEPART_ID": "",
            "cond_TRADE_CITY_CODE": "",
            "cond_TRADE_EPARCHY_CODE": "",
            "cond_CHARGE_ID": "",
            "cond_MISPOS_TAG": "0",
            "cond_PAYCENTER_TAG": "0",
            'cond_TRADE_FEE': '0.00',  # 缴费金额
            "BUYER_TAXPAYER_ID": "",
            "BUYER_NAME": "",
            'BUYER_ADD': '',
            'BUYER_BANK_ACCOUNT': '',
            "BUYER_PHONE": "",
            "BUYER_EMAIL": "",
            "isHaveWo": "",
            "cond_MONTH_PAYYFEE_START_CYCID": "",
            "cond_SELECTED_CYCID": "",
            "cond_TRADE_FEE_FIX": "0.00",
            "cond_MONTH_PAYYFEE_END_CYCID": "",
            "cond_X_CONING_HEAD_DETAILITEM": "",
            "cond_X_CODING_STR_DETAILITEM": "",
            "cond_USER_MONTH_PAYYFEE": "0.00",
            "cond_USER_MONTH_TAG": "3",
            "cond_SPC_FEE": "0.0",
            "cond_CAN_PAY_CONSIGN_TAG": "1",
            "cond_CAN_CHANGE_USERFEE": "0",
            "cond_PAYFEE_PAGE": "PAYFEE",
            "cond_CYCLE_ID": "201808",
            "cond_END_CYCLE_ID": "201809",
            "userinfoback_ACTION_CODE": "",
            "userinfoback_CAMPN_COMMEND_ID": "",
            "cond_REMARK": "",
            # 'bsubmit': ' 收 费 '.encode('gbk'),     # 缴费的时候 要用， 验证号码是否存在的时候不用
            "ELECCOUP_SERIAL_NUMBER": "",
            "CZ_PASSWORD": "",
            "userinfoback_USER_ID": "1118090542271290",   # 用户信息
            "userinfoback_ACCT_ID": "1118090537417462",   #　用户信息
            "userinfoback_SERIAL_NUMBER": '18635985316',  # "17635292945"   业务号码
            "userinfoback_PAY_MODE_CODE": "现金".encode('gbk'),
            "userinfoback_REMOVE_TAG": "0",
            "userinfoback_ROUTE_EPARCHY_CODE": "0359",
            "userinfoback_NET_TYPE_CODE": "10",
            "userinfoback_CUST_NAME": "王宁".encode('gbk'),
            "userinfoback_ALLBOWE_FEE": "0.00",
            "X_CODING_NOTES": "",
            "X_CODING_TAX_NOS": "",
            "cond_NEW_OLD_SELECT": "",
            "userinfoback_PAY_TAG": "1",
            "userinfoback_CANPAY_TAG": "0",
            "cond_RECOVER_TAG": "1",
            "printData_CHARGE_ID": "",
            "printData_PRINT_PARTITION_ID": "",
            "printData_ACCT_ID": "",
            "printData_SERIAL_NUMBER": "",
            "printData_USER_ID": "",
            "printData_ALLBOWE_FEE": "",
            "printData_TRADE_FEE": "",
            "printData_PAY_MODE_CODE": "",
            "printData_CUST_NAME": "",
            "MULTI_ACCT_DATA": "",
            "X_CODING_STR": "",
            "X_CODING_STR_MONTH_FEE": "",
            "NoteMergeFlag": "",
            "printData_BRAND": "沃4G".encode('gbk'),
            "printData_ALL_NEW_MONEY": "",
            "printData_RES_FEE": "",
            "printData_SYS_DOUBLE_SCREEN": "",
            "printData_MERGE_RIGHT": "",
        }

    def validate(self, name, id, number):
        print(name,id,number)
        if self.data.get('bsubmit',None) is not None:
            del self.data['bsubmit']
        if self.data.get('userinfoback_ACCT_ID',None) is not None:
            del self.data['userinfoback_ACCT_ID']
        if self.data.get('userinfoback_USER_ID',None) is not None:
            del self.data['userinfoback_USER_ID']
        self.data['bquerytopwithfee'] = self.query
        self.data['userinfoback_CUST_NAME'] = name.encode('gbk')
        self.data['cond_SERIAL_NUMBER'] = number
        self.data['userinfoback_SERIAL_NUMBER'] = number
        self.data['cond_TRADE_FEE'] = '0.00'
        validate = requests.post(url=self.url, data=self.data, headers=self.headers)
        # print(validate)
        if '错误提示' in validate.content.decode('gbk'):
            # if '没有该号码资料或该用户可能拆机' in validate:
                write(name, id, number, '未激活', self.record_path)
            # else:
            #     write(name, id, number, '其他错误', self.record_path)
        else:
            # pass
            mytree = lxml.etree.HTML(validate.content.decode('gbk'))
            acct_id = mytree.xpath('//input[@id="userinfoback_ACCT_ID"]/@value')[0]
            user_id = mytree.xpath('//input[@id="userinfoback_USER_ID"]/@value')[0]
            self.payment(name, id, number,acct_id,user_id)

    def payment(self, name, id, number,acct_id,user_id):
        if self.data.get('bquerytopwithfee',None) is not None:
            del self.data['bquerytopwithfee']
        self.data['userinfoback_CUST_NAME'] = name.encode('gbk')
        self.data['cond_SERIAL_NUMBER'] = number
        self.data['userinfoback_SERIAL_NUMBER'] = number
        self.data['userinfoback_USER_ID'] = user_id
        self.data['userinfoback_ACCT_ID'] = acct_id
        self.data['cond_TRADE_FEE'] = self.fee
        self.data['bsubmit'] = self.submit
        requests.post(url=self.url, data=self.data, headers=self.headers)
        # print(rs.content.decode('gbk'))
        write(name, id, number, '缴费成功', self.record_path)

    def start(self):
        contents = read_xlsx(self.path, sheet_index=0, start_row=0)
        for name, id, number in contents:
            self.validate(name, id, number)


if __name__ == '__main__':
    p = PayMent()
    p.start()
