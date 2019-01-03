#! /usr/bin/env python3


class HtmlTable:
    """Creates an 'html' table in sections: 'header', 'columns',
    and 'row'. Functionality is very basic.
    Output is a string of html code, optionally saved to file."""
    def __init__(self):
        self.width = str(100)
        self.bg_color = 'rgb(255, 200, 33)'
        self.alt_bg_color = 'rgb(235, 180, 33)'
        self.page = []

    def table_header(self, title='Title'):
        """Returns the html code for a table header, with title."""
        header = '<table style="background-color: ' \
                + self.bg_color \
                + '; width: 100%"> <caption style="background-color: ' \
                + self.bg_color \
                + '; caption-side: top"><h3>' \
                + title + '</h3></caption>'
        self.page.append(header)
        return header

    def table_columns(self):
        columns = '<colgroup>\
            <col style="background-color: ' + self.bg_color + '">,\
            <col style="background-color: ' + self.alt_bg_color + '">\
            <col style="background-color: ' + self.bg_color + '">\
                </colgroup>'
        self.page.append(columns)
        return columns

    def column_headings(self, td1='Col 1', td2='Col 2', td3='Col 3'):
        col_head = '<tr align="center">\
                        <th scope="col">' + td1 + '</th>\
                        <th scope="col">' + td2 + '</th>\
                        <th scope="col">' + td3 + '</th>\
                    </tr>'
        self.page.append(col_head)
        return col_head

    def add_row(self, td1='entry', td2='entry', td3='entry'):
        row = '<tr align="center">\
                    <td>' + td1 + '</td>\
                    <td>' + td2 + '</td>\
                    <td>' + td3 + '</td>\
                </tr>'
        self.page.append(row)
        return row

    def write_page(self, save_as='html_table.html'):
        """Closes table with </table>, and saves table.
        Default name is 'html_table.html'."""
        self.page.append('</table>')
        full_page = ''.join(self.page)
        with open(save_as, 'w') as f:
            f.write(full_page)

    def test_HtmlTable(self):
        """Builds a dummy table using all the class functionality, and opens
        the table in a browser to test.
        The 'os.system()' call should be adjusted for your own OS and browser."""
        self.test_page = HtmlTable()
        self.test_page.bg_color = 'red'
        self.test_page.table_header(title='New Title')
        self.test_page.alt_bg_color = "rgb(235, 180, 33"
        self.test_page.table_columns()
        self.test_page.column_headings(td1='One', td2='Two', td3='Three')
        self.test_page.add_row()
        self.test_page.add_row(td1='next', td2='next', td3='next')
        self.test_page.write_page()

        import os
        os.system('epiphany html_table.html')


if __name__ == '__main__':
    tryout = HtmlTable()
    tryout.test_HtmlTable()
