#! /usr/bin/env python3
"""
This takes a csv of coursename,url', and separates the courses into categories
by IFCELS module [ELAS, ICC, FDPS, Summer, Presessional, Insessional]
"""

import pandas as pd
import re
import requests
from bs4 import BeautifulSoup


def main():
    df, keywords = get_data()
    df = add_id_column(df)
    df = sort_by_id(df)
    df = add_users_column(df)
    df = add_user_numb(df)
#    test(df, keywords)
    df.to_csv('IFCELS_Moodle_sorted_by_id.csv')


def test(df, keywords):  #
    '''To produce test feedback while exploring this code.'''
    print('TEST DATA')
    for key in keywords:
        print(key, keywords[key])
    print(df)
    print()


def get_data():
    '''Reads csv into dataframe, and defines keyword dictionary to help with
    deciding if a course is ICC or ELAS etc. For example, FDPS tend to use
    the code (pg), 'block' = summer, and 'Term' = ELAS.'''
    df = pd.read_csv('course_link_list.csv')
    keywords = {'elas': ['Term', 'A1 ', 'A2 ', 'A3'], 'fdps': ['(pg)']}
    return df, keywords


def add_id_column(df):
    '''Adds an extra column with the course id. This is taken from the url.'''
    course_id = []
    regex = re.compile(r'[0-9]+?$')
    for row in df['url']:
        srch = regex.search(row)
        numerals = srch.group()
        course_id.append(numerals)
    df['course_id'] = course_id
    return df


def sort_by_id(df):
    '''Puts courses in order of course id.'''
    df_id = df.sort_values(by=['course_id'])
    return df_id


def add_users_column(df):
    '''Makes a new column with the url of the 'enrolled users' page.
    The url involves substituting 'users/index' for 'course/view' in the url.
    '''
    urls = []
    for url in df['url']:
        index = url.index('course/view')
        span = (index, index + len('course/view'))
        users_url = url[0:span[0]] + 'user/index' + url[span[1]:]
        urls.append(users_url)
    df['users_url'] = urls
    return df


def add_user_numb(df):
    user_numbs = []
    for url in df['users_url']:
        page = get_page(url)
        print(page)
        user_numbers = get_user_numbers(page)
    return df


def get_page(url):  # Copied from get_course_urls.py
    '''Takes url and returns a 'requests' html object.'''
    r = requests.get(url, auth=('sm2', 'oeurSo61!'))
    if r.status_code == 200:
        print('OK\t', r.status_code, url)
    else:
        print('ERROR\t', r.status_code, url)
    return r


def get_user_numbers(page):
    '''Takes soas html object, and returns list of tuples: (course, url).'''
    soup = BeautifulSoup(page.content, 'html.parser')
    attr = soup.find('div', class_='userlist')
    print(attr)
#    user_numbers = attr.p.text
    return user_numbers

    courselist.append((course.a.text, course.a['href']))
    return courselist

if __name__ == '__main__':
    main()
