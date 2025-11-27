import argparse
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings



parser = argparse.ArgumentParser(description="scrapes data from popular german job posting sites")

parser.add_argument('-s', '--spiders', choices=['1', '2', 'all'], default="all", help='write how many spiders do you want to run(required)')
parser.add_argument('-i', '--items', type=int, help='write how many items do you want to scrape(you can only insert a number that is equal or higher than 250)')


if len(sys.argv) == 1:
    print('Please provide an argument. Use --help for more options.')
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

settings = get_project_settings()

if args.spiders == '1':
    print('running scraper...')
    print('running one spider...')
    spiders_to_run = ['arbeitsagentur']
elif args.spiders == '2':
    print('running scraper...')
    print('running two spiders...')
    spiders_to_run = ['berlinstartupjobs', 'arbeitsagentur']
elif args.spiders == 'all':
    print('running scraper...')
    print('running all spiders...')
    spiders_to_run = ['berlinstartupjobs', 'arbeitsagentur']


if args.items:
    settings.set('CLOSESPIDER_ITEMCOUNT', args.items)
    print(f"Scraping limited to {args.items} items")
# you can't set it lower than 250 because of arbetisagentur.py Pagination logic
else:
    settings.set('CLOSESPIDER_ITEMCOUNT', 250)
    print("Using default item limit (250)")

process = CrawlerProcess(settings)

for spider_name in spiders_to_run:
    print(f'Starting: {spider_name}')
    process.crawl(spider_name)

process.start()
