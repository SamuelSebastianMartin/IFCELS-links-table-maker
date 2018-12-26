#! /usr/bin/env python3
'''
Takes the url of all Moodle IFCELS course pages, which are hard coded here,
and saves a csv of every file with its URL
'''
from bs4 import BeautifulSoup
import requests

url_list = [
        'https://ble.soas.ac.uk/course/index.php?categoryid=103', 
        'https://ble.soas.ac.uk/course/index.php?categoryid=103&browse=courses&perpage=30&page=1', 
        'https://ble.soas.ac.uk/course/index.php?categoryid=103&browse=courses&perpage=30&page=2']


def get_page(url):
    '''Takes url and returns a 'requests' html object.'''
    r = requests.get(url, auth=('sm2', 'oeurSo61!'))
    if r.status_code == 200:
        print('OK\t', r.status_code, url)
    else:
        print('ERROR\t', r.status_code, url)
    return r


def extract_courses(page, courselist):
    '''Takes soas html object, and returns list of tuples: (course, url).'''
    soup = BeautifulSoup(page.content, 'html.parser')
    courses = soup.find_all('div', class_='coursename')
    courselist = []
    for course in courses:
        courselist.append((course.a.text, course.a['href']))
    return courselist


def main():
    courselist = []
    for url in url_list:
        page = get_page(url)
        course = (extract_courses(page, courselist))
        for item in course:
            courselist.append(item)

    coursedict = {}
    courselist.sort()
    f = open('course_link_list.csv', 'w')
    for course in courselist:
        f.write(course[0] + ',' + course[1] + '\n')
    f.close()

if __name__ == '__main__':
    main()
