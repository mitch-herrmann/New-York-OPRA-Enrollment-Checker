
# New York OPRA Enrollment Checker

A simple tool for checking the NYS OPRA enrollment status for a list of provider NPIs. The program reads NPIs in from a local .csv file, queries the OPRA site (https://www.emedny.org/info/opra.aspx) using a Selenium Webdriver, and saves two local .csv files with the results -- one containing the list of NPIs that are currently enrolled, and the other with the NPIs that are not. 


## Software Requirements
- This code was written using Python 3.10
- Selenium and a Chromedriver