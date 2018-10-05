import urllib.parse
import urllib.request
import datetime
import base64
import hmac
import hashlib
import json


def get_current_date():
    date = datetime.datetime.strftime(datetime.datetime.utcnow(), "%a, %d %b %Y %H:%M:%S GMT")
    return date


def to_md5_base64(strBody):
    hash = hashlib.md5()
    hash.update(strBody.encode('utf-8'))
    return base64.b64encode(hash.digest()).strip()
    # return hash.digest().encode('base64').strip()
    # return hash.digest().encode('base64').strip()


def to_sha1_base64(stringToSign, secret):
    # print(type(secret),type(stringToSign),type(hashlib.sha1))
    hmacsha1 = hmac.new(secret.encode('utf-8'), stringToSign.encode('utf-8'), hashlib.sha1)
    return base64.b64encode(hmacsha1.digest())


def face_contrast(identity_path, photo_path):
    ak_id = ''
    ak_secret = ''
    # print(identity_path, photo_path)
    with open(identity_path, 'rb') as identity_card, open(photo_path, 'rb') as photo:
        content_1 = base64.b64encode(identity_card.read())
        content_2 = base64.b64encode(photo.read())
        upload_msg = {'type': 1, 'content_1': content_1.decode('utf-8'), 'content_2': content_2.decode('utf-8')}
        options = {
            'url': 'https://dtplus-cn-shanghai.data.aliyuncs.com/face/verify',
            'method': 'POST',
            'body': json.dumps(upload_msg, separators=(',', ':')),
            'headers': {
                'accept': 'application/json',
                'content-type': 'application/json',
                'date':  get_current_date(),
                'authorization': ''
            }
        }
        # options = {
        #     'url': '<请求的url>',
        #     'method': 'GET',
        #     'headers': {
        #         'accept': 'application/json',
        #         'content-type': 'application/json',
        #         'date': get_current_date(),  # 'Sat, 07 May 2016 08:19:52 GMT',  # get_current_date(),
        #         'authorization': ''
        #     }
        # }
        body = ''
        if 'body' in options:
            body = options['body']
        # print(body)
        bodymd5 = ''
        if not body == '':
            bodymd5 = to_md5_base64(body)
        # print(bodymd5)
        urlPath = urllib.parse.urlparse(options['url'])
        if urlPath.query != '':
            urlPath = urlPath.path + "?" + urlPath.query
        else:
            urlPath = urlPath.path
        # print(type(options),type(bodymd5.decode('utf-8')),type(urlPath))
        stringToSign = options['method'] + '\n' + options['headers']['accept'] + '\n' + bodymd5.decode('utf-8') + '\n' + options['headers']['content-type'] + '\n' + options['headers']['date'] + '\n' + urlPath
        signature = to_sha1_base64(stringToSign, ak_secret)
        # print(stringToSign)
        # print(type(ak_id),type(signature))
        authHeader = 'Dataplus ' + ak_id + ':' + signature.decode('utf-8')
        options['headers']['authorization'] = authHeader
        # print(authHeader)
        request = None
        method = options['method']
        url = options['url']
        # print(method)
        # print(url)
        if 'GET' == method or 'DELETE' == method:
            request = urllib.request.Request(url)
        elif 'POST' == method or 'PUT' == method:
            request = urllib.request.Request(url, body.encode('utf-8'))
        request.get_method = lambda: method
        for key, value in options['headers'].items():
            request.add_header(key, value)
        try:
            # print('准备链接')
            conn = urllib.request.urlopen(request)
            # print('链接成功')
            response = conn.read()
            # print('获取结果')
            # print(response)
            result = json.loads(response.decode('utf-8'))
            return result['confidence'], result['errno']
        except urllib.request.HTTPError as e:
            print(e.read())
            #raise SystemExit(e)
##import os
##confidence, errno = face_contrast(os.path.join('C:\\Users\\Administrator\\Desktop\\自动抽检\\抽检复查\\2018-04-29\\用户照片\\','2976507606.jpg'), os.path.join('C:\\Users\\Administrator\\Desktop\\自动抽检\\抽检复查\\2018-04-29\\身份证\\','2976507606.jpg'))
##print(confidence,errno)
