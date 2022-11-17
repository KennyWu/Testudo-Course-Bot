import requests
from bs4 import BeautifulSoup


# response = requests.get("https://app.testudo.umd.edu/soc/search?courseId=CMSC216&sectionId=&termId=202301&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on")
# # print(response.status_code)
# # print(response.text)
# soup = BeautifulSoup(response.content, "lxml")
# divs = soup.find('div', id='CMSC216')
# print(divs.find('input', value="0"))
# new_div = divs.find_all('div', class_='section-info-container')
# for sec in new_div:
#     if "0101" in sec.find('span').text:
#         print('open seats ' + sec.find('span', class_="open-seats-count").text)
#         print('waitlist ' + sec.find('span', class_="waitlist-count").text)

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

    #TODO - add unit testing for delete
    def delete(self, course, section: set=None):
        """Deletes the course or the specific sections of courses
            - If section is not part of the existing set then nothing happens
            - Returns True if course if found and deleted
            - Returns False otherwise
        """
        success = False
        if course in self._course_selection:
            success = True
            if (section != None):
                for sec in section:
                    if sec in self.course_selection[course]:
                      self.course_selection[course].remove(sec)  
            else:
                self._course_selection.pop(course, None)
        return success  
    
    def __check_semster(self):
        if (self._semester == None):
            raise Exception("No semester added")

    def add(self, course: str, section: set = None):
        self.__check_semster()
        success = False
        if (section != None):
            if course in self._course_selection:
                if self.__verify(course, section=section) :
                    self._course_selection[course] = self._course_selection[course].union(
                        section)
                    success = True
            elif self.__verify(course, section=section):
                self._course_selection[course] = section
                success = True
        return success

    # TODO add section verification
    def __verify(self, course: str, section: set):
        url = f"https://app.testudo.umd.edu/soc/search?courseId={course}&sectionId=&termId={self._semester}&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on"
        response = requests.get(url)
        success = False
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            course_html = soup.find('div', id=course)
            if (course_html != None):
                for sec in section:
                    if soup.find('input', value=sec) != None:
                        success = True
                    else:
                        success = False
                        break
        return success

    # TODO conduct unit testing, change url

    def retrieve(self):
        self.__check_semster()
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
