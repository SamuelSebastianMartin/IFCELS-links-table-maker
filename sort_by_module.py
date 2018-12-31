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
        if 'term ' in name.lower():  # <space> needed to avoid 'intermediate'.
            modules.append('ELAS')
        elif 'block' in name.lower():
            modules.append('Summer')
        elif '(ug)' in name.lower():
            modules.append('ICC')
        elif '(pg)' in name.lower():
            modules.append('FDPS')
        else:
            mod_name = get_hard_names(name)
            modules.append(mod_name)
    df['module'] = modules
    return df


def get_hard_names(name):
    '''Catches the ~9 courses with no obvious module keywords in the name.
    The ~5 courses with 'academic' in are proccessed first.'''
    mod_name = ''
    # Courses with 'academic' in the title.
    academic = re.compile('academic', re.IGNORECASE)
    if academic.search(name):
        hardnames = {
                'intensive': 'ICC', 'understanding': 'ICC',
                'teaching': 'Summer'
                }
        for keyword in hardnames:
            srch = re.compile(keyword, re.IGNORECASE)
            if srch.search(name):
                mod_name = hardnames[keyword]
                break
        # catch awkward FDPS 'Academic English'.
        srch = re.compile(
                '^academic\s+?english\s+?a\d{2}/\d{2}\s?', re.IGNORECASE
                )
        if srch.search(name):
            mod_name = 'FDPS'

    else:  # Courses without 'academic' in the title.
        hardnames = {
                'research': 'FDPS', 'independent': 'FDPS',
                'media': 'Summer', 'language': 'FDPS',
                'european': 'ICC'
                }
        for keyword in hardnames:
            srch = re.compile(keyword, re.IGNORECASE)
            if srch.search(name):
                mod_name = hardnames[keyword]
                break
            else:
                mod_name = 'not known'

    return(mod_name)


if __name__ == '__main__':
    main()
