from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from xml.dom import minidom
import threading
import time
from translate import Translator
import info

import random
import urllib.parse
import hashlib
import json

cnt = 0
his, los, weas1, weas2 = [], [], [], []
flag = False

url_baidu = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

Weather_Icons = {'多云': 'c', '雷阵雨': 'l', '小雨': 's', '中雨': 't', '大雨': 'u', '暴雨': 'i',
                 '晴': 'a', '阴': 'd', '小雪': 'o', '中雪': 'p', '大雪': 'q', '暴雪': 'r'}


def baidu_translate(text, f='zh', t='en'):

    salt = random.randint(32768, 65536)
    sign = info.appid + text + str(salt) + info.secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = url_baidu + '?appid=' + info.appid + '&q=' + urllib.parse.quote(text) + '&from=' + f + '&to=' + t + \
        '&salt=' + str(salt) + '&sign=' + sign
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    data = json.loads(content)
    result = str(data['trans_result'][0]['dst'])
    print(result)


def zh2en(str):

    translator = Translator(from_lang='zh', to_lang='en')

    return translator.translate(str)


def cat_data():

    global flag, his, los, weas

    src = urlopen('https://weather.com/weather/today/l/CHXX0037:1:CH')
    soup = BeautifulSoup(src, 'html.parser')

    wea = soup.find(class_='today-daypart-wxphrase')
    first_tag = soup.find(id='daypart-1')

    first_tem = first_tag.find(class_='today-daypart-temp').span.next

    flag = True


def cat_data_cn():

    global flag, his, los, weas

    src = urlopen('http://www.weather.com.cn/weather/101280101.shtml')
    soup = BeautifulSoup(src, 'html.parser')

    tem_tags = soup.find_all('p', class_='tem')
    wea_tags = soup.find_all('p', class_='wea')

    for i in range(7):
        wea_string = wea_tags[i].string
        result = re.search('转', wea_string)
        if result is not None:
            weas1.append(wea_string[:result.start()])
            weas2.append(wea_string[result.end():])
        else:
            weas1.append(wea_string)
            weas2.append(wea_string)

        if tem_tags[i].span is not None:
            his.append(re.search('\d+', tem_tags[i].span.string).group())
        else:
            his.append(re.search('\d+', tem_tags[i].i.string).group())
        los.append(re.search('\d+', tem_tags[i].i.string).group())

    flag = True


crawler_thread = threading.Thread(target=cat_data_cn)


def count_down():

    global cnt, flag, crawler_thread

    while flag:

        time.sleep(1)
        cnt += 1
        print(cnt)

        if cnt >= 3:
            cnt = 0
            crawler_thread.start()


def xml_root():

    threading.Thread(target=count_down).start()

    global flag, his, los, weas, crawler_thread

    crawler_thread.start()

    while not flag:
        pass

    xmldoc = minidom.Document()

    root = xmldoc.createElement('WeatherReport')
    xmldoc.appendChild(root)

    tem_node = xmldoc.createElement('Tempreture')
    wea1_node = xmldoc.createElement('Weather1')
    wea2_node = xmldoc.createElement('Weather2')
    icon1_node = xmldoc.createElement('Icon1')
    icon2_node = xmldoc.createElement('Icon2')
    root.appendChild(tem_node)
    root.appendChild(wea1_node)
    root.appendChild(wea2_node)
    root.appendChild(icon1_node)
    root.appendChild(icon2_node)

    hi_node = xmldoc.createElement('Highest')
    lo_node = xmldoc.createElement('Lowest')
    tem_node.appendChild(hi_node)
    tem_node.appendChild(lo_node)

    for i in range(7):
        sub_icon1 = xmldoc.createElement('day' + str(i))
        sub_icon1.appendChild(xmldoc.createTextNode(Weather_Icons[weas1[i]]))
        icon1_node.appendChild(sub_icon1)

        sub_icon2 = xmldoc.createElement('day' + str(i))
        sub_icon2.appendChild(xmldoc.createTextNode(Weather_Icons[weas2[i]]))
        icon2_node.appendChild(sub_icon2)

        sub_wea1 = xmldoc.createElement('day' + str(i))
        sub_wea1.appendChild(xmldoc.createTextNode(weas1[i]))
        wea1_node.appendChild(sub_wea1)

        sub_wea2 = xmldoc.createElement('day' + str(i))
        sub_wea2.appendChild(xmldoc.createTextNode(weas2[i]))
        wea2_node.appendChild(sub_wea2)

        sub_hi = xmldoc.createElement('day' + str(i))
        sub_hi.appendChild(xmldoc.createTextNode(his[i]))
        hi_node.appendChild(sub_hi)

        sub_lo = xmldoc.createElement('day' + str(i))
        sub_lo.appendChild(xmldoc.createTextNode(los[i]))
        lo_node.appendChild(sub_lo)

    file = open('./weather.xml', 'w')
    xmldoc.writexml(writer=file, indent='\t', addindent='\t', newl='\n', encoding='utf-8')
    file.close()


if __name__ == '__main__':

    # cat_data()
    xml_root()
