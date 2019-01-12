#! /usr/bin/env python3
"""
Given urls taken from SOAS Moodle, it makes html tables of ICC, ELAS etc.
coursenames with links. These tables can be added to a Moodle 'block'.
Summer courses are found and recorded, but not exported as html table, yet.

First the urls are scaped for courses, with 'OK 200' sent to standard-out.
Then courses are sorted, and the list of courses sent to standard-out:
    Outpus should be grouped with all ELAS together, etc.
Finally, each html block is opened for testing. Close the browser to allow
the program to continue to the next phase.

This file must be in the same directory as:
    get_course_urls.py
    sort_by_module.py
    build_general_block.py
    html_table_class.py
    credentials.py
    regex_names_elas.csv  # Check here if coursenames change
    regex_names_fdps.csv
    regex_names_icc.csv

The URLs are hardcoded below. THEY WILL HAVE TO BE CHANGED EACH YEAR.
They are obtained from https://ble.soas.ac.uk/course/index.php, then
follow the link to IFCELS. There will be ~3 pages of links and ~88 courses.
Paste the urls into the code below.
"""

import get_course_urls
import sort_by_module
import build_general_block

urls = [  # Change these URLs every year
    'https://ble.soas.ac.uk/course/index.php?categoryid=103',
    'https://ble.soas.ac.uk/course/index.php?categoryid=103&browse=courses&perpage=30&page=1',
    'https://ble.soas.ac.uk/course/index.php?categoryid=103&browse=courses&perpage=30&page=2'
        ]

def main():

    get_course_urls.main(urls)
    sort_by_module.main()
    for module in ('elas', 'fdps', 'icc'):
        build_general_block.compile_table_block(module, year='2018-19')

if __name__ == '__main__':
    main()
