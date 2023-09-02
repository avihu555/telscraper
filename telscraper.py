from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

import re

def wordlist(): #creat wordlist
    while True:
        word = input('Please enter words for search: ')
        word = re.sub(r"[^a-zA-Z0-9 ]","",word)
        wordlist = word.split()
        print('\nThis is the wordslist, are you happy?\n')
        for w in wordlist:
            print(w)
        ans = input('\nY or y for continue ')
        if ans != 'y' and ans != 'Y':
            continue
        else:
            break
    wordlist = sorted(set(wordlist), key=lambda x:wordlist.index(x))
    wordlist = [x.lower() for x in wordlist]
    print(wordlist)
    return wordlist


def course_scraper(word_list): # Go through the page and find courses
    browser = webdriver.Chrome(keep_alive=True)
    listofall = []
    browser.get('https://web.telegram.org/k/#@Udemy4U')
    time.sleep(20)
    courses_info = browser.find_elements(By.XPATH,"//div[@class='bubble-content-wrapper']")

    courses_links = browser.find_elements(By.XPATH, "//div[@class='bubble-content-wrapper']//div[@class='reply-markup']//a") 
    for num ,course in enumerate(courses_info,0):
        info = course.text.replace('\n',' ').lower()
        info = info.replace('#','')
        info = info.split("category")[0]
        course_name = info.split("|")[0]
      
        if word_search(word_list,info) == True:
            my_dict = {
                'name' : f"{course_name}",
                'course info' : f"{info}",
                'courses_links' : f"{courses_links[num].get_attribute('href')}"
            }
            
            
            listofall.append(my_dict)
        
    browser.close()
            
    return listofall

def word_search(word_list,info): # Check for the wordslist for the search -- connect to the course_scraper() function
    count = 0
    for word in word_list:
        if word in info:
            count += 1
        else:
            pass
    
    if count == len(word_list):
        return True 
    else:
        return False
    
def currect_url(listofall): # --> currect the link to the UDEMY link
    browser = webdriver.Chrome()
    
    for i in listofall:
        browser.get(i['courses_links'])
        time.sleep(1)
        x =  browser.find_element(By.XPATH,"//div[@class='enroll-btn']//a")
        x = x.get_attribute('href')
        i['courses_links'] = x
        browser.close    

def write_to_csv(listofall): #Write to csv file 
    with open('courses_list.csv', mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['name','info','links'])
        writer.writeheader()
        for course_raw in listofall:
            if doublecheck(csv_file,course_raw) != False:
                writer.writerow({'name': course_raw['name'],
                                'info' : course_raw['course info'],
                                'links' : course_raw['courses_links']
                                })   
    csv_file.close

def doublecheck(csv_file,course_raw): # check for repeated courses
    with open('courses_list.csv', mode='r+') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['name'] == course_raw:
                return False


def main():
    word_list = wordlist()
    listofall = course_scraper(word_list)
    currect_url(listofall)
    write_to_csv(listofall)
    for i in listofall:
        print(f"name: {i['name']}\n")
        print(f"Info: {i['course info']}\n")
        print(f"links:  {i['courses_links']}\n")
        print('\n')
        print('\n')


main()