from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from xml.dom import minidom


def cat_data():

    src = urlopen('http://www.weather.com.cn/weather/101280101.shtml')
    soup = BeautifulSoup(src, 'html.parser')

    tem_tags = soup.find_all('p', class_='tem')
    wea_tags = soup.find_all('p', class_='wea')

    his, los, weas = [], [], []
    for i in range(7):
        weas.append(wea_tags[i].string)
        his.append(re.search('\d+', tem_tags[i].span.string).group())
        los.append(re.search('\d+', tem_tags[i].i.string).group())

    return weas, his, los


def xml_root():

    weas, his, los = cat_data()

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
