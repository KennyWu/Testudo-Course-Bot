import requests
from bs4 import BeautifulSoup


class Retrieve:

    def __init__(self, course_selection: dict = dict(), semester: str = None):
        """Initializes the retrieve object with a course selection dictionary and
        semsester to be retrieved

        Args:
            course_selection (dict, optional): _description_. Defaults to None.
                Format is CourseName:str : {section1:str, section2:str}
            semester (str, optional): _description_. Defaults to None.
                If semester is None and other methods are called Exception will be raised
        """
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

    def delete(self, course: str, section: set = None):
        """Deletes the course or the specific sections of courses

        Args:
            course (str): courses to be deleted
            section (set, optional): sections to be deleted, if no set is passed in and only course
                is passed then, delete entire course from entry 
        Returns:
            True: if successfully deleted, or course at least exists within the entries
            False: If course is never found within the dictionary entry 
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
        """Private method for verifying if the semester exists 
        If semester==None then an exception is raised

        Raises:
            Exception: Exception raised with descriptiong 'No semester added'
        """
        if (self._semester == None):
            raise Exception("No semester added")

    def add(self, course: str, section: set = None):
        """Adds course and sections associated with course to dictionary entry

        Args:
            course (str): course to be added
            section (set, optional): sections to be added,
             if section == None, nothing will be added

        Returns:
            True: if courses and sections are succesfully added
            False: if courses and sections are not added due to being invalid or other
        """
        self.__check_semster()
        success = False
        if (section != None):
            if course in self._course_selection:
                if self.__verify(course, section=section):
                    self._course_selection[course] = self._course_selection[course].union(
                        section)
                    success = True
            elif self.__verify(course, section=section):
                self._course_selection[course] = section
                success = True
        return success

    def __verify(self, course: str, section: set):
        """private method to verify the course and section are actually part of registry

        Args:
            course (str): course to be verified
            section (set): sections to be verified 

        Returns:
            True: If courses and sections are valid
            False: If courses or sections are invalid
        """
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
        """
        Retrieves all data on the courses and returns in dict format

        Returns:
            dict: format (str: dict(tuple()))
        """
        self.__check_semster
        data = dict()
        if (self._course_selection != None):
            for course in self._course_selection:
                data[course] = dict()
                response = requests.get(
                    f'https://app.testudo.umd.edu/soc/search?courseId={course}&sectionId=&termId={self._semester}&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on')
                html_data = BeautifulSoup(response.content, 'lxml')
                html_data = html_data.find('div', id=f'{course}')
                html_set = html_data.find_all(
                    'div', class_='section delivery-f2f')
                for html_course in html_set:
                    section = html_course.find(
                        'span', class_='section-id').text
                    section = section.strip()
                    if section in self._course_selection[course]:
                        times = html_course.find(
                            'span', class_='section-days').text
                        times += " " + \
                            html_course.find(
                                'span', class_='class-start-time').text
                        times += " " + \
                            html_course.find(
                                'span', class_='class-end-time').text
                        open_seats = html_course.find(
                            'span', class_="open-seats-count").text
                        waitlist = html_course.find(
                            'span', class_="waitlist-count").text
                        data[course][section] = (times, open_seats, waitlist)
        return data
