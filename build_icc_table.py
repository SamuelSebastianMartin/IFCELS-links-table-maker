#! /usr/bin/env python3

import pandas as pd
import os
import html_table_class as table
import re

def main():
    df = pd.read_csv('courselist_icc.csv')
    add_brief_name(df)
    print(df['brief name'])
    add_href(df)
    build_block(df)
    os.system('epiphany icc_block.html')


def add_brief_name(df):
    """Extracts the display name from the coursename number."""
    brief_names = []

    for index, row in df.iterrows():
        name = (row['coursename'])

        art = re.compile(r'\bart\b', re.IGNORECASE).search(name)
        bus = re.compile(r'\bbusiness\b', re.IGNORECASE).search(name)
        dev = re.compile(r'\bdevelopment\b', re.IGNORECASE).search(name)
        econ = re.compile(r'\beconomic.?\Wtheory\b/', re.IGNORECASE).search(name)
        est = re.compile(r'\beuropean\Wsociety\b', re.IGNORECASE).search(name)
        hist = re.compile(r'\bhistory\b', re.IGNORECASE).search(name)
        aceng = re.compile(r'\bintensive\Wenglish\b', re.IGNORECASE).search(name)
        law = re.compile(r'\blaw\b', re.IGNORECASE).search(name)
        lit = re.compile(r'\bliterature\b', re.IGNORECASE).search(name)
        qm = re.compile(r'\bquantitative\Wmethods\b', re.IGNORECASE).search(name)
        med = re.compile(r'\bmedia\b', re.IGNORECASE).search(name)
        pol = re.compile(r'\bpolitics\b', re.IGNORECASE).search(name)
        umw = re.compile(r'\bUnderstanding\Wthe\WModern\WWorld\b', re.IGNORECASE).search(name)

        for course in [art, bus, dev, econ, est, hist, aceng,
                        law, lit, qm, med, pol, umw]:

            if course: #  Check regex search
                brief_names.append(course.group())

    df['brief name'] = brief_names
    return brief_names



def add_href(df):
   """Adds a new column to df, giving the html code that will appear in the
   final table. Whatever is in this code will be placed between the tags
   which define the table cell: <td> and </td>. Therefore the Name and href
   must be included: eg '<a href="https://linkpage">Course Name</a>"""
   hrefs = []

   for index, row in df.iterrows():
       name = (row['brief name'])
       url = (row['url'])
       href = '<a href="' + url + '" target="_blank" >' + name + '</a>'
       hrefs.append(href)
   df['href'] = hrefs
   print(df['href'])
   return hrefs


def build_block(df):
   block = table.HtmlTable()
   block.bg_color = '#95aba9'
   block.table_header(title='ICC Courses: 2018/19')
   add_rows(block, df)

   block.write_page('icc_block.html')


def add_rows(block, df):
    courselist = df['href'].tolist()
    while len(courselist) >= 3:
        a, b, c = courselist[0], courselist[1], courselist[2]
        block.add_row(a, b, c)
        for item in (a, b, c):
            courselist.remove(item)
    if len(courselist) == 2:
        a, b, c = courselist[0], courselist[1], ''
        block.add_row(a, b, c)
        return
    elif len(courselist) == 1:
        a, b, c = courselist[0], '', ''
        block.add_row(a, b, c)
        return
    else:
        return

if __name__ == '__main__':
    main()
