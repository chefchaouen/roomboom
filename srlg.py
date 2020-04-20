from bs4 import BeautifulSoup
import urllib.request
import lxml
import re
import random
import pyperclip
import sys
import pymysql

def main():
    url = 'http://suumo.jp/chintai/tokyo/new/pnz1.html'
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp, 'lxml')
    maxpage = int(soup.find('a', href=re.compile('pnz[0-9]{4}')).text)
    pagenum = random.randrange(1, maxpage)
    testurl = 'http://suumo.jp/chintai/tokyo/new/pnz' + str(pagenum) + '.html'
    testresp = urllib.request.urlopen(testurl)
    testsoup = BeautifulSoup(testresp, 'lxml')

    links = soup.find_all('a')
    
    testlinks = []

    for link in links:
        if str(link.text) == '詳細を見る':
            testlinks.append(link.get('href'))
            
    randurl = random.choice(testlinks)

    pyperclip.copy(randurl)

    print(randurl)

if __name__=='__main__':
    main()
