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
        self.user_name = 'YCJTZY15'
        self.password = 'LL1515!!'
        self.brow.get(self.url)

        self.path = r'D:\Desktop\业务_shifan.xlsx'
        self.record = r'D:\Desktop\业务_shifan_record.xlsx'

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

        user_id = self.brow.find_element_by_xpath('//input[@id="USER_ID_HIDEN"]').get_attribute('value')
        user_name = self.brow.find_element_by_xpath('//input[@id="CUST_NAME"]').get_attribute('value')
        trade_base = self.brow.find_element_by_xpath('//input[@id="_tradeBase"]').get_attribute('value')
        # print(trade_base)
        self.continue_submit(user_id, trade_base, product_ot, user_name,number)

    def continue_submit(self, user_id, trade_base, product_ot,name, number):
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        data = {
            'Base': trade_base,
            'Ext': '{"Common": {"ACTOR_NAME": "", "ACTOR_PHONE": "", "ACTOR_CERTTYPEID": "", "ACTOR_CERTNUM": "", "REMARK": ""}, "TF_B_TRADE_DISCNT": {"ITEM": [{"ID": "' + user_id + '", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001024", "DISCNT_CODE": "99051112", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "2018-10-01 00:00:00", "END_DATE": "2019-09-30 23:59:59", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""}, {"ID": "' + user_id + '", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001025", "DISCNT_CODE": "19102407", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "' + time_now + '", "END_DATE": "2050-01-01 00:00:00", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""}, {"ID": "' + user_id + '", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001025", "DISCNT_CODE": "19102923", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "' + time_now + '", "END_DATE": "2050-01-01 00:00:00", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""}, {"ID": "' + user_id + '", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001026", "DISCNT_CODE": "19103204", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "' + time_now + '", "END_DATE": "2050-12-31 00:00:00", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""}]}, "TF_B_TRADE_OTHER": {"ITEM": [{"RSRV_VALUE_CODE": "NEXP", "RSRV_VALUE": "' + user_id + '", "RSRV_STR1": "20104142", "RSRV_STR2": "00", "RSRV_STR3": "19001094", "RSRV_STR4": "4444", "RSRV_STR5": "undefined", "RSRV_STR6": "-1", "RSRV_STR7": "0", "RSRV_STR8": "", "RSRV_STR9": "4G02", "RSRV_STR10": "' + number + '", "MODIFY_TAG": "1", "START_DATE": "' + product_ot + '", "END_DATE": "' + time_now + '", "X_DATATYPE": "NULL"}, {"RSRV_VALUE_CODE": "DLPK", "RSRV_VALUE": "' + user_id + '", "RSRV_STR1": "20104142", "RSRV_STR2": "00", "RSRV_STR3": "19001094", "X_DATATYPE": "NULL"}]}, "TF_B_TRADE_USER": {"ITEM": {"PRODUCT_ID": "20104142", "BRAND_CODE": "4G02", "USER_ID": "' + user_id + '", "NET_TYPE_CODE": "10"}}, "TF_B_TRADE": {"PRODUCT_ID": "20104142", "BRAND_CODE": "4G02", "EXEC_TIME": "' + time_now + '"}, "TRADE_SUB_ITEM": {}, "MANYOU_TEMP": {"ITEM": {"ManYouCreditTag": false}}, "TRADE_ITEM": {"DEVELOP_SUB_TYPE": "", "DEVELOP_STAFF_ID": "", "IS_TELEKET": "0", "TELEKET_TYPE": "", "DEVELOP_DEPART_ID": ""}}',
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
            'Cookie': '__guid=221721176.840067343969089200.1536318815165.4204; LOGIN_SUBSYS_CODEBSS=CRM; LOGIN_STAFF_IDBSS=YCJTZY15; BSS_BSS_STATSERV_JSESSIONID=lJLRbcHJFzN4lMQypqbGv23vvTJ1Pqg2Nw5DT3LWrnk18rlshy5g!105771892!1549156998; BSS_BSS_JSESSIONID=GyMGbcHJnj2LtpHTFjXynhnlmgzwJ1TTQ1GSHxySBtv4NQsQJ8ms!1551878969!-1702348738; BSS_RESMANM_JSESSIONID=7q27bcHJtVHLNJZvkJQL4hmCpJCdmWRC43CWbnhwMhhWDM3TjjLJ!1672713234!1101795391; BSS_SYSMANM_JSESSIONID=k9phbcHJMYTgS8Pkhp3s3HwZphyJqyl998tMxyypt3QpJQGkLppk!-269914159!-1433269564; BSS_BSS_SALEMANM_JSESSIONID=VtQNbcHJgT61W7vJjfm3c7WQ8X5cJ6TsGnJKsngzGfby87sJTCps!159647921!2061263565; BSS_BSS_ACCTMANM_JSESSIONID=TvRqbcHJCL2d7mwbvSLpQ85KDKjQXcz1RvmPpNGqtGsflQJTyyBy!-1652137237!626944312; BSS_CHNLMANM_JSESSIONID=TByzbcHJMT46qKPwnvbBWfdFNR2yV4c7QmGYGbCf79tvWTSVJnGQ!112363500!-798000933; BSS_BSS_CUSTMANM_JSESSIONID=RdvxbcHJ6f3G8Y0GzHLGvp34d1hShLy2vT3YfJVzymhDKp0W1c8F!-1850198033!-2050571229; BSS_BSS_CUSTSERV_JSESSIONID=KGNsbcHSqdgKnVnnl8BKJwSr3vn1hQDqtPyZmYG9w1GyLQ7n3d1q!2104451838!-782718536'
        }

        rs = requests.post(
            url='http://133.128.6.186:8080/custserv?service=swallow/personalserv.changeelement.ChangeElement/submitMobTrade/1',
            data=data, headers=headers)

        str_1 = rs.content.decode('gbk')
        # print(str_1)
        trade_id = re.findall("tradeId='(\d+)'", str_1)[0]
        subscribe_id = re.findall("subscribeId='(\d+)'", str_1)[0]
        startDate = re.findall("START_DATE&gt;(.+)&lt;/START_DATE&gt;", str_1)[0]
        inDepart = re.findall('inDepartId="(.+)" leaveRealFee', str_1)[0]
        developDepartId = re.findall('developDepartId="(.+)" firstCallTime', str_1)[0]
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
            tradeMain = '[{"TRADE_ID": "'+trade_id+'", "TRADE_TYPE": "产品/服务变更", "SERIAL_NUMBER": "'+number+'", "TRADE_FEE": "50.00", "CUST_NAME": "'+name+'", "CUST_ID": "'+cust_id+'", "USER_ID": "'+user_id+'", "ACCT_ID": "'+acct_id+'", "NET_TYPE_CODE": "10", "TRADE_TYPE_CODE": "120", "PSPT_TYPE_CODE": "0"}]'
            fees = '[{"X_TAG": "1", "TRADE_ID": "'+trade_id+'", "CALCULATE_ID": "", "FEE_MODE": "2", "FEEITEM_CODE": "100005", "OLDFEE": "50.00", "FEE": "50.00", "DERATE_REMARK": "", "PAY_MONEY_CODE": "0", "PAY_TAG": "0", "CALCULATE_TAG": "N", "MODIFY_TAG": "", "TRADE_TYPE_CODE": "120", "NET_TYPE_CODE": "10", "FEEITEM_NAME": "[预存]营业厅收入(营业缴费)_普通预存款(不可清退))"}]'
            feePayMoney = '[{"TRADE_ID": "'+trade_id+'", "PAY_MONEY_CODE": "0", "MONEY": 5000}]'
            base = json.dumps({"xCodingStr1": "1</MODIFY_TAG><RSRV_STR3>19001094</RSRV_STR3><RSRV_STR6>-1</RSRV_STR6><END_DATE>"+time_now+"</END_DATE><RSRV_STR5>undefined</RSRV_STR5><RSRV_STR8/><X_DATATYPE>NULL</X_DATATYPE><RSRV_STR7>0</RSRV_STR7><RSRV_STR9>4G02</RSRV_STR9><RSRV_STR10>"+number+"</RSRV_STR10><START_DATE>"+startDate+"</START_DATE><RSRV_VALUE>"+user_id+"</RSRV_VALUE><RSRV_VALUE_CODE>NEXP</RSRV_VALUE_CODE></ITEM><ITEM><RSRV_STR2>00</RSRV_STR2><RSRV_STR1>20104142</RSRV_STR1><RSRV_VALUE>"+user_id+"</RSRV_VALUE><RSRV_VALUE_CODE>DLPK</RSRV_VALUE_CODE><RSRV_STR3>19001094</RSRV_STR3><X_DATATYPE>NULL</X_DATATYPE></ITEM></TF_B_TRADE_OTHER></Ext></ROOT>", "xCodingStr2": "", "xCheckTag": "1", "creditClass": "-1", "usecustId": ""+cust_id+"", "routeEparchy": "运城", "acctTag": "0", "remark": "", "feeState": "", "developDate": ""+developDate+"", "scoreValue": "0", "execTime": ""+execTime+"", "termIp": ""+ip+"", "xCodingStr9": "", "openDate": ""+openDate+"", "userTypeCode": "0", "xCodingStr8": "", "xCodingStr7": "", "xCodingStr6": "", "tradeId": ""+trade_id+"", "receiptInfo2": "担保人姓名:    担保类型:    担保人联系电话: 担保人证件类型:担保人证件类型\n担保人证件号码: ~代理人姓名:   代理人联系电话: 代理人证件类型:   代理人证件号码: ", "provinceCode": "SXCU", "xCodingStr5": "", "receiptInfo1": "                                                   "+name+"~~\n                                                   "+number+"                                                                 "+pspt_id+"~~\n                                                   个人                                                                   \n                                                   "+phone+"~~", "tradeDepartId": ""+tradeDepartId+"", "receiptInfo4": "", "xCodingStr4": "", "xCodingStr3": "", "receiptInfo3": "认证方式: \n~新增优惠:1元/月,拨打本地网联通免费~   生效时间:2018-09-15~0元500分钟本地拨打长市合一分钟数~   生效时间:2018-09-15~10元国内流量不限量包,100G后限速为1Mbps(立即生效)~   生效时间:2018-09-15~存50送180元话费，预存款一次性到账，赠款次月分12个月返还~   生效时间:2018-10-01~~取消优惠:校园小区(运城)-0元校区流量不限量包15GB后限速3Mbps~  生效时间: 2018-09-05  失效时间: 2018-09-30 ~新增服务: ~取消服务: ~新增SP: ~取消SP: \n~提醒:初次使用时请修改密码.~~~月套餐国内（不含台港澳）流量当月不清零，剩余流量自动结转至下月，有效期至下月月底。套餐内其他业务量以及定向流量叠加包、后向流量产品、赠送流量等仅限当月使用，不能延续至下月使用。~ ~~ ~当月套餐及叠加流量包以外的流量计费达到600元后，国内（不含台港澳）流量不再收费，达到15GB后系统自动关闭数据网络，次月自动打开。用户主动申请，当月打开；当月国际及港澳台漫游和套餐内、套餐外、各种收费、免费、各类定向等数据流量总和达到100GB后系统自动关闭数据网络，当月不再开放，次月自动开\n", "xCodingStr12": "", "receiptInfo7": "", "xCodingStr13": "", "receiptInfo5": "~ ~ ~认证方式: ~ ~手机串号:~ ~", "xCodingStr14": "", "receiptInfo6": "", "xCodingStr15": "", "mputeMonthFee": "1", "openDepartId": "M0959", "xCodingStr10": "", "removeReasonCode": "", "xCodingStr11": "", "tradeEparchyCode": "0359", "xCodingStr16": "", "xCodingStr17": "", "xCodingStr18": "", "xCodingStr19": "", "removeEparchyCode": "", "feeTime": "", "creditRuleId": "-1", "feeStaffId": "", "checkTypeCode": "", "brandCode": "4G02", "tradeStatus": "query", "prepayTag": "0", "dealType": "1", "inModeCode": "0", "productId": "20104142", "serialNumber": ""+number+"", "userStateCodeset": "0", "actorCertnum": ":", "removeCityCode": "", "itemId": ""+item_id+"", "userPasswd": ""+userPasswd+"", "routeEparchyCode": "0359", "contactAddress": "", "assureCustId": "", "strisneedprint": "1", "checkResult": "0000", "custId": ""+cust_id+"", "acctId": ""+acct_id+"", "xLcuLogstep": "32", "xCodingStr": "", "xCheckInfo": "SpPt00102000110370特殊限制判断:用户在本次业务中:<br><br>新增优惠：【1元/月,拨打本地网联通免费】，【0元500分钟本地拨打长市合一分钟数】，【10元国内流量不限量包,100G后限速为1Mbps(立即生效)】，【存50送180元话费，预存款一次性到账，赠款次月分12个月返还】<br>删除优惠：【校园小区(运城)-0元校区流量不限量包15GB后限速3Mbps】<br><b><font color :'red'></font></b><br>请提醒用户查看免填单中变更的信息", "endAcycId": "203701", "actorCerttypeid": "", "actorPhone": "", "xRecordnum": "1", "xSelcount": "0", "cityCode": "MQ00", "detailInstallAddress": "", "inStaffId": ""+instaff_id+"", "invoiceNo": "", "inNetMode": "0", "priority": "320", "developStaffId": ""+develop_staff+"", "userType": "普通用户", "attrTypeCode": "0", "lastStopTime": "", "tradeAttr": "1", "openMode": "0", "tradeLcuName": "TCS_ChangeServiceReg", "userDiffCode": "00", "xLastResultinfo": "", "tradeInfoTagSet": "111111    ", "nextDealTag": "Z", "xResultinfo": "", "olcomTag": "0", "removeTag": "0", "partitionId": "2623", "foregift": "0", "contactPostAddr": "", "id": ""+user_id+"", "rightCode": "csChangeServiceTrade", "chkTag": "0", "fee": "0", "operFee": "0", "tradeTypeCode": "120", "cancelTag": "0", "changeuserDate": "", "tradeTagSet": "10100000000000000000", "xTransCode": "TCS_ChangeServiceReg", "basicCreditValue": "0", "xLastResultcode": "0", "updateTime": "", "tradeCityCode": "MQ00", "custType": "个人客户", "netTypeCode": "10", "custName": ""+name+"", "developDepartId": ""+developDepartId+"", "firstCallTime": "", "inDepartId": ""+inDepart+"", "leaveRealFee": "0", "tradeStaffId": ""+tradestaff_id+"", "openStaffId": ""+openstaff_id+"", "processTagSet": " ", "xResultcode": "0", "advancePay": "0", "acceptDate": ""+acceptDate+"", "destroyTime": "", "tradeJudgeOweTag": "0", "contactName": "", "idType": "1", "preDestroyTime": "", "creditValue": "0", "contactPhone": "", "psptId": "身份证:"+pspt_id+"", "xTag": "1", "contactPostCode": "", "contractId": "", "acceptMonth": "9", "assureDate": "", "userId": ""+user_id+"", "developEparchyCode": "0359", "startAcycId": "194910", "xLcuTxdservCount": "0", "eparchyCode": "0359", "contact": "", "developNo": "", "developCityCode": "MQ00", "removeDepartId": "", "productTypeCode": "4444", "inDate": ""+inDate+"", "mputeDate": ""+mputeDate+"", "assureTypeCode": "", "subscribeId": ""+subscribe_id+"", "tradeType": "产品/服务变更", "actorName": ""})
            data = {
                'cancelTag':'false',
                'funcType':'0',
                'dataType':'0',
                'tradeMain':tradeMain.encode('gbk'),
                'fees':fees.encode('gbk'),
                'unChargedfees':'[]',
                'feePayMoney':feePayMoney,
                'feeCheck':'[]',
                'PSPT_TYPE_CODE_BAK':'0',
                'ALL_OLD_FEE':'50.00',
                'ALL_FEE':'50.00',
                'DERATE_STAFF_ID':tradestaff_id,
                'NEW_PAYTAG':'C',
                'CONTINUE_MODE':'0',
                'isNotTax':'0',
                'base': base,
                'CASH':'50.00',
                'SEND_TYPE':'0',
                'TRADE_ID':trade_id
            }

            url = 'http://133.128.6.186:8080/custserv?service=swallow/personalserv.dealtradefee.DealTradeFee/continueTradeReg/1'
            rs = requests.post(url=url,data=data,headers=headers)

            if 'chargeOK' in rs.content.decode('utf-8'):
                print('成功')
                write(self.name, self.id, self.number, '成功', self.record)

    def run(self):
        self.login()
        self.into_frame()
        for content in read_xlsx(self.path, sheet_index=0, start_row=0):
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

'''
HTTP/1.1 200 OK
Date: Sat, 15 Sep 2018 08:38:11 GMT
Content-Type: text/xml
X-Powered-By: Servlet/2.5 JSP/2.1
X-Powered-By: Servlet/2.5 JSP/2.1
Vary: Accept-Encoding
Content-Length: 10893

<?xml version="1.0" encoding="UTF-8"?><root><message></message><TradeSubmitOk tradeId='1118091527945278' subscribeId='1118091527945278'><Fee feenum='1'></Fee><checkAfterData><data checkType="1" checkData="&#29305;&#27530;&#38480;&#21046;&#21028;&#26029;:&#29992;&#25143;&#22312;&#26412;&#27425;&#19994;&#21153;&#20013;:&lt;br&gt;&lt;br&gt;&#26032;&#22686;&#20248;&#24800;&#65306;&#12304;1&#20803;/&#26376;,&#25320;&#25171;&#26412;&#22320;&#32593;&#32852;&#36890;&#20813;&#36153;&#12305;&#65292;&#12304;0&#20803;500&#20998;&#38047;&#26412;&#22320;&#25320;&#25171;&#38271;&#24066;&#21512;&#19968;&#20998;&#38047;&#25968;&#12305;&#65292;&#12304;10&#20803;&#22269;&#20869;&#27969;&#37327;&#19981;&#38480;&#37327;&#21253;,100G&#21518;&#38480;&#36895;&#20026;1Mbps(&#31435;&#21363;&#29983;&#25928;)&#12305;&#65292;&#12304;&#23384;50&#36865;180&#20803;&#35805;&#36153;&#65292;&#39044;&#23384;&#27454;&#19968;&#27425;&#24615;&#21040;&#36134;&#65292;&#36192;&#27454;&#27425;&#26376;&#20998;12&#20010;&#26376;&#36820;&#36824;&#12305;&lt;br&gt;&#21024;&#38500;&#20248;&#24800;&#65306;&#12304;&#26657;&#22253;&#23567;&#21306;(&#36816;&#22478;)-0&#20803;&#26657;&#21306;&#27969;&#37327;&#19981;&#38480;&#37327;&#21253;15GB&#21518;&#38480;&#36895;3Mbps&#12305;&lt;br&gt;&lt;b&gt;&lt;font color ='red'&gt;&lt;/font&gt;&lt;/b&gt;&lt;br&gt;&#35831;&#25552;&#37266;&#29992;&#25143;&#26597;&#30475;&#20813;&#22635;&#21333;&#20013;&#21464;&#26356;&#30340;&#20449;&#24687;"/></checkAfterData><TradeData xCodingStr1="1&lt;/MODIFY_TAG&gt;&lt;RSRV_STR3&gt;19001094&lt;/RSRV_STR3&gt;&lt;RSRV_STR6&gt;-1&lt;/RSRV_STR6&gt;&lt;END_DATE&gt;2018-09-15 16:38:12&lt;/END_DATE&gt;&lt;RSRV_STR5&gt;undefined&lt;/RSRV_STR5&gt;&lt;RSRV_STR8/&gt;&lt;X_DATATYPE&gt;NULL&lt;/X_DATATYPE&gt;&lt;RSRV_STR7&gt;0&lt;/RSRV_STR7&gt;&lt;RSRV_STR9&gt;4G02&lt;/RSRV_STR9&gt;&lt;RSRV_STR10&gt;18534315009&lt;/RSRV_STR10&gt;&lt;START_DATE&gt;2018-09-06 15:56:54&lt;/START_DATE&gt;&lt;RSRV_VALUE&gt;1118090642282865&lt;/RSRV_VALUE&gt;&lt;RSRV_VALUE_CODE&gt;NEXP&lt;/RSRV_VALUE_CODE&gt;&lt;/ITEM&gt;&lt;ITEM&gt;&lt;RSRV_STR2&gt;00&lt;/RSRV_STR2&gt;&lt;RSRV_STR1&gt;20104142&lt;/RSRV_STR1&gt;&lt;RSRV_VALUE&gt;1118090642282865&lt;/RSRV_VALUE&gt;&lt;RSRV_VALUE_CODE&gt;DLPK&lt;/RSRV_VALUE_CODE&gt;&lt;RSRV_STR3&gt;19001094&lt;/RSRV_STR3&gt;&lt;X_DATATYPE&gt;NULL&lt;/X_DATATYPE&gt;&lt;/ITEM&gt;&lt;/TF_B_TRADE_OTHER&gt;&lt;/Ext&gt;&lt;/ROOT&gt;" xCodingStr2="" xCheckTag="1" creditClass="-1" usecustId="1118090527825956" routeEparchy="&#36816;&#22478;" acctTag="0" remark="" feeState="" developDate="2018-09-06 15:57:37" scoreValue="0" execTime="2018-09-15 16:38:11" termIp="133.150.40.81" xCodingStr9="" openDate="2018-09-12 07:59:42" userTypeCode="0" xCodingStr8="" xCodingStr7="" xCodingStr6="" tradeId="1118091527945278" receiptInfo2="&#25285;&#20445;&#20154;&#22995;&#21517;:    &#25285;&#20445;&#31867;&#22411;:    &#25285;&#20445;&#20154;&#32852;&#31995;&#30005;&#35805;: &#25285;&#20445;&#20154;&#35777;&#20214;&#31867;&#22411;:&#25285;&#20445;&#20154;&#35777;&#20214;&#31867;&#22411;
&#25285;&#20445;&#20154;&#35777;&#20214;&#21495;&#30721;: ~&#20195;&#29702;&#20154;&#22995;&#21517;:   &#20195;&#29702;&#20154;&#32852;&#31995;&#30005;&#35805;: &#20195;&#29702;&#20154;&#35777;&#20214;&#31867;&#22411;:   &#20195;&#29702;&#20154;&#35777;&#20214;&#21495;&#30721;: " provinceCode="SXCU" xCodingStr5="" receiptInfo1="                                                   &#29579;&#38177;&#23071;~~
                                                   18534315009                                                                 622821199911190022~~
                                                   &#20010;&#20154;                                                                   
                                                   18603595441~~" tradeDepartId="M0959" receiptInfo4="" xCodingStr4="" xCodingStr3="" receiptInfo3="&#35748;&#35777;&#26041;&#24335;: 
~&#26032;&#22686;&#20248;&#24800;:1&#20803;/&#26376;,&#25320;&#25171;&#26412;&#22320;&#32593;&#32852;&#36890;&#20813;&#36153;~   &#29983;&#25928;&#26102;&#38388;:2018-09-15~0&#20803;500&#20998;&#38047;&#26412;&#22320;&#25320;&#25171;&#38271;&#24066;&#21512;&#19968;&#20998;&#38047;&#25968;~   &#29983;&#25928;&#26102;&#38388;:2018-09-15~10&#20803;&#22269;&#20869;&#27969;&#37327;&#19981;&#38480;&#37327;&#21253;,100G&#21518;&#38480;&#36895;&#20026;1Mbps(&#31435;&#21363;&#29983;&#25928;)~   &#29983;&#25928;&#26102;&#38388;:2018-09-15~&#23384;50&#36865;180&#20803;&#35805;&#36153;&#65292;&#39044;&#23384;&#27454;&#19968;&#27425;&#24615;&#21040;&#36134;&#65292;&#36192;&#27454;&#27425;&#26376;&#20998;12&#20010;&#26376;&#36820;&#36824;~   &#29983;&#25928;&#26102;&#38388;:2018-10-01~~&#21462;&#28040;&#20248;&#24800;:&#26657;&#22253;&#23567;&#21306;(&#36816;&#22478;)-0&#20803;&#26657;&#21306;&#27969;&#37327;&#19981;&#38480;&#37327;&#21253;15GB&#21518;&#38480;&#36895;3Mbps~  &#29983;&#25928;&#26102;&#38388;: 2018-09-06  &#22833;&#25928;&#26102;&#38388;: 2018-09-30 ~&#26032;&#22686;&#26381;&#21153;: ~&#21462;&#28040;&#26381;&#21153;: ~&#26032;&#22686;SP: ~&#21462;&#28040;SP: 
~&#25552;&#37266;:&#21021;&#27425;&#20351;&#29992;&#26102;&#35831;&#20462;&#25913;&#23494;&#30721;.~~~&#26376;&#22871;&#39184;&#22269;&#20869;&#65288;&#19981;&#21547;&#21488;&#28207;&#28595;&#65289;&#27969;&#37327;&#24403;&#26376;&#19981;&#28165;&#38646;&#65292;&#21097;&#20313;&#27969;&#37327;&#33258;&#21160;&#32467;&#36716;&#33267;&#19979;&#26376;&#65292;&#26377;&#25928;&#26399;&#33267;&#19979;&#26376;&#26376;&#24213;&#12290;&#22871;&#39184;&#20869;&#20854;&#20182;&#19994;&#21153;&#37327;&#20197;&#21450;&#23450;&#21521;&#27969;&#37327;&#21472;&#21152;&#21253;&#12289;&#21518;&#21521;&#27969;&#37327;&#20135;&#21697;&#12289;&#36192;&#36865;&#27969;&#37327;&#31561;&#20165;&#38480;&#24403;&#26376;&#20351;&#29992;&#65292;&#19981;&#33021;&#24310;&#32493;&#33267;&#19979;&#26376;&#20351;&#29992;&#12290;~ ~~ ~&#24403;&#26376;&#22871;&#39184;&#21450;&#21472;&#21152;&#27969;&#37327;&#21253;&#20197;&#22806;&#30340;&#27969;&#37327;&#35745;&#36153;&#36798;&#21040;600&#20803;&#21518;&#65292;&#22269;&#20869;&#65288;&#19981;&#21547;&#21488;&#28207;&#28595;&#65289;&#27969;&#37327;&#19981;&#20877;&#25910;&#36153;&#65292;&#36798;&#21040;15GB&#21518;&#31995;&#32479;&#33258;&#21160;&#20851;&#38381;&#25968;&#25454;&#32593;&#32476;&#65292;&#27425;&#26376;&#33258;&#21160;&#25171;&#24320;&#12290;&#29992;&#25143;&#20027;&#21160;&#30003;&#35831;&#65292;&#24403;&#26376;&#25171;&#24320;&#65307;&#24403;&#26376;&#22269;&#38469;&#21450;&#28207;&#28595;&#21488;&#28459;&#28216;&#21644;&#22871;&#39184;&#20869;&#12289;&#22871;&#39184;&#22806;&#12289;&#21508;&#31181;&#25910;&#36153;&#12289;&#20813;&#36153;&#12289;&#21508;&#31867;&#23450;&#21521;&#31561;&#25968;&#25454;&#27969;&#37327;&#24635;&#21644;&#36798;&#21040;100GB&#21518;&#31995;&#32479;&#33258;&#21160;&#20851;&#38381;&#25968;&#25454;&#32593;&#32476;&#65292;&#24403;&#26376;&#19981;&#20877;&#24320;&#25918;&#65292;&#27425;&#26376;&#33258;&#21160;&#24320;
" xCodingStr12="" receiptInfo7="" xCodingStr13="" receiptInfo5="~ ~ ~&#35748;&#35777;&#26041;&#24335;: ~ ~&#25163;&#26426;&#20018;&#21495;:~ ~" xCodingStr14="" receiptInfo6="" xCodingStr15="" mputeMonthFee="1" openDepartId="0CC7B" xCodingStr10="" removeReasonCode="" xCodingStr11="" tradeEparchyCode="0359" xCodingStr16="" xCodingStr17="" xCodingStr18="" xCodingStr19="" removeEparchyCode="" feeTime="" creditRuleId="-1" feeStaffId="" checkTypeCode="" brandCode="4G02" tradeStatus="query" prepayTag="0" dealType="1" inModeCode="0" productId="20104142" serialNumber="18534315009" userStateCodeset="0" actorCertnum=":" removeCityCode="" itemId="1118090642282865" userPasswd="IKKwcM" routeEparchyCode="0359" contactAddress="" assureCustId="" strisneedprint="1" checkResult="0000" custId="1118090527825956" acctId="1118090637429437" xLcuLogstep="32" xCodingStr="" xCheckInfo="SpPt00102000110370&#29305;&#27530;&#38480;&#21046;&#21028;&#26029;:&#29992;&#25143;&#22312;&#26412;&#27425;&#19994;&#21153;&#20013;:&lt;br&gt;&lt;br&gt;&#26032;&#22686;&#20248;&#24800;&#65306;&#12304;1&#20803;/&#26376;,&#25320;&#25171;&#26412;&#22320;&#32593;&#32852;&#36890;&#20813;&#36153;&#12305;&#65292;&#12304;0&#20803;500&#20998;&#38047;&#26412;&#22320;&#25320;&#25171;&#38271;&#24066;&#21512;&#19968;&#20998;&#38047;&#25968;&#12305;&#65292;&#12304;10&#20803;&#22269;&#20869;&#27969;&#37327;&#19981;&#38480;&#37327;&#21253;,100G&#21518;&#38480;&#36895;&#20026;1Mbps(&#31435;&#21363;&#29983;&#25928;)&#12305;&#65292;&#12304;&#23384;50&#36865;180&#20803;&#35805;&#36153;&#65292;&#39044;&#23384;&#27454;&#19968;&#27425;&#24615;&#21040;&#36134;&#65292;&#36192;&#27454;&#27425;&#26376;&#20998;12&#20010;&#26376;&#36820;&#36824;&#12305;&lt;br&gt;&#21024;&#38500;&#20248;&#24800;&#65306;&#12304;&#26657;&#22253;&#23567;&#21306;(&#36816;&#22478;)-0&#20803;&#26657;&#21306;&#27969;&#37327;&#19981;&#38480;&#37327;&#21253;15GB&#21518;&#38480;&#36895;3Mbps&#12305;&lt;br&gt;&lt;b&gt;&lt;font color ='red'&gt;&lt;/font&gt;&lt;/b&gt;&lt;br&gt;&#35831;&#25552;&#37266;&#29992;&#25143;&#26597;&#30475;&#20813;&#22635;&#21333;&#20013;&#21464;&#26356;&#30340;&#20449;&#24687;" endAcycId="203701" actorCerttypeid="" actorPhone="" xRecordnum="1" xSelcount="0" cityCode="MQ00" detailInstallAddress="" inStaffId="YCCB0591" invoiceNo="" inNetMode="0" priority="320" developStaffId="YCCB0591" userType="&#26222;&#36890;&#29992;&#25143;" attrTypeCode="0" lastStopTime="" tradeAttr="1" openMode="0" tradeLcuName="TCS_ChangeServiceReg" userDiffCode="00" xLastResultinfo="" tradeInfoTagSet="111111    " nextDealTag="Z" xResultinfo="" olcomTag="0" removeTag="0" partitionId="2865" foregift="0" contactPostAddr="" id="1118090642282865" rightCode="csChangeServiceTrade" chkTag="0" fee="0" operFee="0" tradeTypeCode="120" cancelTag="0" changeuserDate="" tradeTagSet="10100000000000000000" xTransCode="TCS_ChangeServiceReg" basicCreditValue="0" xLastResultcode="0" updateTime="" tradeCityCode="MQ00" custType="&#20010;&#20154;&#23458;&#25143;" netTypeCode="10" custName="&#29579;&#38177;&#23071;" developDepartId="0CC7B" firstCallTime="" inDepartId="0CC7B" leaveRealFee="0" tradeStaffId="YCJTZY15" openStaffId="YCCB0591" processTagSet=" " xResultcode="0" advancePay="0" acceptDate="2018-09-15 16:38:11" destroyTime="" tradeJudgeOweTag="0" contactName="" idType="1" preDestroyTime="" creditValue="0" contactPhone="" psptId="&#36523;&#20221;&#35777;:622821199911190022" xTag="1" contactPostCode="" contractId="" acceptMonth="9" assureDate="" userId="1118090642282865" developEparchyCode="0359" startAcycId="194910" xLcuTxdservCount="0" eparchyCode="0359" contact="" developNo="" developCityCode="MQ00" removeDepartId="" productTypeCode="4444" inDate="2018-09-06 15:57:37" mputeDate="2018-09-12 07:59:43" assureTypeCode="" subscribeId="1118091527945278" tradeType="&#20135;&#21697;/&#26381;&#21153;&#21464;&#26356;" actorName=""/></TradeSubmitOk></root>
'''

'''
cancelTag=false&
funcType=0&dataType=0&tradeMain=%5B%7B%22TRADE_ID%22%3A%20%221118091527943915%22%2C%20%22TRADE_TYPE%22%3A%20%22%E4%BA%A7%E5%93%81%2F%E6%9C%8D%E5%8A%A1%E5%8F%98%E6%9B%B4%22%2C%20%22SERIAL_NUMBER%22%3A%20%2218534315008%22%2C%20%22TRADE_FEE%22%3A%20%2250.00%22%2C%20%22CUST_NAME%22%3A%20%22%E8%8C%83%E6%96%87%E6%85%A7%22%2C%20%22CUST_ID%22%3A%20%221118090527825955%22%2C%20%22USER_ID%22%3A%20%221118090642282848%22%2C%20%22ACCT_ID%22%3A%20%221118090637429416%22%2C%20%22NET_TYPE_CODE%22%3A%20%2210%22%2C%20%22TRADE_TYPE_CODE%22%3A%20%22120%22%2C%20%22PSPT_TYPE_CODE%22%3A%20%220%22%7D%5D&fees=%5B%7B%22X_TAG%22%3A%20%221%22%2C%20%22TRADE_ID%22%3A%20%221118091527943915%22%2C%20%22CALCULATE_ID%22%3A%20%22%22%2C%20%22FEE_MODE%22%3A%20%222%22%2C%20%22FEEITEM_CODE%22%3A%20%22100005%22%2C%20%22OLDFEE%22%3A%20%2250.00%22%2C%20%22FEE%22%3A%20%2250.00%22%2C%20%22DERATE_REMARK%22%3A%20%22%22%2C%20%22PAY_MONEY_CODE%22%3A%20%220%22%2C%20%22PAY_TAG%22%3A%20%220%22%2C%20%22CALCULATE_TAG%22%3A%20%22N%22%2C%20%22MODIFY_TAG%22%3A%20%22%22%2C%20%22TRADE_TYPE_CODE%22%3A%20%22120%22%2C%20%22NET_TYPE_CODE%22%3A%20%2210%22%2C%20%22FEEITEM_NAME%22%3A%20%22%5B%E9%A2%84%E5%AD%98%5D%E8%90%A5%E4%B8%9A%E5%8E%85%E6%94%B6%E5%85%A5(%E8%90%A5%E4%B8%9A%E7%BC%B4%E8%B4%B9)_%E6%99%AE%E9%80%9A%E9%A2%84%E5%AD%98%E6%AC%BE(%E4%B8%8D%E5%8F%AF%E6%B8%85%E9%80%80))%22%7D%5D&unChargedfees=%5B%5D&feePayMoney=%5B%7B%22TRADE_ID%22%3A%20%221118091527943915%22%2C%20%22PAY_MONEY_CODE%22%3A%20%220%22%2C%20%22MONEY%22%3A%205000%7D%5D&feeCheck=%5B%5D&PSPT_TYPE_CODE_BAK=0&ALL_OLD_FEE=50.00&ALL_FEE=50.00&DERATE_STAFF_ID=YCJTZY15&NEW_PAYTAG=C&CONTINUE_MODE=0&isNotTax=0&base=%7B%22xCodingStr1%22%3A%20%221%3C%2FMODIFY_TAG%3E%3CRSRV_STR3%3E19001094%3C%2FRSRV_STR3%3E%3CRSRV_STR6%3E-1%3C%2FRSRV_STR6%3E%3CEND_DATE%3E2018-09-15%2016%3A29%3A33%3C%2FEND_DATE%3E%3CRSRV_STR5%3Eundefined%3C%2FRSRV_STR5%3E%3CRSRV_STR8%2F%3E%3CX_DATATYPE%3ENULL%3C%2FX_DATATYPE%3E%3CRSRV_STR7%3E0%3C%2FRSRV_STR7%3E%3CRSRV_STR9%3E4G02%3C%2FRSRV_STR9%3E%3CRSRV_STR10%3E18534315008%3C%2FRSRV_STR10%3E%3CSTART_DATE%3E2018-09-06%2015%3A55%3A19%3C%2FSTART_DATE%3E%3CRSRV_VALUE%3E1118090642282848%3C%2FRSRV_VALUE%3E%3CRSRV_VALUE_CODE%3ENEXP%3C%2FRSRV_VALUE_CODE%3E%3C%2FITEM%3E%3CITEM%3E%3CRSRV_STR2%3E00%3C%2FRSRV_STR2%3E%3CRSRV_STR1%3E20104142%3C%2FRSRV_STR1%3E%3CRSRV_VALUE%3E1118090642282848%3C%2FRSRV_VALUE%3E%3CRSRV_VALUE_CODE%3EDLPK%3C%2FRSRV_VALUE_CODE%3E%3CRSRV_STR3%3E19001094%3C%2FRSRV_STR3%3E%3CX_DATATYPE%3ENULL%3C%2FX_DATATYPE%3E%3C%2FITEM%3E%3C%2FTF_B_TRADE_OTHER%3E%3C%2FExt%3E%3C%2FROOT%3E%22%2C%20%22xCodingStr2%22%3A%20%22%22%2C%20%22xCheckTag%22%3A%20%221%22%2C%20%22creditClass%22%3A%20%22-1%22%2C%20%22usecustId%22%3A%20%221118090527825955%22%2C%20%22routeEparchy%22%3A%20%22%E8%BF%90%E5%9F%8E%22%2C%20%22acctTag%22%3A%20%220%22%2C%20%22remark%22%3A%20%22%22%2C%20%22feeState%22%3A%20%22%22%2C%20%22developDate%22%3A%20%222018-09-06%2015%3A56%3A25%22%2C%20%22scoreValue%22%3A%20%220%22%2C%20%22execTime%22%3A%20%222018-09-15%2016%3A29%3A55%22%2C%20%22termIp%22%3A%20%22133.150.40.81%22%2C%20%22xCodingStr9%22%3A%20%22%22%2C%20%22openDate%22%3A%20%222018-09-12%2009%3A06%3A22%22%2C%20%22userTypeCode%22%3A%20%220%22%2C%20%22xCodingStr8%22%3A%20%22%22%2C%20%22xCodingStr7%22%3A%20%22%22%2C%20%22xCodingStr6%22%3A%20%22%22%2C%20%22tradeId%22%3A%20%221118091527943915%22%2C%20%22receiptInfo2%22%3A%20%22%E6%8B%85%E4%BF%9D%E4%BA%BA%E5%A7%93%E5%90%8D%3A%20%20%20%20%E6%8B%85%E4%BF%9D%E7%B1%BB%E5%9E%8B%3A%20%20%20%20%E6%8B%85%E4%BF%9D%E4%BA%BA%E8%81%94%E7%B3%BB%E7%94%B5%E8%AF%9D%3A%20%E6%8B%85%E4%BF%9D%E4%BA%BA%E8%AF%81%E4%BB%B6%E7%B1%BB%E5%9E%8B%3A%E6%8B%85%E4%BF%9D%E4%BA%BA%E8%AF%81%E4%BB%B6%E7%B1%BB%E5%9E%8B%5Cn%E6%8B%85%E4%BF%9D%E4%BA%BA%E8%AF%81%E4%BB%B6%E5%8F%B7%E7%A0%81%3A%20~%E4%BB%A3%E7%90%86%E4%BA%BA%E5%A7%93%E5%90%8D%3A%20%20%20%E4%BB%A3%E7%90%86%E4%BA%BA%E8%81%94%E7%B3%BB%E7%94%B5%E8%AF%9D%3A%20%E4%BB%A3%E7%90%86%E4%BA%BA%E8%AF%81%E4%BB%B6%E7%B1%BB%E5%9E%8B%3A%20%20%20%E4%BB%A3%E7%90%86%E4%BA%BA%E8%AF%81%E4%BB%B6%E5%8F%B7%E7%A0%81%3A%20%22%2C%20%22provinceCode%22%3A%20%22SXCU%22%2C%20%22xCodingStr5%22%3A%20%22%22%2C%20%22receiptInfo1%22%3A%20%22%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%E8%8C%83%E6%96%87%E6%85%A7~~%5Cn%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%2018534315008%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20620524199704301827~~%5Cn%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%E4%B8%AA%E4%BA%BA%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5Cn%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%2018603595441~~%22%2C%20%22tradeDepartId%22%3A%20%22M0959%22%2C%20%22receiptInfo4%22%3A%20%22%22%2C%20%22xCodingStr4%22%3A%20%22%22%2C%20%22xCodingStr3%22%3A%20%22%22%2C%20%22receiptInfo3%22%3A%20%22%E8%AE%A4%E8%AF%81%E6%96%B9%E5%BC%8F%3A%20%5Cn~%E6%96%B0%E5%A2%9E%E4%BC%98%E6%83%A0%3A1%E5%85%83%2F%E6%9C%88%2C%E6%8B%A8%E6%89%93%E6%9C%AC%E5%9C%B0%E7%BD%91%E8%81%94%E9%80%9A%E5%85%8D%E8%B4%B9~%20%20%20%E7%94%9F%E6%95%88%E6%97%B6%E9%97%B4%3A2018-09-15~0%E5%85%83500%E5%88%86%E9%92%9F%E6%9C%AC%E5%9C%B0%E6%8B%A8%E6%89%93%E9%95%BF%E5%B8%82%E5%90%88%E4%B8%80%E5%88%86%E9%92%9F%E6%95%B0~%20%20%20%E7%94%9F%E6%95%88%E6%97%B6%E9%97%B4%3A2018-09-15~10%E5%85%83%E5%9B%BD%E5%86%85%E6%B5%81%E9%87%8F%E4%B8%8D%E9%99%90%E9%87%8F%E5%8C%85%2C100G%E5%90%8E%E9%99%90%E9%80%9F%E4%B8%BA1Mbps(%E7%AB%8B%E5%8D%B3%E7%94%9F%E6%95%88)~%20%20%20%E7%94%9F%E6%95%88%E6%97%B6%E9%97%B4%3A2018-09-15~%E5%AD%9850%E9%80%81180%E5%85%83%E8%AF%9D%E8%B4%B9%EF%BC%8C%E9%A2%84%E5%AD%98%E6%AC%BE%E4%B8%80%E6%AC%A1%E6%80%A7%E5%88%B0%E8%B4%A6%EF%BC%8C%E8%B5%A0%E6%AC%BE%E6%AC%A1%E6%9C%88%E5%88%8612%E4%B8%AA%E6%9C%88%E8%BF%94%E8%BF%98~%20%20%20%E7%94%9F%E6%95%88%E6%97%B6%E9%97%B4%3A2018-10-01~~%E5%8F%96%E6%B6%88%E4%BC%98%E6%83%A0%3A%E6%A0%A1%E5%9B%AD%E5%B0%8F%E5%8C%BA(%E8%BF%90%E5%9F%8E)-0%E5%85%83%E6%A0%A1%E5%8C%BA%E6%B5%81%E9%87%8F%E4%B8%8D%E9%99%90%E9%87%8F%E5%8C%8515GB%E5%90%8E%E9%99%90%E9%80%9F3Mbps~%20%20%E7%94%9F%E6%95%88%E6%97%B6%E9%97%B4%3A%202018-09-06%20%20%E5%A4%B1%E6%95%88%E6%97%B6%E9%97%B4%3A%202018-09-30%20~%E6%96%B0%E5%A2%9E%E6%9C%8D%E5%8A%A1%3A%20~%E5%8F%96%E6%B6%88%E6%9C%8D%E5%8A%A1%3A%20~%E6%96%B0%E5%A2%9ESP%3A%20~%E5%8F%96%E6%B6%88SP%3A%20%5Cn~%E6%8F%90%E9%86%92%3A%E5%88%9D%E6%AC%A1%E4%BD%BF%E7%94%A8%E6%97%B6%E8%AF%B7%E4%BF%AE%E6%94%B9%E5%AF%86%E7%A0%81.~~~%E6%9C%88%E5%A5%97%E9%A4%90%E5%9B%BD%E5%86%85%EF%BC%88%E4%B8%8D%E5%90%AB%E5%8F%B0%E6%B8%AF%E6%BE%B3%EF%BC%89%E6%B5%81%E9%87%8F%E5%BD%93%E6%9C%88%E4%B8%8D%E6%B8%85%E9%9B%B6%EF%BC%8C%E5%89%A9%E4%BD%99%E6%B5%81%E9%87%8F%E8%87%AA%E5%8A%A8%E7%BB%93%E8%BD%AC%E8%87%B3%E4%B8%8B%E6%9C%88%EF%BC%8C%E6%9C%89%E6%95%88%E6%9C%9F%E8%87%B3%E4%B8%8B%E6%9C%88%E6%9C%88%E5%BA%95%E3%80%82%E5%A5%97%E9%A4%90%E5%86%85%E5%85%B6%E4%BB%96%E4%B8%9A%E5%8A%A1%E9%87%8F%E4%BB%A5%E5%8F%8A%E5%AE%9A%E5%90%91%E6%B5%81%E9%87%8F%E5%8F%A0%E5%8A%A0%E5%8C%85%E3%80%81%E5%90%8E%E5%90%91%E6%B5%81%E9%87%8F%E4%BA%A7%E5%93%81%E3%80%81%E8%B5%A0%E9%80%81%E6%B5%81%E9%87%8F%E7%AD%89%E4%BB%85%E9%99%90%E5%BD%93%E6%9C%88%E4%BD%BF%E7%94%A8%EF%BC%8C%E4%B8%8D%E8%83%BD%E5%BB%B6%E7%BB%AD%E8%87%B3%E4%B8%8B%E6%9C%88%E4%BD%BF%E7%94%A8%E3%80%82~%20~~%20~%E5%BD%93%E6%9C%88%E5%A5%97%E9%A4%90%E5%8F%8A%E5%8F%A0%E5%8A%A0%E6%B5%81%E9%87%8F%E5%8C%85%E4%BB%A5%E5%A4%96%E7%9A%84%E6%B5%81%E9%87%8F%E8%AE%A1%E8%B4%B9%E8%BE%BE%E5%88%B0600%E5%85%83%E5%90%8E%EF%BC%8C%E5%9B%BD%E5%86%85%EF%BC%88%E4%B8%8D%E5%90%AB%E5%8F%B0%E6%B8%AF%E6%BE%B3%EF%BC%89%E6%B5%81%E9%87%8F%E4%B8%8D%E5%86%8D%E6%94%B6%E8%B4%B9%EF%BC%8C%E8%BE%BE%E5%88%B015GB%E5%90%8E%E7%B3%BB%E7%BB%9F%E8%87%AA%E5%8A%A8%E5%85%B3%E9%97%AD%E6%95%B0%E6%8D%AE%E7%BD%91%E7%BB%9C%EF%BC%8C%E6%AC%A1%E6%9C%88%E8%87%AA%E5%8A%A8%E6%89%93%E5%BC%80%E3%80%82%E7%94%A8%E6%88%B7%E4%B8%BB%E5%8A%A8%E7%94%B3%E8%AF%B7%EF%BC%8C%E5%BD%93%E6%9C%88%E6%89%93%E5%BC%80%EF%BC%9B%E5%BD%93%E6%9C%88%E5%9B%BD%E9%99%85%E5%8F%8A%E6%B8%AF%E6%BE%B3%E5%8F%B0%E6%BC%AB%E6%B8%B8%E5%92%8C%E5%A5%97%E9%A4%90%E5%86%85%E3%80%81%E5%A5%97%E9%A4%90%E5%A4%96%E3%80%81%E5%90%84%E7%A7%8D%E6%94%B6%E8%B4%B9%E3%80%81%E5%85%8D%E8%B4%B9%E3%80%81%E5%90%84%E7%B1%BB%E5%AE%9A%E5%90%91%E7%AD%89%E6%95%B0%E6%8D%AE%E6%B5%81%E9%87%8F%E6%80%BB%E5%92%8C%E8%BE%BE%E5%88%B0100GB%E5%90%8E%E7%B3%BB%E7%BB%9F%E8%87%AA%E5%8A%A8%E5%85%B3%E9%97%AD%E6%95%B0%E6%8D%AE%E7%BD%91%E7%BB%9C%EF%BC%8C%E5%BD%93%E6%9C%88%E4%B8%8D%E5%86%8D%E5%BC%80%E6%94%BE%EF%BC%8C%E6%AC%A1%E6%9C%88%E8%87%AA%E5%8A%A8%E5%BC%80%5Cn%22%2C%20%22xCodingStr12%22%3A%20%22%22%2C%20%22receiptInfo7%22%3A%20%22%22%2C%20%22xCodingStr13%22%3A%20%22%22%2C%20%22receiptInfo5%22%3A%20%22~%20~%20~%E8%AE%A4%E8%AF%81%E6%96%B9%E5%BC%8F%3A%20~%20~%E6%89%8B%E6%9C%BA%E4%B8%B2%E5%8F%B7%3A~%20~%22%2C%20%22xCodingStr14%22%3A%20%22%22%2C%20%22receiptInfo6%22%3A%20%22%22%2C%20%22xCodingStr15%22%3A%20%22%22%2C%20%22mputeMonthFee%22%3A%20%221%22%2C%20%22openDepartId%22%3A%20%220CC7B%22%2C%20%22xCodingStr10%22%3A%20%22%22%2C%20%22removeReasonCode%22%3A%20%22%22%2C%20%22xCodingStr11%22%3A%20%22%22%2C%20%22tradeEparchyCode%22%3A%20%220359%22%2C%20%22xCodingStr16%22%3A%20%22%22%2C%20%22xCodingStr17%22%3A%20%22%22%2C%20%22xCodingStr18%22%3A%20%22%22%2C%20%22xCodingStr19%22%3A%20%22%22%2C%20%22removeEparchyCode%22%3A%20%22%22%2C%20%22feeTime%22%3A%20%22%22%2C%20%22creditRuleId%22%3A%20%22-1%22%2C%20%22feeStaffId%22%3A%20%22%22%2C%20%22checkTypeCode%22%3A%20%22%22%2C%20%22brandCode%22%3A%20%224G02%22%2C%20%22tradeStatus%22%3A%20%22query%22%2C%20%22prepayTag%22%3A%20%220%22%2C%20%22dealType%22%3A%20%221%22%2C%20%22inModeCode%22%3A%20%220%22%2C%20%22productId%22%3A%20%2220104142%22%2C%20%22serialNumber%22%3A%20%2218534315008%22%2C%20%22userStateCodeset%22%3A%20%220%22%2C%20%22actorCertnum%22%3A%20%22%3A%22%2C%20%22removeCityCode%22%3A%20%22%22%2C%20%22itemId%22%3A%20%221118090642282848%22%2C%20%22userPasswd%22%3A%20%22cwk0cY%22%2C%20%22routeEparchyCode%22%3A%20%220359%22%2C%20%22contactAddress%22%3A%20%22%22%2C%20%22assureCustId%22%3A%20%22%22%2C%20%22strisneedprint%22%3A%20%221%22%2C%20%22checkResult%22%3A%20%220000%22%2C%20%22custId%22%3A%20%221118090527825955%22%2C%20%22acctId%22%3A%20%221118090637429416%22%2C%20%22xLcuLogstep%22%3A%20%2232%22%2C%20%22xCodingStr%22%3A%20%22%22%2C%20%22xCheckInfo%22%3A%20%22SpPt00102000110370%E7%89%B9%E6%AE%8A%E9%99%90%E5%88%B6%E5%88%A4%E6%96%AD%3A%E7%94%A8%E6%88%B7%E5%9C%A8%E6%9C%AC%E6%AC%A1%E4%B8%9A%E5%8A%A1%E4%B8%AD%3A%3Cbr%3E%3Cbr%3E%E6%96%B0%E5%A2%9E%E4%BC%98%E6%83%A0%EF%BC%9A%E3%80%901%E5%85%83%2F%E6%9C%88%2C%E6%8B%A8%E6%89%93%E6%9C%AC%E5%9C%B0%E7%BD%91%E8%81%94%E9%80%9A%E5%85%8D%E8%B4%B9%E3%80%91%EF%BC%8C%E3%80%900%E5%85%83500%E5%88%86%E9%92%9F%E6%9C%AC%E5%9C%B0%E6%8B%A8%E6%89%93%E9%95%BF%E5%B8%82%E5%90%88%E4%B8%80%E5%88%86%E9%92%9F%E6%95%B0%E3%80%91%EF%BC%8C%E3%80%9010%E5%85%83%E5%9B%BD%E5%86%85%E6%B5%81%E9%87%8F%E4%B8%8D%E9%99%90%E9%87%8F%E5%8C%85%2C100G%E5%90%8E%E9%99%90%E9%80%9F%E4%B8%BA1Mbps(%E7%AB%8B%E5%8D%B3%E7%94%9F%E6%95%88)%E3%80%91%EF%BC%8C%E3%80%90%E5%AD%9850%E9%80%81180%E5%85%83%E8%AF%9D%E8%B4%B9%EF%BC%8C%E9%A2%84%E5%AD%98%E6%AC%BE%E4%B8%80%E6%AC%A1%E6%80%A7%E5%88%B0%E8%B4%A6%EF%BC%8C%E8%B5%A0%E6%AC%BE%E6%AC%A1%E6%9C%88%E5%88%8612%E4%B8%AA%E6%9C%88%E8%BF%94%E8%BF%98%E3%80%91%3Cbr%3E%E5%88%A0%E9%99%A4%E4%BC%98%E6%83%A0%EF%BC%9A%E3%80%90%E6%A0%A1%E5%9B%AD%E5%B0%8F%E5%8C%BA(%E8%BF%90%E5%9F%8E)-0%E5%85%83%E6%A0%A1%E5%8C%BA%E6%B5%81%E9%87%8F%E4%B8%8D%E9%99%90%E9%87%8F%E5%8C%8515GB%E5%90%8E%E9%99%90%E9%80%9F3Mbps%E3%80%91%3Cbr%3E%3Cb%3E%3Cfont%20color%20%3D'red'%3E%3C%2Ffont%3E%3C%2Fb%3E%3Cbr%3E%E8%AF%B7%E6%8F%90%E9%86%92%E7%94%A8%E6%88%B7%E6%9F%A5%E7%9C%8B%E5%85%8D%E5%A1%AB%E5%8D%95%E4%B8%AD%E5%8F%98%E6%9B%B4%E7%9A%84%E4%BF%A1%E6%81%AF%22%2C%20%22endAcycId%22%3A%20%22203701%22%2C%20%22actorCerttypeid%22%3A%20%22%22%2C%20%22actorPhone%22%3A%20%22%22%2C%20%22xRecordnum%22%3A%20%221%22%2C%20%22xSelcount%22%3A%20%220%22%2C%20%22cityCode%22%3A%20%22MQ00%22%2C%20%22detailInstallAddress%22%3A%20%22%22%2C%20%22inStaffId%22%3A%20%22YCCB0591%22%2C%20%22invoiceNo%22%3A%20%22%22%2C%20%22inNetMode%22%3A%20%220%22%2C%20%22priority%22%3A%20%22320%22%2C%20%22developStaffId%22%3A%20%22YCCB0591%22%2C%20%22userType%22%3A%20%22%E6%99%AE%E9%80%9A%E7%94%A8%E6%88%B7%22%2C%20%22attrTypeCode%22%3A%20%220%22%2C%20%22lastStopTime%22%3A%20%22%22%2C%20%22tradeAttr%22%3A%20%221%22%2C%20%22openMode%22%3A%20%220%22%2C%20%22tradeLcuName%22%3A%20%22TCS_ChangeServiceReg%22%2C%20%22userDiffCode%22%3A%20%2200%22%2C%20%22xLastResultinfo%22%3A%20%22%22%2C%20%22tradeInfoTagSet%22%3A%20%22111111%20%20%20%20%22%2C%20%22nextDealTag%22%3A%20%22Z%22%2C%20%22xResultinfo%22%3A%20%22%22%2C%20%22olcomTag%22%3A%20%220%22%2C%20%22removeTag%22%3A%20%220%22%2C%20%22partitionId%22%3A%20%222848%22%2C%20%22foregift%22%3A%20%220%22%2C%20%22contactPostAddr%22%3A%20%22%22%2C%20%22id%22%3A%20%221118090642282848%22%2C%20%22rightCode%22%3A%20%22csChangeServiceTrade%22%2C%20%22chkTag%22%3A%20%220%22%2C%20%22fee%22%3A%20%220%22%2C%20%22operFee%22%3A%20%220%22%2C%20%22tradeTypeCode%22%3A%20%22120%22%2C%20%22cancelTag%22%3A%20%220%22%2C%20%22changeuserDate%22%3A%20%22%22%2C%20%22tradeTagSet%22%3A%20%2210100000000000000000%22%2C%20%22xTransCode%22%3A%20%22TCS_ChangeServiceReg%22%2C%20%22basicCreditValue%22%3A%20%220%22%2C%20%22xLastResultcode%22%3A%20%220%22%2C%20%22updateTime%22%3A%20%22%22%2C%20%22tradeCityCode%22%3A%20%22MQ00%22%2C%20%22custType%22%3A%20%22%E4%B8%AA%E4%BA%BA%E5%AE%A2%E6%88%B7%22%2C%20%22netTypeCode%22%3A%20%2210%22%2C%20%22custName%22%3A%20%22%E8%8C%83%E6%96%87%E6%85%A7%22%2C%20%22developDepartId%22%3A%20%220CC7B%22%2C%20%22firstCallTime%22%3A%20%22%22%2C%20%22inDepartId%22%3A%20%220CC7B%22%2C%20%22leaveRealFee%22%3A%20%220%22%2C%20%22tradeStaffId%22%3A%20%22YCJTZY15%22%2C%20%22openStaffId%22%3A%20%22YCCB0591%22%2C%20%22processTagSet%22%3A%20%22%20%22%2C%20%22xResultcode%22%3A%20%220%22%2C%20%22advancePay%22%3A%20%220%22%2C%20%22acceptDate%22%3A%20%222018-09-15%2016%3A29%3A55%22%2C%20%22destroyTime%22%3A%20%22%22%2C%20%22tradeJudgeOweTag%22%3A%20%220%22%2C%20%22contactName%22%3A%20%22%22%2C%20%22idType%22%3A%20%221%22%2C%20%22preDestroyTime%22%3A%20%22%22%2C%20%22creditValue%22%3A%20%220%22%2C%20%22contactPhone%22%3A%20%22%22%2C%20%22psptId%22%3A%20%22%E8%BA%AB%E4%BB%BD%E8%AF%81%3A620524199704301827%22%2C%20%22xTag%22%3A%20%221%22%2C%20%22contactPostCode%22%3A%20%22%22%2C%20%22contractId%22%3A%20%22%22%2C%20%22acceptMonth%22%3A%20%229%22%2C%20%22assureDate%22%3A%20%22%22%2C%20%22userId%22%3A%20%221118090642282848%22%2C%20%22developEparchyCode%22%3A%20%220359%22%2C%20%22startAcycId%22%3A%20%22194910%22%2C%20%22xLcuTxdservCount%22%3A%20%220%22%2C%20%22eparchyCode%22%3A%20%220359%22%2C%20%22contact%22%3A%20%22%22%2C%20%22developNo%22%3A%20%22%22%2C%20%22developCityCode%22%3A%20%22MQ00%22%2C%20%22removeDepartId%22%3A%20%22%22%2C%20%22productTypeCode%22%3A%20%224444%22%2C%20%22inDate%22%3A%20%222018-09-06%2015%3A56%3A25%22%2C%20%22mputeDate%22%3A%20%222018-09-12%2009%3A06%3A24%22%2C%20%22assureTypeCode%22%3A%20%22%22%2C%20%22subscribeId%22%3A%20%221118091527943915%22%2C%20%22tradeType%22%3A%20%22%E4%BA%A7%E5%93%81%2F%E6%9C%8D%E5%8A%A1%E5%8F%98%E6%9B%B4%22%2C%20%22actorName%22%3A%20%22%22%7D&CASH=50.00&SEND_TYPE=0&TRADE_ID=1118091527943915
'''