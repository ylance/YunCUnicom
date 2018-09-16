
import time,lxml
from lxml import etree

import os
import requests

from pyexcel_io import iget_data
from pyexcel_xlsx import get_data, save_data
from collections import OrderedDict

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
        data.update({'Sheet 1': [['姓名', '身份证号', '号码', '结果']]})
        save_data(record_path, data)
    else:
        data = get_data(afile=record_path)
    rows = data["Sheet 1"]
    if [name, id, number, result] not in rows:
        rows.append([name, id, number, result])
    data.update({"Sheet 1": rows})
    save_data(record_path, data)

headers = {
    'Accept': 'image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*',
    'Referer': 'http://133.128.6.186:8080/acctmanm',
    'Accept-Language': 'zh-CN',
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Length': '2132',
    'Host': '133.128.6.186:8080',
    'Connection': 'Keep-Alive',
    'Pragma': 'no-cache',
    'Cookie': '__guid=221721176.840067343969089200.1536318815165.4204; LOGIN_SUBSYS_CODEBSS=CRM; LOGIN_STAFF_IDBSS=YCZY0835; BSS_BSS_CUSTSERV_JSESSIONID=Vpv9bbcd9czbnT4qTLHFm1kGFppyvBzDT3znPL2y2Tn0J9sThZQh!1301866683!-243533903; BSS_BSS_ACCTMANM_JSESSIONID=ZW8JbbcHKqkPcn1SRtxV13frNpzmcLJTLcT7kbQX95xTSvcj5yMR!1192800156!-1652137237; BSS_BSS_JSESSIONID=0NSqbbjJbZNQVpVyCyhvDbCsLGw4rNkjqycJl112NvVYRVCJ1bhy!-178863608!1551878969',
}
time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
url = 'http://133.128.6.186:8080/acctmanm'

for content in read_xlsx(r'D:/Desktop/返销明细.xlsx',sheet_index=0,start_row=0):
    name,id,number = content
    print(name,id,number)
    data = 'service=direct/1/amcharge.paycancel.PayCancel/$Form&sp=S0&Form0=cond_EARLY_TIME,cond_BEGIN_TIME,cond_END_TIME,cond_DESIGNATE_PAY,bquerytop,daochu2,bSubmit&cond_ACCT_ID=&cond_USER_ID=&cond_EPARCHY_CODE2=&cond_LOG_IN_STAFFID=YCZY0835&cond_NET_TYPE_CODE=&cond_ID_TYPE=0&cond_SERIAL_NUMBER={number}&cond_REMOVE_TAG=0&cond_EARLY_TIME=2018-06-16&cond_BEGIN_TIME=2018-09-12&cond_END_TIME=2018-09-14&bquerytop= 查询 &cond_X_USER_COUNT=&cond_CANCEL_REMARK=&cond_QRY_DATE='+time_now+'&MULTI_ACCT_DATA=&ALERT_FLAG=&X_CONING_HEAD=&X_CODING_STR=&cond_MODULE_TAG=0&cond_QRYSUCCESS=&cond_RIGHTHAVE=&CANCEL_PRINT_DATA='
    data = data.format(number=str(number))
    rs = requests.post(url=url,headers=headers,data=data.encode('gbk'))
    # print(rs.content.decode('gbk'))
    mytree = lxml.etree.HTML(rs.content.decode('gbk'))
    tr_num = len(mytree.xpath('//table[@id="PayLogTable"]/tbody/tr'))
    print(tr_num)
    if tr_num != 3:
        write(name,id,number,'失败',r'D:/Desktop/返销_record.xlsx')
        print('失败')
    else:
        user_1 = mytree.xpath('//tr[@class="row_odd"][1]/td[4]')[0].text
        user_2 = mytree.xpath('//tr[@class="row_odd"][1]/td[5]')[0].text
        user_3 = mytree.xpath('//tr[@class="row_odd"][1]/td[6]')[0].text
        user_4 = mytree.xpath('//tr[@class="row_odd"][1]/td[7]')[0].text
        user_5 = mytree.xpath('//tr[@class="row_odd"][1]/td[9]')[0].text
        user_6 = mytree.xpath('//tr[@class="row_even"][1]/td[9]')[0].text

        data_2 ={
            'X_CONING_HEAD':'RADIO,SN,X_TAG,CHARGE_ID,SERIAL_NUMBER,USER_ID,ACCT_ID,PAY_NAME,RECV_TIME,RECV_FEE,PAYMENT,PAY_FEE_MODE,RECV_STAFF_ID,RECV_DEPART_ID,RECV_EPARCHY_CODE,RECV_CITY_CODE,ACT_TAG,OPERT_INFO,EPARCHY_CODE,CANCEL_FLAG,PARTITION_ID,PRESENT_FLAG,EXTEND_TAG,BATCH_ID,OUTER_TRADE_ID,PAYMENT_ID,PAYMENT_OP,PAY_FEE_MODE_CODE,CHANNEL_ID,REMARK,TIME_LIMIT',
            'X_CODING_STR':'PayL0003031000000010000110016{user_1}0011{user_2}0016{user_3}0016{user_4}00000019{user_5}000550.000017营业厅收入(帐务收费)_普通预存款0002现金0008YCCB059100050CC7B000403590004MQ0000011000000040359000000019000000010000000000006100001000516000000100005150010000000000000001100000016{user_1}0011{user_2}0016{user_3}0016{user_4}00000019{user_6}0006-16.000007冻结款分月解冻0005非现金优惠0007SYSUSER000500000000403590004000000011000000040359000000019000000010000000000006100022000516004000140005150060004预存转兑0000000000012000000167018091393456172001118534312036001611180907422915760016111809073743832600000019{user_6}000516.000007冻结款分月解冻0005非现金优惠0007SYSUSER000500000000403590004000000011000000040359000000019000000010000000000006100023000516005000140005150060004预存转兑0000'.format(user_1=user_1,user_2=user_2,user_3=user_3,user_4=user_4,user_5=user_5,user_6=user_6).encode('gbk'),
            'cond_LOG_IN_STAFFID':'YCZY0835',
            'X_OPTION':'1',
            'cond_CANCEL_REMARK':'师范',
            'cond_PAYMENT_ID':'null',
            'cond_REMOVE_TAG': '0',
            'globalPageName':'amcharge.paycancel.PayCancel'
        }
        rs = requests.post(url='http://133.128.6.186:8080/acctmanm?service=swallow/amcharge.paycancel.PayCancel/submitPayCancel/1',headers=headers,data=data_2)
        print('成功')
        write(name,id,number,'成功','D:/Desktop/返销_record.xlsx')