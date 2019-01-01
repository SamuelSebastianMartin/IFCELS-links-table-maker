#! /usr/bin/env python3
'''
Takes the url of all Moodle IFCELS course pages, which are hard coded here,
and saves a csv of every file with its URL
If this fails, the most likely problems are a) that the url_list has changed.
b) that the classname in the html is no longer "coursename". These will have
to be investigated with "inspect element" in the browser.
It should find around 88 courses.
'''
from bs4 import BeautifulSoup
import requests

url_list = [
        'https://ble.soas.ac.uk/course/index.php?categoryid=103',
        'https://ble.soas.ac.uk/course/index.php?categoryid=103&browse=courses&perpage=30&page=1',
        'https://ble.soas.ac.uk/course/index.php?categoryid=103&browse=courses&perpage=30&page=2']


def get_page(url):
    '''Takes url and returns a 'requests' html object.'''
    import credentials
    r = requests.get(url, auth=('credentials.username',
                                'credentials.password'))
    if r.status_code == 200:
        print('OK\t', r.status_code, url)
    else:
        print('ERROR\t', r.status_code, url)
    return r


def extract_courses(page):
    '''Takes soas html object, and returns list of tuples: (course, url).'''
    soup = BeautifulSoup(page.content, 'html.parser')
    courses = soup.find_all('div', class_='coursename')
    courselist = []
    for course in courses:
        courselist.append((course.a.text, course.a['href']))
    return courselist


def main():
    coursedict = {}
    all_courselist = []

    # Get list of [(coursename,url)...]
    for url in url_list:
        page = get_page(url)
        courses_on_page = (extract_courses(page))
        for item in courses_on_page:
            all_courselist.append(item)

    # Clean up list & add headers.
    courseset = set(all_courselist)
    all_courselist = list(courseset)
    all_courselist.sort()
    number_of_courses = len(all_courselist)
    all_courselist.insert(0, ('coursename', 'url'))  # Column headers.

    # Write results
    f = open('courses_scraped_urls.csv', 'w')
    for course in all_courselist:
        f.write(course[0] + ',' + course[1] + '\n')
    f.close()
    print(number_of_courses, 'courses found')


if __name__ == '__main__':
    main()
