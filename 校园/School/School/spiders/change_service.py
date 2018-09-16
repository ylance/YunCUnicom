import requests

from lxml import etree


# url = 'http://133.128.6.186:8080/custserv?service=swallow/pub.chkcust.MainChkCust/queryCustAuth/1'
# headers = {
#     'X-Requested-With': 'XMLHttpRequest',
# 'X-Prototype-Version': '1.5.1',
# 'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
# 'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
# 'Referer': 'http://133.128.6.186:8080/',
# 'Accept-Language': 'zh-cn',
# 'Accept-Encoding': 'gzip, deflate',
# 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)',
# 'Host': '133.128.6.186:8080',
# 'Connection': 'Keep-Alive',
# 'Pragma': 'no-cache',
# 'Cookie': 'LOGIN_STAFF_IDBSS=YCZY0884; LOGIN_SUBSYS_CODEBSS=CRM; BSS_BSS_ACCTMANM_JSESSIONID=RQvqbSnGytCD3qFCvZsJyzwPBgVN1svJvNB4X6pZRXG3bHhc9LWz!1050168802!-2096381672; BSS_BSS_STATSERV_JSESSIONID=KGPnbSMWzqzVJSYy0DxxLmZMgb1Gxy088VRpSVYx15MdbDmG64pp!76779210!-1192166273; BSS_SYSMANM_JSESSIONID=8YhkbSMXjTSp2CjnhC6xryn0G3pXWSmnjFySc1hp5Jbhkn3p1bGz!-269914159!-1433269564; BSS_RESMANM_JSESSIONID=pCZKbSMX692DkJKQNrcWF8lsNvJ6mpvC9pphLTvMp2lVQ7Z1dJSv!1101795391!1672713234; BSS_BSS_SALEMANM_JSESSIONID=yPpvbSMXCW9nmdhQ26CRL2Y3WNNf1S1YsKWvfT4MMRh3yn0mZ22C!2061263565!159647921; BSS_BSS_CUSTMANM_JSESSIONID=vszGbSMXpSvJ9vSRmG3wtK5KpN5Qqg113ngJntQs6N8JLN2QYmYJ!-705794729!-1850198033; BSS_CHNLMANM_JSESSIONID=nHsZbSMXJDnhWYswR7yynhjVcty297Wx6pKrg0D3XXL8sDvK4bnk!-798000933!112363500; BSS_BSS_JSESSIONID=FRVWbSPfycQLwqdnGfyfFflyJfVGcL5G9mZhDf5gpGQjpjsrzmwv!-476549662!1407862710; BSS_BSS_CUSTSERV_JSESSIONID=Yq7gbSQW7mFqKl9sWrDxxSt0GXcD9jyDKs1KpvMn1QTJKgLlTHJ4!-234211607!755799831'
# }
#
# data = {
#     'touchId':'',
#     'serialNumber':'17635292945',
#     'netTypeCode':'',
#     'rightCode':'',
#     'csChangeServiceTrade':''
# }
#
# rs = requests.post(url=url,data=data,headers=headers)
# xml_rs = etree.fromstring(rs.content)
# print(xml_rs.xpath('//data/@userId')[0].encode('utf-8').decode('utf-8'))
# if xml_rs.xpath('//data/@userId')[0].encode('utf-8').decode('utf-8') != '':  # xpah[0] 是个 _ElementUnicodeResult 是unicode的子类，需要变成二进制，然后再转换成unicode
#     pass
# else:
#     pass   # 该号码没有激活。

# Ext={"Common": {"ACTOR_NAME": "", "ACTOR_PHONE": "", "ACTOR_CERTTYPEID": "", "ACTOR_CERTNUM": "", "REMARK": ""},
# "TF_B_TRADE_DISCNT": {"ITEM": [{"ID": "1118090542275670", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001024", "DISCNT_CODE": "99051111", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "2018-10-01 00:00:00", "END_DATE": "2019-09-30 23:59:59", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""},
#                                {"ID": "1118090542275670", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001025", "DISCNT_CODE": "19102407", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "2018-09-07 16:37:19", "END_DATE": "2050-01-01 00:00:00", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""},
#                                {"ID": "1118090542275670", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001025", "DISCNT_CODE": "19102923", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "2018-09-07 16:37:19", "END_DATE": "2050-01-01 00:00:00", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""},
#                                {"ID": "1118090542275670", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001026", "DISCNT_CODE": "19103198", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "2018-09-07 16:37:19", "END_DATE": "2050-01-01 00:00:00", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""}]},
# "TF_B_TRADE_USER":   {"ITEM": {"PRODUCT_ID": "20104142", "BRAND_CODE": "4G02", "USER_ID": "1118090542275670", "NET_TYPE_CODE": "10"}},
#                 "TF_B_TRADE": {"PRODUCT_ID": "20104142", "BRAND_CODE": "4G02", "EXEC_TIME": "2018-09-07 16:37:19"},
#             "TRADE_SUB_ITEM": {}, "MANYOU_TEMP": {"ITEM": {"ManYouCreditTag": false}},
#                 "TRADE_ITEM": {"DEVELOP_SUB_TYPE": "", "DEVELOP_STAFF_ID": "", "IS_TELEKET": "0", "TELEKET_TYPE": "", "DEVELOP_DEPART_ID": ""}}



# Ext={"Common": {"ACTOR_NAME": "", "ACTOR_PHONE": "", "ACTOR_CERTTYPEID": "", "ACTOR_CERTNUM": "", "REMARK": ""},
# "TF_B_TRADE_DISCNT": {"ITEM": [{"ID": "1117090640337878", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001026", "DISCNT_CODE": "19102935", "SPEC_TAG": "0", "MODIFY_TAG": "1", "START_DATE": "2017-12-08 19:14:01", "END_DATE": "2018-09-07 18:57:05", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": "1117120808215994"},
#                                {"ID": "1117090640337878", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001026", "DISCNT_CODE": "19103201", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "2018-09-07 18:57:05", "END_DATE": "2050-01-01 00:00:00", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""},
#                                {"ID": "1117090640337878", "ID_TYPE": "1", "PRODUCT_ID": "20104142", "PACKAGE_ID": "19001087", "DISCNT_CODE": "99051060", "SPEC_TAG": "0", "MODIFY_TAG": "0", "START_DATE": "2018-09-07 18:57:05", "END_DATE": "2018-11-30 23:59:59", "RELATION_TYPE_CODE": "", "USER_ID_A": "-1", "ITEM_ID": ""}]},
# "TF_B_TRADE_USER":   {"ITEM": {"PRODUCT_ID": "20104142", "BRAND_CODE": "4G02", "USER_ID": "1117090640337878", "NET_TYPE_CODE": "10"}},
#                 "TF_B_TRADE": {"PRODUCT_ID": "20104142", "BRAND_CODE": "4G02", "EXEC_TIME": "2018-09-07 18:57:05"},
#             "TRADE_SUB_ITEM": {}, "MANYOU_TEMP": {"ITEM": {"ManYouCreditTag": false}},
#                 "TRADE_ITEM": {"DEVELOP_SUB_TYPE": "", "DEVELOP_STAFF_ID": "", "IS_TELEKET": "0", "TELEKET_TYPE": "", "DEVELOP_DEPART_ID": ""}}

"""
<data packageTypeCode="3" modifyTag="9" productId="20104142" userId="1117090640337878" productName="校园沃派畅视卡16元套餐" xLastResultinfo="" xLastResultcode="0" xLcuTxdservCount="0" xResultinfo="OK!" packageInvalid="0" packageId="19001019" packageName="流量放心用混合包" xResultcode="0" xRecordnum="7" />
<data packageTypeCode="2" modifyTag="9" productId="20104142" userId="1117090640337878" productName="校园沃派畅视卡16元套餐" xLastResultinfo="" xLastResultcode="" xLcuTxdservCount="" xResultinfo="" packageInvalid="0" packageId="19001025" packageName="语音叠加包" xResultcode="" xRecordnum="" />
<data packageTypeCode="2" modifyTag="9" productId="20104142" userId="1117090640337878" productName="校园沃派畅视卡16元套餐" xLastResultinfo="" xLastResultcode="" xLcuTxdservCount="" xResultinfo="" packageInvalid="0" packageId="19001026" packageName="流量叠加包" xResultcode="" xRecordnum="" />
<data packageTypeCode="2" modifyTag="9" productId="20104142" userId="1117090640337878" productName="校园沃派畅视卡16元套餐" xLastResultinfo="" xLastResultcode="" xLcuTxdservCount="" xResultinfo="" packageInvalid="0" packageId="19001088" packageName="16元套餐赠送国内流量包" xResultcode="" xRecordnum="" />
<data packageTypeCode="2" modifyTag="9" productId="20104142" userId="1117090640337878" productName="校园沃派畅视卡16元套餐" xLastResultinfo="" xLastResultcode="" xLcuTxdservCount="" xResultinfo="" packageInvalid="0" packageId="19001094" packageName="0元校区流量不限量包" xResultcode="" xRecordnum="" />
<data packageTypeCode="4" modifyTag="9" productId="20104142" userId="1117090640337878" productName="校园沃派畅视卡16元套餐" xLastResultinfo="" xLastResultcode="" xLcuTxdservCount="" xResultinfo="" packageInvalid="0" packageId="19100011" packageName="校园沃派流量王服务包" xResultcode="" xRecordnum="" />
<data packageTypeCode="2" modifyTag="9" productId="20104142" userId="1117090640337878" productName="校园沃派畅视卡16元套餐" xLastResultinfo="" xLastResultcode="" xLcuTxdservCount="" xResultinfo="" packageInvalid="0" packageId="20104142" packageName="校园沃派畅视卡16元套餐资费包" xResultcode="" xRecordnum="" />
<data packageTypeCode="2" rsrvStr2="" defaultTag="0" rsrvStr1="" modifyTag="0" productId="20104142" forceTag="0" needExp="1" endDate="2050-01-01 00:00:00" updateTime="2017-12-19 10:43:49" maxNumber="1" eparchyCode="ZZZZ" packageInvalid="0" startDate="2017-12-19 00:00:00" itemIndex="1004" updateDepartId="00000" packageDesc="无限畅视包月套餐包" minNumber="1" packageId="19003632" packageName="无限畅视包月套餐包" updateStaffId="SUPERUSR" />
<data packageTypeCode="2" rsrvStr2="" defaultTag="0" rsrvStr1="" modifyTag="0" productId="20104142" forceTag="0" needExp="0" endDate="2050-01-01 00:00:00" updateTime="2017-08-18 14:46:34" maxNumber="1" eparchyCode="ZZZZ" packageInvalid="0" startDate="2017-08-18 00:00:00" itemIndex="1007" updateDepartId="00000" packageDesc="预存赠费活动包" minNumber="1" packageId="19001024" packageName="预存赠费活动包" updateStaffId="SUPERUSR" />
<data packageTypeCode="2" rsrvStr2="" defaultTag="0" rsrvStr1="" modifyTag="0" productId="20104142" forceTag="0" needExp="1" endDate="2050-01-01 00:00:00" updateTime="2017-08-09 17:22:30" maxNumber="-1" eparchyCode="ZZZZ" packageInvalid="0" startDate="2017-08-09 00:00:00" itemIndex="2000" updateDepartId="00000" packageDesc="开卡送48元包" minNumber="-1" packageId="19001087" packageName="开卡送48元包" updateStaffId="SUPERUSR" />
<data packageTypeCode="2" rsrvStr2="" defaultTag="0" rsrvStr1="" modifyTag="0" productId="20104142" forceTag="0" needExp="1" endDate="2050-01-01 00:00:00" updateTime="2017-08-09 17:22:30" maxNumber="-1" eparchyCode="ZZZZ" packageInvalid="0" startDate="2017-08-09 00:00:00" itemIndex="2000" updateDepartId="00000" packageDesc="开卡送16元包" minNumber="-1" packageId="19001016" packageName="开卡送16元包" updateStaffId="SUPERUSR" />
<data packageTypeCode="2" rsrvStr2="" defaultTag="0" rsrvStr1="" modifyTag="0" productId="20104142" forceTag="0" needExp="0" endDate="2050-01-01 00:00:00" updateTime="2017-07-26 17:22:30" maxNumber="-1" eparchyCode="ZZZZ" packageInvalid="0" startDate="2017-07-26 00:00:00" itemIndex="2000" updateDepartId="00000" packageDesc="校园流量叠加包" minNumber="-1" packageId="19001018" packageName="校园流量叠加包" updateStaffId="SUPERUSR" />
<data packageTypeCode="2" rsrvStr2="" defaultTag="0" rsrvStr1="" modifyTag="0" productId="20104142" forceTag="0" needExp="1" endDate="2050-01-01 00:00:00" updateTime="2017-07-28 17:24:23" maxNumber="1" eparchyCode="ZZZZ" packageInvalid="0" startDate="2017-07-28 00:00:00" itemIndex="3500" updateDepartId="00000" packageDesc="存费送通用券包" minNumber="1" packageId="19001098" packageName="存费送通用券包" updateStaffId="SUPERUSR" />
<data packageTypeCode="2" rsrvStr2="" defaultTag="0" rsrvStr1="" modifyTag="0" productId="20104142" forceTag="0" needExp="1" endDate="2050-01-01 00:00:00" updateTime="2017-08-11 15:16:03" maxNumber="1" eparchyCode="ZZZZ" packageInvalid="0" startDate="2017-08-11 00:00:00" itemIndex="4200" updateDepartId="00000" packageDesc="16元套餐活动包" minNumber="1" packageId="19001101" packageName="16元套餐活动包" updateStaffId="SUPERUSR" />
<data packageTypeCode="2" rsrvStr2="" defaultTag="0" rsrvStr1="" modifyTag="0" productId="20104142" forceTag="0" needExp="1" endDate="2050-01-01 00:00:00" updateTime="2017-08-18 15:18:56" maxNumber="-1" eparchyCode="ZZZZ" packageInvalid="0" startDate="2017-08-18 00:00:00" itemIndex="6000" updateDepartId="00000" packageDesc="5元校区流量不限量包" minNumber="-1" packageId="19001095" packageName="5元校区流量不限量包" updateStaffId="SUPERUSR" />
"""
''
'http://133.128.6.186:8080/custserv?service=ajaxDirect/1/personalserv.changeelement.ChangeElement/personalserv.changeelement.ChangeElement/javascript/Actor_Base_Part_&pagename=personalserv.changeelement.ChangeElement&eventname=initCustType&&CUST_ID=&SERIAL_NUMBER=18635985316&staffId=YCZY0884&departId=0CC7B&subSysCode=custserv&eparchyCode=0359&partids=Actor_Base_Part_&random=2018981272738&ajaxSubmitType=get'
'H4sIAAAAAAAAAFvzloG1fArDpGqlkCBHF9d4H+fQeD9HX1clK6UQ5+B454zEvPTU4NSisszk1KDUdCUdqLqQyADXeGd/F6BCQyMDHaUgT3ePEKiAUnIxir6QosSUVKDOIP/QENd41wDHIGePSKCyF/snPJ3fBzcyOMQxJDQYKJ6Zl1miVAsAg3v5u5oAAAA="/>'
'H4sIAAAAAAAAAFvzloG1fArDpGqlkCBHF9d4H+fQeD9HX1clK6UQ5+B454zEvPTU4NSisszk1KDUdCUdqLqQyADXeGd/F6BCQyMDHaUg/9AQ13jXAMcgZ49IoOYX+yc8nd8HVB7k6e4RAlWplFyMYmBIUWJKKtzI4BDHkNBgoKrMvMwSpVoAXn48tpoAAAA='
'H4sIAAAAAAAAAFvzloG1fArDpGqlkCBHF9d4H+fQeD9HX1clK6UQ5+B454zEvPTU4NSisszk1KDUdCUdqLqQyADXeGd/F6BCQyMDHaUg/9AQ13jXAMcgZ49IoOYX+yc8nd8HVB7k6e4RAlWplFyMYmBIUWJKKtzI4BDHkNBgoKrMvMwSpVoAXn48tpoAAAA='

'H4sIAAAAAAAAAHVSTUvDQBAtBf+H5CyYzyb1tt1s00ib1M0E6WkpNVQvghUFFQ8eVbSCF0FBPXnxphdF8c+Yogf/g5OYhEboHN+892be7D7+VOb2K5XqafX4QAJObCbaNBQe6TBpSQIaCLre3xxGQTTa3RhEPBpKCxkPel0mqG8jUVHlAiWOCBigWJEV+X+hmLrQy2RSZyWFwoBxYbvNZo6naJf7dkhBuDYiKprpiq4W05dD22HCX00nJpLcJ6UrimLKdbmmy5pmWqaFTey5pC28sNNgPKEYhmpYlqKZ5p+UhgFMqS3ZUmuaodb0pM/9EJhgXcJpq4eUr4+L+Pa82Mb1mv509LTmsZDhAuvM3CpzLIJrRh1Rj8H0efGUyeGS/bKHid/uJk/v3y9jxAkAL7ETMqEUykMxSt3QNCN3mpnUdVqQWw22S88Po/5aVIROBiceCDQ48excpDuyWvoliH2+PsSXR4uTm7P45D4eX02unwtKAATCAElbO9FoTzr8BTnIR/qUAgAA'
'H4sIAAAAAAAAAFvzloG1fArDpGqlkCBHF9d4H%2BfQeD9HX1clK6UQ5%2BB454zEvPTU4NSisszk1KDUdCUdqLqQyADXeGd%2FF6BCQyMDHaUg%2F9AQ13jXAMcgZ49IoOYX%2Byc8nd8HVB7k6e4RAlWplFyMYmBIUWJKKtzI4BDHkNBgoKrMvMwSpVoAXn48tpoAAAA%3D'
'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"/>'
#  201897232521170

# import execjs
# random_path = r'D:\Development\Pycharm\Workspace\School\School\utils\random.js'
# random = execjs.compile(open(random_path, encoding='utf-8').read()).call('getRandomParam')
# url = 'http://133.128.6.186:8080/custserv?service=ajaxDirect/1/personalserv.changeelement.ChangeElement/personalserv.changeelement.ChangeElement/javascript/Actor_Base_Part_&pagename=personalserv.changeelement.ChangeElement&eventname=initCustType&&CUST_ID=&SERIAL_NUMBER=15525881377&staffId=YCZY0884&departId=0CC7B&subSysCode=custserv&eparchyCode=0359&partids=Actor_Base_Part_&random={random}&ajaxSubmitType=get HTTP/1.1'.format(random=random)
#
# headers ={
    # 'X-Requested-With': 'XMLHttpRequest',
# 'X-Prototype-Version': '1.5.1',
# 'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
# 'Referer': 'http://133.128.6.186:8080/',
# 'Accept-Language': 'zh-cn',
# 'Accept-Encoding': 'gzip, deflate',
# 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
# 'Host': '133.128.6.186:8080',
# 'Connection': 'Keep-Alive',
# 'Cookie': 'LOGIN_STAFF_IDBSS=YCZY0884; LOGIN_SUBSYS_CODEBSS=CRM; __guid=221721176.840067343969089200.1536318815165.4204; monitor_count=1; BSS_BSS_JSESSIONID=Qw7DbSFbf06G5pn5C7L13NzzHvfZXRpvyMDQjWRwXMT1hby4zF1H!-1702348738!1536362037; BSS_BSS_CUSTSERV_JSESSIONID=hFJcbSFG7RZhyxLQRJ1D9pLrQShbMjMc5p86Hzmjp9pJnTn8W19N!-1807624111!944341557'
# }
# 'H4sIAAAAAAAAAHVSTUvDQBAtBf%2BH5CyYzyb1tt1s00ib1M0E6WkpNVQvghUFFQ8eVbSCF0FBPXnxphdF8c%2BYogf%2Fg5OYhEboHN%2B892be7D7%2BVOb2K5XqafX4QAJObCbaNBQe6TBpSQIaCLre3xxGQTTa3RhEPBpKCxkPel0mqG8jUVHlAiWOCBigWJEV%2BX%2BhmLrQy2RSZyWFwoBxYbvNZo6naJf7dkhBuDYiKprpiq4W05dD22HCX00nJpLcJ6UrimLKdbmmy5pmWqaFTey5pC28sNNgPKEYhmpYlqKZ5p%2BUhgFMqS3ZUmuaodb0pM%2F9EJhgXcJpq4eUr4%2BL%2BPa82Mb1mv509LTmsZDhAuvM3CpzLIJrRh1Rj8H0efGUyeGS%2FbKHid%2FuJk%2Fv3y9jxAkAL7ETMqEUykMxSt3QNCN3mpnUdVqQWw22S88Po%2F5aVIROBiceCDQ48excpDuyWvoliH2%2BPsSXR4uTm7P45D4eX02unwtKAATCAElbO9FoTzr8BTnIR%2FqUAgAA'
# rs= requests.get(url,headers=headers)
# print(rs.content.decode('gbk'))

# 'http://133.128.6.186:8080/custserv?service=ajaxDirect/1/personalserv.changeelement.ChangeElement/personalserv.changeelement.ChangeElement/javascript/Actor_Base_Part_&pagename=personalserv.changeelement.ChangeElement&eventname=initCustType&&CUST_ID=&SERIAL_NUMBER=15525881377&staffId=YCZY0884&departId=0CC7B&subSysCode=custserv&eparchyCode=0359&partids=Actor_Base_Part_&random=20189723386895&ajaxSubmitType=get'