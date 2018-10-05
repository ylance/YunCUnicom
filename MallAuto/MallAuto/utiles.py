import winreg
import os
import sqlite3

from pyexcel_xlsx import get_data,save_data
from collections import OrderedDict
from win32crypt import CryptUnprotectData

def read_xlsx(path, sheet_index, start_row):
    dict_data = get_data(afile=path,sheet_index=sheet_index,start_row=start_row)
    orderNo_dict = {}
    orderNos = []
    for value in dict_data.values():
        for row in value:
            if '下单日期' in row:
                orderNo_index = row.index('订单号')
            if '订单号' in row:
                order_date_index = row.index('下单日期')
                continue
            orderNo = str(row[orderNo_index])
            order_date = str(row[order_date_index])[0:8]
            orderNo_dict[order_date] = []
            orderNo_date = (orderNo,order_date)
            orderNos.append(orderNo_date)
    for item in orderNos:
        orderNo_dict[item[1]].append(item[0])
    return orderNo_dict

def write(orderNo, order_date, result, record_path):
    if not os.path.exists(record_path):
        data = OrderedDict()
        data.update({'Sheet 1': [['订单号', '下单日期', '结果']]})
        save_data(record_path, data)
    else:
        data = get_data(afile=record_path)
    rows = data["Sheet 1"]
    if [orderNo, order_date, result] not in rows:
        rows.append([orderNo, order_date, result])
    data.update({"Sheet 1": rows})
    save_data(record_path, data)


def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')  # 利用系统的链表
    return winreg.QueryValueEx(key, "Desktop")[0]


def create_dir(create_path):
    if not os.path.exists(create_path):
        os.makedirs(create_path)
    return create_path


def getcookiefromchrome(host='.10010.com'):
    cookiepath = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"
    sql = "select name,encrypted_value from cookies where host_key = '%s'" % host
    with sqlite3.connect(cookiepath) as conn:
        cu = conn.cursor()
        cookies = {result[0]: CryptUnprotectData(result[1])[1].decode() for result in cu.execute(sql).fetchall()}
        # print(cookies['AdminStaff'])
        return cookies


s = getcookiefromchrome()
print(s)
