from libs.JobListingsDao import JobListingsDao
from OnlineProcessor import CosineSimiCalculator as cal
import queue as Q
import numpy;
from flask import Flask, request, g, redirect, url_for, render_template
# import things
from flask_table import Table, Col

app = Flask(__name__.split('.')[0])   # create the application instance

class Result(object):
    def __init__(self, priority, url, company_name, location, job_title, salary):
        self.priority = priority
        self.url = url
        self.company_name = company_name
        self.location = location
        self.job_title = job_title
        self.salary = salary
        return

    def __lt__(self, other):
        return -1 * cmp(self.priority, other.priority)

    def __repr__(self):
        return str(self.priority) + " : " + self.url

# Declare your table
class ItemTable(Table):
    company_name = Col('company_name')
    location = Col('location')
    job_title = Col('job_title')
    salary = Col('salary')
    url = Col('url')

# Get some objects
class Item(object):
    def __init__(self, company_name, location, url, job_title, salary):
        self.company_name = company_name.encode('ascii')
        self.location = location
        self.job_title = job_title
        self.salary = salary
        self.url = url

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/index', methods=['GET'])
def index_page_get():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def index_page_post():
    location = request.form.get('location')
    sector = request.form.get('sector')
    experience = request.form['experience']
    entry = "hello, this, is, america"
    print (location , sector , experience)
    result = __get_top_10_job(sector, location, experience)
    table = ItemTable(result, classes=["table", "table-striped"], border=True)
    header = "Recommended Jobs in %s for category %s" % (location, sector)
    return render_template('index.html', header=header, entries=result)

def __get_top_10_job(sector, location, experience):
    dao = JobListingsDao()
    job_listings = dao.get_url_job_description_sector(location, sector)
    q = Q.PriorityQueue()
    for job in job_listings:
        if job[1]:
            job_description = job[1] + "Job Title: " + job[4]
            q.put(Result(cal.get_sim(experience, job_description), job[0], job[2], job[3], job[4], job[5]))
    result = []
    for i in range(0, 10):
        result.append(q.get())
    return result

def cmp(a, b):
    return bool(a) ^ bool(b) 

if __name__ == '__main__':
    print ("Starting application")
    app.run(host="localhost", port=5000, debug=True)



# Print the html
print()