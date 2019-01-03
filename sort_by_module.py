#! /usr/bin/env python3
"""
This takes courses_scraped_urls.csv, a csv of coursename+url', so it must be
run after get_course_urls.py. It separates the courses into categories
by IFCELS module [ELAS, ICC, FDPS, Summer, Presessional, Insessional],
and saves the resulting dataframes as (eg) 'icc.csv', 'summer.csv'. This is
in preparation to the modules being proccessed individually into html tables.
"""

import pandas as pd
import re


def main():
    df = pd.read_csv('courses_scraped_urls.csv')  # From get_course_urls.py
    df = add_id_column(df)
    df.set_index('course_id', inplace=True)
    df = add_module_names(df)

    df = df.sort_index()
    elas, summer, fdps, icc = group_and_split(df)
    elas.to_csv('courselist_elas.csv')
    summer.to_csv('courselist_summer.csv')
    fdps.to_csv('courselist_fdps.csv')
    icc.to_csv('courselist_icc.csv')
    df.to_csv('courses_sorted.csv')
    for mod in [elas, summer, fdps, icc]:
        print(mod[['module', 'coursename']].to_string())


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
                r'^academic\s+?english\s+?a\d{2}/\d{2}\s?', re.IGNORECASE
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


def group_and_split(df):
    '''Splits the entire ICC dataframe into individual modules (eg icc).'''
    df.groupby('module')
    elas = df.groupby('module').get_group('ELAS')
    summer = df.groupby('module').get_group('Summer')
    fdps = df.groupby('module').get_group('FDPS')
    icc = df.groupby('module').get_group('ICC')
    return elas, summer, fdps, icc


if __name__ == '__main__':
    main()
