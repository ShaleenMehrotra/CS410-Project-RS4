from bs4 import BeautifulSoup  # For HTML parsing
from urllib.request import urlopen  # Website connections
import re  # Regular expressions
from time import sleep  # To prevent overwhelming the server between connections
import sqlite3
from OfflineProcessors.JobListingUrls import finance
from OfflineProcessors.JobListingUrls import information_technology
from OfflineProcessors.JobListingUrls import telecommunication
from OfflineProcessors.JobListingUrls import health_care
from OfflineProcessors.JobListingUrls import insurance


from libs import DatabaseProvider as db

import time

headers = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"

def __drop_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS job_listings')

def __create_job_listings_table(create):
    if create:
        connection = db.get_db()
        cursor = connection.cursor()
        __drop_table(cursor)
        cursor.execute('CREATE TABLE job_listings(sector TEXT, job_title TEXT, company_name TEXT, salary TEXT, location TEXT, url TEXT, job_description TEXT)')
        cursor.close()
        connection.close()

def __insert_record(cursor, sector, job_title, company_name, salary, location, url, description):
    cursor.execute(
        'INSERT OR REPLACE INTO job_listings (sector, job_title, company_name, salary, location, url, job_description) VALUES(?, ?, ?, ?, ?, ?, ?)',
        (sector, job_title, company_name, salary, location, url, description))

def __get_JobView(soup):
    return soup.find("div", {"id" : "JobView"})

def __get_emp_info(soup):
    return soup.find("div", {"class" :"empInfo tbl"})

def __get_emp_name(soup):
    emp_name = soup.find("span", {"class" : "strong ib"})
    if emp_name:
        return emp_name.text.encode('ascii', 'ignore').strip()
    return None

def __get_job_title(soup):
    job_title = soup.find("h2", {"class" : "noMargTop margBotXs strong"})
    if job_title:
         return job_title.text.encode('ascii', 'ignore')
    return None

def __get_salary_range(soup):
    salary = soup.find("span", {"class" : "salEst green"})
    if salary:
        return salary.text.encode('ascii', 'ignore').split("(")[0]
    return None

def __get_emp_location(soup):
    loc = soup.find("span", {"class" : "subtle ib"})
    if loc:
        loc = loc.text.encode('ascii', 'ignore')
        return loc
    return None

def __get__JobDescription(soup):
    item = soup.find("div", {"id": "JobContent"})
    return item.find("div", {"class": "jobDescriptionContent desc"})

def __clean_JobDescription(job_description):
    if job_description:
        return job_description.get_text(separator='\n').encode('ascii', 'ignore')
    return None

def __clean_location(location):
    return location

def crawl_and_populate_db(base_url, url, header, sector):
    q = Request(url)
    q.add_header("User-Agent", header)
    connection = db.get_db()
    cursor = connection.cursor()
    try:
        html = urlopen(q).read()
        soup = BeautifulSoup(html, "html.parser")
        items = soup.findAll("ul", {"class": "jlGrid hover"})
        job_URLS = set()
        for link in items[0].findAll('a', href=True):
            job_URLS.add(str(base_url + link.get('href')))
        #job_URLS = [base_url + link.get('href') for link in items[0].findAll('a', href=True)]
        print("count of Job URLs %d" % len(job_URLS))
        for url in job_URLS:
            print(url)
            time.sleep(1)
            q = Request(url)
            q.add_header("User-Agent", header)
            html = urlopen(q).read()
            soup = BeautifulSoup(html, "html.parser")
            job_view_soup = __get_JobView(soup)
            emp_info_soup = __get_emp_info(job_view_soup)
            job_title = __get_job_title(emp_info_soup)
            emp_name = __get_emp_name(emp_info_soup)
            loc = __get_emp_location(emp_info_soup)
            salary = __get_salary_range(emp_info_soup)
            loc = __clean_location(loc)
            job_description = __get__JobDescription(job_view_soup)
            job_description = __clean_JobDescription(job_description)
            __insert_record(cursor, sector, job_title, emp_name, salary, loc, url, job_description)
            connection.commit()
    except e:
        print(e.code)
        print(e.msg)
        print(e.fp.read())
    finally:
        cursor.close()
        connection.close()


def __create_job_listings_for_finance():
    for url in [li['url'] for li in f_url]:
        print("using url %s" % url)
        crawl_and_populate_db(base_url, url, headers, "Finance")

def __create_job_listings_for_IT():
    for url in [li['url'] for li in it_url]:
        print("using url %s" % url)
        crawl_and_populate_db(base_url, url, headers, "Information Technology")

def __create_job_listings_for_telecommunication():
    for url in [li['url'] for li in t_url]:
        print("using url %s" % url)
        crawl_and_populate_db(base_url, url, headers, "Telecommunications")

def __create_job_listings_for_health_care():
    for url in [li['url'] for li in hc_url]:
        print("using url %s" % url)
        crawl_and_populate_db(base_url, url, headers, "Health Care")

def __create_job_listings_for_insurance():
    for url in [li['url'] for li in in_url]:
        print("using url %s" % url)
        crawl_and_populate_db(base_url, url, headers, "Insurance")


if __name__ == '__main__':
    base_url = "https://www.glassdoor.com/"
    #__create_job_listings_table(True)
    #__create_job_listings_for_finance()
    #__create_job_listings_for_IT()
    #__create_job_listings_for_telecommunication()
    #__create_job_listings_for_health_care()
    #__create_job_listings_for_insurance()
    sales_force = [
    "https://www.glassdoor.com/Job/california-google-jobs-SRCH_IL.0,10_IS2280_KE11,17.htm",
    "https://www.glassdoor.com/Job/california-google-jobs-SRCH_IL.0,10_IS2280_KE11,17_IP2.htm",
    "https://www.glassdoor.com/Job/california-google-jobs-SRCH_IL.0,10_IS2280_KE11,17_IP3.htm",
    "https://www.glassdoor.com/Job/california-google-jobs-SRCH_IL.0,10_IS2280_KE11,17_IP4.htm",
    "https://www.glassdoor.com/Job/california-google-jobs-SRCH_IL.0,10_IS2280_KE11,17_IP5.htm",
    "https://www.glassdoor.com/Job/california-google-jobs-SRCH_IL.0,10_IS2280_KE11,17_IP6.htm",
    "https://www.glassdoor.com/Job/california-google-jobs-SRCH_IL.0,10_IS2280_KE11,17_IP7.htm",
    "https://www.glassdoor.com/Job/california-google-jobs-SRCH_IL.0,10_IS2280_KE11,17_IP8.htm",
    "https://www.glassdoor.com/Job/california-google-jobs-SRCH_IL.0,10_IS2280_KE11,17_IP9.htm"
    ]

    for url in insurance:
        crawl_and_populate_db(base_url, url, headers, "Insurance")



