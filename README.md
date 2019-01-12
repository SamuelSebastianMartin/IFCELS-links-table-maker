The aim is to move from a list of URLs (the Moodle IFCELS pages) to a complete html code for a block.

`get_course_urls.py` provides pairs of coursename+url. These are saved as a `courses_scraped_urls.csv`.
`sort_by_module.py` opens `courses_scraped_urls.csv` and sorts the courses in to modules (icc, fdps etc.). The output of this is saved as courses_sorted.csv.
`build_general_block.py` then uses this data to build the actual block. It uses the helper class `html_table_class.py`.

**TO DO**
Make an `index.py` to combine all these proccesses.
