# An offline crawler to build below table
# Table Name :
#     companyInfo
# Fields :
#     companyId
#     companyName
#     companyLocation
#     sectorName
#     website
#     industry
#     numberofratings
#     recommendtofriendRating
import json, requests
import time
from libs import DatabaseProvider as db

key_response = 'response'
key_employers = 'employers'
key_current_page_number = 'currentPageNumber'
key_total_number_pages = 'totalNumberOfPages'
key_total_record_count = 'totalRecordCount'

base_url = "http://api.glassdoor.com/api/api.htm?t.p=ert&t.k=ertre"
final_url = "http://api.glassdoor.com/api/api.htm?t.p=2157ert13&t.k=QzNlSQzertreMSQ&userip=0.0.0.0&city=san%20jose&state=california&useragent=&format=json&v=1&action=employers"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

def __get(employer, key):
    if key not in employer:
        return None
    return employer[key]

def __create_employer_info_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS job_recommender_employee_info')
    cursor.execute('CREATE TABLE job_recommender_employee_info(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,'
                   ' location TEXT, sectorname TEXT, website TEXT, industry TEXT, recommendation_ratings INTEGER,'++
                   ' rating_description TEXT)')

def __get_response(url, page):
    if page is None:
        page = 1
    url = url + "&pn="+ page
    print(url)
    response = requests.get(url=url, headers=headers)
    print(response)
    return json.loads(response.text)['response']

def __process_employer_data(data, cursor, connection):
    for employer in data[key_employers][:]:
        print (employer['name'])
        print (employer['id'])
        cursor.execute('INSERT OR REPLACE INTO job_recommender_employee_info (id, name, location, sectorname, website, industry,' 
                       ' recommendation_ratings, rating_description ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
                  (__get(employer, 'id'), __get(employer, 'name'), __get(employer['featuredReview'], 'location'),
                   __get(employer, 'sectorName'), __get(employer, 'website'),
                   __get(employer, 'industry'), __get(employer, 'recommendToFriendRating'), __get(employer, 'ratingDescription')))
        connection.commit()

def crawl_and_populate_db():
    connection = db.get_db()
    cursor = connection.cursor()
    __create_employer_info_table(cursor)
    data = __get_response(final_url, None)
    current_page_number = data[key_current_page_number]
    total_page_number = data[key_total_number_pages]
    total_record_count = data[key_total_record_count]
    for page in range(1 , total_page_number):
        time.sleep(5)
        data = __get_response(final_url, page)
        __process_employer_data(data, cursor, connection)
    cursor.close()
    connection.close()

if __name__ == '__main__':
    print ("Starting to crawl glassdoor")
    crawl_and_populate_db()
