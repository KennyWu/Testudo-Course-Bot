import requests
from bs4 import BeautifulSoup


response = requests.get("https://app.testudo.umd.edu/soc/search?courseId=CMSC216&sectionId=&termId=202301&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on")
# print(response.status_code)
# print(response.text)
soup = BeautifulSoup(response.content, "lxml")
divs = soup.find('div', id='CMSC216')
# print(divs)
divs = divs.find_all('div', class_='section-info-container')
for s in divs:
    print(s)
