import argparse
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from germantechjobs.spiders.arbeitsagentur import ArbeitsagenturSpider


parser = argparse.ArgumentParser(description="scrapes data from popular german job posting sites")

parser.add_argument('-i', '--items', type=int, help='write how many items do you want to scrape')


if len(sys.argv) == 1:
    print('Please provide an argument. Use --help for more options.')
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

settings = get_project_settings()


if args.items:
    settings.set('CLOSESPIDER_ITEMCOUNT', args.items)
    print(f"Scraping limited to {args.items} items")
# the default scraped number for items is 1
else:
    settings.set('CLOSESPIDER_ITEMCOUNT', 1)
    print("Using default item limit (1)")


process = CrawlerProcess(settings)
process.crawl(ArbeitsagenturSpider)

process.start()
