#This program gets listing urls really fast. use judiciously.
#!usr/bin/env python3
# -*- coding: utf=8 -*-

import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import uvloop
import lxml

def main():
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)

    tasks = []
    
    baseurl = "https://www.homes.co.jp/chintai/tokyo/23ku/list/?page=1"

    url = "https://www.homes.co.jp/chintai/tokyo/23ku/list/?page={}"

    basesoup = BeautifulSoup(baseurl, 'lxml')



    for i in range(14):
        task = asyncio.ensure_future(get_listing_urls(url.format(i)))
        tasks.append(task)

    loop.run_until_complete(asyncio.wait(tasks))

async def get_listing_urls(base_url):
    async with ClientSession() as session:
        async with session.get(base_url) as response:
            response = await response.read()
            soup = BeautifulSoup(response, 'lxml')
            listing_links = []
            for link in soup.find_all('a'):
                if str(link.text) == '詳細を見る':
                    print(link.get('href'))
                
if __name__=="__main__":
    main()
