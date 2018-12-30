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
    test(df, keywords)
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


if __name__ == '__main__':
    main()
