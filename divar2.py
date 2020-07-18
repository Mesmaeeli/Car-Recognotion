import json
import requests
import os
import urllib
import time
from bs4 import BeautifulSoup
import re
from openpyxl import Workbook
from threading import Timer
import signal

w = Workbook()
sheet = w.active
sheet['A1'] = 'brand'
sheet['B1'] = 'model'
sheet['C1'] = 'year'
sheet['D1'] = 'token'
counter = 120001
excel_num = 0
token_number = 0
try:os.mkdir('images/');print('Folder created')
except:print('Folder is already created')

start_time = int(time.time())        
print('\n**********','Please Wait',1 * chr(35),'00.00% Completed','**********\n',sep = '\n')
def download_the_link(link,btag,cnum):
        urllib.request.urlretrieve(link, "images/{}/{}.jpg".format(btag,cnum))

def exiter(signum,frame):
        return TimeoutError

signal.signal(signal.SIGALRM, exiter)

with open('tokens.txt', "r") as tokens_file:
        for token in tokens_file:
                token_number += 1
                time.sleep(1)
                token = token[:-1]
                source = requests.get('https://divar.ir/v/{}'.format(token))
                page = BeautifulSoup(source.text,'html.parser')
                new = page.find_all('img',attrs={'style':'width:100%;display:inline-block'})
                title = page.find_all('div',attrs={'class':'post-fields-item'})
                title = str(title)
                a1 = page.find_all('div',attrs={'class':'breadcrumb-card'})
                a2 = re.findall(r'title="(.*?)">',str(a1))
                try:brand_tag = a2[4];model = a2[5]
                #try:brand = re.findall(r'برند</span><div class="post-fields-item__value">(.*?)</div>',title)[0];brand_tag = brand.split(sep=' ')[0]
                except:brand_tag = 'Not mentioned';model = 'Not mentioned'
                try:year = re.findall(r'سال ساخت</span><div class="post-fields-item__value">(.*?)</div>',title)[0]
                except:year = 'Not mentioned' 
                new = str(new)
                res = re.findall(r'src="(.*?)" style',new)
                res = list(set(res))
                try:os.mkdir('images/'+brand_tag);
                except:pass
                for i in range(len(res)):
                        counter += 1
                        
                        signal.alarm(5)
                        try:download_the_link(res[i],brand_tag,counter);sheet['A'+str(counter)]=brand_tag;sheet['B'+str(counter)]=model;sheet['C'+str(counter)]=year;sheet['D'+str(counter)]=token
                        except:break
                        else:signal.alarm(0)
                        if counter % 10000 == 0:
                                print('saving data')
                                w.save(filename = 'data{}.xlsx'.format(excel_num))
                                excel_num += 1
                                print('saved')
                prgrs = int(token_number / 1516)
                percentage = round(token_number/47000*100,2)
                print('\n**********','Please Wait',str(percentage)+'% Completed','**********\n',sep = '\n')
                passed_time = int(time.time()) - start_time
                try:Estimated_time = int(((passed_time / percentage)*(100 - percentage))/60)
                except: Estimated_time = 'Calculating remaining'
                print('Estimated time remaining:',Estimated_time,'minutes')
                

                
                
                
excel_num += 1        
w.save(filename = 'data{}.xlsx'.format(excel_num)) 

print('done')
