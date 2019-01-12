This moves from a list of URLs (the Moodle IFCELS pages) to a complete html table code for each IFCELS module (ICC, ELAS etc).

## USE

   `python3 index.py`
    Note that the list of URLs in `index.py` will have to be updated manually each year.

They are obtained from https://ble.soas.ac.uk/course/index.php, then follow the link to IFCELS. There will be ~3 pages of links and ~88 courses.
Paste the urls into the code.

## What to expect
1. the urls are scaped for courses, with `OK 200` sent to standard-out for each url.

2. courses are sorted, and the list of courses sent to standard-out

    Output should be grouped with all ELAS together, etc.

3.  Finally, each html block is opened for testing one at a time. Close the browser to allow
the program to continue to the next phase.

## What code runs

- `get_course_urls.py` provides pairs of coursename+url. These are saved as a `courses_scraped_urls.csv`.
- `sort_by_module.py` opens `courses_scraped_urls.csv` and sorts the courses in to modules (icc, fdps etc.). The output of this is saved as courses_sorted.csv.
- `build_general_block.py` then uses this data to build the actual block. It uses the helper class `html_table_class.py`.

- `index.py` combines all these proccesses.

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
All `os.system` calls are written for Linux only.
    Some 'os.system' calls require epiphany-browser. Can change to firefox or anything.
    If the final table contents contain 'No Name' in any or all cells,
    it is probably a problem with the regex csv's. They are saved
    as, for eg, 'regex_names_elas.csv
