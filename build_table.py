#! /usr/bin/env python3

import pandas as pd
import os

def main():
    page = []
    header = table_header()
    page.append(header)
    check_output(page)


def check_output(page):
    html = ''.join(page)
    with open('deleteme.html', 'w') as test:
        test.write(html)
    os.system('epiphany deleteme.html')

def table_header(title='ELAS COURSES 2018/19', width='100', bg_color='rgb(255, 200, 33)'):
    width = str(width)
    header = '<table style="background-color: ' + bg_color + '; width: 100%"> <caption style="background-color: ' + bg_color + '; caption-side: top"><h3>' + title + '</h3></caption>'
    return header


if __name__ == '__main__':
    main()



#<table style="background-color: rgb(255, 200, 33); width: 100%">
#        <caption style="background-color: rgb(255, 200, 33); caption-side: top"><h3>ELAS COURSES 2018/19</h3></caption>
#                <tr align="center"; style="background-color: rgb(255, 200, 33)">
#                <colgroup>
#                        <col>
#                        <col style="background-color: rgb(235, 180, 33">
#                        <col>
#                </colgroup>
#                <tr align="center">
#                        <th scope="col">Term 1
#                        </th>
#                        <th scope="col">Term 2
#                        </th>
#                        <th scope="col">Term 3
#                        </th>
#                </tr>
#                <tr align="center">
#                        <td></td>
#                        <td></td>
#                        <td></td>
#                </tr>
#                <tr align="center">
#                        <td></td>
#                        <td></td>
#                        <td></td>
#                </tr>
#                <tr align="center">
#                        <td></td>
#                        <td></td>
#                        <td></td>
#                </tr>
#                <tr align="center">
#                        <td></td>
#                        <td></td>
#                        <td></td>
#                </tr>
#                <tr align="center">
#                        <td></td>
#                        <td></td>
#                        <td></td>
#                </tr>
#                <tr align="center">
#                        <td></td>
#                        <td></td>
#                        <td></td>
#                </tr>
#                <tr align="center">
#                        <td></td>
#                        <td></td>
#                        <td></td>
#                </tr>
#                <tr><tr>
#</table>
