This moves from a list of URLs (the Moodle IFCELS pages) to a complete html
table code for each IFCELS module (ICC, ELAS etc).

## USE

        `python3 index.py`
   

Note that the year is hard coded into `index.py` and will have to be updated
each year.


Note that the list of URLs in `index.py` will be the same each year. However,
the number of pages required to be read will change according to the phase
in the academic year in which the programme is run. For example, in mid-July,
the following year's ICC, ELAS & FDPS courses will be already displayed, while
the summer courses will still be for the current year. Therefore, depending
on when the program is run the number of URLs to be scraped may vary (probably 
from 3 to 4). Therefore this will have to be checked and, if necessary,
updated manually each year.

These URLs are obtained from https://ble.soas.ac.uk/course/index.php, then 
follow the link to IFCELS. There will be ~3 pages of links and ~88 courses.
Look at the first 3 or 4 pages (i.e. clicking "next") to see which pages
contain the required links. You may have to add (or comment out) one of the
 URLs in the code.

## What to expect
1.  While the URLs are scraped for courses, the terminal will show
   `OK 200` sent to standard-out for each URL.

2.  Then, while the courses are sorted, the list of courses is sent to 
    standard-out.    Output should be grouped with all ELAS together, etc.

3.  Finally, each html block is opened for testing one at a time. 
    This phase is interactive, and allows you to check the links for
    some sampls courses. Links open in a new page, and the first time
    you will have to log in. Close the browser after each module to allow
    the program to continue to the next phase.

## What code runs

- `get_course_urls.py` provides pairs of coursename+URL.
    These are saved as a `courses_scraped_urls.csv`.
- `sort_by_module.py` opens `courses_scraped_urls.csv` and sorts the courses
    in to modules (icc, fdps etc.). The output of this is saved as
    `courses_sorted.csv`.
- `build_general_block.py` then uses this data to build the actual block.
    It uses the helper class `html_table_class.py`.

- `index.py` combines all these processes.

## Requirements

Some of the code requires Linux `os.system('...')` calls.
In the same calls, `epiphany` browser is used.

### This file must be in the same directory as
#### Programs:

- `get_course_urls.py`
- `sort_by_module.py`
- `build_general_block.py`
- `html_table_class.py`
- `credentials.py`
#### Data:
- `regex_names_elas.csv`  # Check here if coursenames change
- `regex_names_fdps.csv`
- `regex_names_icc.csv`

## Troubleshooting.

-   All `os.system` calls are written for Linux only.

-   Some 'os.system' calls require epiphany-browser, though this can be
    changed to firefox or anything.

-   If the final table contents contain 'No Name' in any or all cells,
    it is probably a problem with the regex csv's. They are saved
    as, for eg, `regex_names_elas.csv`. If a course has changed its title,
    this would cause a problem here.

-   If the URLs appear to contain a mixture of last year's and next year's
    courses, it means that the wrong URLs are being scraped. Manually check
    the soas webpages for 'IFCELS' to see how many (and which) URLs are
    being scraped. You may have to alter the hard-coded URL list in
    `index.py`.
