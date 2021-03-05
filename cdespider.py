from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
import time


colnam_list = ['受理号','药品名称','药品类型','申请类型','注册分类','企业名称','承办日期']
df = pd.DataFrame(columns=(colnam_list))

start_urls = 'http://www.cde.org.cn/transparent.do?method=list&year=2020&currentPageNumber=1&checktype=1&statenow=0'

firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--proxy-server=socks5://127.0.0.1:1081')
driver = webdriver.Firefox(firefox_options=firefox_options)
driver.get(start_urls)
time.sleep(60)
data = driver.page_source
soup = BeautifulSoup(data, 'lxml')

context = soup.select('td[class="newsindex"]')
tmp_list = []
tmp_dict = {}
for step, c in enumerate(context):
    ndx = step % len(colnam_list)
    tmp_dict[colnam_list[ndx]] = c.string
    if (step+1) % len(colnam_list) == 0:
        tmp_list.append(tmp_dict)
        tmp_dict = {}
df = df.append(tmp_list)
#df.to_csv('cde_2020.csv', index=False)
driver.close()

total_page_num = int(soup.find(id='pageNumber').get_text().split()[-2])


for p in tqdm(range(1, total_page_num)):
    urls = 'http://www.cde.org.cn/transparent.do?method=list&year=2020&currentPageNumber=%s&checktype=1&statenow=0' % str(p+1)
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('--proxy-server=socks5://127.0.0.1:1081')
    driver = webdriver.Firefox(firefox_options=firefox_options)
    driver.get(urls)
    time.sleep(60)
    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')
    
    context = soup.select('td[class="newsindex"]')
    tmp_list = []
    tmp_dict = {}
    for step, c in enumerate(context):
        ndx = step % len(colnam_list)
        tmp_dict[colnam_list[ndx]] = c.string
        if (step+1) % len(colnam_list) == 0:
            tmp_list.append(tmp_dict)
            tmp_dict = {}
    df = df.append(tmp_list)
    df.to_csv('cde_2020.csv', index=False)
    driver.close()
