#! /usr/bin/env python3

"""
Given the input of the name of a course module (eg ICC, ELAS etc.)
This program produces an html table which displays all the Moodle
courses in that module, with links to the Moodle page.
It requires:
    a list of 'regex_names_***.csv' to match the coursename to the
    abbreviated name displayed in the table.
    'courselist_****.csv', which is output from 'sort_by_module.py'.
    The helper class 'html_table_class.py'
Possible Errors:
    All 'os.system' calls are written for Linux only.
    Some 'os.system' calls require epiphany-browser. Can change to anything.
    If the final table contents contain 'No Name' in any or all cells,
    it is probably a problem with the regex csv's. They are saved
    as, for eg, 'regex_names_elas.csv'
"""
import pandas as pd
import os
import html_table_class as table
import re


def main():
    """
    'main()' is really a wrapper for 'compile_table_block()' so
    the program can run as a stand-alone.
    """
    module = input('Which Module are you building,\
                    \nELAS, ICC, FDPS or Summer: ')
    block = compile_table_block(module)


def compile_table_block(module, year='2019-20'):
    """
    When passed the name of a module, it outputs a html table, and
    saves it as '*module_name*_block.html'.
    """
    # Get variable names.
    module = module.lower()
    module_title = module.upper() + ' Courses: ' + year
    module_courselist = 'courselist_' + module + '.csv'
    module_saveas = module + '_block.html'
    module_regex = 'regex_names_' + module + '.csv'
    os_instruction = 'epiphany ' + module_saveas
    if module == 'icc':
        bg_color = '#d3f486'
    if module == 'elas':
        bg_color = '#ffc821'
    if module == 'fdps':
        bg_color = '#fdd4ce'

    # Run program.
    df = pd.read_csv(module_courselist)  # Output from sort_by_module.py
    add_term(df)  # Extra column on dataframe
    add_brief_name(df, module_regex)
    add_href(df)
    block = build_block(df, module_saveas, module_title, bg_color)
    os.system(os_instruction)  # Opens in browser, for test.
    return block


def add_term(df):
    "Adds a column to the dataframe with the term/block number"
    terms = []

    for index, row in df.iterrows():
        name = (row['coursename'])
        term = re.compile(r'\bterm\s+?[123]', re.IGNORECASE).search(name)
        block = re.compile(r'\bblock\s+?[123]', re.IGNORECASE).search(name)
        if term:
            terms.append(term.group()[-1])  # Add term number
        elif block:
            terms.append(block.group()[-1])  # Add block number
        else:
            terms.append(None)  # 'None' if no term or block in coursename.
    df['term/block'] = terms


def add_brief_name(df, module_regex):
    """Adds a column with the shortened coursename that will be displayed
    in the final table."""
    brief_names = []

    for index, row in df.iterrows():
        name = (row['coursename'])
        term = (row['term/block'])
        brief_name = assign_names(name, module_regex)
        if brief_name:
            brief_names.append(brief_name)
        else:
            brief_names.append('No Name')

    df['brief name'] = brief_names
    return brief_names


def assign_names(name, module_regex):
    """Extracts the display name from the coursename.
    The 'regex_names' list is unique for each module (ICC, ELAS etc.), and
    must be hard coded. Each item in the list is a 2-tuple, consisting in
    a regex to identify the course from the official course title, and
    a display name for the table. Each regex will match only one result,
    except ELAS A1, A2 etc, which reterns the group() of the regex"""

    # Academic English courses: A1, A2 etc.
    ae = re.compile(r'academic\W+english\W+a[1-5]\b',
                    re.IGNORECASE).search(name)
    if ae:
        return ae.group()[-2:]

    else:
        # Other courses: read the list of regex/name pairs.
        regex_names = pd.read_csv(module_regex, sep=';')

        for index, row in regex_names.iterrows():
            regex = row['regex']
            if re.compile(regex, re.IGNORECASE).search(name):  # if regex found
                return row['name']

    # In the unlikely event of no match found:
    return None


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
    return hrefs


def build_block(df, module_saveas, module_title, bg_color):
    block = table.HtmlTable()
    block.bg_color = bg_color
    block.table_header(title=module_title)
    if 'elas' in module_saveas or 'summer' in module_saveas:
        #  Only make columns for ELAS and SUMMER.
        block.table_columns()
        block.column_headings(td1='Term 1', td2='Term 2', td3='Term 3')
    add_rows(block, df)

    block.write_page(module_saveas)
    return block


def add_rows(block, df):
    """
    Adds the row of links and names. This is the actual content,
    once the column headers and title are done.
    """
    courselist = df['href'].tolist()
    while len(courselist) >= 3:  # Only works for 3 columns
        a, b, c = courselist[0], courselist[1], courselist[2]
        block.add_row(a, b, c)
        for item in (a, b, c):
            courselist.remove(item)
    if len(courselist) == 2:  # Deal with remainders
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
