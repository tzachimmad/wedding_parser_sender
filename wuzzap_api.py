#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import listdir, remove
import sys
import datetime
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

reload(sys)
sys.setdefaultencoding('utf-8')

dico = {}

def write_to_csv(contact,filename):
    with open(filename, "a") as myfile:
        for item in dico[contact]:
            myfile.write(",")
            myfile.write(item)
        myfile.write("\n")
    myfile.close()

def scorllUp():
    try:
        driver.find_element_by_class_name("icon-refresh").click()
    except:
        pass

def sendMessage(message,num):
    msgbox = driver.find_element_by_class_name("input-container")
    msgbox.click()
    msgbox.send_keys(message.decode("utf-8"))
    driver.find_element_by_class_name("icon-send").click()

def click_contact(contact):
    msgbox = driver.find_element_by_class_name("input-search")
    msgbox.click()
    stringo = "//*[@title='" + contact + "']"
    driver.find_element_by_xpath(stringo).click()
    time.sleep(1)

def parser(date, contact):
    txt = driver.find_element_by_class_name("message-list").get_attribute("innerHTML")
    for elem in txt.split("bubble bubble"):
        tmp_date =  elem[elem.find('['):elem.find('[')+30]
        month = tmp_date[tmp_date.find(',')+2:tmp_date.find('/')]
        tmp_date = tmp_date[tmp_date.find('/')+1:]
        day = tmp_date[:tmp_date.find('/')]
        year = tmp_date[tmp_date.find('/')+1:tmp_date.find(']')]
        if day==" " or day=="":
            continue
        if (int(day)<date or int(month)<3 or int(year)<2017):
            continue
        ##get msg
        written_msg = elem[elem.find("selectable-text"):elem.find("message-meta text-clickable")]
        aa = written_msg.find("-->")+3
        bb= written_msg.find("<!-- /react-text -->")
        cur_msg = written_msg[aa:bb]
        final_msg = cur_msg.replace("\n",". ")
        ##put message in dico
        arr = dico.get(contact,[])
        arr.append(final_msg)
        dico[contact]=arr

###find group
def get_msgs(contact, day):
    click_contact(contact)
    scorllUp()
    parser(day, contact)

def get_contact_list_from_file(path):
    contacts = []
    date_made = datetime.date.today()
    f = open(path, 'rb')
    reader = csv.reader(f)
    for row in reader:
        contacts.append(row[0].decode("utf-8"))
    f.close()
    return contacts

###load whatsapp web
chrome_driver_path = '/home/redbend/Desktop/training/Hackathon/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/home/redbend/Desktop/training/python scripts/whatsapp_poll-master/tmp") #Path to your chrome profile
driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=options)
driver.set_window_size(1024,768)
driver.get('https://web.whatsapp.com/')
time.sleep(7)

contacts = get_contact_list_from_file("/home/redbend/Desktop/training/contact_list")
get_msgs(contacts[0], 14)
driver.quit()
