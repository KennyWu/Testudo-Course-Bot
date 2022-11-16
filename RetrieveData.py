import requests
from bs4 import BeautifulSoup


# response = requests.get("https://app.testudo.umd.edu/soc/search?courseId=CMSC216&sectionId=&termId=202301&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on")
# # print(response.status_code)
# # print(response.text)
# soup = BeautifulSoup(response.content, "lxml")
# divs = soup.find('div', id='CMSC216')
# print(divs)
# new_div = divs.find_all('div', class_='section-info-container')
# # print(divs.prettify)
# for sec in new_div:
#     print(sec)
#     # if "0101" in sec.find('span').text:
#     #     print('open seats ' + sec.find('span', class_="open-seats-count").text)
#     #     print('waitlist ' + sec.find('span', class_="waitlist-count").text)

# TODO - please add testing holy shit add testing i wrote too much code i dont know if it works lmao


class Retrieve:

    def __init__(self, course_selection: dict = None, semester: str = None):
        self._course_selection = course_selection
        self._semester = semester

    @property
    def semester(self):
        return self._semester

    @semester.setter
    def semester(self, semester: str):
        self._semester = semester

    @property
    def course_selection(self):
        return self._course_selection

    @course_selection.setter
    def course_selection(self, d: dict):
        self._course_selection = d

    def delete(course, Section=None):
        raise Exception

    def add(self, course: str, section: set = None):
        success = False
        if (section != None):
            if course in self._course_selection:
                self._course_selection[course] = self._course_selection[course].union(
                    section)
                success = True
            elif self.__verify(course):
                self._course_selection[course] = section
                success = True
        return success

    # TODO add section verification
    def __verify(self, course: str, section: set = None):
        url = f"https://app.testudo.umd.edu/soc/search?courseId={course}&sectionId=&termId={self._semester}&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on"
        response = requests.get(url)
        if response.status_code == 400:
            return False
        soup = BeautifulSoup(response.content, 'lxml')
        return soup.find('div', id=course) != None

    # TODO conduct unit testing, change url

    def retrieve(self):
        if (self._course_selection != None):
            response = requests.get("https://app.testudo.umd.edu/soc/search?courseId=CMSC216&sectionId=&termId=202301&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on")
            soup = BeautifulSoup(response.content, 'lxml')
            for course_name in self._course_selection.keys():
                div = soup.find('div', id=course_name)
                if (div != None):
                    new_div = div.find_all(
                        'div', class_='section-info-container')
                    for section in self._course_selection[course_name]:
                        for section_html in new_div:
                            if section in section_html.find('span').text:
                                print('Course' + course_name)
                                print('section' + section)
                                print('open seats ' + sec.find('span',
                                      class_="open-seats-count").text)
                                print('waitlist ' + sec.find('span',
                                      class_="waitlist-count").text)
                else:
                    raise BaseException().add_note('Could not retrieve html data for class')
        else:
            return False
