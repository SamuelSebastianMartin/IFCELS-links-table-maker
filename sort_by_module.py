#! /usr/bin/env python3
"""
This takes a csv of coursename,url', and separates the courses into categories
by IFCELS module [ELAS, ICC, FDPS, Summer, Presessional, Insessional]
It also tries to identify unused courses.
"""

import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main():
    df, keywords = get_data()
    df = add_id_column(df)
    df = sort_by_id(df)
    df = add_users_url_column(df)
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
    df = pd.read_csv('scraped_course_urls.csv')
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


def add_users_url_column(df):
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
    '''Adds a column with the number of users in each course'''
    browser = get_browser()
    user_numbs = []
    for url in df['users_url']:
        print(url)
        user_page = browser.get(url)
        user_numb = find_user_numbers(user_page)
        user_numbs.append(user_numb)
    df['no_of_users'] = user_numbs
    print(df)#
    return df


def get_browser():
    '''Returns selenium browser, logged in to Moodle.'''
    login = 'https://ble.soas.ac.uk/login/index.php'

    browser = webdriver.Firefox()
    browser.get(login)
    browser.find_element_by_id("username").send_keys("sm2")
    browser.find_element_by_id("password").send_keys("oeurSo61!")
    browser.find_element_by_id("loginbtn").click()
    return browser


def find_user_numbers(page):
    return 99

if __name__ == '__main__':
    main()
