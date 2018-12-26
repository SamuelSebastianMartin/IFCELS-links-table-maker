#! /usr/bin/env python3

from bs4 import BeautifulSoup
import requests

url = 'https://ble.soas.ac.uk/course/index.php?categoryid=103'
coursedict = {}


def get_page(url):
    r = requests.get(url, auth=('sm2', 'oeurSo61!'))
    print(r.status_code)
    return r


def extract_courses(page, coursedict):
    soup = BeautifulSoup(page.content, 'html.parser')
    courses = soup.find_all('div', class_='coursename')
    for course in courses:
        print(course.a.text, course.a['href'])


def main():
    page = get_page(url)
    extract_courses(page, coursedict)

if __name__ == '__main__':
    main()
