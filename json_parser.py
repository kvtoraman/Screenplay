
# coding: utf-8

import json
from bs4 import BeautifulSoup
from urllib import request
import sys

with open(sys.argv[1]) as data_file:    
    data = json.load(data_file)
    
with open('all_name_script.txt','w') as out:    
    for movie in data:
        url = movie['link'].replace(' ','%20')
        name = movie['name'].replace('\t',' ')
        name = name.replace('Script','')

        print(url)
        html = request.urlopen(url).read().decode('utf8',errors='ignore')
        soup = BeautifulSoup(html,'html.parser')
        links_in_page = soup.find_all('a')
        found = False
        for link in links_in_page:
            text = link.get_text()
            # print("->" + text)
            if 'Read' in text and 'Script' in text:
                found = True
                script_link = 'http://www.imsdb.com' + link.get('href')
                print(name + '\t' + script_link)
                out.write(name + '\t' + script_link + '\n')
                break
        if found == False:
             print('NOTFOUND',name + '\t' + script_link)