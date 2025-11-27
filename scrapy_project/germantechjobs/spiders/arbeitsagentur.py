import scrapy
import json
from urllib.parse import urlencode, parse_qs, urlparse, urlunparse
from germantechjobs.items import ArbeitsAgenTur


class ArbeitsagenturSpider(scrapy.Spider):
    name = "arbeitsagentur"
    

    def start_requests(self):
        url = 'https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v6/jobs'

        params = {
            'berufsfeld': 'Informatik',
            'page': '1',
            'size': '250',
            'pav': 'false',
            'facetten': 'veroeffentlichtseit,arbeitszeit,arbeitsort'
        }

        custom_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'X-API-Key': 'jobboerse-jobsuche',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.7',
            'Correlation-Id': 'fe7ff7c2-b2d4-49ed-b764-dc6a350dd549',
            'Origin': 'https://www.arbeitsagentur.de',
            'Priority': 'u=1, i',
        }

        yield scrapy.Request(
            url=f'{url}?{urlencode(params)}', 
            callback=self.parse, 
            headers=custom_headers,
            meta={'page': 1}
        )

    def parse(self, response):
        data = json.loads(response.text)
        current_page = response.meta['page']

        jobs = data.get('ergebnisliste', [])
        
        self.logger.info(f"Page {current_page}: Found {len(jobs)} jobs")

        for job in jobs:
            yield self.extract_job_data(job, current_page)
    
        # Pagination logic
        if self.should_continue_pagination(jobs, current_page):
            next_page = current_page + 1
            next_url = self.build_next_page_url(response.url, next_page)

            yield scrapy.Request(
                url=next_url,
                callback=self.parse, 
                headers=response.request.headers,
                meta={'page': next_page}
            )
    

    def should_continue_pagination(self, jobs, current_page):
        if not jobs:
            self.logger.info("No jobs found - stopping")
            return False

        if len(jobs) < 250:
            self.logger.info(f"Only {len(jobs)} jobs - likely last page")
            return False

        if current_page >= 100:
            self.logger.info("Reached maximum page limit")
            return False

        self.logger.info(f"Continuing to next page - got {len(jobs)} jobs")
        return True
    

    def build_next_page_url(self, current_url, next_page):
        parsed = urlparse(current_url)
        query_params = parse_qs(parsed.query)
        query_params['page'] = [str(next_page)]

        new_query = urlencode(query_params, doseq=True)
        return urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))


    def extract_job_data(self, job, page_number):
        """Extract job data from the actual API response structure"""
        item = ArbeitsAgenTur()
        
        # Extract location from stellenlokationen array
        location = ""
        if job.get('stellenlokationen') and len(job['stellenlokationen']) > 0:
            first_location = job['stellenlokationen'][0]
            location = first_location.get('adresse', {}).get('ort', '').strip()
        
        # Extract published date with fallbacks
        published_date = (
            job.get('datumErsteVeroeffentlichung') or 
            job.get('veroeffentlichungszeitraum', {}).get('von') or 
            job.get('aenderungsdatum', '')
        )
        
        # Extract all the data based on the actual API structure
        item['title'] = job.get('stellenangebotsTitel', '').strip()
        item['company'] = job.get('firma', '').strip()
        item['location'] = location
        item['full_time'] = "Yes" if job.get('arbeitszeitVollzeit') else "No"
        item['ref_number'] = job.get('referenznummer') or job.get('chiffrenummer', '')
        item['apply_for_this_job'] = f"https://www.arbeitsagentur.de/jobboerse/jobsuche/detail/{item['ref_number']}"
        item['url'] = item['apply_for_this_job']
        item['tags'] = None
        return item

