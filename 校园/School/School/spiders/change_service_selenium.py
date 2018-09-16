import time, os

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

    def open_school_service(self, number):
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
        WebDriverWait(self.brow, 30, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//img[contains(@onclick,"20104142")]')))


        # else:
        #     print('there')
        #     WebDriverWait(self.brow, 180, 0.5).until_not(
        #         EC.presence_of_element_located((By.XPATH, '//img[contains(@onclick,"20104142")]')))
        #     WebDriverWait(self.brow, 180, 0.5).until(
        #         EC.presence_of_element_located((By.XPATH, '//img[contains(@onclick,"20104142")]')))
        img_xiaoyuan = self.brow.find_element_by_xpath('//img[contains(@onclick,"20104142")]')
        self.brow.execute_script('arguments[0].click();', img_xiaoyuan)

        # 等待校园沃派畅视卡16元套餐下的各个包出现
        WebDriverWait(self.brow, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//div[@id="p20104142"]')))

    def judge_service(self):
        for i in range(15):  # 因为这个套餐下面有15个包，这种方式不太好，应该换成XPATH下有多少个tr标签来作为标准
            WebDriverWait(self.brow, 10, 0.5).until(EC.presence_of_element_located(
                (By.XPATH, '//div[@id="p20104142"]/table/tbody/tr[' + str(i + 1) + ']/td/fieldset/legend/span')))
            info = self.brow.find_element_by_xpath(
                '//div[@id="p20104142"]/table/tbody/tr[' + str(i + 1) + ']/td/fieldset/legend/span').text
            radio = self.brow.find_element_by_xpath(
                '//div[@id="p20104142"]/table/tbody/tr[' + str(i + 1) + ']/td/fieldset/legend/input')  # radio

            if info == '开卡送48元包':
                if not radio.is_selected():
                    self.brow.execute_script('arguments[0].click();', radio)

            elif info == '0元校区流量不限量包':
                if radio.is_selected():  # 这句话测试的时候给注释了，后面需要添加上！！！！！
                    self.brow.execute_script('arguments[0].click();', radio)

            elif info == '预存赠费活动包':
                if not radio.is_selected():
                    # open
                    WebDriverWait(self.brow, 10, 0.5).until(
                        EC.presence_of_element_located((By.XPATH, '//img[contains(@onclick,"19001024")]')))
                    zero_img = self.brow.find_element_by_xpath('//img[contains(@onclick,"19001024")]')
                    self.brow.execute_script('arguments[0].click();', zero_img)

                    WebDriverWait(self.brow, 10, 0.5).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@id="_p20104142k19001024e99051112TD"]')))
                    input = self.brow.find_element_by_xpath('//input[@id="_p20104142k19001024e99051112TD"]')
                    self.brow.execute_script('arguments[0].click();', input)

            elif info == '语音叠加包':
                if not radio.is_selected():
                    # open
                    WebDriverWait(self.brow, 10, 0.5).until(
                        EC.presence_of_element_located((By.XPATH, '//img[contains(@onclick,"19001025")]')))
                    tel_img = self.brow.find_element_by_xpath('//img[contains(@onclick,"19001025")]')
                    self.brow.execute_script('arguments[0].click();', tel_img)

                    # more
                    # WebDriverWait(self.brow, 10, 0.5).until(
                    #     EC.presence_of_element_located(
                    #         (By.XPATH, '//div[contains(@onclick,"D2010414219001025_tmptbl")]')))
                    # more_btn = self.brow.find_element_by_xpath(
                    #     '//div[contains(@onclick,"D2010414219001025_tmptbl")]')
                    # self.brow.execute_script('arguments[0].click();', more_btn)

                    # input
                    WebDriverWait(self.brow, 10, 0.5).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@id="_p20104142k19001025e19102923TD"]')))
                    input_1 = self.brow.find_element_by_xpath('//input[@id="_p20104142k19001025e19102923TD"]')
                    if not input_1.is_selected():
                        self.brow.execute_script('arguments[0].click();', input_1)
                    input_2 = self.brow.find_element_by_xpath('//input[@id="_p20104142k19001025e19102407TD"]')
                    if not input_2.is_selected():
                        self.brow.execute_script('arguments[0].click();', input_2)

            elif info == '流量叠加包':
                if not radio.is_selected():
                    # open
                    WebDriverWait(self.brow, 10, 0.5).until(
                        EC.presence_of_element_located((By.XPATH, '//img[contains(@onclick,"19001026")]')))
                    tel_img = self.brow.find_element_by_xpath('//img[contains(@onclick,"19001026")]')
                    self.brow.execute_script('arguments[0].click();', tel_img)

                    # more
                    # WebDriverWait(self.brow, 10, 0.5).until(
                    #     EC.presence_of_element_located(
                    #         (By.XPATH, '//div[contains(@onclick,"D2010414219001026_tmptbl")]')))
                    # more_btn = self.brow.find_element_by_xpath(
                    #     '//div[contains(@onclick,"D2010414219001026_tmptbl")]')
                    # self.brow.execute_script('arguments[0].click();', more_btn)

                    # input
                    WebDriverWait(self.brow, 10, 0.5).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@id="_p20104142k19001026e19103198TD"]')))
                    if self.brow.find_element_by_xpath('//input[@id="_p20104142k19001026e19103198TD"]').is_selected():
                        self.brow.find_element_by_xpath(
                            '//input[@id="_p20104142k19001026e19103198TD"]').click()  # 取消10元20G

                    input = self.brow.find_element_by_xpath(
                        '//input[@id="_p20104142k19001026e19103204TD"]')  # 添加10元100g
                    if not input.is_selected():
                        self.brow.execute_script('arguments[0].click();', input)

    def submit_service(self):
        WebDriverWait(self.brow, 10, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="submitTrade"]')))
        submit_btn = self.brow.find_element_by_xpath('//input[@id="submitTrade"]')
        self.brow.execute_script('arguments[0].click();', submit_btn)
        alert = WebDriverWait(self.brow, 180, 0.5).until(EC.alert_is_present())
        alert.accept()

    def charge_fee_submit(self):
        WebDriverWait(self.brow, 180, 0.5).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@name="feeframe"]')))
        fee = WebDriverWait(self.brow, 30, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="chargefee"]')))
        fee.clear()
        fee.send_keys('50.00')

        fee_submit_btn = WebDriverWait(self.brow, 30, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="continueTrade"]')))
        self.brow.execute_script('arguments[0].click();', fee_submit_btn)

        WebDriverWait(self.brow, 10, 0.5).until(EC.alert_is_present()).dismiss()
        WebDriverWait(self.brow, 10, 0.5).until(EC.alert_is_present()).accept()
        # time.sleep(1.5)
        WebDriverWait(self.brow, 10, 0.5).until(EC.alert_is_present()).accept()  # 一个或多个ACTIVEX无法显示
        # self.close_window()
        # WebDriverWait(self.brow, 10, 0.5).until(EC.alert_is_present()).accept()
        self.brow.switch_to.default_content()

    def close_window(self):
        handles_before = self.brow.window_handles
        WebDriverWait(self.brow, 180).until(
            lambda driver: len(driver.window_handles) == 2)
        print(self.brow.window_handles)
        for window in self.brow.window_handles:
            if window != handles_before[0]:
                self.brow.switch_to.window(window)
                WebDriverWait(self.brow, 180, 0.5).until(EC.frame_to_be_available_and_switch_to_it('contentframe'))
                continue_btn = WebDriverWait(self.brow, 30, 0.5).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@id="continueTrade"]')))
                self.brow.execute_script('arguments[0].click();', continue_btn)
                self.brow.switch_to.window(handles_before[0])
        print(self.brow.window_handles)

    def run(self):
        self.login()
        self.into_frame()
        for content in read_xlsx(self.path, sheet_index=0, start_row=0):
            self.name, self.id, self.number = content
            print(self.name, self.id, self.number)
            # time.sleep(1)
            try:
                self.open_school_service(self.number)
                self.judge_service()
                self.submit_service()
                self.charge_fee_submit()
            except UnexpectedAlertPresentException:
                # print('sdf')
                self.result = '失败'
                write(self.name, self.id, self.number, self.result, self.record)
                ##                self.brow.execute_script("location.reload()")
                ##                WebDriverWait(self.brow,10,0.5).until(EC.alert_is_present()).dismiss()
                self.brow.switch_to.default_content()
                continue
            except TimeoutException:
                self.result = '失败'
                write(self.name, self.id, self.number, self.result, self.record)
                ##                self.brow.execute_script("location.reload()")
                ##                WebDriverWait(self.brow, 10, 0.5).until(EC.alert_is_present()).dismiss()
                self.brow.switch_to.default_content()
                continue
            except Exception as e :
                self.result = '失败'+ e.__str__()
                write(self.name,self.id,self.number,self.result,self.record)
                self.brow.switch_to.default_content()
                continue
            # try:
            #
            # except Exception:
            #     self.result = '提交失败'
            #     write(self.name, self.id, self.number, self.result, self.record)
            #     self.brow.switch_to.default_content()
            #     continue
            #
            # try:
            #
            # except Exception:
            #     self.result = '提交费用失败'
            #     write(self.name, self.id, self.number, self.result, self.record)
            #     self.brow.switch_to.default_content()
            #     continue
            self.result = '成功'
            write(self.name, self.id, self.number, self.result, self.record)


if __name__ == '__main__':
    change = Change()
    change.run()
