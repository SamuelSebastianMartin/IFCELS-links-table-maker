#! /usr/bin/env python3

import pandas as pd
import os
import html_table_class as table
import re

def main():
    df = pd.read_csv('courselist_fdps.csv')
    add_brief_name(df)
    print(df['brief name'])
    add_href(df)
    build_block(df)
    os.system('epiphany fdps_block.html')


def add_brief_name(df):
    """Extracts the display name from the coursename number."""
    brief_names = []

    for index, row in df.iterrows():
        name = (row['coursename'])

        aeng = re.compile(r'\bacademic\Wenglish\b', re.IGNORECASE).search(name)
        bus = re.compile(r'\bbusiness\b', re.IGNORECASE).search(name)
        cult = re.compile(r'\bculture.?\b', re.IGNORECASE).search(name)
        dev = re.compile(r'\bdevelopment\b', re.IGNORECASE).search(name)
        soc = re.compile(r'\bsociety\b', re.IGNORECASE).search(name)
        gram = re.compile(r'\bgrammar\b', re.IGNORECASE).search(name)
        ielts = re.compile(r'\bielts\b', re.IGNORECASE).search(name)
        ir = re.compile(r'\binternational\Wrelations\b', re.IGNORECASE).search(name)
        isp = re.compile(r'\bindependent\Wstudy\b', re.IGNORECASE).search(name)
        law = re.compile(r'\blaw\b', re.IGNORECASE).search(name)
        med = re.compile(r'\bmedia\b', re.IGNORECASE).search(name)
        rsch = re.compile(r'\bresearch\Wmethods\b', re.IGNORECASE).search(name)
        lang = re.compile(r'\benglish\Wlanguage\b', re.IGNORECASE).search(name)

        for course in [aeng, bus, cult, dev, soc, gram, ielts,
                        ir, isp, law, med, rsch, lang]:

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
       href = '<a href="' + url + '" >' + name + '</a>'
       hrefs.append(href)
   df['href'] = hrefs
   print(df['href'])
   return hrefs


def build_block(df):
   block = table.HtmlTable()
   block.bg_color = '#fdd4ce'
   block.table_header(title='FDPS Courses: 2018/19')
   add_rows(block, df)

   block.write_page('fdps_block.html')


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
