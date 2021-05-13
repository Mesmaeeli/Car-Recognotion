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


def download(last_post_date):
	print("Downloading: " + str(last_post_date))
	request_data = '{"jsonrpc":"2.0","id":0,"method":"getPostList","params":[[["place2",0,["1"]],["cat2",0,[68]],["cat1",0,[67]],["image",0,["1"]],["v01",0,["-100"]]],' + str(last_post_date) + ']}'
	response = requests.post("https://search.divar.ir/json/", data = request_data)
	if response.status_code == 200:
		return response.text
	else:
		response.raise_for_status()

def extract_tokens(json_data):
	tokens = []
	post_list_count = len(response_json["result"]["post_list"])
	for i in range(0, post_list_count):
		token = response_json["result"]["post_list"][i]["token"]
		tokens.insert(0,token)
	return tokens
try:
        pass
except:
        pass

                
        

last_post_date = 0
counter = 0
file_length = 0
while True:
	try:response_data = download(last_post_date)
	except:continue
	response_json = json.loads(response_data)
	if response_json["error"] != None:
		raise Exception("Error: " + str(response_json["error"]))

	directory_name = "browse"
	data_file_name = directory_name + "/" + str(counter) + "-" + str(last_post_date) + ".txt"
	json_file_name = directory_name + "/" + str(counter) + "-" + str(last_post_date) + ".json"
	if not os.path.exists(directory_name):
		os.makedirs(directory_name)
	with open(data_file_name, "w") as data_file:
		data_file.write(response_data)
	with open(json_file_name, "w") as json_file:
		json_file.write(json.dumps(response_json, indent=4, sort_keys=True))

	tokens = extract_tokens(response_json)
	tokens_file_name = "tokens.txt"
	with open(tokens_file_name, "a") as tokens_file:
		for token in tokens:
			tokens_file.write(token + "\n")
	files = open(tokens_file_name, "r")
	file_length = len(files.readlines())
	print(file_length)
           
                                

	post_list_count = len(response_json["result"]["post_list"])
	print ("Done! counter: " + str(counter) + ", post_list_count: " + str(post_list_count) + "\n")

	if post_list_count == 0:
		break
	last_post_date = response_json["result"]["last_post_date"]
	counter = counter + 1

w = Workbook()
sheet = w.active
sheet['A1'] = 'brand'
sheet['B1'] = 'model'
sheet['C1'] = 'year'
sheet['D1'] = 'token'
counter = 1
excel_num = 0
token_number = 0
try:os.mkdir('images/');print('Folder created')
except:print('Folder is already created')
start_time = int(time.time())        
print('\n**********','Please Wait',1 * chr(35),'00.00% Completed','**********\n',sep = '\n')
def download_the_link(link,btag,cnum):
        urllib.request.urlretrieve(link, "images/{}/{}.jpg".format(btag,cnum))

def exiter(signum,frame):
        raise TimeoutError

signal.signal(signal.SIGALRM, exiter)

with open('previous_tokens.txt', 'r') as file1:
	with open('tokens.txt', 'r') as file2:
		diff = set(file2).difference(file1)

diff.discard('\n')

def remover(self):
	return self[:-1]

new_tokens = list(map(remover,diff))
print(len(new_tokens),':new tokens')

with open('previous_tokens.txt', "a") as tokens_file:
        for token in (new_tokens):
                
                token_number += 1
                time.sleep(1)
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
                        
                        signal.alarm(3)
                        try:download_the_link(res[i],brand_tag,counter);sheet['A'+str(counter)]=brand_tag;sheet['B'+str(counter)]=model;sheet['C'+str(counter)]=year;sheet['D'+str(counter)]=token
                        except:break
                        else:signal.alarm(0)
                        if counter % 20000 == 0:
                                print('saving data')
                                w.save(filename = 'data{}.xlsx'.format(excel_num))
                                excel_num += 1
                                print('saved')
                                
                prgrs = token_number//31+1
                percentage = round(token_number/file_length*100,2)
                print('\n**********','Please Wait',str(percentage)+'% Completed','**********\n',sep = '\n')
                passed_time = int(time.time()) - start_time
                try:Estimated_time = int(((passed_time / percentage)*(100 - percentage))/60)
                except: Estimated_time = 'Calculating remaining'
                print('Estimated time remaining:',Estimated_time,'minutes')
                tokens_file.write(token +'\n')
                
                
excel_num += 1
w.save(filename = 'data{}.xlsx'.format(excel_num))
                
                
                
                        


print('done')
