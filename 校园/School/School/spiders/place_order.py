import os
import json

import execjs

from scrapy import Spider
from scrapy.http import FormRequest
from pyexcel_io import iget_data
from pyexcel_xlsx import get_data, save_data
from urllib.parse import quote

from collections import OrderedDict

path = 'D:/Desktop/师范二批.xlsx'
error_path = 'D:/Desktop/error_orders.xlsx'
sheet_index = 0
start_row = 0
sid_path = r'D:\Development\Pycharm\Workspace\School\School\utils\school.js'
sign_path = r'D:\Development\Pycharm\Workspace\School\School\utils\md5.js'


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


class place_order(Spider):
    name = 'spider_place_order'

    def start_requests(self):
        url = 'http://480.sxltkhfw.com/gateway/rest/abilitysx/rest/wechatSelf/openCard/cardOrderRecive'
        remark1 = '10105'  # 学校编码
        for content in read_xlsx(path, sheet_index, start_row):
            name, id, number = content
            # print(content)
            sid = execjs.compile(open(sid_path, encoding='utf-8').read()).call('sid')
            param = "openid=&openId=&productId={productId}&selectedPhone={selectedPhone}&idcardNum={idcardNum}&idcardName={idcardName}&cardCity={cardCity}&contactProvince={contactProvince}&contactCity={contactCity}&contactDistrict={contactDistrict}&contactAddress={contactAddress}&contactPhone={contactPhone}&contactFixPhone={contactFixPhone}&contactName={contactName}&contactRemark={contactRemark}&orderSource={orderSource}&remark1={remark1}&sid={sid}".format(
                sid=sid, openid='', openId='', productId='2018050900017098', selectedPhone=str(number),
                idcardNum=str(id), idcardName=quote(str(name)),
                cardCity='0359', contactProvince=quote('山西省'), contactCity=quote('运城市'), contactDistrict=quote('盐湖区'),
                contactAddress=quote('粮库路金地花苑北联通公司'),
                contactPhone='18603595441', contactFixPhone='03592502006', contactName=quote(str(name)), contactRemark='',
                orderSource='1002', remark1='10105')
            # param = 'openid=&openId=&productId=2018050900017098&selectedPhone=18534310529&idcardNum=140428200009148825&idcardName=%E6%9D%A8%E9%A2%96&cardCity=0359&contactProvince=%E5%B1%B1%E8%A5%BF%E7%9C%81&contactCity=%E8%BF%90%E5%9F%8E%E5%B8%82&contactDistrict=%E7%9B%90%E6%B9%96%E5%8C%BA&contactAddress=%E7%B2%AE%E5%BA%93%E8%B7%AF%E9%87%91%E5%9C%B0%E8%8A%B1%E8%8B%91%E5%8C%97%E8%81%94%E9%80%9A%E5%85%AC%E5%8F%B8&contactPhone=18603595441&contactFixPhone=03592502006&contactName=%E8%A7%A3%E6%99%B6%E7%90%B3&contactRemark=&orderSource=1002&remark1=10105&sid=1536055700227106349'
            # print(param)
            sign = execjs.compile(open(sign_path, encoding='utf-8').read()).call('md5', param,
                                                                                 '2c90806954842ab30154842cb43cf25a').lower()
            # print(sign)
            # print(sign)
            data = {
                'openid': '',
                'openId': '',
                'productId': '2018050900017098',  # 套餐id
                'selectedPhone': str(number),  # 选定号码
                'idcardNum': str(id),  # 身份证号
                'idcardName': str(name),  # 姓名
                'cardCity': '0359',  # 城市代码
                'contactProvince': '山西省',
                'contactCity': '运城市',
                'contactDistrict': '盐湖区',
                'contactAddress': '粮库路金地花苑北联通公司',
                'contactPhone': '18603595441',  # 联系电话
                'contactFixPhone': '03592502006',  # 固话
                'contactName': str(name),
                'contactRemark': '',  # 备注
                'orderSource': '1002',  # 1002 代表校园卡，可以跳过年龄限制，只是在网页上登陆的时候游泳
                'remark1': remark1,  # 学校编码
                'sid': str(sid),  # 根据当前时间得到的一个数值，在生成签名的时候用
                'sign': str(sign)  # 签名
            }
            headers = {
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'http://480.sxltkhfw.com/hollybeacon-cloud-abilitywebsx-web/hollywechat/wechat/card/productShow.jsp?param=757365724e616d652533442575373338422575354238312532366964436172642533443134323730323139393030313231303031332532366361726474797065253344322532366f72646572536f757263652533443130303225323673436f64652533443130313037253236734369747925334430333539038c8846',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
            }
            yield FormRequest(url=url,
                              method='POST',
                              dont_filter=True,
                              formdata=data,
                              meta={'name': name, 'id': id, 'number': number},
                              headers=headers,
                              # callback=self.parse,
                              )

    def parse(self, response):
        rs = response.body.decode('utf-8')
        # print(rs)
        name = response.meta['name']
        id = response.meta['id']
        number = response.meta['number']
        print(response.meta['name'], response.meta['id'], response.meta['number'])
        rs_text = json.loads(rs)
        # print(rs_text)
        if rs_text['success'] is True:
            write(name, id, number, '下单成功')
        if rs_text['errorType'] == '8888':  # 8888 错误，15日内只能申请一次
            write(name, id, number, '15日只能申请一次')
        elif rs_text['errorType'] == '9999':  # 9999 错误，提交订单异常
            write(name, id, number, '提交订单异常')
        else:  # 其他错误
            write(name, id, number, '其他错误')


def write(name, id, number, result, path=error_path):
    if not os.path.exists(error_path):
        data = OrderedDict()
        data.update({'Sheet 1': [['姓名', '身份证号', '号码', '下单结果']]})
        save_data(error_path, data)
    else:
        data = get_data(afile=path)
    rows = data["Sheet 1"]
    if [name, id, number, result] not in rows:
        rows.append([name, id, number, result])
    data.update({"Sheet 1": rows})
    save_data(path, data)

# count = 0
# for i in read_xlsx(path,0,0):
#     count += 1
#     print(i)
# print(count)

