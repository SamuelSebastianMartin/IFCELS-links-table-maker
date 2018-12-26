#! /usr/bin/env python3

from bs4 import BeautifulSoup
import requests

url_list = [
        'https://ble.soas.ac.uk/course/index.php?categoryid=103', 
        'https://ble.soas.ac.uk/course/index.php?categoryid=103&browse=courses&perpage=30&page=1', 
        'https://ble.soas.ac.uk/course/index.php?categoryid=103&browse=courses&perpage=30&page=2']
courselist = []


def get_page(url):
    r = requests.get(url, auth=('sm2', 'oeurSo61!'))
    print(r.status_code)
    return r


def extract_courses(page, courselist):
    soup = BeautifulSoup(page.content, 'html.parser')
    courses = soup.find_all('div', class_='coursename')
    courselist = []
    for course in courses:
        courselist.append((course.a.text, course.a['href']))
    return courselist


def main():
    for url in url_list:
        page = get_page(url)
        course = (extract_courses(page, courselist))
        for item in course:
            courselist.append(item)

    coursedict = {}
    courselist.sort()
    for course in courselist:
        print(course)

if __name__ == '__main__':
    main()
