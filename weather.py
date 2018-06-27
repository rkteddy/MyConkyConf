from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from xml.dom import minidom
import threading
import time


cnt = 0
his, los, weas = [], [], []
flag = False


def cat_data():

    global flag, his, los, weas

    src = urlopen('http://www.weather.com.cn/weather/101280101.shtml')
    soup = BeautifulSoup(src, 'html.parser')

    tem_tags = soup.find_all('p', class_='tem')
    wea_tags = soup.find_all('p', class_='wea')

    for i in range(7):
        weas.append(wea_tags[i].string)
        his.append(re.search('\d+', tem_tags[i].span.string).group())
        los.append(re.search('\d+', tem_tags[i].i.string).group())

    flag = True


def count_down():

    global cnt, flag, crawler_thread

    while flag:

        time.sleep(1)
        cnt += 1
        print(cnt)

        if cnt >= 5:
            cnt = 0
            crawler_thread.start()


crawler_thread = threading.Thread(target=cat_data)


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
    wea_node = xmldoc.createElement('Weather')
    root.appendChild(tem_node)
    root.appendChild(wea_node)

    hi_node = xmldoc.createElement('Highest')
    lo_node = xmldoc.createElement('Lowest')
    tem_node.appendChild(hi_node)
    tem_node.appendChild(lo_node)

    for i in range(7):
        sub_wea = xmldoc.createElement('day' + str(i))
        sub_wea.appendChild(xmldoc.createTextNode(weas[i]))
        wea_node.appendChild(sub_wea)

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

    # print(cat_data())
    xml_root()
