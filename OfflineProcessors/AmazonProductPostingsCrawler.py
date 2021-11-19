from bs4 import BeautifulSoup  # For HTML parsing
from urllib.request import urlopen, Request  # Website connections
import re  # Regular expressions
from time import sleep  # To prevent overwhelming the server between connections
import sqlite3
from ProductListingUrls import hoodies
from ProductListingUrls import information_technology
from ProductListingUrls import telecommunication
from ProductListingUrls import health_care
from ProductListingUrls import insurance

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from libs import DatabaseProvider as db

import time

headers = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"

def __drop_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS product_listings')

def __create_product_listings_table(create):
    if create:
        connection = db.get_db()
        cursor = connection.cursor()
        __drop_table(cursor)
        cursor.execute('CREATE TABLE product_listings(sector TEXT, product_title TEXT, product_price TEXT, product_description TEXT, product_rating TEXT, url TEXT)')
        cursor.close()
        connection.close()

def __insert_record(cursor, sector, product_title, product_price, product_description, product_rating, url):
    cursor.execute(
        'INSERT OR REPLACE INTO product_listings (sector, product_title, product_price, product_description, product_rating, url) VALUES(?, ?, ?, ?, ?, ?)',
        (sector, product_title, product_price, product_description, product_rating, url))

def __get_ProductView(soup):
    return soup.find("div", {"id" : "centerCol"})

# def __get_emp_info(soup):
#     return soup.find("div", {"class" :"empInfo tbl"})

# def __get_emp_name(soup):
#     emp_name = soup.find("span", {"class" : "strong ib"})
#     if emp_name:
#         return emp_name.text.encode('ascii', 'ignore').strip()
#     return None

def __get_product_title(soup):
    product_title = soup.find("h1", {"id" : "title"})
    if product_title:
         return product_title.text.strip()#.encode('ascii', 'ignore')
    return None

def __get_product_price(soup):
    product_price = soup.find("span", {"class" : "a-price a-text-price a-size-medium apexPriceToPay"})
    if product_price:
         return product_price.find('span', class_='a-offscreen').text#.encode('ascii', 'ignore')
    return None

def __get_product_description(soup):
    product_description = ""
    lis = []
    description = soup.find("div", {"id" : "featurebullets_feature_div"})
    if description:
        ul = description.find('ul')
        if ul:
            lis = ul.findAll('li')
        for li in lis:
            product_description += li.text.strip() + '. '
        return product_description#.encode('ascii','ignore')
    return None

def __get_product_rating(soup):
    product_rating = soup.find("div", {"id" : "averageCustomerReviews"})
    if product_rating:
        return product_rating.find('span', class_='a-icon-alt').text#.encode('ascii', 'ignore')
    return None

# def __get_salary_range(soup):
#     salary = soup.find("span", {"class" : "salEst green"})
#     if salary:
#         return salary.text.encode('ascii', 'ignore').split("(")[0]
#     return None

# def __get_emp_location(soup):
#     loc = soup.find("span", {"class" : "subtle ib"})
#     if loc:
#         loc = loc.text.encode('ascii', 'ignore')
#         return loc
#     return None

# def __get__JobDescription(soup):
#     item = soup.find("div", {"id": "JobContent"})
#     return item.find("div", {"class": "jobDescriptionContent desc"})

# def __clean_JobDescription(job_description):
#     if job_description:
#         return job_description.get_text(separator='\n').encode('ascii', 'ignore')
#     return None

# def __clean_location(location):
#     return location

def crawl_and_populate_db(base_url, url, header, sector):
    q = Request(url)
    q.add_header("User-Agent", header)
    connection = db.get_db()
    cursor = connection.cursor()
    try:
        html = urlopen(q).read()
        soup = BeautifulSoup(html, "html.parser")
        items = soup.findAll("div", {"class": "s-main-slot s-result-list s-search-results sg-row"})
        product_URLS = set()
        for link in items[0].findAll('a', class_="a-link-normal s-no-outline",  href=True):
            product_URLS.add(str(base_url + link.get('href')))
        #job_URLS = [base_url + link.get('href') for link in items[0].findAll('a', href=True)]
        print("count of Job URLs %d" % len(product_URLS))
        for url in product_URLS:
            try:
                print(url)
                time.sleep(60)
                q = Request(url)
                q.add_header("User-Agent", header)
                html = urlopen(q).read()
                soup = BeautifulSoup(html, "html.parser")
                product_view_soup = __get_ProductView(soup)
                #emp_info_soup = __get_emp_info(job_view_soup)
                product_title = __get_product_title(product_view_soup)
                product_price = __get_product_price(product_view_soup)
                product_description = __get_product_description(product_view_soup)
                product_rating = __get_product_rating(product_view_soup)
                #emp_name = __get_emp_name(emp_info_soup)
                #loc = __get_emp_location(emp_info_soup)
                #salary = __get_salary_range(emp_info_soup)
                #loc = __clean_location(loc)
                #job_description = __get__JobDescription(job_view_soup)
                #job_description = __clean_JobDescription(job_description)
                __insert_record(cursor, sector, product_title, product_price, product_description, product_rating, url)
                connection.commit()
            except Exception as e:
                pass
    except Exception as e:
        print(e.msg)
        print(e.fp.read())
    finally:
        cursor.close()
        connection.close()


# def __create_product_listings_for_hoodies():
#     for url in [li['url'] for li in f_url]:
#         print("using url %s" % url)
#         crawl_and_populate_db(base_url, url, headers, "Hoodies")

# def __create_listings_for_hoodies():
#     for url in [li['url'] for li in f_url]:
#         print("using url %s" % url)
#         crawl_and_populate_db(base_url, url, headers, "Finance")

# def __create_job_listings_for_IT():
#     for url in [li['url'] for li in it_url]:
#         print("using url %s" % url)
#         crawl_and_populate_db(base_url, url, headers, "Information Technology")

# def __create_job_listings_for_telecommunication():
#     for url in [li['url'] for li in t_url]:
#         print("using url %s" % url)
#         crawl_and_populate_db(base_url, url, headers, "Telecommunications")

# def __create_job_listings_for_health_care():
#     for url in [li['url'] for li in hc_url]:
#         print("using url %s" % url)
#         crawl_and_populate_db(base_url, url, headers, "Health Care")

# def __create_job_listings_for_insurance():
#     for url in [li['url'] for li in in_url]:
#         print("using url %s" % url)
#         crawl_and_populate_db(base_url, url, headers, "Insurance")


if __name__ == '__main__':
    base_url = "https://www.amazon.com/"
    __create_product_listings_table(True)
    #__create_product_listings_for_hoodies()
    #__create_job_listings_for_finance()
    #__create_job_listings_for_IT()
    #__create_job_listings_for_telecommunication()
    #__create_job_listings_for_health_care()
    #__create_job_listings_for_insurance()
    # sales_force = [
    # "https://www.amazon.com/b?node=16225009011&pf_rd_r=6AXDZVK7SR3Y76223FDE&pf_rd_p=5232c45b-5929-4ff0-8eae-5f67afd5c3dc&pd_rd_r=156de284-dec8-4938-82ef-a8bd087c3d22&pd_rd_w=2XCAY&pd_rd_wg=u1daC&ref_=pd_gw_unk",
    # "https://www.amazon.com/s?k=home+%26+kitchen&crid=4FXFGW4D4CH1&pd_rd_r=d3eaf7d7-44a4-42ad-b34d-51e3e5e23190&pd_rd_w=sRp0p&pd_rd_wg=4i8Qi&pf_rd_p=a4c19d76-658e-4331-b2b2-585bbcf49e79&pf_rd_r=6AXDZVK7SR3Y76223FDE&sprefix=home+%26+ki%2Caps%2C230&ref=pd_gw_unk"
    # ]

    for url in hoodies:
        crawl_and_populate_db(base_url, url, headers, "Hoodies")
        x = 0