import requests
from bs4 import BeautifulSoup
import re
import os
import zipfile
from pathlib import Path

def main(): 
    def download(path,name):
        response = requests.get(base_url+path, cookies=cookies)

        soup = BeautifulSoup(response.content,'html.parser')

        download = soup.find(class_='solution-link')
        
        if download:
            response = requests.get(base_url+download['href'], cookies=cookies)

            open(f'/home/joaocalem/LeWagon/Challenges/lewagon{name}.zip', 'wb').write(response.content)
    
    os.system('mkdir /home/joaocalem/LeWagon')
    os.system('rm -rf /home/joaocalem/LeWagon')
    os.system('mkdir /home/joaocalem/LeWagon')
    os.system('mkdir /home/joaocalem/LeWagon/Challenges')
    os.system('mkdir /home/joaocalem/LeWagon/Lecture')
    os.system('gnome-terminal --tab --working-directory=/home/joaocalem/LeWagon/Lecture')
    
    base_url = 'https://kitt.lewagon.com/'

    path = os.path.join(Path(__file__).parent,'kitt_cookies.txt')
    with open(path) as file:
        cookies = {'_kitt2017_': file.readline()[:-1]}

    response = requests.get(base_url, cookies=cookies)

    soup = BeautifulSoup(response.content,'html.parser')

    today = soup.find(class_='text-decoration-none')

    if not today:
        cookies = input("cookies:")
        with open("kitt_cookies.txt", "r+") as file:
            file.truncate(0)
            file.write(cookies+'\n')
        cookies = {'_kitt2017_': cookies}
        response = requests.get(base_url, cookies=cookies)
        soup = BeautifulSoup(response.content,'html.parser')
        today = soup.find(class_='text-decoration-none')

    today = today['href']
    day = re.findall('\d{2}-.*\d{2}[-\w]*',today)[0]

    response = requests.get(base_url+today, cookies=cookies)

    soup = BeautifulSoup(response.content,'html.parser')

    exercises = soup.find_all(class_='exercise')

    for exercise in exercises:
        if day in exercise['href']:
            spans = exercise.find_all('span')
            if len(spans) == 3 and not spans[1].string.strip() == 'Flashcards':
                name = spans[0].string[0]+' - '+spans[1].string.strip()
                print(f'Downloading {name}')
                download(exercise['href'],name)
            elif spans[0].get('class') and len(spans[0]['class']) == 2:
                print(f'Downloading {spans[0]["class"][1]}')
                download(exercise['href'],
                        spans[0]['class'][1].strip().capitalize()+
                        ' - '+
                        spans[0].string.strip())


    for file in os.listdir('/home/joaocalem/LeWagon/Challenges'):
        if file.endswith('.zip') and 'lewagon' in file:
            name= file.replace('.zip','').replace('lewagon','')
            print(name)
            file = os.path.join('/home/joaocalem/LeWagon/Challenges',file)
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall(os.path.join('/home/joaocalem/LeWagon/Challenges',name))
            os.remove(file)
            
    os.system('jupyter lab /home/joaocalem/LeWagon/Challenges')