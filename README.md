The aim is to move from a list of URLs (the Moodle IFCELS pages) to a complete html code for a block.
The `get_course_urls.py` provides pairs of coursename+url. These are saved as a `courses_scraped_urls.csv`.
Then `sort_by_module.py` opens `courses_scraped_urls.csv` and sorts the courses in to modules (icc, fdps etc.)
The output of this is saved as courses_sorted.csv.

**TO DO**
Make ELAS block hyperlinks.
Make FDPS, ICC, and Summer blocks
