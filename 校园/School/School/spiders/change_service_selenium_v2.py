import time, os, requests, json, re

from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException

from pyexcel_io import iget_data
from pyexcel_xlsx import save_data, get_data


# from retrying import retry


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

        self.path = r'D:\Desktop\业务.xlsx'
        self.record = r'D:\Desktop\业务_record.xlsx'

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

        # if is_not_visible(self.brow, '//img[contains(@onclick,"20104142")]', 2):
        #     print('here')
        time.sleep(2)
        WebDriverWait(self.brow, 30, 0.5).until(EC.presence_of_element_located((By.XPATH, '//input[@id="_p20104142"]')))
        product_ot = self.brow.find_element_by_xpath('//input[@id="_p20104142"]').get_attribute('_startDate')

        WebDriverWait(self.brow, 30, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="_tradeBase"]')))

        user_id = self.brow.find_element_by_xpath('//input[@id="USER_ID_HIDEN"]').get_attribute('value')
        trade_base = self.brow.find_element_by_xpath('//input[@id="_tradeBase"]').get_attribute('value')

        # id = self.brow.find_element_by_xpath('//input[@id="PSPT_ID"]').get_attribute('value')

        # all_info = json.loads(self.brow.find_element_by_xpath('//input[@id="_all_infos"]').get_attribute('value'))
        # print(all_info)
        self.continue_submit(user_id, trade_base, product_ot, name,number)

    def continue_submit(self, user_id, trade_base, product_ot,name, number):
        import time
        # user_id = '1118090542272586'
        # trade_base = 'H4sIAAAAAAAAAHVSTUvDQBQsBf+H5CyY3SRN6m272aaRNqmbXaSnpdRQvQhWFFQ8eBIVP8CLoCCe9CCeevKgf8bUXvwP7sYkNELfcd7MvDdv9/WnsnBYqVQvqmdHGqPIJaKNuQhQh2grGsORwJv97WEcxaP9rUFM46G2lPFYr0sEDl1JBFAvUOSJiDApBjrQ/5cUY5/1MpnWWUshHhEqXL/ZzPEU7dLQ5ZgJ35UIlGYmMGExfZW7HhHhejpRSXKflA4AcPS6bpkQ2tByarIpez5qi4B3GoQqimMZpgF0G9b+pJhHrKQ2oe1Aw4Z12achZ0SQLqK41ZOU6edN8nhVbOMHzXA2elqLsiTDZ6Qzd6vMsQhuWGpaQNjseeUp1eHUftnDTMcfydvp98uFxBFjtMRWZIRxOYxl2CZwbAhzp7lJfa/FcqvBbun52ai/EReh1WDlIYEGRYGbi0xPh6VfIrGv9+fk9mR58nCZnD8l13eT+3FBiRhiPJKknb14dKAd/wLtWraalAIAAA==',
        # product_ot = '2018-09-05 12:48:20'
        # number = '18534310726'

        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        data = {
            'Base': trade_base,
            'Ext': '{"Common": {"ACTOR_NAME": "", "ACTOR_PHONE": "", "ACTOR_CERTTYPEID": "", "ACTOR_CERTNUM": "", "REMARK": ""}, "TF_B_TRADE_DISCNT": {"ITEM": [{"ID": "' + user_id + '", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001024", "DISCNT_CODE": "99051112", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "2018-10-01 00:00:00", "END_DATE": "2019-09-30 23:59:59", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""}, {"ID": "' + user_id + '", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001025", "DISCNT_CODE": "19102407", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "' + time_now + '", "END_DATE": "2050-01-01 00:00:00", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""}, {"ID": "' + user_id + '", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001025", "DISCNT_CODE": "19102923", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "' + time_now + '", "END_DATE": "2050-01-01 00:00:00", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""}, {"ID": "' + user_id + '", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001026", "DISCNT_CODE": "19103204", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "' + time_now + '", "END_DATE": "2050-12-31 00:00:00", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""}]}, "TF_B_TRADE_OTHER": {"ITEM": [{"RSRV_VALUE_CODE": "NEXP", "RSRV_VALUE": "' + user_id + '", "RSRV_STR1": "20104142", "RSRV_STR2": "00", "RSRV_STR3": "19001094", "RSRV_STR4": "4444", "RSRV_STR5": "undefined", "RSRV_STR6": "-1", "RSRV_STR7": "0", "RSRV_STR8": "", "RSRV_STR9": "4G02", "RSRV_STR10": "' + number + '", "MODIFY_TAG": "1", "START_DATE": "' + product_ot + '", "END_DATE": "' + time_now + '", "X_DATATYPE": "NULL"}, {"RSRV_VALUE_CODE": "DLPK", "RSRV_VALUE": "' + user_id + '", "RSRV_STR1": "20104142", "RSRV_STR2": "00", "RSRV_STR3": "19001094", "X_DATATYPE": "NULL"}]}, "TF_B_TRADE_USER": {"ITEM": {"PRODUCT_ID": "20104142", "BRAND_CODE": "4G02", "USER_ID": "' + user_id + '", "NET_TYPE_CODE": "10"}}, "TF_B_TRADE": {"PRODUCT_ID": "20104142", "BRAND_CODE": "4G02", "EXEC_TIME": "' + time_now + '"}, "TRADE_SUB_ITEM": {}, "MANYOU_TEMP": {"ITEM": {"ManYouCreditTag": false}}, "TRADE_ITEM": {"DEVELOP_SUB_TYPE": "", "DEVELOP_STAFF_ID": "", "IS_TELEKET": "0", "TELEKET_TYPE": "", "DEVELOP_DEPART_ID": ""}}'}
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
            'Cookie': '__guid=221721176.840067343969089200.1536318815165.4204; LOGIN_SUBSYS_CODEBSS=CRM; BSS_BSS_ACCTMANM_JSESSIONID=9NJsbbsJY1mY1LHvbpkpG8T92w0nNJsTbbn6TkKqfNWh1nzWyx3K!1192800156!-1652137237; BSS_BSS_JSESSIONID=0nq2bbvJwsLSzMyQFctYG0DxVp63zjJ1PTcNVzTpvmvtvqgJTr24!-178863608!1551878969; BSS_BSS_STATSERV_JSESSIONID=p9xmbbvLh8fDjsQT1PwSJd1cCgPH1wRnlh8wqFN1snjmGJD9FtBy!-2127903152!-1715235729; BSS_SYSMANM_JSESSIONID=21dLbbvJj2k2MH1vyyJ11BT2mslfhp2sQyHJNzRGTJ2Qbkg5W11Y!-1433269564!-269914159; BSS_RESMANM_JSESSIONID=G7CsbbvLJyhfjql8PXbFTptl8J3xTCGdF2HTmqYPCbJk49CqPy2c!1672713234!1101795391; BSS_BSS_CUSTMANM_JSESSIONID=9J9bbbvJ7Qgfvvh8f0VhG1sYHXQ1BHN7wVrvQkCJ2RHRMW42JWWQ!-355411734!-245996366; BSS_BSS_SALEMANM_JSESSIONID=g070bbvLB3DLJhqQpKyGQx12nm3bPZD45J842TMTZ9V51b2h2vwd!2061263565!159647921; BSS_CHNLMANM_JSESSIONID=9z25bbvLF0686HZydy2VpR0Xwhc1cQsN1c2b9m7mG14dwWMJRVQ3!-798000933!112363500; LOGIN_STAFF_IDBSS=YCJTZY15; BSS_BSS_CUSTSERV_JSESSIONID=R2hgbbvJxSqvx2TNpMYFF3LT24bsQTtsdRJkFGySpwpPGv9GzpGc!1301866683!-243533903'
        }
        rs = requests.post(
            url='http://133.128.6.186:8080/custserv?service=swallow/personalserv.changeelement.ChangeElement/submitMobTrade/1',
            data=data, headers=headers)
        print(rs.content.decode('gbk'))
        str_1 = rs.content.decode('gbk')
        trade_id = re.findall("tradeId='(\d+)'", str_1)[0]
        subscribe_id = re.findall("subscribeId='(\d+)'", str_1)[0]
        startDate = re.findall('START_DATE&gt;(.+)&lt;/START_DATE', str_1)[0]
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
        phone = re.findall('(\d+)~~" tradeDepartId', str_1)[0]
        ip = re.findall('termIp="(.+)" xCodingStr9', str_1)[0]
        userPasswd = re.findall('userPasswd="(.+)" routeEparchyCode', str_1)[0]
        if '该号码有未完工的产品' in rs.content.decode('gbk'):
            print('here')
            write(self.name, self.id, self.number, '失败', self.record)
        else:
            print('there')
            tradeMain = '[{"TRADE_ID": "'+trade_id+'", "TRADE_TYPE": "产品/服务变更", "SERIAL_NUMBER": "'+number+'", "TRADE_FEE": "50.00", "CUST_NAME": "'+name+'", "CUST_ID": "'+cust_id+'", "USER_ID": "'+user_id+'", "ACCT_ID": "'+acct_id+'", "NET_TYPE_CODE": "10", "TRADE_TYPE_CODE": "120", "PSPT_TYPE_CODE": "0"}]'
            fees = '[{"X_TAG": "1", "TRADE_ID": "'+trade_id+'", "CALCULATE_ID": "", "FEE_MODE": "2", "FEEITEM_CODE": "100005", "OLDFEE": "50.00", "FEE": "50.00", "DERATE_REMARK": "", "PAY_MONEY_CODE": "0", "PAY_TAG": "0", "CALCULATE_TAG": "N", "MODIFY_TAG": "", "TRADE_TYPE_CODE": "120", "NET_TYPE_CODE": "10", "FEEITEM_NAME": "[预存]营业厅收入(营业缴费)_普通预存款(不可清退))"}]'
            feePayMoney = '[{"TRADE_ID": "'+trade_id+'", "PAY_MONEY_CODE": "0", "MONEY": 5000}]'
            base = '{"xCodingStr1": "1</MODIFY_TAG><RSRV_STR3>19001094</RSRV_STR3><RSRV_STR6>-1</RSRV_STR6><END_DATE>'+time_now+'</END_DATE><RSRV_STR5>undefined</RSRV_STR5><RSRV_STR8/><X_DATATYPE>NULL</X_DATATYPE><RSRV_STR7>0</RSRV_STR7><RSRV_STR9>4G02</RSRV_STR9><RSRV_STR10>'+number+'</RSRV_STR10><START_DATE>'+startDate+'</START_DATE><RSRV_VALUE>'+user_id+'</RSRV_VALUE><RSRV_VALUE_CODE>NEXP</RSRV_VALUE_CODE></ITEM><ITEM><RSRV_STR2>00</RSRV_STR2><RSRV_STR1>20104142</RSRV_STR1><RSRV_VALUE>'+user_id+'</RSRV_VALUE><RSRV_VALUE_CODE>DLPK</RSRV_VALUE_CODE><RSRV_STR3>19001094</RSRV_STR3><X_DATATYPE>NULL</X_DATATYPE></ITEM></TF_B_TRADE_OTHER></Ext></ROOT>", "xCodingStr2": "", "xCheckTag": "1", "creditClass": "-1", "usecustId": "'+cust_id+'", "routeEparchy": "运城", "acctTag": "0", "remark": "", "feeState": "", "developDate": "'+developDate+'", "scoreValue": "0", "execTime": "'+execTime+'", "termIp": "'+ip+'", "xCodingStr9": "", "openDate": "'+openDate+'", "userTypeCode": "0", "xCodingStr8": "", "xCodingStr7": "", "xCodingStr6": "", "tradeId": "'+trade_id+'", "receiptInfo2": "担保人姓名:    担保类型:    担保人联系电话: 担保人证件类型:担保人证件类型\n担保人证件号码: ~代理人姓名:   代理人联系电话: 代理人证件类型:   代理人证件号码: ", "provinceCode": "SXCU", "xCodingStr5": "", "receiptInfo1": "                                                   '+name+'~~\n                                                   '+number+'                                                                 '+pspt_id+'~~\n                                                   个人                                                                   \n                                                   '+phone+'~~", "tradeDepartId": "M0959", "receiptInfo4": "", "xCodingStr4": "", "xCodingStr3": "", "receiptInfo3": "认证方式: \n~新增优惠:1元/月,拨打本地网联通免费~   生效时间:2018-09-14~0元500分钟本地拨打长市合一分钟数~   生效时间:2018-09-14~10元国内流量不限量包,100G后限速为1Mbps(立即生效)~   生效时间:2018-09-14~存50送180元话费，预存款一次性到账，赠款次月分12个月返还~   生效时间:2018-10-01~~取消优惠:校园小区(运城)-0元校区流量不限量包15GB后限速3Mbps~  生效时间: 2018-09-05  失效时间: 2018-09-30 ~新增服务: ~取消服务: ~新增SP: ~取消SP: \n~提醒:初次使用时请修改密码.~~~月套餐国内（不含台港澳）流量当月不清零，剩余流量自动结转至下月，有效期至下月月底。套餐内其他业务量以及定向流量叠加包、后向流量产品、赠送流量等仅限当月使用，不能延续至下月使用。~ ~~ ~当月套餐及叠加流量包以外的流量计费达到600元后，国内（不含台港澳）流量不再收费，达到15GB后系统自动关闭数据网络，次月自动打开。用户主动申请，当月打开；当月国际及港澳台漫游和套餐内、套餐外、各种收费、免费、各类定向等数据流量总和达到100GB后系统自动关闭数据网络，当月不再开放，次月自动开\n", "xCodingStr12": "", "receiptInfo7": "", "xCodingStr13": "", "receiptInfo5": "~ ~ ~认证方式: ~ ~手机串号:~ ~", "xCodingStr14": "", "receiptInfo6": "", "xCodingStr15": "", "mputeMonthFee": "1", "openDepartId": "M0959", "xCodingStr10": "", "removeReasonCode": "", "xCodingStr11": "", "tradeEparchyCode": "0359", "xCodingStr16": "", "xCodingStr17": "", "xCodingStr18": "", "xCodingStr19": "", "removeEparchyCode": "", "feeTime": "", "creditRuleId": "-1", "feeStaffId": "", "checkTypeCode": "", "brandCode": "4G02", "tradeStatus": "query", "prepayTag": "0", "dealType": "1", "inModeCode": "0", "productId": "20104142", "serialNumber": "'+number+'", "userStateCodeset": "0", "actorCertnum": ":", "removeCityCode": "", "itemId": "'+item_id+'", "userPasswd": "'+userPasswd+'", "routeEparchyCode": "0359", "contactAddress": "", "assureCustId": "", "strisneedprint": "1", "checkResult": "0000", "custId": "'+cust_id+'", "acctId": "'+acct_id+'", "xLcuLogstep": "32", "xCodingStr": "", "xCheckInfo": "SpPt00102000110370特殊限制判断:用户在本次业务中:<br><br>新增优惠：【1元/月,拨打本地网联通免费】，【0元500分钟本地拨打长市合一分钟数】，【10元国内流量不限量包,100G后限速为1Mbps(立即生效)】，【存50送180元话费，预存款一次性到账，赠款次月分12个月返还】<br>删除优惠：【校园小区(运城)-0元校区流量不限量包15GB后限速3Mbps】<br><b><font color :'+'red'+'></font></b><br>请提醒用户查看免填单中变更的信息", "endAcycId": "203701", "actorCerttypeid": "", "actorPhone": "", "xRecordnum": "1", "xSelcount": "0", "cityCode": "MQ00", "detailInstallAddress": "", "inStaffId": "'+instaff_id+'", "invoiceNo": "", "inNetMode": "0", "priority": "320", "developStaffId": "'+develop_staff+'", "userType": "普通用户", "attrTypeCode": "0", "lastStopTime": "", "tradeAttr": "1", "openMode": "0", "tradeLcuName": "TCS_ChangeServiceReg", "userDiffCode": "00", "xLastResultinfo": "", "tradeInfoTagSet": "111111    ", "nextDealTag": "Z", "xResultinfo": "", "olcomTag": "0", "removeTag": "0", "partitionId": "2623", "foregift": "0", "contactPostAddr": "", "id": "'+user_id+'", "rightCode": "csChangeServiceTrade", "chkTag": "0", "fee": "0", "operFee": "0", "tradeTypeCode": "120", "cancelTag": "0", "changeuserDate": "", "tradeTagSet": "10100000000000000000", "xTransCode": "TCS_ChangeServiceReg", "basicCreditValue": "0", "xLastResultcode": "0", "updateTime": "", "tradeCityCode": "MQ00", "custType": "个人客户", "netTypeCode": "10", "custName": "'+name+'", "developDepartId": "M0959", "firstCallTime": "", "inDepartId": "M0959", "leaveRealFee": "0", "tradeStaffId": "'+tradestaff_id+'", "openStaffId": "'+openstaff_id+'", "processTagSet": " ", "xResultcode": "0", "advancePay": "0", "acceptDate": "'+acceptDate+'", "destroyTime": "", "tradeJudgeOweTag": "0", "contactName": "", "idType": "1", "preDestroyTime": "", "creditValue": "0", "contactPhone": "", "psptId": "身份证:'+pspt_id+'", "xTag": "1", "contactPostCode": "", "contractId": "", "acceptMonth": "9", "assureDate": "", "userId": "'+user_id+'", "developEparchyCode": "0359", "startAcycId": "194910", "xLcuTxdservCount": "0", "eparchyCode": "0359", "contact": "", "developNo": "", "developCityCode": "MQ00", "removeDepartId": "", "productTypeCode": "4444", "inDate": "'+inDate+'", "mputeDate": "'+mputeDate+'", "assureTypeCode": "", "subscribeId": "'+subscribe_id+'", "tradeType": "产品/服务变更", "actorName": ""}'
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
            print(rs.content.decode('utf-8'))


    def run(self):
        self.login()
        self.into_frame()
        for content in read_xlsx(self.path, sheet_index=0, start_row=0):
            self.name, self.id, self.number = content
            print(self.name, self.id, self.number)
            try:
                self.open_school_service(self.name,self.number)
            except UnexpectedAlertPresentException:
                # print('sdf')
                self.result = '失败'
                write(self.name, self.id, self.number, self.result, self.record)
                ##                self.brow.execute_script("location.reload()")
                ##                WebDriverWait(self.brow,10,0.5).until(EC.alert_is_present()).dismiss()
                self.brow.switch_to.default_content()
            #     continue
            # except TimeoutException:
            #     self.result = '失败'
            #     write(self.name, self.id, self.number, self.result, self.record)
            #     ##                self.brow.execute_script("location.reload()")
            #     ##                WebDriverWait(self.brow, 10, 0.5).until(EC.alert_is_present()).dismiss()
            #     self.brow.switch_to.default_content()
            #     continue
            # except Exception as e:
            #     self.result = '失败' + e.__str__()
            #     write(self.name, self.id, self.number, self.result, self.record)
            #     self.brow.switch_to.default_content()
            #     continue

            self.result = '成功'
            write(self.name, self.id, self.number, self.result, self.record)


# Base='H4sIAAAAAAAAAHVSTUvDQBQsBf+H5CyY3SRN6m272aaRNqmbXaSnpdRQvQhWFFQ8eBIVP8CLoCCe9CCeevKgf8bUXvwP7sYkNELfcd7MvDdv9/WnsnBYqVQvqmdHGqPIJaKNuQhQh2grGsORwJv97WEcxaP9rUFM46G2lPFYr0sEDl1JBFAvUOSJiDApBjrQ/5cUY5/1MpnWWUshHhEqXL/ZzPEU7dLQ5ZgJ35UIlGYmMGExfZW7HhHhejpRSXKflA4AcPS6bpkQ2tByarIpez5qi4B3GoQqimMZpgF0G9b+pJhHrKQ2oe1Aw4Z12achZ0SQLqK41ZOU6edN8nhVbOMHzXA2elqLsiTDZ6Qzd6vMsQhuWGpaQNjseeUp1eHUftnDTMcfydvp98uFxBFjtMRWZIRxOYxl2CZwbAhzp7lJfa/FcqvBbun52ai/EReh1WDlIYEGRYGbi0xPh6VfIrGv9+fk9mR58nCZnD8l13eT+3FBiRhiPJKknb14dKAd/wLtWraalAIAAA=='
# Ext = {
#     "Common": {"ACTOR_NAME": "", "ACTOR_PHONE": "", "ACTOR_CERTTYPEID": "", "ACTOR_CERTNUM": "", "REMARK": ""},
#     "TF_B_TRADE_DISCNT": {
#         "ITEM": [
#             {
#                 "ID": "1118090542272586",
#                 "ID_TYPE": "1",
#                 "PRODUCT_ID": "20104142",
#                 "PACKAGE_ID": "19001024",
#                 "DISCNT_CODE": "99051112",
#                 "SPEC_TAG": "0",
#                 "MODIFY_TAG": "0",
#                 "START_DATE": "2018-10-01 00:00:00",
#                 "END_DATE": "2019-09-30 23:59:59",
#                 "RELATION_TYPE_CODE": "",
#                 "USER_ID_A": "-1", "ITEM_ID": ""
#             },
#             {
#                 "ID": "1118090542272586",
#                 "ID_TYPE": "1",
#                 "PRODUCT_ID": "20104142",
#                 "PACKAGE_ID": "19001025",
#                 "DISCNT_CODE": "19102407",
#                 "SPEC_TAG": "0",
#                 "MODIFY_TAG": "0",
#                 "START_DATE": "2018-09-13 22:52:14",
#                 "END_DATE": "2050-01-01 00:00:00",
#                 "RELATION_TYPE_CODE": "",
#                 "USER_ID_A": "-1",
#                 "ITEM_ID": ""
#             },
#             {"ID": "1118090542272586",
#              "ID_TYPE": "1",
#              "PRODUCT_ID": "20104142",
#              "PACKAGE_ID": "19001025",
#              "DISCNT_CODE": "19102923",
#              "SPEC_TAG": "0",
#              "MODIFY_TAG": "0",
#              "START_DATE": "2018-09-13 22:52:14",
#              "END_DATE": "2050-01-01 00:00:00",
#              "RELATION_TYPE_CODE": "",
#              "USER_ID_A": "-1", "ITEM_ID": ""
#              },
#             {"ID": "1118090542272586",
#              "ID_TYPE": "1",
#              "PRODUCT_ID": "20104142",
#              "PACKAGE_ID": "19001026",
#              "DISCNT_CODE": "19103204",
#              "SPEC_TAG": "0",
#              "MODIFY_TAG": "0",
#              "START_DATE": "2018-09-13 22:52:14",
#              "END_DATE": "2050-12-31 00:00:00",
#              "RELATION_TYPE_CODE": "",
#              "USER_ID_A": "-1",
#              "ITEM_ID": ""}
#         ]},
#     "TF_B_TRADE_OTHER": {
#         "ITEM": [
#             {
#                 "RSRV_VALUE_CODE": "NEXP",
#                 "RSRV_VALUE": "1118090542272586",
#                 "RSRV_STR1": "20104142",
#                 "RSRV_STR2": "00",
#                 "RSRV_STR3": "19001094",
#                 "RSRV_STR4": "4444",
#                 "RSRV_STR5": "undefined",
#                 "RSRV_STR6": "-1",
#                 "RSRV_STR7": "0",
#                 "RSRV_STR8": "",
#                 "RSRV_STR9": "4G02",
#                 "RSRV_STR10": "18534310726",
#                 "MODIFY_TAG": "1",
#                 "START_DATE": "2018-09-05 12:48:20",
#                 "END_DATE": "2018-09-13 22:52:14",
#                 "X_DATATYPE": "NULL"
#             },
#             {
#                 "RSRV_VALUE_CODE": "DLPK",
#                 "RSRV_VALUE": "1118090542272586",
#                 "RSRV_STR1": "20104142",
#                 "RSRV_STR2": "00",
#                 "RSRV_STR3": "19001094",
#                 "X_DATATYPE": "NULL"}]},
#     "TF_B_TRADE_USER": {
#         "ITEM": {
#             "PRODUCT_ID": "20104142",
#             "BRAND_CODE": "4G02",
#             "USER_ID": "1118090542272586",
#             "NET_TYPE_CODE": "10"}
#     },
#     "TF_B_TRADE": {
#         "PRODUCT_ID": "20104142",
#         "BRAND_CODE": "4G02",
#         "EXEC_TIME": "2018-09-13 22:52:14"
#     },
#     "TRADE_SUB_ITEM": {},
#     "MANYOU_TEMP": {
#         "ITEM": {"ManYouCreditTag": false}
#     },
#     "TRADE_ITEM": {
#         "DEVELOP_SUB_TYPE": "",
#         "DEVELOP_STAFF_ID": "",
#         "IS_TELEKET": "0",
#         "TELEKET_TYPE": "",
#         "DEVELOP_DEPART_ID": ""
#     }
# }



if __name__ == '__main__':
    change = Change()
    change.run()
