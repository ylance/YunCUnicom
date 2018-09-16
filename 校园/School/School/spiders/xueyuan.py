# coding:gbk

import os,requests,json,re

from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException

from pyexcel_io import iget_data
from pyexcel_xlsx import save_data, get_data
import time

def is_not_visible(b, locator, timeout=60):
    try:
        WebDriverWait(b, timeout, 0.5).until_not(EC.visibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False


def alert_isexit(b):
    try:
        alert_refresh = WebDriverWait(b, 2, 0.5).until(EC.alert_is_present())
        return True, alert_refresh
    except TimeoutException as e:
        return False, None


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


class Change(object):
    def __init__(self):
        self.brow = webdriver.Ie()
        self.url = 'http://133.128.6.186:8080/bssframe'
        self.user_name = 'YCZY0451'
        self.password = 'WANG123+'
        self.brow.get(self.url)

        self.path = r'D:\Desktop\xueyuan_2.xlsx'
        self.record = r'D:\Desktop\xueyuan_2_record.xlsx'

        self.name = ''
        self.id = ''
        self.number = ''
        self.result = ''

    def login(self):
        user_name = self.brow.find_element_by_xpath('//*[@id="STAFF_ID"]')
        user_name.clear()
        user_name.send_keys(self.user_name)
        self.brow.find_element_by_xpath('//*[@id="PASSWORD"]').send_keys(self.password)
        time.sleep(10)
        self.brow.switch_to.frame(self.brow.find_element_by_xpath('//frame[@id="navframe"]'))
        btn = self.brow.find_element_by_xpath('//a[@id="SECOND_MENU_LINK_CSM2000"]')
        self.brow.execute_script('arguments[0].click();', btn)

    def into_frame(self):
        self.brow.switch_to.parent_frame()
        WebDriverWait(self.brow, 30, 0.5).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//frame[@id="sidebarframe"]')))
        WebDriverWait(self.brow, 30, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="CSM2007"]')))
        c_bn = self.brow.find_element_by_xpath('//*[@id="CSM2007"]')
        self.brow.execute_script('arguments[0].click();', c_bn)
        self.brow.switch_to.parent_frame()

    def open_school_service(self, name,number):
        WebDriverWait(self.brow, 30, 0.5).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//frame[@id="contentframe"]')))
        WebDriverWait(self.brow, 30, 0.5).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//frame[@id="navframe_1"]')))

        WebDriverWait(self.brow, 30, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="SERIAL_NUMBER"]')))
        number_input = self.brow.find_element_by_xpath('//input[@id="SERIAL_NUMBER"]')
        number_input.clear()
        number_input.send_keys(number)
        query_btn = self.brow.find_element_by_xpath('//input[@id="queryTrade"]')
        self.brow.execute_script('arguments[0].click();', query_btn)


        time.sleep(2)
        WebDriverWait(self.brow, 30, 0.5).until(EC.presence_of_element_located((By.XPATH, '//input[@id="_p20104142"]')))
        product_ot = self.brow.find_element_by_xpath('//input[@id="_p20104142"]').get_attribute('_startDate')

        WebDriverWait(self.brow, 30, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="_tradeBase"]')))
        user_name = self.brow.find_element_by_xpath('//input[@id="CUST_NAME"]').get_attribute('value')
        user_id = self.brow.find_element_by_xpath('//input[@id="USER_ID_HIDEN"]').get_attribute('value')
        trade_base = self.brow.find_element_by_xpath('//input[@id="_tradeBase"]').get_attribute('value')
        # print(trade_base)
        self.continue_submit(user_id, trade_base, product_ot, user_name,number)

    def continue_submit(self, user_id, trade_base, product_ot,name, number):
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        data = {
            'Base': trade_base,
            'Ext':'{"Common": {"ACTOR_NAME": "", "ACTOR_PHONE": "", "ACTOR_CERTTYPEID": "", "ACTOR_CERTNUM": "", "REMARK": ""}, "TF_B_TRADE_DISCNT": {"ITEM": [{"ID": "'+user_id+'", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001024", "DISCNT_CODE": "99051112", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "2018-10-01 00:00:00", "END_DATE": "2019-09-30 23:59:59", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""}, {"ID": "'+user_id+'", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001025", "DISCNT_CODE": "19102407", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "'+time_now+'", "END_DATE": "2050-01-01 00:00:00", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""}, {"ID": "'+user_id+'", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001025", "DISCNT_CODE": "19102923", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "'+time_now+'", "END_DATE": "2050-01-01 00:00:00", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""}, {"ID": "'+user_id+'", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001026", "DISCNT_CODE": "19103204", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "'+time_now+'", "END_DATE": "2050-01-01 00:00:00", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""}]}, "TF_B_TRADE_USER": {"ITEM": {"PRODUCT_ID": "20104142", "BRAND_CODE": "4G02", "USER_ID": "'+user_id+'", "NET_TYPE_CODE": "10"}}, "TF_B_TRADE": {"PRODUCT_ID": "20104142", "BRAND_CODE": "4G02", "EXEC_TIME": "'+time_now+'"}, "TRADE_SUB_ITEM": {}, "MANYOU_TEMP": {"ITEM": {"ManYouCreditTag": false}}, "TRADE_ITEM": {"DEVELOP_SUB_TYPE": "", "DEVELOP_STAFF_ID": "", "IS_TELEKET": "0", "TELEKET_TYPE": "", "DEVELOP_DEPART_ID": ""}}'
        }
        headers = {
            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
            'Accept-Language': 'zh-CN',
            'x-prototype-version': '1.5.1',
            'Referer': 'http://133.128.6.186:8080/custserv',
            'x-requested-with': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; InfoPath.2; .NET4.0C; .NET4.0E)',
            'Host': '133.128.6.186:8080',
            'Content-Length': '4529',
            'Connection': 'Keep-Alive',
            'Pragma': 'no-cache',
            'Cookie': '__guid=221721176.840067343969089200.1536318815165.4204; LOGIN_SUBSYS_CODEBSS=CRM; BSS_BSS_ACCTMANM_JSESSIONID=n2JJbcrT3LT27H2BWJpjvGnBBjyv6QfZnPTc7GWQBW782LS8f9zZ!-1652137237!626944312; BSS_BSS_STATSERV_JSESSIONID=h1NKbctJ2KDLfrJQKKx20ytXym2kQWvGnC2yj96tFldvdcSNQcRW!105771892!1549156998; BSS_SYSMANM_JSESSIONID=rbWtbctJH8ZZSCPm0S5y4F85nqQtnqGXG27wd6H4Qk2STQ60XRCv!-269914159!-1433269564; BSS_RESMANM_JSESSIONID=fw8BbctJLcFF1JTCyhSBdvv42j11wx8PgHxQp1JvvC3pkkwCTnND!1672713234!1101795391; BSS_BSS_JSESSIONID=ZK51bctJnnn7vvCS68Rh8LmWyGcklWhg4Qw8QPrRGhyLdh1pWJW3!1551878969!-1702348738; BSS_CHNLMANM_JSESSIONID=bvC5bctJ1tJjbJtSpqyLTPHNl2LpCyWhL3yvLwq2TZFJ02XhhJsk!112363500!-798000933; BSS_BSS_SALEMANM_JSESSIONID=2vKLbctJwYQW0JJwJQbTDM0JnMBCkX212LmsVbXCyzN1c52GvpWd!159647921!2061263565; BSS_BSS_CUSTMANM_JSESSIONID=ywC6bctJBQMvhG2tLV73nNJPtGvLf8w7mhv6Q0mNtwGTQy0yvGS0!-1850198033!-2050571229; LOGIN_STAFF_IDBSS=YCZY0451; BSS_BSS_CUSTSERV_JSESSIONID=lL75bctGbkT62B2Q3hgpgQ04qPq2fBxRpxmGKqx0GTNLhpS2xbmq!2104451838!-782718536'
        }

        rs = requests.post(
            url='http://133.128.6.186:8080/custserv?service=swallow/personalserv.changeelement.ChangeElement/submitMobTrade/1',
            data=data, headers=headers)

        str_1 = rs.content.decode('gbk')
        trade_id = re.findall("tradeId='(\d+)'", str_1)[0]
        subscribe_id = re.findall("subscribeId='(\d+)'", str_1)[0]
        # startDate = re.findall('START_DATE&gt;(.+)&lt;/START_DATE', str_1)[0]
        inDepart = re.findall('inDepartId="(\d+)"', str_1)[0]
        developDepartId = re.findall('developDepartId="(\d+)"', str_1)[0]
        execTime = re.findall('execTime="(.+)" termIp', str_1)[0]
        developDate = re.findall('developDate="(.+)" scoreValue', str_1)[0]
        openDate = re.findall('openDate="(.+)" userTypeCode', str_1)[0]
        item_id = re.findall('itemId="(\d+)"', str_1)[0]
        cust_id = re.findall('custId="(\d+)"', str_1)[0]
        user_id = re.findall('userId="(\d+)"', str_1)[0]
        acct_id = re.findall('acctId="(\d+)"', str_1)[0]
        develop_staff = re.findall('developStaffId="(.+)" userType', str_1)[0]
        instaff_id = re.findall('inStaffId="(.+)" invoiceNo', str_1)[0]
        tradestaff_id = re.findall('tradeStaffId="(.+)" openStaffId', str_1)[0]
        openstaff_id = re.findall('openStaffId="(.+)" processTagSet', str_1)[0]
        acceptDate = re.findall('acceptDate="(.+)" destroyTime', str_1)[0]
        pspt_id = re.findall('#36523;&#20221;&#35777;:(\d+)', str_1)[0]
        inDate = re.findall('inDate="(.+)" mputeDate', str_1)[0]
        mputeDate = re.findall('mputeDate="(.+)" assureTypeCode', str_1)[0]
        phone = re.findall('(\d+)~~" tradeDepartId', str_1)
        if phone == []:
            phone = '18535915441'
        else:
            phone = re.findall('(\d+)~~" tradeDepartId', str_1)[0]
        ip = re.findall('termIp="(.+)" xCodingStr9', str_1)[0]
        userPasswd = re.findall('userPasswd="(.+)" routeEparchyCode', str_1)[0]
        tradeDepartId = re.findall('tradeDepartId=(.+) receiptInfo4', str_1)[0]
        if '该号码有未完工的产品' in rs.content.decode('gbk'):
            print('失败')
            write(self.name, self.id, self.number, '失败', self.record)
        elif '业务无法继续' in rs.content.decode('gbk'):
            print('失败')
            write(self.name, self.id, self.number, '失败', self.record)
        else:
            tradeMain = '[{"TRADE_ID": "' + trade_id + '", "TRADE_TYPE": "产品/服务变更", "SERIAL_NUMBER": "' + number + '", "TRADE_FEE": "50.00", "CUST_NAME": "' + name + '", "CUST_ID": "' + cust_id + '", "USER_ID": "' + user_id + '", "ACCT_ID": "' + acct_id + '", "NET_TYPE_CODE": "10", "TRADE_TYPE_CODE": "120", "PSPT_TYPE_CODE": "0"}]'
            fees = '[{"X_TAG": "1", "TRADE_ID": "' + trade_id + '", "CALCULATE_ID": "", "FEE_MODE": "2", "FEEITEM_CODE": "100005", "OLDFEE": "50.00", "FEE": "50.00", "DERATE_REMARK": "", "PAY_MONEY_CODE": "0", "PAY_TAG": "0", "CALCULATE_TAG": "N", "MODIFY_TAG": "", "TRADE_TYPE_CODE": "120", "NET_TYPE_CODE": "10", "FEEITEM_NAME": "[预存]营业厅收入(营业缴费)_普通预存款(不可清退))"}]'
            feePayMoney = '[{"TRADE_ID": "' + trade_id + '", "PAY_MONEY_CODE": "0", "MONEY": 5000}]'
            base = json.dumps({"xCodingStr1": "", "xCodingStr2": "", "xCheckTag": "1", "creditClass": "-1", "usecustId": "" + cust_id + "", "routeEparchy": "运城", "acctTag": "0", "remark": "", "feeState": "", "developDate": "" + developDate + "", "scoreValue": "0", "execTime": "" + execTime + "", "termIp": "" + ip + "", "xCodingStr9": "", "openDate": "" + openDate + "", "userTypeCode": "0", "xCodingStr8": "", "xCodingStr7": "", "xCodingStr6": "", "tradeId": "" + trade_id + "", "receiptInfo2": "担保人姓名:    担保类型:    担保人联系电话: 担保人证件类型:担保人证件类型\n担保人证件号码: ~代理人姓名:   代理人联系电话: 代理人证件类型:   代理人证件号码: ", "provinceCode": "SXCU", "xCodingStr5": "", "receiptInfo1": "                                                   " + name + "~~\n                                                   " + number + "                                                                 " + pspt_id + "~~\n                                                   个人                                                                   \n                                                   " + phone + "~~", "tradeDepartId": ""+tradeDepartId+"", "receiptInfo4": "", "xCodingStr4": "", "xCodingStr3": "", "receiptInfo3": "认证方式: \n~新增优惠:1元/月,拨打本地网联通免费~   生效时间:2018-09-14~0元500分钟本地拨打长市合一分钟数~   生效时间:2018-09-14~10元国内流量不限量包,100G后限速为1Mbps(立即生效)~   生效时间:2018-09-14~存50送180元话费，预存款一次性到账，赠款次月分12个月返还~   生效时间:2018-10-01~~取消优惠: ~新增服务: ~取消服务: ~新增SP: ~取消SP: \n~提醒:初次使用时请修改密码.~~~月套餐国内（不含台港澳）流量当月不清零，剩余流量自动结转至下月，有效期至下月月底。套餐内其他业务量以及定向流量叠加包、后向流量产品、赠送流量等仅限当月使用，不能延续至下月使用。~ ~~ ~当月套餐及叠加流量包以外的流量计费达到600元后，国内（不含台港澳）流量不再收费，达到15GB后系统自动关闭数据网络，次月自动打开。用户主动申请，当月打开；当月国际及港澳台漫游和套餐内、套餐外、各种收费、免费、各类定向等数据流量总和达到100GB后系统自动关闭数据网络，当月不再开放，次月自动开\n", "xCodingStr12": "", "receiptInfo7": "", "xCodingStr13": "", "receiptInfo5": "~ ~ ~认证方式: ~ ~手机串号:~ ~", "xCodingStr14": "", "receiptInfo6": "", "xCodingStr15": "", "mputeMonthFee": "1", "openDepartId": "M0959", "xCodingStr10": "", "removeReasonCode": "", "xCodingStr11": "", "tradeEparchyCode": "0359", "xCodingStr16": "", "xCodingStr17": "", "xCodingStr18": "", "xCodingStr19": "", "removeEparchyCode": "", "feeTime": "", "creditRuleId": "-1", "feeStaffId": "", "checkTypeCode": "", "brandCode": "4G02", "tradeStatus": "query", "prepayTag": "0", "dealType": "1", "inModeCode": "0", "productId": "20104142", "serialNumber": "" + number + "", "userStateCodeset": "0", "actorCertnum": ":", "removeCityCode": "", "itemId": "" + item_id + "", "userPasswd": "" + userPasswd + "", "routeEparchyCode": "0359", "contactAddress": "", "assureCustId": "", "strisneedprint": "1", "checkResult": "0000", "custId": "" + cust_id + "", "acctId": "" + acct_id + "", "xLcuLogstep": "32", "xCodingStr": "", "xCheckInfo": "SpPt00102000110370特殊限制判断:用户在本次业务中:<br><br>新增优惠：【1元/月,拨打本地网联通免费】，【0元500分钟本地拨打长市合一分钟数】，【10元国内流量不限量包,100G后限速为1Mbps(立即生效)】，【存50送180元话费，预存款一次性到账，赠款次月分12个月返还】<br><br><b><font color :'red'></font></b><br>请提醒用户查看免填单中变更的信息", "endAcycId": "203701", "actorCerttypeid": "", "actorPhone": "", "xRecordnum": "1", "xSelcount": "0", "cityCode": "MQ00", "detailInstallAddress": "", "inStaffId": "" + instaff_id + "", "invoiceNo": "", "inNetMode": "0", "priority": "320", "developStaffId": "" + develop_staff + "", "userType": "普通用户", "attrTypeCode": "0", "lastStopTime": "", "tradeAttr": "1", "openMode": "0", "tradeLcuName": "TCS_ChangeServiceReg", "userDiffCode": "00", "xLastResultinfo": "", "tradeInfoTagSet": "111111    ", "nextDealTag": "Z", "xResultinfo": "", "olcomTag": "0", "removeTag": "0", "partitionId": "2623", "foregift": "0", "contactPostAddr": "", "id": "" + user_id + "", "rightCode": "csChangeServiceTrade", "chkTag": "0", "fee": "0", "operFee": "0", "tradeTypeCode": "120", "cancelTag": "0", "changeuserDate": "", "tradeTagSet": "10100000000000000000", "xTransCode": "TCS_ChangeServiceReg", "basicCreditValue": "0", "xLastResultcode": "0", "updateTime": "", "tradeCityCode": "MQ00", "custType": "个人客户", "netTypeCode": "10", "custName": "" + name + "", "developDepartId": ""+developDepartId+"", "firstCallTime": "", "inDepartId": ""+inDepart+"", "leaveRealFee": "0", "tradeStaffId": "" + tradestaff_id + "", "openStaffId": "" + openstaff_id + "", "processTagSet": " ", "xResultcode": "0", "advancePay": "0", "acceptDate": "" + acceptDate + "", "destroyTime": "", "tradeJudgeOweTag": "0", "contactName": "", "idType": "1", "preDestroyTime": "", "creditValue": "0", "contactPhone": "", "psptId": "身份证:" + pspt_id + "", "xTag": "1", "contactPostCode": "", "contractId": "", "acceptMonth": "9", "assureDate": "", "userId": "" + user_id + "", "developEparchyCode": "0359", "startAcycId": "194910", "xLcuTxdservCount": "0", "eparchyCode": "0359", "contact": "", "developNo": "", "developCityCode": "MQ00", "removeDepartId": "", "productTypeCode": "4444", "inDate": "" + inDate + "", "mputeDate": "" + mputeDate + "", "assureTypeCode": "", "subscribeId": "" + subscribe_id + "", "tradeType": "产品/服务变更", "actorName": ""})
            data = {
                'cancelTag': 'false',
                'funcType': '0',
                'dataType': '0',
                'tradeMain': tradeMain.encode('gbk'),
                'fees': fees.encode('gbk'),
                'unChargedfees': '[]',
                'feePayMoney': feePayMoney,
                'feeCheck': '[]',
                'PSPT_TYPE_CODE_BAK': '0',
                'ALL_OLD_FEE': '50.00',
                'ALL_FEE': '50.00',
                'DERATE_STAFF_ID': tradestaff_id,
                'NEW_PAYTAG': 'C',
                'CONTINUE_MODE': '0',
                'isNotTax': '0',
                'base': base,
                'CASH': '50.00',
                'SEND_TYPE': '0',
                'TRADE_ID': trade_id
            }

            url = 'http://133.128.6.186:8080/custserv?service=swallow/personalserv.dealtradefee.DealTradeFee/continueTradeReg/1'
            rs = requests.post(url=url,data=data,headers=headers)

            if 'chargeOK' in rs.content.decode('utf-8'):
                print('成功')
                write(self.name, self.id, self.number, '成功', self.record)

    def run(self):
        self.login()
        self.into_frame()
        for content in read_xlsx(self.path, sheet_index=1, start_row=0):
            self.name, self.id, self.number = content
            print(self.name, self.id, self.number)
            try:
                self.open_school_service(self.name,self.number)
                self.brow.switch_to.default_content()
            except UnexpectedAlertPresentException:
                # print('sdf')
                print('失败')
                self.result = '失败'
                write(self.name, self.id, self.number, self.result, self.record)

                self.brow.switch_to.default_content()
                continue
            except TimeoutException:
                self.result = '失败'
                print('失败')
                write(self.name, self.id, self.number, self.result, self.record)
                self.brow.switch_to.default_content()
                continue
            except Exception as e:
                self.result = '失败' + e.__str__()
                write(self.name, self.id, self.number, self.result, self.record)
                self.brow.switch_to.default_content()
                continue

if __name__ == '__main__':
    change = Change()
    change.run()
    # str_1 =
    '''
    <?xml version="1.0" encoding="UTF-8"?><root><message></message><TradeSubmitOk tradeId='1118091527921278' subscribeId='1118091527921278'><Fee feenum='1'></Fee><checkAfterData><data checkType="1" checkData="&#29305;&#27530;&#38480;&#21046;&#21028;&#26029;:&#29992;&#25143;&#22312;&#26412;&#27425;&#19994;&#21153;&#20013;:&lt;br&gt;&lt;br&gt;&#26032;&#22686;&#20248;&#24800;&#65306;&#12304;1&#20803;/&#26376;,&#25320;&#25171;&#26412;&#22320;&#32593;&#32852;&#36890;&#20813;&#36153;&#12305;&#65292;&#12304;0&#20803;500&#20998;&#38047;&#26412;&#22320;&#25320;&#25171;&#38271;&#24066;&#21512;&#19968;&#20998;&#38047;&#25968;&#12305;&#65292;&#12304;10&#20803;&#22269;&#20869;&#27969;&#37327;&#19981;&#38480;&#37327;&#21253;,20G&#21518;&#38480;&#36895;&#20026;3Mbps(&#31435;&#21363;&#29983;&#25928;)&#12305;&#65292;&#12304;&#23384;50&#36865;180&#20803;&#35805;&#36153;&#65292;&#39044;&#23384;&#27454;&#19968;&#27425;&#24615;&#21040;&#36134;&#65292;&#36192;&#27454;&#27425;&#26376;&#20998;12&#20010;&#26376;&#36820;&#36824;&#12305;&lt;br&gt;&lt;br&gt;&lt;b&gt;&lt;font color ='red'&gt;&lt;/font&gt;&lt;/b&gt;&lt;br&gt;&#35831;&#25552;&#37266;&#29992;&#25143;&#26597;&#30475;&#20813;&#22635;&#21333;&#20013;&#21464;&#26356;&#30340;&#20449;&#24687;"/></checkAfterData><TradeData xCodingStr1="" xCodingStr2="" xCheckTag="1" creditClass="0" usecustId="1118091327856464" routeEparchy="&#36816;&#22478;" acctTag="0" remark="" feeState="" developDate="2018-09-13 17:57:20" scoreValue="0" execTime="2018-09-15 13:49:46" termIp="133.150.40.81" xCodingStr9="" openDate="2018-09-13 17:57:20" userTypeCode="0" xCodingStr8="" xCodingStr7="" xCodingStr6="" tradeId="1118091527921278" receiptInfo2="&#25285;&#20445;&#20154;&#22995;&#21517;:    &#25285;&#20445;&#31867;&#22411;:    &#25285;&#20445;&#20154;&#32852;&#31995;&#30005;&#35805;: &#25285;&#20445;&#20154;&#35777;&#20214;&#31867;&#22411;:&#25285;&#20445;&#20154;&#35777;&#20214;&#31867;&#22411;
&#25285;&#20445;&#20154;&#35777;&#20214;&#21495;&#30721;: ~&#20195;&#29702;&#20154;&#22995;&#21517;:   &#20195;&#29702;&#20154;&#32852;&#31995;&#30005;&#35805;: &#20195;&#29702;&#20154;&#35777;&#20214;&#31867;&#22411;:   &#20195;&#29702;&#20154;&#35777;&#20214;&#21495;&#30721;: " provinceCode="SXCU" xCodingStr5="" receiptInfo1="                                                   &#20130;&#26059;&#26059;~~
                                                   15525894985                                                                 142601199809174922~~
                                                   &#20010;&#20154;                                                                   
                                                    ~~" tradeDepartId="M1079" receiptInfo4="" xCodingStr4="" xCodingStr3="" receiptInfo3="&#35748;&#35777;&#26041;&#24335;: 
~&#26032;&#22686;&#20248;&#24800;:1&#20803;/&#26376;,&#25320;&#25171;&#26412;&#22320;&#32593;&#32852;&#36890;&#20813;&#36153;~   &#29983;&#25928;&#26102;&#38388;:2018-09-15~0&#20803;500&#20998;&#38047;&#26412;&#22320;&#25320;&#25171;&#38271;&#24066;&#21512;&#19968;&#20998;&#38047;&#25968;~   &#29983;&#25928;&#26102;&#38388;:2018-09-15~10&#20803;&#22269;&#20869;&#27969;&#37327;&#19981;&#38480;&#37327;&#21253;,20G&#21518;&#38480;&#36895;&#20026;3Mbps(&#31435;&#21363;&#29983;&#25928;)~   &#29983;&#25928;&#26102;&#38388;:2018-09-15~&#23384;50&#36865;180&#20803;&#35805;&#36153;&#65292;&#39044;&#23384;&#27454;&#19968;&#27425;&#24615;&#21040;&#36134;&#65292;&#36192;&#27454;&#27425;&#26376;&#20998;12&#20010;&#26376;&#36820;&#36824;~   &#29983;&#25928;&#26102;&#38388;:2018-10-01~~&#21462;&#28040;&#20248;&#24800;:  ~&#26032;&#22686;&#26381;&#21153;: ~&#21462;&#28040;&#26381;&#21153;: ~&#26032;&#22686;SP: ~&#21462;&#28040;SP: 
~&#25552;&#37266;:&#21021;&#27425;&#20351;&#29992;&#26102;&#35831;&#20462;&#25913;&#23494;&#30721;.~~~&#26376;&#22871;&#39184;&#22269;&#20869;&#65288;&#19981;&#21547;&#21488;&#28207;&#28595;&#65289;&#27969;&#37327;&#24403;&#26376;&#19981;&#28165;&#38646;&#65292;&#21097;&#20313;&#27969;&#37327;&#33258;&#21160;&#32467;&#36716;&#33267;&#19979;&#26376;&#65292;&#26377;&#25928;&#26399;&#33267;&#19979;&#26376;&#26376;&#24213;&#12290;&#22871;&#39184;&#20869;&#20854;&#20182;&#19994;&#21153;&#37327;&#20197;&#21450;&#23450;&#21521;&#27969;&#37327;&#21472;&#21152;&#21253;&#12289;&#21518;&#21521;&#27969;&#37327;&#20135;&#21697;&#12289;&#36192;&#36865;&#27969;&#37327;&#31561;&#20165;&#38480;&#24403;&#26376;&#20351;&#29992;&#65292;&#19981;&#33021;&#24310;&#32493;&#33267;&#19979;&#26376;&#20351;&#29992;&#12290;~ ~~ ~&#24403;&#26376;&#22871;&#39184;&#21450;&#21472;&#21152;&#27969;&#37327;&#21253;&#20197;&#22806;&#30340;&#27969;&#37327;&#35745;&#36153;&#36798;&#21040;600&#20803;&#21518;&#65292;&#22269;&#20869;&#65288;&#19981;&#21547;&#21488;&#28207;&#28595;&#65289;&#27969;&#37327;&#19981;&#20877;&#25910;&#36153;&#65292;&#36798;&#21040;15GB&#21518;&#31995;&#32479;&#33258;&#21160;&#20851;&#38381;&#25968;&#25454;&#32593;&#32476;&#65292;&#27425;&#26376;&#33258;&#21160;&#25171;&#24320;&#12290;&#29992;&#25143;&#20027;&#21160;&#30003;&#35831;&#65292;&#24403;&#26376;&#25171;&#24320;&#65307;&#24403;&#26376;&#22269;&#38469;&#21450;&#28207;&#28595;&#21488;&#28459;&#28216;&#21644;&#22871;&#39184;&#20869;&#12289;&#22871;&#39184;&#22806;&#12289;&#21508;&#31181;&#25910;&#36153;&#12289;&#20813;&#36153;&#12289;&#21508;&#31867;&#23450;&#21521;&#31561;&#25968;&#25454;&#27969;&#37327;&#24635;&#21644;&#36798;&#21040;100GB&#21518;&#31995;&#32479;&#33258;&#21160;&#20851;&#38381;&#25968;&#25454;&#32593;&#32476;&#65292;&#24403;&#26376;&#19981;&#20877;&#24320;&#25918;&#65292;&#27425;&#26376;&#33258;&#21160;&#24320;
" xCodingStr12="" receiptInfo7="" xCodingStr13="" receiptInfo5="~ ~ ~&#35748;&#35777;&#26041;&#24335;: ~ ~&#25163;&#26426;&#20018;&#21495;:~ ~" xCodingStr14="" receiptInfo6="" xCodingStr15="" mputeMonthFee="1" openDepartId="42335" xCodingStr10="" removeReasonCode="" xCodingStr11="" tradeEparchyCode="0359" xCodingStr16="" xCodingStr17="" xCodingStr18="" xCodingStr19="" removeEparchyCode="" feeTime="" creditRuleId="-1" feeStaffId="" checkTypeCode="" brandCode="4G02" tradeStatus="query" prepayTag="0" dealType="1" inModeCode="0" productId="20104142" serialNumber="15525894985" userStateCodeset="0" actorCertnum=":" removeCityCode="" itemId="1118091342316862" userPasswd="4YULip" routeEparchyCode="0359" contactAddress="" assureCustId="" strisneedprint="1" checkResult="0000" custId="1118091327856464" acctId="1118091337463840" xLcuLogstep="32" xCodingStr="" xCheckInfo="SpPt00102000110306&#29305;&#27530;&#38480;&#21046;&#21028;&#26029;:&#29992;&#25143;&#22312;&#26412;&#27425;&#19994;&#21153;&#20013;:&lt;br&gt;&lt;br&gt;&#26032;&#22686;&#20248;&#24800;&#65306;&#12304;1&#20803;/&#26376;,&#25320;&#25171;&#26412;&#22320;&#32593;&#32852;&#36890;&#20813;&#36153;&#12305;&#65292;&#12304;0&#20803;500&#20998;&#38047;&#26412;&#22320;&#25320;&#25171;&#38271;&#24066;&#21512;&#19968;&#20998;&#38047;&#25968;&#12305;&#65292;&#12304;10&#20803;&#22269;&#20869;&#27969;&#37327;&#19981;&#38480;&#37327;&#21253;,20G&#21518;&#38480;&#36895;&#20026;3Mbps(&#31435;&#21363;&#29983;&#25928;)&#12305;&#65292;&#12304;&#23384;50&#36865;180&#20803;&#35805;&#36153;&#65292;&#39044;&#23384;&#27454;&#19968;&#27425;&#24615;&#21040;&#36134;&#65292;&#36192;&#27454;&#27425;&#26376;&#20998;12&#20010;&#26376;&#36820;&#36824;&#12305;&lt;br&gt;&lt;br&gt;&lt;b&gt;&lt;font color ='red'&gt;&lt;/font&gt;&lt;/b&gt;&lt;br&gt;&#35831;&#25552;&#37266;&#29992;&#25143;&#26597;&#30475;&#20813;&#22635;&#21333;&#20013;&#21464;&#26356;&#30340;&#20449;&#24687;" endAcycId="203701" actorCerttypeid="" actorPhone="" xRecordnum="1" xSelcount="0" cityCode="MQ00" detailInstallAddress="" inStaffId="YCHZ3333" invoiceNo="" inNetMode="" priority="320" developStaffId="YCHZ0659" userType="&#26222;&#36890;&#29992;&#25143;" attrTypeCode="0" lastStopTime="" tradeAttr="1" openMode="0" tradeLcuName="TCS_ChangeServiceReg" userDiffCode="00" xLastResultinfo="" tradeInfoTagSet="111111    " nextDealTag="Z" xResultinfo="" olcomTag="0" removeTag="0" partitionId="6862" foregift="0" contactPostAddr="" id="1118091342316862" rightCode="csChangeServiceTrade" chkTag="0" fee="0" operFee="0" tradeTypeCode="120" cancelTag="0" changeuserDate="" tradeTagSet="10100000000000000000" xTransCode="TCS_ChangeServiceReg" basicCreditValue="0" xLastResultcode="0" updateTime="" tradeCityCode="MQ00" custType="&#20010;&#20154;&#23458;&#25143;" netTypeCode="10" custName="&#20130;&#26059;&#26059;" developDepartId="42335" firstCallTime="" inDepartId="42335" leaveRealFee="0" tradeStaffId="YCZY0451" openStaffId="YCHZ3333" processTagSet=" " xResultcode="0" advancePay="0" acceptDate="2018-09-15 13:49:46" destroyTime="" tradeJudgeOweTag="0" contactName="" idType="1" preDestroyTime="" creditValue="0" contactPhone="" psptId="&#36523;&#20221;&#35777;:142601199809174922" xTag="1" contactPostCode="" contractId="" acceptMonth="9" assureDate="" userId="1118091342316862" developEparchyCode="" startAcycId="194910" xLcuTxdservCount="0" eparchyCode="0359" contact="" developNo="" developCityCode="" removeDepartId="" productTypeCode="4444" inDate="2018-09-13 17:57:20" mputeDate="2018-09-13 18:07:07" assureTypeCode="" subscribeId="1118091527921278" tradeType="&#20135;&#21697;/&#26381;&#21153;&#21464;&#26356;" actorName=""/></TradeSubmitOk></root>

    '''
    # trade_id = re.findall("tradeId='(\d+)'", str_1)[0]
    # subscribe_id = re.findall("subscribeId='(\d+)'", str_1)[0]
    # # startDate = re.findall('START_DATE&gt;(.+)&lt;/START_DATE', str_1)[0]
    # inDepart = re.findall('inDepartId="(\d+)"',str_1)[0]
    # developDepartId = re.findall('developDepartId="(\d+)"',str_1)[0]
    # execTime = re.findall('execTime="(.+)" termIp', str_1)[0]
    # developDate = re.findall('developDate="(.+)" scoreValue', str_1)[0]
    # openDate = re.findall('openDate="(.+)" userTypeCode', str_1)[0]
    # item_id = re.findall('itemId="(\d+)"', str_1)[0]
    # cust_id = re.findall('custId="(\d+)"', str_1)[0]
    # user_id = re.findall('userId="(\d+)"', str_1)[0]
    # acct_id = re.findall('acctId="(\d+)"', str_1)[0]
    # develop_staff = re.findall('developStaffId="(.+)" userType', str_1)[0]
    # instaff_id = re.findall('inStaffId="(.+)" invoiceNo', str_1)[0]
    # tradestaff_id = re.findall('tradeStaffId="(.+)" openStaffId', str_1)[0]
    # openstaff_id = re.findall('openStaffId="(.+)" processTagSet', str_1)[0]
    # acceptDate = re.findall('acceptDate="(.+)" destroyTime', str_1)[0]
    # pspt_id = re.findall('#36523;&#20221;&#35777;:(\d+)', str_1)[0]
    # inDate = re.findall('inDate="(.+)" mputeDate', str_1)[0]
    # mputeDate = re.findall('mputeDate="(.+)" assureTypeCode', str_1)[0]
    # phone = re.findall('(\d+)~~" tradeDepartId', str_1)
    # if phone == []:
    #     phone = '18535915441'
    # else:
    #     phone = re.findall('(\d+)~~" tradeDepartId', str_1)[0]
    # ip = re.findall('termIp="(.+)" xCodingStr9', str_1)[0]
    # userPasswd = re.findall('userPasswd="(.+)" routeEparchyCode', str_1)[0]
    # tradeDepartId = re.findall('tradeDepartId=(\d+)',str_1)[0]
    # print(trade_id)
    # print(subscribe_id)
    # # print(startDate)
    # print(inDepart)
    # print(developDepartId)
    # print(execTime)
    # print(developDate)
    # print(openDate)
    # print(item_id)
    # print(cust_id)
    # print(user_id)
    # print(acct_id)
    # print(develop_staff)
    # print(instaff_id)
    # print(tradestaff_id)
    # print(openstaff_id)
    # print(acceptDate)
    # print(pspt_id)
    # print(inDate)
    # print(mputeDate)
    # # print(phone)
    # print(ip)
    # print(userPasswd)
    # print(tradeDepartId)
    # cancelTag=false
    # funcType=0
    # dataType=0
    # tradeMain=[{"TRADE_ID": "1118091527923131", "TRADE_TYPE": "产品/服务变更", "SERIAL_NUMBER": "17536011288", "TRADE_FEE": "50.00", "CUST_NAME": "刘娜", "CUST_ID": "1118091327856604", "USER_ID": "1118091342317072", "ACCT_ID": "1118091337464043", "NET_TYPE_CODE": "10", "TRADE_TYPE_CODE": "120", "PSPT_TYPE_CODE": "0"}]
    # fees=[{"X_TAG": "1", "TRADE_ID": "1118091527923131", "CALCULATE_ID": "", "FEE_MODE": "2", "FEEITEM_CODE": "100005", "OLDFEE": "50.00", "FEE": "50.00", "DERATE_REMARK": "", "PAY_MONEY_CODE": "0", "PAY_TAG": "0", "CALCULATE_TAG": "N", "MODIFY_TAG": "", "TRADE_TYPE_CODE": "120", "NET_TYPE_CODE": "10", "FEEITEM_NAME": "[预存]营业厅收入(营业缴费)_普通预存款(不可清退))"}]
    # unChargedfees=[]
    # feePayMoney=[{"TRADE_ID": "1118091527923131", "PAY_MONEY_CODE": "0", "MONEY": 5000}]
    # feeCheck=[]
    # PSPT_TYPE_CODE_BAK=0
    # ALL_OLD_FEE=50.00
    # ALL_FEE=50.00
    # DERATE_STAFF_ID=YCZY0451
    # NEW_PAYTAG=C
    # CONTINUE_MODE=0
    # isNotTax=0
    # base = '{"xCodingStr1": "", "xCodingStr2": "", "xCheckTag": "1", "creditClass": "-1", "usecustId": "' + cust_id + '", "routeEparchy": "运城", "acctTag": "0", "remark": "", "feeState": "", "developDate": "' + developDate + '", "scoreValue": "0", "execTime": "' + execTime + '", "termIp": "' + ip + '", "xCodingStr9": "", "openDate": "' + openDate + '", "userTypeCode": "0", "xCodingStr8": "", "xCodingStr7": "", "xCodingStr6": "", "tradeId": "' + trade_id + '", "receiptInfo2": "担保人姓名:    担保类型:    担保人联系电话: 担保人证件类型:担保人证件类型\n担保人证件号码: ~代理人姓名:   代理人联系电话: 代理人证件类型:   代理人证件号码: ", "provinceCode": "SXCU", "xCodingStr5": "", "receiptInfo1": "                                                   ' + name + '~~\n                                                   ' + number + '                                                                 ' + pspt_id + '~~\n                                                   个人                                                                   \n                                                   ' + phone + '~~", "tradeDepartId": "M0959", "receiptInfo4": "", "xCodingStr4": "", "xCodingStr3": "", "receiptInfo3": "认证方式: \n~新增优惠:1元/月,拨打本地网联通免费~   生效时间:2018-09-14~0元500分钟本地拨打长市合一分钟数~   生效时间:2018-09-14~10元国内流量不限量包,100G后限速为1Mbps(立即生效)~   生效时间:2018-09-14~存50送180元话费，预存款一次性到账，赠款次月分12个月返还~   生效时间:2018-10-01~~取消优惠:  ~新增服务: ~取消服务: ~新增SP: ~取消SP: \n~提醒:初次使用时请修改密码.~~~月套餐国内（不含台港澳）流量当月不清零，剩余流量自动结转至下月，有效期至下月月底。套餐内其他业务量以及定向流量叠加包、后向流量产品、赠送流量等仅限当月使用，不能延续至下月使用。~ ~~ ~当月套餐及叠加流量包以外的流量计费达到600元后，国内（不含台港澳）流量不再收费，达到15GB后系统自动关闭数据网络，次月自动打开。用户主动申请，当月打开；当月国际及港澳台漫游和套餐内、套餐外、各种收费、免费、各类定向等数据流量总和达到100GB后系统自动关闭数据网络，当月不再开放，次月自动开\n", "xCodingStr12": "", "receiptInfo7": "", "xCodingStr13": "", "receiptInfo5": "~ ~ ~认证方式: ~ ~手机串号:~ ~", "xCodingStr14": "", "receiptInfo6": "", "xCodingStr15": "", "mputeMonthFee": "1", "openDepartId": "M0959", "xCodingStr10": "", "removeReasonCode": "", "xCodingStr11": "", "tradeEparchyCode": "0359", "xCodingStr16": "", "xCodingStr17": "", "xCodingStr18": "", "xCodingStr19": "", "removeEparchyCode": "", "feeTime": "", "creditRuleId": "-1", "feeStaffId": "", "checkTypeCode": "", "brandCode": "4G02", "tradeStatus": "query", "prepayTag": "0", "dealType": "1", "inModeCode": "0", "productId": "20104142", "serialNumber": "' + number + '", "userStateCodeset": "0", "actorCertnum": ":", "removeCityCode": "", "itemId": "' + item_id + '", "userPasswd": "' + userPasswd + '", "routeEparchyCode": "0359", "contactAddress": "", "assureCustId": "", "strisneedprint": "1", "checkResult": "0000", "custId": "' + cust_id + '", "acctId": "' + acct_id + '", "xLcuLogstep": "32", "xCodingStr": "", "xCheckInfo": "SpPt00102000110370特殊限制判断:用户在本次业务中:<br><br>新增优惠：【1元/月,拨打本地网联通免费】，【0元500分钟本地拨打长市合一分钟数】，【10元国内流量不限量包,100G后限速为1Mbps(立即生效)】，【存50送180元话费，预存款一次性到账，赠款次月分12个月返还】<br><br><b><font color :' + 'red' + '></font></b><br>请提醒用户查看免填单中变更的信息", "endAcycId": "203701", "actorCerttypeid": "", "actorPhone": "", "xRecordnum": "1", "xSelcount": "0", "cityCode": "MQ00", "detailInstallAddress": "", "inStaffId": "' + instaff_id + '", "invoiceNo": "", "inNetMode": "0", "priority": "320", "developStaffId": "' + develop_staff + '", "userType": "普通用户", "attrTypeCode": "0", "lastStopTime": "", "tradeAttr": "1", "openMode": "0", "tradeLcuName": "TCS_ChangeServiceReg", "userDiffCode": "00", "xLastResultinfo": "", "tradeInfoTagSet": "111111    ", "nextDealTag": "Z", "xResultinfo": "", "olcomTag": "0", "removeTag": "0", "partitionId": "2623", "foregift": "0", "contactPostAddr": "", "id": "' + user_id + '", "rightCode": "csChangeServiceTrade", "chkTag": "0", "fee": "0", "operFee": "0", "tradeTypeCode": "120", "cancelTag": "0", "changeuserDate": "", "tradeTagSet": "10100000000000000000", "xTransCode": "TCS_ChangeServiceReg", "basicCreditValue": "0", "xLastResultcode": "0", "updateTime": "", "tradeCityCode": "MQ00", "custType": "个人客户", "netTypeCode": "10", "custName": "' + name + '", "developDepartId": "M0959", "firstCallTime": "", "inDepartId": "M0959", "leaveRealFee": "0", "tradeStaffId": "' + tradestaff_id + '", "openStaffId": "' + openstaff_id + '", "processTagSet": " ", "xResultcode": "0", "advancePay": "0", "acceptDate": "' + acceptDate + '", "destroyTime": "", "tradeJudgeOweTag": "0", "contactName": "", "idType": "1", "preDestroyTime": "", "creditValue": "0", "contactPhone": "", "psptId": "身份证:' + pspt_id + '", "xTag": "1", "contactPostCode": "", "contractId": "", "acceptMonth": "9", "assureDate": "", "userId": "' + user_id + '", "developEparchyCode": "0359", "startAcycId": "194910", "xLcuTxdservCount": "0", "eparchyCode": "0359", "contact": "", "developNo": "", "developCityCode": "MQ00", "removeDepartId": "", "productTypeCode": "4444", "inDate": "' + inDate + '", "mputeDate": "' + mputeDate + '", "assureTypeCode": "", "subscribeId": "' + subscribe_id + '", "tradeType": "产品/服务变更", "actorName": ""}'
    # base=   {"xCodingStr1": "", "xCodingStr2": "", "xCheckTag": "1", "creditClass": "-1", "usecustId": "1118091327856604", "routeEparchy": "运城", "acctTag": "0", "remark": "", "feeState": "", "developDate": "2018-09-13 18:40:28", "scoreValue": "0", "execTime": "2018-09-15 14:07:59", "termIp": "133.150.40.81", "xCodingStr9": "", "openDate": "2018-09-13 18:40:28", "userTypeCode": "0", "xCodingStr8": "", "xCodingStr7": "", "xCodingStr6": "", "tradeId": "1118091527923131", "receiptInfo2": "担保人姓名:    担保类型:    担保人联系电话: 担保人证件类型:担保人证件类型\n担保人证件号码: ~代理人姓名:   代理人联系电话: 代理人证件类型:   代理人证件号码: ", "provinceCode": "SXCU", "xCodingStr5": "", "receiptInfo1": "                                                   刘娜~~\n                                                   17536011288                                                                 140224199812181227~~\n                                                   个人                                                                   \n                                                   17835695523~~", "tradeDepartId": "M1079", "receiptInfo4": "", "xCodingStr4": "", "xCodingStr3": "", "receiptInfo3": "认证方式: \n~新增优惠:1元/月,拨打本地网联通免费~   生效时间:2018-09-15~0元500分钟本地拨打长市合一分钟数~   生效时间:2018-09-15~10元国内流量不限量包,100G后限速为1Mbps(立即生效)~   生效时间:2018-09-15~存50送180元话费，预存款一次性到账，赠款次月分12个月返还~   生效时间:2018-10-01~~取消优惠:  ~新增服务: ~取消服务: ~新增SP: ~取消SP: \n~提醒:初次使用时请修改密码.~~~月套餐国内（不含台港澳）流量当月不清零，剩余流量自动结转至下月，有效期至下月月底。套餐内其他业务量以及定向流量叠加包、后向流量产品、赠送流量等仅限当月使用，不能延续至下月使用。~ ~~ ~当月套餐及叠加流量包以外的流量计费达到600元后，国内（不含台港澳）流量不再收费，达到15GB后系统自动关闭数据网络，次月自动打开。用户主动申请，当月打开；当月国际及港澳台漫游和套餐内、套餐外、各种收费、免费、各类定向等数据流量总和达到100GB后系统自动关闭数据网络，当月不再开放，次月自动开\n", "xCodingStr12": "", "receiptInfo7": "", "xCodingStr13": "", "receiptInfo5": "~ ~ ~认证方式: ~ ~手机串号:~ ~", "xCodingStr14": "", "receiptInfo6": "", "xCodingStr15": "", "mputeMonthFee": "1", "openDepartId": "42335", "xCodingStr10": "", "removeReasonCode": "", "xCodingStr11": "", "tradeEparchyCode": "0359", "xCodingStr16": "", "xCodingStr17": "", "xCodingStr18": "", "xCodingStr19": "", "removeEparchyCode": "", "feeTime": "", "creditRuleId": "-1", "feeStaffId": "", "checkTypeCode": "", "brandCode": "4G02", "tradeStatus": "query", "prepayTag": "0", "dealType": "1", "inModeCode": "0", "productId": "20104142", "serialNumber":    "17536011288", "userStateCodeset": "0", "actorCertnum": ":", "removeCityCode": "", "itemId": "1118091342317072",            "userPasswd": "pAaozk", "routeEparchyCode": "0359", "contactAddress": "", "assureCustId": "", "strisneedprint": "1", "checkResult": "0000", "custId": "1118091327856604", "acctId": "1118091337464043", "xLcuLogstep": "32", "xCodingStr": "", "xCheckInfo": "SpPt00102000110307特殊限制判断:用户在本次业务中:<br><br>新增优惠：【1元/月,拨打本地网联通免费】，【0元500分钟本地拨打长市合一分钟数】，【10元国内流量不限量包,100G后限速为1Mbps(立即生效)】，【存50送180元话费，预存款一次性到账，赠款次月分12个月返还】<br><br><b><font color ='red'></font></b>                                                     <br>请提醒用户查看免填单中变更的信息", "endAcycId": "203701", "actorCerttypeid": "", "actorPhone": "", "xRecordnum": "1", "xSelcount": "0", "cityCode": "MQ00", "detailInstallAddress": "", "inStaffId": "YCHZ3333", "invoiceNo": "", "inNetMode": "0", "priority": "320", "developStaffId": "YCHZ0659", "userType": "普通用户", "attrTypeCode": "0", "lastStopTime": "", "tradeAttr": "1", "openMode": "0", "tradeLcuName": "TCS_ChangeServiceReg", "userDiffCode": "00", "xLastResultinfo": "", "tradeInfoTagSet": "111111    ", "nextDealTag": "Z", "xResultinfo": "", "olcomTag": "0", "removeTag": "0", "partitionId": "7072", "foregift": "0", "contactPostAddr": "", "id": "1118091342317072", "rightCode": "csChangeServiceTrade", "chkTag": "0", "fee": "0", "operFee": "0", "tradeTypeCode": "120", "cancelTag": "0", "changeuserDate": "", "tradeTagSet": "10100000000000000000", "xTransCode": "TCS_ChangeServiceReg", "basicCreditValue": "0", "xLastResultcode": "0", "updateTime": "", "tradeCityCode": "MQ00", "custType": "个人客户", "netTypeCode": "10", "custName": "刘娜", "developDepartId": "42335", "firstCallTime": "", "inDepartId": "42335", "leaveRealFee": "0", "tradeStaffId": "YCZY0451", "openStaffId": "YCHZ3333", "processTagSet": " ", "xResultcode": "0", "advancePay": "0", "acceptDate": "2018-09-15 14:07:59", "destroyTime": "", "tradeJudgeOweTag": "0", "contactName": "", "idType": "1", "preDestroyTime": "", "creditValue": "0", "contactPhone": "", "psptId": "身份证:140224199812181227", "xTag": "1", "contactPostCode": "", "contractId": "", "acceptMonth": "9", "assureDate": "", "userId": "1118091342317072", "developEparchyCode": "0359", "startAcycId": "194910", "xLcuTxdservCount": "0", "eparchyCode": "0359", "contact": "", "developNo": "", "developCityCode": "MQ00", "removeDepartId": "", "productTypeCode": "4444", "inDate": "2018-09-13 18:40:28", "mputeDate": "2018-09-13 19:01:20", "assureTypeCode": "", "subscribeId": "1118091527923131", "tradeType": "产品/服务变更", "actorName": ""}
    # CASH=50.00
    # SEND_TYPE=0
    # TRADE_ID=1118091527923131