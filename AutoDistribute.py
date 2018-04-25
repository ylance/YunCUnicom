from selenium import webdriver
from recevie_email import get_email_code
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time, datetime
import os
import winreg


def error_repeat(func):
    def inner(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except Exception as e:
            print(e)
            def alert_isexit():
                try:
                    alert_refresh = WebDriverWait(self.b, 3, 0.5).until(EC.alert_is_present())
                    return True, alert_refresh
                except TimeoutException as e:
                    return False, None
            flag_network, alert_network = alert_isexit()
            if flag_network:
                alert_network.accept()
            self.b.refresh()
            time.sleep(1)
            flag, alert_refreshed = alert_isexit()
            if flag:
                alert_refreshed.accept()
            time.sleep(1)
            inner(self, *args, **kwargs)
    return inner


def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')  # 利用系统的链表
    return winreg.QueryValueEx(key, "Desktop")[0]


def create_dir(create_path):
    if not os.path.exists(create_path):
        os.makedirs(create_path)
    return create_path


# def file_name(dir_name):
#     city_list = []
#     fns = [os.path.join(root, fn) for root, dirs, files in os.walk(dir_name) for fn in files]
#     for f in fns:
#         city_list.append(f)
#     return city_list


def read_file(file_name):
    import xlrd
    data = xlrd.open_workbook(file_name)
    table_names = data.sheet_names()
    districts = {}

    for name in table_names:
        districts[name] = []
        cols = data.sheet_by_name(name).ncols
        for i in range(cols):
            if '' in data.sheet_by_name(name).col_values(i):
                s = list(set(data.sheet_by_name(name).col_values(i)))
                s.remove('')
                districts[name].extend(s)
            else:
                districts[name].extend(data.sheet_by_name(name).col_values(i))
    return districts


#遍历Excel文件中每个标签的关键字是否在地址当中，并将每个关键字的结果存入list中，形式如：标签1：[False, False, False, False, False, False, False, False, False, False, False, False, False, False]
def keyword_isin(keywords, addr):
    return list(map(lambda x: True if x in addr else False, keywords))


def get_map_count(districts, addr):
    # print(districts)
    true_dict = {}
    addr_map_count = {'area': []}
    for k in districts.keys():
        # print(keyword_isin(districts[k],addr))
        true_dict[k] = keyword_isin(districts[k], addr)
        if True in true_dict[k]:
            addr_map_count['area'].append(k)
    return addr_map_count


class AutoDistrbute:

    def __init__(self):
        self.b = webdriver.Chrome()
        self.url = 'http://admin.mall.10010.com/'
        self.base_dir = create_dir(str(get_desktop())+'/自动调度/')
        self.rowth = 0
        self.invalid_record = []
        self.click_or_not = False
        self.count = 0

    def get_district_code(self):
        district_dic = {
            '140821': '赵晓艳',
            '140822': '卫颖',
            '140823': '陈萍',
            '140824': '杨英兰',
            '140825': '程燕',
            '140826': '高密脂',
            '140827': '王娟',
            '140828': '屈霞',
            '140829': '范恩生',
            '140830': '张芬娜',
            '140881': '张军丽',
            '140882': [self.base_dir + '/运城订单分配区域/河津.xlsx', '高秀萍'],
            '140802': [create_dir(self.base_dir + '运城订单分配区域/') + '城区.xlsx', '']
        }
        return district_dic

    def open(self):
        self.b.get(self.url)

    def is_not_visible(self, locator, timeout=60):
        try:
            WebDriverWait(self.b, timeout, 0.5).until_not(EC.visibility_of_element_located((By.CLASS_NAME, locator)))
            return True
        except TimeoutException:
            return False

    def element_isexist_xpath(self, xpath):
        try:
            WebDriverWait(self.b, 60, 0.5).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except Exception as e:
            return False

    def element_isexist_xpath_shrot_time(self,xpath):
        try:
            WebDriverWait(self.b, 3, 0.5).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except Exception as e:
            return False

    def login(self):
        # 登陆开始
        WebDriverWait(self.b, 60, 0.5).until(EC.presence_of_element_located((By.ID, "merchantId")))
        self.b.find_element_by_id("merchantId").send_keys('SXYC0044')
        WebDriverWait(self.b, 60, 0.5).until(EC.presence_of_element_located((By.ID, "merchantPwd")))
        self.b.find_element_by_id("merchantPwd").send_keys('wangning123')

        # todo 短信验证码开始
        WebDriverWait(self.b, 60, 0.5).until(EC.presence_of_element_located((By.ID, "phone")))
        self.b.find_element_by_id('phone').click()
        WebDriverWait(self.b, 60, 0.5).until(EC.presence_of_element_located((By.ID, "merchantSafetyCodeBtn")))
        email_button = self.b.find_element_by_id("merchantSafetyCodeBtn")
        email_button.click()

    def before_distribute(self):
        WebDriverWait(self.b, 180, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mainbBodyer"]/div[1]/div[1]/h3')))
        self.b.find_element_by_xpath('//*[@id="mainbBodyer"]/div[1]/div[1]/h3').click()
        WebDriverWait(self.b, 60, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mainbBodyer"]/div[1]/div[3]/h3')))
        select_button = self.b.find_element_by_xpath('//*[@id="mainbBodyer"]/div[1]/div[3]/h3')
        self.b.execute_script("arguments[0].click();", select_button)
        WebDriverWait(self.b, 60, 0.5).until(EC.presence_of_element_located((By.ID, "menu_5655")))
        distribute_link = self.b.find_element_by_id("menu_5655")
        self.b.execute_script("arguments[0].click();", distribute_link)

    def change_to_main_frame(self):
        WebDriverWait(self.b, 5, 0.5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'main')))
        self.is_not_visible("thickdiv")
        WebDriverWait(self.b, 60, 0.5).until(EC.presence_of_element_located((By.ID, "cityCode")))
        city = self.b.find_element_by_id("cityCode")
        Select(city).select_by_value("140800")
        self.is_not_visible("thickdiv")
        WebDriverWait(self.b, 60, 0.5).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="pageTable"]/tbody/tr/td/table[3]/tbody/tr/td/div[1]/span[2]/select')))
        page_size = self.b.find_element_by_xpath(
            '//*[@id="pageTable"]/tbody/tr/td/table[3]/tbody/tr/td/div[1]/span[2]/select')
        Select(page_size).select_by_value("20")
        time.sleep(1)

    def select_all(self,file,code,all_district):
        name = file[1] if code in ['140882'] else all_district[code]
        while self.element_isexist_xpath_shrot_time(
                '//*[@id="pageTable"]/tbody/tr/td/table[2]/tbody/tr/td/div[1]/table/tbody/tr/td[1]/input'):
            select_all = self.b.find_element_by_class_name("selectAll")
            time.sleep(1)
            self.b.execute_script("arguments[0].click();", select_all)
            self.click_or_not = True
            orgin_rowth = self.rowth
            changed_i = self.click_confirm(name)
            print(changed_i, orgin_rowth)
            if changed_i != orgin_rowth:
                self.rowth = 0
            continue

    def test(self, district_dict, distribute_dir='', district_name=''):
        self.rowth = 0
        table = WebDriverWait(self.b, 3, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pageTable"]/tbody/tr/td/table[2]')))
        write_list = []
        # print('HERE')
        while self.element_isexist_xpath_shrot_time('//*[@id="pageTable"]/tbody/tr/td/table[2]/tbody/tr/td/div[' + str(
                        self.rowth + 1) + ']/table/tbody/tr/td[4]/table/tbody/tr[3]/td'):
            self.click_or_not = False
            # print('opiqwuerowq')
            if self.rowth >= 19:
                self.rowth = 0
                temp = self.b.find_element_by_xpath(
                    '//*[@id="pageTable"]/tbody/tr/td/table[3]/tbody/tr/td/div[1]/span[5]')
                self.b.execute_script("arguments[0].click();", temp)
                self.is_not_visible("thickdiv")
                time.sleep(3)
                continue
            addr_orgin = \
                self.b.find_element_by_xpath('//*[@id="pageTable"]/tbody/tr/td/table[2]/tbody/tr/td/div[' + str(
                    self.rowth + 1) + ']/table/tbody/tr/td[4]/table/tbody/tr[3]/td').text.split(',')[-1]
            addr = addr_orgin if '街道' not in addr_orgin else addr_orgin.split('街道')[-1]
            addr_map = get_map_count(district_dict, addr)
            print(addr_orgin)
            if len(addr_map['area']) == 1:
                billing_no = self.b.find_element_by_xpath(
                    '//*[@id="pageTable"]/tbody/tr/td/table[2]/tbody/tr/td/div[' + str(
                        self.rowth + 1) + ']/table/tbody/tr/td[2]/table/tbody/tr[1]/td').text.split('：')[-1]
                commodity = self.b.find_element_by_xpath(
                    '//*[@id="pageTable"]/tbody/tr/td/table[2]/tbody/tr/td/div[' + str(
                        self.rowth + 1) + ']/table/tbody/tr/td[4]/table/tbody/tr[1]/td').text.split('：')[-1]
                scheduled_no = self.b.find_element_by_xpath(
                    '//*[@id="pageTable"]/tbody/tr/td/table[2]/tbody/tr/td/div[' + str(
                        self.rowth + 1) + ']/table/tbody/tr/td[4]/table/tbody/tr[2]/td').text.split('(')[0]
                # print(billing_no, commodity, scheduled_no, addr_orgin)
                write_list.append(billing_no + ' ' + commodity + ' ' + scheduled_no + ' ' + addr_orgin + '\n')
                time.sleep(0.8)
                if billing_no not in self.invalid_record:
                    temp = self.b.find_element_by_xpath('//*[@id="pageTable"]/tbody/tr/td/table[2]/tbody/tr/td/div[' + str(
                        self.rowth + 1) + ']/table/tbody/tr/td[1]/input')
                    self.b.execute_script("arguments[0].click();", temp)
                    self.count += 1
                    self.click_or_not = True
                    self.invalid_record.append(billing_no)

                div_list = table.find_elements_by_tag_name('div')
                for j in range(self.rowth + 1, len(div_list)):
                    addr_sibling_orgin = \
                        self.b.find_element_by_xpath('//*[@id="pageTable"]/tbody/tr/td/table[2]/tbody/tr/td/div[' + str(
                            j + 1) + ']/table/tbody/tr/td[4]/table/tbody/tr[3]/td').text.split(',')[-1]

                    addr_sibling = addr_sibling_orgin if '街道' not in addr_sibling_orgin else \
                        addr_sibling_orgin.split('街道')[-1]
                    addr_sibling_map = get_map_count(district_dict, addr_sibling)
                    print(addr_map['area'], addr_sibling_map['area'])
                    if len(addr_sibling_map['area']) == 1 and addr_map['area'] == addr_sibling_map[
                        'area']:
                        billing_no_sibling = self.b.find_element_by_xpath(
                            '//*[@id="pageTable"]/tbody/tr/td/table[2]/tbody/tr/td/div[' + str(
                                j + 1) + ']/table/tbody/tr/td[2]/table/tbody/tr[1]/td').text.split('：')[-1]
                        commodity_sibling = self.b.find_element_by_xpath(
                            '//*[@id="pageTable"]/tbody/tr/td/table[2]/tbody/tr/td/div[' + str(
                                j + 1) + ']/table/tbody/tr/td[4]/table/tbody/tr[1]/td').text.split('：')[-1]
                        scheduled_no_sibling = self.b.find_element_by_xpath(
                            '//*[@id="pageTable"]/tbody/tr/td/table[2]/tbody/tr/td/div[' + str(
                                j + 1) + ']/table/tbody/tr/td[4]/table/tbody/tr[2]/td').text.split('(')[0]
                        write_list.append(billing_no_sibling + ' ' + commodity_sibling + ' ' + scheduled_no_sibling + ' ' + addr_sibling_orgin + '\n')
                        WebDriverWait(self.b, 5, 0.5).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="pageTable"]/tbody/tr/td/table[2]/tbody/tr/td/div[' + str(
                                j + 1) + ']/table/tbody/tr/td[1]/input')))
                        temp = self.b.find_element_by_xpath(
                            '//*[@id="pageTable"]/tbody/tr/td/table[2]/tbody/tr/td/div[' + str(
                                j + 1) + ']/table/tbody/tr/td[1]/input')
                        time.sleep(0.8)
                        if billing_no_sibling not in self.invalid_record:
                            self.invalid_record.append(billing_no_sibling)
                            self.b.execute_script("arguments[0].click();", temp)
                orgin_rowth = self.rowth
                changed_i = self.click_confirm(addr_map['area'][0],distribute_dir,district_name,write_list)
                print(changed_i, orgin_rowth)
                if changed_i != orgin_rowth:
                    self.rowth = 0
                    continue
                self.rowth = 0
            else:
                self.rowth += 1
                if not self.element_isexist_xpath_shrot_time(
                    '//*[@id="pageTable"]/tbody/tr/td/table[2]/tbody/tr/td/div[' + str(
                        self.rowth + 1) + ']/table/tbody/tr/td[4]/table/tbody/tr[3]/td'):
                    print('over')
                    break

    def click_confirm(self, input_name,distribute_dir='',district_name='',write_list=[]):
        WebDriverWait(self.b, 60, 0.5).until(EC.element_to_be_clickable((
            By.XPATH, '//*[@id="pageTable"]/tbody/tr/td/table[3]/tbody/tr/td/input[3]')))
        distribute = self.b.find_element_by_xpath('//*[@id="pageTable"]/tbody/tr/td/table[3]/tbody/tr/td/input[3]')
        print(self.click_or_not)
        if self.click_or_not is True:
            self.b.execute_script("arguments[0].click();", distribute)
            self.is_not_visible('thickdiv')
            self.b.switch_to.default_content()

            if self.element_isexist_xpath_shrot_time('//*[@id="pop_div"]'):
                self.b.find_element_by_xpath('//*[@id="pop_comfirm"]').click()
                self.is_not_visible('thickdiv')
                WebDriverWait(self.b, 30, 0.5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'main')))
            else:
                WebDriverWait(self.b, 30, 0.5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'coverlayer')))
                WebDriverWait(self.b, 30, 0.5).until(EC.presence_of_element_located((By.ID, 'searchText')))
                self.b.find_element_by_id("searchText").send_keys(input_name)
                time.sleep(1)
                WebDriverWait(self.b, 30, 0.5).until(EC.presence_of_element_located((By.ID, 'searchBtn')))
                self.b.find_element_by_id("searchBtn").click()
                time.sleep(1)
                self.is_not_visible('modal')

                try:
                    WebDriverWait(self.b, 5, 0.5).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[ @ id = "showDespatcherPage"]/tbody/tr/td/table[2]/tbody/tr/td/div/ul/li')))
                except TimeoutException as e:
                    self.b.find_element_by_id("hrefImgClose").click()
                    self.b.switch_to.default_content()
                    self.is_not_visible('thickdiv')
                    WebDriverWait(self.b, 30, 0.5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'main')))
                    if distribute_dir != '' and district_name != ''and write_list != []:
                        distribute_record = open(distribute_dir + '/' + district_name + '.txt', 'a')
                        for record in set(write_list):
                            distribute_record.write(record)
                        distribute_record.write('以上订单将要派给：' + input_name + ',但'+input_name+"没有开接单。")
                        write_list.clear()
                        distribute_record.close()
                    time.sleep(1.5)
                    self.rowth += 1
                    return self.rowth

                temp = self.b.find_element_by_xpath(
                    '//*[ @ id = "showDespatcherPage"]/tbody/tr/td/table[2]/tbody/tr/td/div/ul/li')
                time.sleep(1)
                name = self.b.find_element_by_xpath(
                    '//*[@id="showDespatcherPage"]/tbody/tr/td/table[2]/tbody/tr/td/div/ul/li/div[1]'
                ).text
                tel = self.b.find_element_by_xpath('//*[@id="showDespatcherPage"]/tbody/tr/td/table[2]/tbody/tr/td/div/ul/li[1]/div[2]/span[1]').text

                # print(name, tel, input_name)
                while input_name not in name and tel not in input_name:
                    WebDriverWait(self.b, 30, 0.5).until(EC.presence_of_element_located((By.ID, 'searchText')))
                    input_text = self.b.find_element_by_id("searchText")
                    input_text.clear()
                    input_text.send_keys(input_name)
                    WebDriverWait(self.b, 30, 0.5).until(EC.presence_of_element_located((By.ID, 'searchBtn')))
                    self.b.find_element_by_id("searchBtn").click()
                    self.is_not_visible('modal')
                    time.sleep(2)
                    name = self.b.find_element_by_xpath(
                        '//table[@id="showDespatcherPage"]/tbody/tr/td/table[2]/tbody/tr/td/div/ul/li[1]/div[1]').text
                    tel = self.b.find_element_by_xpath(
                        '//*[@id="showDespatcherPage"]/tbody/tr/td/table[2]/tbody/tr/td/div/ul/li[1]/div[2]/span[1]').text
                self.b.execute_script("arguments[0].click();", temp)

                finished = len(write_list)
                if distribute_dir != '' and district_name != '' and write_list != []:
                    distribute_record = open(distribute_dir + '/' + district_name + '.txt', 'a')
                    for record in set(write_list):
                        distribute_record.write(record)
                    distribute_record.write('以上订单派给了：'+name + '\n\n')
                    write_list.clear()
                    distribute_record.close()

                for i in range(finished):
                    self.invalid_record.pop()

                time.sleep(1)
                self.b.find_element_by_class_name('sureRelease').click()
                self.is_not_visible('thickdiv')
                self.b.switch_to.default_content()
                self.is_not_visible('thickdiv')
                WebDriverWait(self.b, 60, 0.5).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="pop_comfirm"]')))
                self.b.find_element_by_xpath('//*[@id="pop_comfirm"]').click()
                self.is_not_visible('thickdiv')
                WebDriverWait(self.b, 30, 0.5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'main')))
                time.sleep(1)

    def process_district(self):
        all_district = self.get_district_code()
        distribute_dir = create_dir(self.base_dir+'调度记录/' + str(datetime.date.today()))
        for code, file in all_district.items():
            WebDriverWait(self.b, 60, 0.5).until(EC.presence_of_element_located((By.ID, "districtCode")))
            district = self.b.find_element_by_id('districtCode')
            Select(district).select_by_value(code)
            WebDriverWait(self.b, 60, 0.5).until(EC.presence_of_element_located((
                By.XPATH, '/html/body/table/tbody/tr[2]/td[6]/input[1]')))
            self.b.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[6]/input[1]').click()
            self.is_not_visible("thickdiv")

            if file[0].endswith('.xlsx'):
                district_dict = read_file(file[0])
                district_name = file[0].split('/')[-1].split('.')[0] if file[0].find('/') else file[0].split('\\')[-1].split('.')[0]
                print('sdfdsf')
                print(district_dict)
                self.test(district_dict, distribute_dir, district_name)
                if code == '140802':
                    self.b.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[6]/input[1]').click()
                    self.is_not_visible("thickdiv")
                    admin_file = read_file(create_dir(self.base_dir + '运城订单分配区域/') + '盐湖区.xlsx')
                    self.rowth = 0
                    self.test(admin_file)
                else:
                    self.select_all(file, code, all_district)
            else:
                self.select_all(file, code, all_district)

    @error_repeat
    def main_process(self):
        self.change_to_main_frame()
        self.process_district()


if __name__ == "__main__":
    auto = AutoDistrbute()
    auto.open()
    auto.login()
    auto.before_distribute()
    auto.main_process()
    auto.b.quit()


