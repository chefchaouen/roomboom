from bs4 import BeautifulSoup
import lxml
import urllib.request as u
import sys, re

def main(url):
    resp = u.urlopen(url)
    soup = BeautifulSoup(resp, 'lxml')
    bldg_mat = soup.find('th', string='構造').next_element.next_element.next_element.text.strip()
    print(bldg_mat)
if __name__=='__main__':
    main(sys.argv[1])

