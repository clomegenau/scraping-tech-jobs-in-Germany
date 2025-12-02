# scraping-tech-jobs-in-Germany
using scrapy to scrape tech job posts from Germany from various job sites.

## Features:
- store the data in a sqlite3 data base.
- scrapes job listings from arbeitsagentur.de API.

## Installation:
`git clone https://github.com/clomegenau/scraping-tech-jobs-in-Germany`

`cd scraping-tech-jobs-in-Germany/`

`python3 -m venv venv`

`source venv/bin/activate`

`pip3 install -r  requirements.txt`

## Usage:
- you can run 'run_scraper.py' without activating the venv.
- run the script to see the different flags that you can use.
    `python3 run_scraper.py --help`
- you can find the results in a file called 'scraped_data.db'.

**Note**: if you don't specify the desired number after the -i flag, the default number of scraped items will be 1,
