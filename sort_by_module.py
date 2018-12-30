#! /usr/bin/env python3
"""
This takes a csv of coursename,url', and separates the courses into categories
by IFCELS module [ELAS, ICC, FDPS, Summer, Presessional, Insessional]
It also tries to identify unused courses.
"""

import pandas as pd
import re


def main():
    df = pd.read_csv('scraped_course_urls.csv')
    df = add_id_column(df)
    df.set_index('course_id', inplace=True)
    df = add_module_names(df)

    df = df.sort_index()
    print(df[['module', 'coursename']].to_string())


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


def add_module_names(df):
    '''Adds a column with module name: eg 'ELAS' or 'ICC' '''
    # Simple keywords first: no regex. Will get all but a few.
    modules = []
    for name in df['coursename']:
        if 'term' in name.lower():
            modules.append('ELAS')
        elif 'block' in name.lower():
            modules.append('Summer')
        elif '(ug)' in name.lower():
            modules.append('ICC')
        elif '(pg)' in name.lower():
            modules.append('FDPS')
        else:
            modules.append('not known')
    df['module'] = modules
    # Hard cases still to solve.
    return df


if __name__ == '__main__':
    main()
