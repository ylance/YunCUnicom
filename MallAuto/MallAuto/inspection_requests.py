import requests

url = "http://admin.mall.10010.com/OdmQuery/ServiceOrderQuery/query"

payload ={
            'orderNo': '2476438782',
            'pageSize': '5',
            'page.webPager.action': 'refresh',
            'page.webPager.pageInfo.totalSize': '1000',
            'page.webPager.pageInfo.pageSize': '5',
            'page.webPager.currentPage': '1'
}
headers = {

    'Host': 'admin.mall.10010.com',
    'Connection': 'keep-alive',
    # 'Accept': '*/*',
    'Origin': 'http://admin.mall.10010.com',
    # 'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    # 'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://admin.mall.10010.com/OdmQuery/ServiceOrderQuery/init',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '_n3+fa_cid=c0927d16fc204d8c95e8be31a195577e; _n3fa_ext=ft=1537701948; _n3fa_lvt_a9e72dfe4a54a20c3d6e671b3bad01d9=1537701948; _n3fa_lpvt_a9e72dfe4a54a20c3d6e671b3bad01d9=1537701964; AdminStaff=qITWpHb/vJa5Bx9l1aQmaZIDzUlNpBjLfcXINni36LpzaiyxF7bRZ7CZJhU9K7ZRB3BQNBNNpLD5TG+PPUSL0oIIG7N/Q6+NphNXD4NJdxtuz2pl2+3UWeH0Ey+uXBcmp+4XEeHJa+ZUfK9NBzvmUYh1EDdb1rAF5k8QwICA77+PJo4Sctv5bAUK6FeyzAUablKvXCAecNlxxSBBPEbVKMUa8jYuQy5n0NpcgPlnqSr2+ofWpCW4SiqWwfgfU/4D4P2SW6iix4rvxTNwyu6rp1T3dTaeMwWKRwVY6MeBnqZfcEv7E5vXOVDPQJfjVQN0M/1uQs2gJShKu6dZc0UUYHN47JQrddHpNpa1QtSMXmxKVadxHs+Xilv73EMJZf3KWDf283Ph3ueark3qviZyeNsd3f3X4yZZtLnDITNrVIfwDW8SjoVYfzdeG15eR+zqbck+WCHmT6kcGY0wG2rvmu1tKuiYFam5YhDMWNAUvfFDOsW2/7apUPNt+64CB1Rf9hpTWI6Ls6hT9WpZU9K9/OrCOC1Z2SqkkM4TNVr9GEobV7ubd8PjXrnxDn6OSTaqVRh7mHuN+zpKCroVxFpURmp7RAx9iPCXoukmKnlZNAiWOGpEk/YR8d7mWlZiCE/NPfdmXJfutOLQK//iX3KPXX0p+taDdOf5h1hlnvE52M1c6s3mtt3OLxz+c6W3Seh3QtQhFEURVhhWCqTwvqpfiMd2Cz9eKfuXD2c7MiS5lo8Bkc5XpTil0K+GZdg4uFnCjj3rqmKOmELZdt//J8frWtNovV+RWrOjiNBlCH39BasNpkh6Z1Sd0w==; _MSC=fKohZCHWCjW7GvJFL5vsIg0Dtkv7Q8btZsEPs8omWVKSpduP6ca16ha5dukYel8nDWOzhH6trvA='

}

response = requests.post(url=url,headers=headers,data=payload)
print(response.text)