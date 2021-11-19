from libs.ProductListingsDao import ProductListingsDao
from OnlineProcessor import CosineSimiCalculator as cal
import queue as Q
import numpy;
from flask import Flask, request, g, redirect, url_for, render_template
# import things
from flask_table import Table, Col

app = Flask(__name__.split('.')[0])   # create the application instance

class Result(object):
    def __init__(self, priority, url, rating, product_title, price):
        self.priority = priority
        self.url = url
        self.rating = rating
        self.product_title = product_title
        self.price = price
        return

    def __lt__(self, other):
        return -1 * cmp(self.priority, other.priority)

    def __repr__(self):
        return str(self.priority) + " : " + self.url

# Declare your table
class ItemTable(Table):
    #company_name = Col('company_name')
    #location = Col('location')
    product_title = Col('product_title')
    price = Col('price')
    url = Col('url')
    rating = Col('rating')

# Get some objects
class Item(object):
    def __init__(self, url, product_title, price, rating):
        #self.company_name = company_name.encode('ascii')
        #self.location = location
        self.product_title = product_title
        self.price = price
        self.url = url
        self.rating = rating

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/index', methods=['GET'])
def index_page_get():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def index_page_post():
    #location = request.form.get('location')
    sector = request.form.get('sector')
    freesearch = request.form['freesearch']
    entry = "hello, this, is, america"
    print (sector , freesearch)
    result = __get_top_10_products(sector, freesearch)
    table = ItemTable(result, classes=["table", "table-striped"], border=True)
    header = "Recommended Products for category %s" % (sector)
    return render_template('index.html', header=header, entries=result)

def __get_top_10_products(sector, freesearch):
    dao = ProductListingsDao()
    product_listings = dao.get_url_product_description(sector)
    q = Q.PriorityQueue()
    for product in product_listings:
        if product[1]:
            product_description = product[1] + "Product Title: " + product[3]
            q.put(Result(cal.get_sim(freesearch, product_description), product[0], product[2], product[3], product[4]))
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