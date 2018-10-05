import json, os

from collections import OrderedDict

import scrapy, requests
from scrapy import FormRequest
from MallAuto.face_contrast import face_contrast
from MallAuto.utiles import read_xlsx, write, create_dir, get_desktop, getcookiefromchrome

headers = {
    'Host': 'admin.mall.10010.com',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Origin': 'http://admin.mall.10010.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://admin.mall.10010.com/OdmQuery/ServiceOrderQuery/init',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# cookies = {
#     '_n3fa_cid': 'c0927d16fc204d8c95e8be31a195577e', ' _n3fa_ext': 'ft=1537701948',
#     '_n3fa_lvt_a9e72dfe4a54a20c3d6e671b3bad01d9': '1537790155,1537794216,1537852203,1537858427',
#     '_n3fa_lpvt_a9e72dfe4a54a20c3d6e671b3bad01d9': '1537858660',
#     'AdminStaff': 'qITWpHb/vJa5Bx9l1aQmaZIDzUlNpBjLfcXINni36LpzaiyxF7bRZ7CZJhU9K7ZRB3BQNBNNpLD5TG+PPUSL0oIIG7N/Q6+NphNXD4NJdxtuz2pl2+3UWeH0Ey+uXBcmp+4XEeHJa+ZUfK9NBzvmUYh1EDdb1rAF5k8QwICA77+PJo4Sctv5bAUK6FeyzAUablKvXCAecNlxxSBBPEbVKMUa8jYuQy5n0NpcgPlnqSr2+ofWpCW4Sox8porfZ/bp7qMhkKx0dInxknW/1z7GQM23ZV88Ue77T3Pa6h05cNSgg3sJjK837Twxm+Fb4speEIZkdbeCgPS/EjWyrzKNvawKqX6Brdj/WAn13SqahBi4WYoheiNndn5wLCM95TukWde6Dspm5ueXpyc5brQqlVAGI8XpjivyqMR7TAfla2iesGnHwhS/W5q5hpKw5Or9R2GiSH1K+LfC3euhjlm7Yi0GnZ8+0gVvku8R6UpKJHfO3D8nP3tlUzari46Amitp69PfD2uFfEe1fpXzKfxJhO18X02DhLPwkmxPr068o5FhaM4lvf6Tv5UA66IA6ZHBysu0bcBB7mr4ZlUHC76oGe4HDq8VcKbS96vEf2z1hBxRdrceuc2UvsN9ML3bANghbKtqooVMcxYesTj7UpN6mdSiQ9w0f0pjoP66SzsxXSVMJofhcUKUjPG7UrW65QQGqc/OI9DiFsFK3BCTpd7xZA7Hu0R4SLrP32/WGUrSXKFfyoBaWRx43MKghiQzXb7OpKVPucICqeK/TpC1jMYGcOK/MGrPwo5B; _MSC=fKohZCHWCjW7GvJFL5vsIiJpz1fLQhFFidmiOacQz6Cxo61sCanZCenLdDLyuxd+OhRf2qslF/o=',
#     '_MSC': 'fKohZCHWCjW7GvJFL5vsIkbHe97Gkud/b2jLURBsBXpz/G+yE3WSuyQN51JbyO/EOSOXuUPFGvg='
# }

cookies = getcookiefromchrome()

class InspectionSpider(scrapy.Spider):
    name = 'inspection'
    allowed_domains = ['admin.mall.10010.com']

    def __init__(self):
        super(InspectionSpider, self).__init__()
        self.desktop_path = get_desktop()
        self.save_base_path = self.desktop_path + '/自动抽检/复查'
        import time
        self.save_excel_path = self.save_base_path + '/抽检结果_' + str(int(time.time())) + '.xlsx'
        self.no_picture_path = self.desktop_path + '/自动抽检/temp/0.jpg'
        self.xlsx_path = self.desktop_path + '/test.xlsx'

    def start_requests(self):
        url = 'http://admin.mall.10010.com/OdmQuery/ServiceOrderQuery/query'
        orderNo_dict = read_xlsx(self.xlsx_path, sheet_index=0, start_row=0)

        for date, orderNo_list in orderNo_dict.items():
            base_path = create_dir(self.save_base_path + '/' + date)
            id_path = create_dir(base_path + '/身份证')
            photo_path = create_dir(base_path + '/用户照片')
            video_path = create_dir(base_path + '/视频')
            for orderNo in orderNo_list:
                order_map = {orderNo: 0, 'order_date': date}
                data = {
                    'orderNo': orderNo,
                    'pageSize': '5',
                    'page.webPager.action': 'refresh',
                    'page.webPager.pageInfo.totalSize': '1000',
                    'page.webPager.pageInfo.pageSize': '5',
                    'page.webPager.currentPage': '1'
                }

                yield FormRequest(
                    url=url,
                    method='POST',
                    headers=headers,
                    formdata=data,
                    callback=self.get_inspection_content,
                    cookies=cookies,
                    meta={'dont_redirect': True, 'cookiejar': 1, 'order_map': order_map, 'id_path': id_path,
                          'photo_path': photo_path, 'video_path': video_path},
                    dont_filter=True
                )

    def get_inspection_content(self, response):
        url = 'http://admin.mall.10010.com/Odm/RealNameSpotCheck/getCertInfo'
        order_id = \
            response.xpath('//div[@class="tableBody" and @width="100%"]/table/tr/td[1]/p[1]/text()').extract()[0].split(
                '：')[-1]
        order_map = response.meta.get('order_map', None)
        id_path = response.meta.get('id_path')
        photo_path = response.meta.get('photo_path')
        video_path = response.meta.get('video_path')
        data = {
            'orderId': order_id
        }
        old_flag = response.xpath('//*[@id="pageTable"]/div[2]/table/tr/td[2]/dl/dd/span')  # 老用户标志，判断有没有副卡
        if old_flag != []:
            numbers = response.xpath('//*[@id="pageTable"]/div[2]/table/tr/td[2]/dl/dd/ul/li/text()').extract()
            for i in range(len(numbers)):
                number = numbers[i].split('(')[0].strip()
                data['preNum'] = number
                yield FormRequest(
                    url=url,
                    formdata=data,
                    headers=headers,
                    cookies=cookies,
                    callback=self.inspection,
                    meta={'mul': True, 'num': number, 'order_id': order_id, 'order_map': order_map, 'id_path': id_path,
                          'photo_path': photo_path, 'video_path': video_path},
                    dont_filter=True
                )
        else:
            if data.get('preNum', None) is not None:
                del data['preNum']
            yield FormRequest(
                url=url,
                formdata=data,
                headers=headers,
                cookies=cookies,
                callback=self.inspection,
                meta={'order_id': order_id, 'order_map': order_map, 'id_path': id_path, 'photo_path': photo_path,
                      'video_path': video_path},
                dont_filter=True
            )

    def pro_mul(self, number, urls):
        mul_urls = {}
        for name, url in urls.items():
            if 'getLiving' not in url:
                mul_urls[name] = url.replace('getPhotoPic', 'getPhotoPic4ZFK').replace('/0/', '/' + str(
                    number) + '/0/')
            else:
                mul_urls[name] = urls[name] + '/' + number
        return mul_urls

    def inspection(self, response):
        rs = json.loads(response.text)
        order_id = response.meta.get('order_id')
        id_path = response.meta.get('id_path')
        photo_path = response.meta.get('photo_path')
        video_path = response.meta.get('video_path')
        verifySimilarity = rs['certInfo']['verifySimilarity']
        id_front_url = 'http://admin.mall.10010.com/Acodm/ArtificialDetail/getPhotoPic/{order_id}/0/02/front/0'.format(
            order_id=order_id)
        # id_back_url = 'http://admin.mall.10010.com/Acodm/ArtificialDetail/getPhotoPic/{order_id}/0/02/back/0'.format(
        #     order_id=order_id)

        GZT_urls = {
            'front': id_front_url,
            # 'back': id_back_url,
            # 'gztliving_1': 'http://admin.mall.10010.com/Acodm/ArtificialDetail/getPhotoPic/{order_id}/0/02/gztliving_1/0'.format(
            #    order_id=order_id),
            # 'gztliving_2': 'http://admin.mall.10010.com/Acodm/ArtificialDetail/getPhotoPic/{order_id}/0/02/gztliving_2/0'.format(
            #     order_id=order_id),
            'gztliving_3': 'http://admin.mall.10010.com/Acodm/ArtificialDetail/getPhotoPic/{order_id}/0/02/gztliving_3/0'.format(
                order_id=order_id)
        }

        usual_urls = OrderedDict({
            'front': id_front_url,
            # 'back': id_back_url,
            'hand': 'http://admin.mall.10010.com/Acodm/ArtificialDetail/getPhotoPic/{order_id}/0/02/hand/0'.format(
                order_id=order_id),
            'certCard': 'http://admin.mall.10010.com/Acodm/ArtificialDetail/getPhotoPic/{order_id}/0/02/certCard/0'.format(
                order_id=order_id),

            # 'certNet': 'http://admin.mall.10010.com/Acodm/ArtificialDetail/getPhotoPic/{order_id}/0/02/certNet/0'.format(
            #     order_id=order_id),
            # 'livingphoto': 'http://admin.mall.10010.com/Acodm/ArtificialDetail/getLivingPhoto/{order_id}'.format(
            #     order_id=order_id),

            'living3_1': 'http://admin.mall.10010.com/Acodm/ArtificialDetail/getPhotoPic/{order_id}/0/02/living3_1/0'.format(
                order_id=order_id),

            #
            # 'living3_2': 'http://admin.mall.10010.com/Acodm/ArtificialDetail/getPhotoPic/{order_id}/0/02/living3_2/0'.format(
            #     order_id=order_id),
        })

        if rs['certInfo']['verifyStaff'] is not None:  # 需要去掉 not
            order_map = response.meta.get('order_map')
            urls = usual_urls
            if rs.get('hasLivingVideo', None):
                url = 'http://admin.mall.10010.com/Acodm/ArtificialDetail/getLivingVideo/{order_id}'.format(
                    order_id=order_id)
                usual_urls['livingvideo'] = url
                urls = usual_urls
            elif rs.get('hasLivingVideo', None) is None:
                if usual_urls.get('livingvideo', None):
                    del usual_urls['livingvideo']
                    urls = usual_urls

            if rs['hasLivingGZT'] is True:
                urls = GZT_urls

            mul = response.meta.get('mul', None)
            number = response.meta.get('num', None)
            if mul is True:
                urls = self.pro_mul(number, urls)

            for key, url in urls.items():
                try:
                    rs = requests.get(url=url, cookies=cookies)
                except Exception:
                    orderNo = list(order_map.keys())[0]
                    order_date = list(order_map.values())[1]
                    write(orderNo, order_date, '连接错误，请稍后重新对比该订单', self.save_excel_path)
                self.save_img(rs.content, order_id, order_map, key, verifySimilarity, mul, number, id_path, photo_path,
                              video_path)

    def save_img(self, response, order_id, order_map, key, verifySimilarity, mul, number, id_path, photo_path,
                 video_path):
        orderNo = list(order_map.keys())[0]
        order_date = list(order_map.values())[1]
        if key == 'livingvideo':
            with open(video_path + '/' + orderNo + '.mp4', 'wb') as video_file:
                video_file.write(response)
        else:
            with open(self.no_picture_path, 'rb') as read_c:
                content = read_c.read()
                if content != response:
                    file_name = orderNo
                    if mul is True:
                        file_name = orderNo + '_' + number
                    if key == 'front' or key == 'hand':
                        with open(id_path + '/' + file_name + '.jpg', 'wb') as id_file:
                            id_file.write(response)
                    else:
                        with open(photo_path + '/' + file_name + '.jpg', 'wb') as photo_file:
                            photo_file.write(response)
                            # order_map[orderNo] += 1
                            # if order_map[orderNo] == 1:
                            self.face_tag(order_id, file_name, order_date, verifySimilarity, mul, number, id_path,
                                          photo_path)

    def face_tag(self, order_id, orderNo, order_date, verifySimilarity, mul, number, id_path, photo_path):
        data = {
            'orderId': order_id,
            'phoneHaltVerifyRst': '0',
            'loginRst': '1',
            'photosHaltVerifyRst': '3',
            'realNameVerifyRst': '1',
            'verifyReason': '',
            'verifyRemark': '',
        }
        if mul is True:
            data['preNum'] = number
        else:
            if data.get('preNum'):
                del data['preNum']
        url = 'http://admin.mall.10010.com/Odm/RealNameSpotCheck/saveRealNameVerifyInfo'
        if verifySimilarity is not None and float(verifySimilarity) >= 70.00:
            try:
                rs = requests.post(url=url, data=data, headers=headers, cookies=cookies)
                if rs.text == '{}':
                    write(orderNo, order_date, '通过', self.save_excel_path)
                else:
                    write(orderNo, order_date, '未知原因，失败', self.save_excel_path)
            except:
                write(orderNo, order_date, '连接错误，请稍后重新对比该订单', self.save_excel_path)
        else:
            id_picture = os.path.join(id_path, orderNo + '.jpg')
            photo_picture = os.path.join(photo_path, orderNo + '.jpg')
            if os.path.exists(id_picture) and os.path.exists(photo_picture):
                confidence, errno = face_contrast(id_picture, photo_picture)
                print(confidence)
                if confidence >= 25.00:
                    try:
                        rs = requests.post(url=url, data=data, headers=headers, cookies=cookies)
                        print(rs.text)
                        if rs.text == '{}':
                            write(orderNo, order_date, '通过', self.save_excel_path)
                        else:
                            write(orderNo, order_date, '未知原因，失败', self.save_excel_path)
                    except:
                        write(orderNo, order_date, '连接错误，请稍后重新对比该订单', self.save_excel_path)
                else:
                    data = {
                        'orderId': order_id,
                        'phoneHaltVerifyRst': '1',
                        'loginRst': '0',
                        'photosHaltVerifyRst': '3',
                        'realNameVerifyRst': '0',
                        'verifyReason': '活体不合格',
                        'verifyRemark': '证件或活体不合格'
                    }
                    try:
                        rs = requests.post(url=url, data=data, headers=headers, cookies=cookies)
                        if rs.text == '{}':
                            write(orderNo, order_date, '不通过', self.save_excel_path)
                        else:
                            write(orderNo, order_date, '未知原因，失败', self.save_excel_path)
                    except:
                        write(orderNo, order_date, '连接错误，请稍后重新对比该订单', self.save_excel_path)
            else:
                write(orderNo, order_date, '只有视频，需要人工审核', self.save_excel_path)

    def process_info(self, response):
        print(response.text)
