from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


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


if __name__ == '__main__':

    # print(cat_data())
