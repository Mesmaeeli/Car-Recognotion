print('\n**********','Please Wait',1 * chr(35),'00.00% Completed','**********\n',sep = '\n')

from bs4 import BeautifulSoup
import requests
import re
import urllib
from openpyxl import Workbook
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt



w = Workbook()
sheet = w.active
sheet['A1'] = 'fa-brand'
sheet['B1'] = 'model'
sheet['C1'] = 'year'
sheet['D1'] = 'en-brand'

source = requests.get('http://bama.ir/car/')
page = BeautifulSoup(source.text,'html.parser')
num = page.find('h4')
num = re.sub(r'\s+',"",num.text)
#print(num)
m = num
num = num[4:]
num = re.sub(',','',num)
#print(num)
num = int(num)//30
excel_num = 0
defaul_images_count = 0


for i in range(1,num//4):
   prgrs = i//31+1
   print('\n**********','Please Wait',prgrs * chr(35),str(round(i/num*100,2))+'% Completed','**********\n',sep = '\n')
   links = []
   source = requests.get('https://bama.ir/car/all-brands/all-models/all-trims?page='+str(i))
   page = BeautifulSoup(source.text,'html.parser')
   new = page.find_all('span',attrs={'class':'photo'})
   new = str(new)
   res = re.findall(r'href="(.*)" title',new)
   links.extend(res)
   #print(i)

   counter1 = 0

   for pages in links:
      #print(counter1)
      page_str = str(pages)
      car_type = re.findall(r'detail-.*?-(.*?)-',page_str)
      car_type = car_type[0]
   
      try:
      
         image_links = []
         car_page = requests.get(pages)
         New_page = BeautifulSoup(car_page.text,'html.parser')
         car_image = New_page.find_all('img',attrs={'id':'main-image'})
         result = str(car_image)
         result = result.split('>,')
         counter2 = 0
         for j in result:
            
            URLimage = re.findall(r'src="(.*)" title',j)
            URLimage = URLimage[0]
            Titleimage = re.findall(r'alt="(.*)" class',j)
            Titleimage = Titleimage[0]
            Titleimage = Titleimage.split(sep='،')
            #print(Titleimage)
            Brand = Titleimage[0]
            Model = Titleimage[1]
            Year  = Titleimage[2]
            #print(Titleimage)
            
            #Brand_tag = 'A' + str(counter1+2) + str(counter2)
            #Model_tag = 'B' + str(counter1+2) + str(counter2)
            #Year_tag = 'C' + str(counter1+2) + str(counter2)
            Brand_tag = 'A' + str(excel_num+2)
            Model_tag = 'B' + str(excel_num+2)
            Year_tag = 'C' + str(excel_num+2)
            eng_brand_tag = 'D' + str(excel_num+2)

            sheet[Brand_tag] = Brand
            sheet[Model_tag] = Model
            sheet[Year_tag] = Year
            sheet[eng_brand_tag] = car_type
            w.save(filename = 'hello_world.xlsx')
            
            
         

            #name = Brand+str(counter1)+str(counter2)
            name = str(excel_num)
            
            try:
               os.mkdir('C:\\Users\\esmae\\Desktop\\Data set4\\{}'.format(car_type))
            except:
               pass
            check_default = urllib.request.urlopen(URLimage)
            arr = np.asarray(bytearray(check_default.read()), dtype=np.uint8)
            image_check = cv2.imdecode(arr, -1)
            img = image_check[:20,:20,:20]
            if not np.all(img == 220):
               urllib.request.urlretrieve(URLimage, "C:\\Users\\esmae\\Desktop\\Data set4\\{}\\{}.png".format(car_type,name))
               excel_num += 1
            else:
               defaul_images_count += 1
               

            
            counter2 += 1
         counter1 += 1
      except:
         #print('error')
         counter1 += 1
         excel_num += 1
      
      
      
      
      
      
   
   
   
   
   
   

   

