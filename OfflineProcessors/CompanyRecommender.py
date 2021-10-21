# Build on top of naivebased commany classifer to calssify companies based on rating description sentiments

from libs import DatabaseProvider as db
from Classifier import NaiveBasedCompanyClassifier as classifier

default_industry_name = 'Computer Hardware & Software'

def __create_employer_recomender_table(connection):
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS employer_recommender')
    cursor.execute('CREATE TABLE employer_recommender(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                   ' location TEXT, sector TEXT, industry TEXT, company_name TEXT,recommendation_ratings INTEGER)')
    cursor.close()

def __get_industry(industry):
    if industry and industry.strip():
        return industry
    return default_industry_name

def __persist_entry(cursor, entry):
    cursor.execute(
        'INSERT OR REPLACE INTO employer_recommender (id, location, sector, industry, company_name, recommendation_ratings) VALUES(?, ?, ?, ?, ?, ?)',
        (entry[0], entry[1], entry[2], __get_industry(entry[3]), entry[4], entry[6]))

def __crawl_and_populate_db():
    connection = db.get_db()
    __create_employer_recomender_table(connection)
    cursor = connection.execute('SELECT id, location, sectorname, industry, name, rating_description, recommendation_ratings'
                                ' FROM job_recommender_employee_info')

    entries = cursor.fetchall()
    for entry in entries:
        try:
            if entry[2] is None:
                continue
            if len(entry[2]) == 0:
                print(entry)
                continue
            if entry[5] is not None:
                if classifier.is_good(entry[5]):
                    print(entry)
                    print("good")
                    __persist_entry(cursor, entry)
                    connection.commit()
        except:
            print("error")

    cursor.close()
    connection.close()

def recommendCompanies(location , industry):
    connection = db.get_db()
    cur = connection.execute('SELECT company_name, recommendation_ratings FROM employee_recommender where location=\'%s\' and industry=\'%s\''
                             % (location, industry))
    print (cur.fetchall())
    cur.close()
    connection.close()

if __name__ == '__main__':
    print ("Starting Company recomender")
    __crawl_and_populate_db()
    recommendCompanies("San Jose, CA", "Computer Hardware & Software")
