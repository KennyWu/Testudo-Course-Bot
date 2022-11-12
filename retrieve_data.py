import requests
from bs4 import BeautifulSoup


response = requests.get("https://app.testudo.umd.edu/soc/search?courseId=CMSC216&sectionId=&termId=202301&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on")
# print(response.status_code)
# print(response.text)
soup = BeautifulSoup(response.content, "lxml")
divs = soup.find('div', id='CMSC216')
# print(divs)
new_div = divs.find_all('div', class_='section-info-container')
# print(divs.prettify)
for sec in new_div:
    print(sec)
    # if "0101" in sec.find('span').text:
    #     print('open seats ' + sec.find('span', class_="open-seats-count").text)
    #     print('waitlist ' + sec.find('span', class_="waitlist-count").text)

    

# class Retrieve:
    
#     def __init__(self, course_selection:dict = None) :
#          self.course_selection = course_selection

#     def updateFields(self, d:dict):
#         self.course_selection = d
        
#To do add testing perferably unit testing, however since small project might be more efficent to do print
    def retrieve(self):
        if (self.course_selection != None):
            response = requests.get("https://app.testudo.umd.edu/soc/search?courseId=CMSC216&sectionId=&termId=202301&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on")
            soup = BeautifulSoup(response.content, 'lxml')
            for course_name in self.course_selection.keys():
                div = soup.find('div', id=course_name)
                if (div != None):
                    new_div = divs.find_all('div', class_='section-info-container')
                    for section in self.course_selection[course_name]:
                        for section_html in new_div:
                            if section in section_html.find('span').text:
                                print('Course' + course_name)
                                print('section' + section)
                                print('open seats ' + sec.find('span', class_="open-seats-count").text)
                                print('waitlist ' + sec.find('span', class_="waitlist-count").text)     
                else:
                    raise BaseException().add_note('Could not retrieve html data for class')
            