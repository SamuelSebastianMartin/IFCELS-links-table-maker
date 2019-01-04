#! /usr/bin/env python3

import pandas as pd
import os
import html_table_class as table
import re

def main():
    df = pd.read_csv('courselist_elas.csv')
    add_brief_name(df)
    build_block(df)
    os.system('epiphany html_table.html')


def add_brief_name(df):
    brief_names = []

    for index, row in df.iterrows():
        name = (row['coursename'])
        term = re.compile(r'term\s+?[123]', re.IGNORECASE).search(name)
        # Academic English
        comp = re.compile(r'academic\W+english\W+a[1-5]\b', re.IGNORECASE)
        srch = comp.search(name)
        if srch:
            grp = srch.group()
            if term:
                t = ' (t' + term.group()[-1] + ')'
            brief_names.append(grp[-2:] + t)

        else:
            briefname = tricky_names(name, term)
            brief_names.append(briefname)

    df['brief name'] = brief_names
    return brief_names


def tricky_names(name, term):
    """Extracts the display name from the coursename, and appends the term
    number.
    """
    art = re.compile(r'\bart\b', re.IGNORECASE).search(name)
    hum = re.compile(r'\bhumanities\b', re.IGNORECASE).search(name)
    bus = re.compile(r'\bbusiness\b', re.IGNORECASE).search(name)
    ielts = re.compile(r'\bielts\b', re.IGNORECASE).search(name)
    els = re.compile(r'\blanguage\Wskills\b', re.IGNORECASE).search(name)
    med = re.compile(r'\bmedia\b', re.IGNORECASE).search(name)
    rsch = re.compile(r'\bresearch\Wmethods\b', re.IGNORECASE).search(name)
    soc = re.compile(r'\bsocial\Wsciences\b', re.IGNORECASE).search(name)

    for course in [art, hum, bus, ielts, els, med, rsch, soc]:

        if course: #  Check regex search
            if term: #  Get term number, if there is one.
                t = ' (t' + term.group()[-1] + ')'
                return course.group() + t
            else:
                return course.group()


    else:
        return None


def build_block(df):
    block = table.HtmlTable()
    block.table_header(title='ELAS Courses: 2018/19')
    block.table_columns()
    block.column_headings(td1='Term 1', td2='Term 2', td3='Term 3')
    add_rows(block, df)

    block.write_page()


def add_rows(block, df):
    courselist = df['brief name'].tolist()
    while len(courselist) >= 3:
        a, b, c = courselist[0], courselist[1], courselist[2]
        block.add_row(a, b, c)
        for item in (a, b, c):
            courselist.remove(item)


if __name__ == '__main__':
    main()
