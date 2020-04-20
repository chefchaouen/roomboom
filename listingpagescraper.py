 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from multiprocessing import Pool
import re
import csv
import lxml
import sys

def scrape(listingurl):
    listingid = urllib.parse.urlparse(listingurl).path
    listingidquoted = urllib.parse.quote_plus(listingid)
    resp = urllib.request.urlopen(listingurl)
    soup = BeautifulSoup(resp, 'lxml')
    
    listing_name = soup.find('span', id = 'chk-bkh-name').text
    imagelinks = [re.sub('\&width\=[0-9]{1,5}\&height\=[0-9]{1,5}', '', link.get('src')) for link in soup.find_all('img', src = re.compile('apaman'))]
    rent = soup.find('dd', id = 'chk-bkc-moneyroom').span.text
    mgmtfees = re.search('(?<= )[0-9].*(?=円)', soup.find('dd', id = 'chk-bkc-moneyroom').text).group()
    deposit_keymoney = soup.find('dd', id = 'chk-bkc-moneyshikirei').text
    secdeposit_deduct_dep = soup.find('dd', id = 'chk-bkc-moneyhoshoukyaku').text
    trainline1 = re.findall('(?<=\n).*(?=線)', soup.find('dd', id = 'chk-bkc-fulltraffic').text)[0]
    station1 = re.findall('(?<= ).*(?=駅)', soup.find('dd', id = 'chk-bkc-fulltraffic').text)[0]
    station_dist1 = re.findall('(?<= ).*(?=分)', soup.find('dd', id = 'chk-bkc-fulltraffic').text)[0]
    trainline2 = re.findall('(?<=\n).*(?=線)', soup.find('dd', id = 'chk-bkc-fulltraffic').text)[1]
    station2 = re.findall('(?<= ).*(?=駅)', soup.find('dd', id = 'chk-bkc-fulltraffic').text)[1]
    station_dist2 = re.findall('(?<= ).*(?=分)', soup.find('dd', id = 'chk-bkc-fulltraffic').text)[1]
    trainline3 = re.findall('(?<=\n).*(?=線)', soup.find('dd', id = 'chk-bkc-fulltraffic').text)[2]
    station3 = re.findall('(?<= ).*(?=駅)', soup.find('dd', id = 'chk-bkc-fulltraffic').text)[2]
    station_dist3 = re.findall('(?<= ).*(?=分)', soup.find('dd', id = 'chk-bkc-fulltraffic').text)[2]
    trainline4 = re.findall('(?<=\n).*(?=線)', soup.find('dd', id = 'chk-bkc-fulltraffic').text)[3]
    station4 = re.findall('(?<= ).*(?=駅)', soup.find('dd', id = 'chk-bkc-fulltraffic').text)[3]
    station_dist4 = re.findall('(?<= ).*(?=分)', soup.find('dd', id = 'chk-bkc-fulltraffic').text)[3]
    trainline5 = re.findall('(?<=\n).*(?=線)', soup.find('dd', id = 'chk-bkc-fulltraffic').text)[4]
    station5 = re.findall('(?<= ).*(?=駅)', soup.find('dd', id = 'chk-bkc-fulltraffic').text)[4]
    station_dist5 = re.findall('(?<= ).*(?=分)', soup.find('dd', id = 'chk-bkc-fulltraffic').text)[4]
    built_year = re.search('[0-9]{4}', soup.find('dd', id = 'chk-bkc-kenchikudate').text).group()
    built_month = re.search('(?<=築).*(?=年)', soup.find('dd', id = 'chk-bkc-kenchikudate').text).group()
    building_age = re.search('[0-9]{4}', soup.find('dd', id = 'chk-bkc-kenchikudate').text).group()
    floor_area = re.search('[1-9].*(?=m)',soup.find('dd', id = 'chk-bkc-housearea').text.replace(' ', '')).group()
    balcony_area = re.search('[1-9].*(?=m)',soup.find('dd', id = 'chk-bkc-balconyarea').text.replace(' ', '')).group()
    floor_plan = re.search('[1-9].*K', soup.find('dd', id = 'chk-bkc-marodi').text).group()
    floor_plan_details = re.search('(?<=X).*(?=Y)', soup.find('dd', id = 'chk-bkc-marodi').text.replace(' ', '').replace('\n', ' ').replace('(','X').replace(')','Y')).group()
    listing_post_date = soup.find('dd', id = 'chk-bkh-newdate').text
    valid_date = soup.find('dd', id = 'chk-bkh-timelimitdate').text
    selling_points = soup.find('dd', id = 'chk-bkp-featurecomment').text
    building_construction_materials = soup.find('td', id = 'chk-bkd-housekouzou').text.replace(' ', '').replace('\n', '')
    floor = re.search('[0-9]{1,3}(?=階)', soup.find('td', id = 'chk-bkd-housekai').text).group()
    num_floors = re.search('[0-9]{1,3}(?=階建)', soup.find('td', id = 'chk-bkd-housekai').text).group()
    parking = soup.find('td', id = 'chk-bkd-parking').text
    num_units = re.search('[0-9]{1,4}(?=戸)', soup.find('td', id = 'chk-bkd-parkunit').text).group()
    contract_period = soup.find('td', id = 'chk-bkd-conterm').text.replace(' ', '')
    renewal_fee = soup.find('td', id = 'chk-bkd-moneykoushin').text.replace(' ', '')
    guarantor_company = soup.find('td', id = 'chk-bkd-guaranteecom').text.replace(' ', '')
    current_status = soup.find('td', id = 'chk-bkd-genkyo').text.replace(' ', '')
    movein_date = soup.find('td', id = 'chk-bkd-usable').text.replace(' ', '')
    real_estate_agent = soup.find('p', id = 'chk-rtd-name').contents[0].text
    transaction_type = soup.find('td', id = 'chk-bkd-taiyou').text
    schools = soup.find('td', id = 'chk-bkd-schooldistance').text.replace(' ','').replace('\n','')
    shopping = soup.find('td', id = 'chk-bkd-shopdistance').text.replace(' ','').replace('\n','')
    hospitals = soup.find('td', id = 'chk-bkd-hospitaldistance').text.replace(' ','').replace('\n','')
    
    print(
    
    rent, mgmtfees, deposit_keymoney, secdeposit_deduct_dep 
            
    )
    
if __name__ == "__main__":
    scrape(sys.argv[1])
