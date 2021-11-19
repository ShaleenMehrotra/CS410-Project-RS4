import libs.DatabaseProvider as db

class ProductListingsDao:
    connection = None

    def __init__(self):
        if self.connection is None:
            self.connection = db.get_db()
        return

    def get_url_product_description_sector(self, freesearch, sector):
        cur = self.connection.execute('SELECT distinct url, product_description, product_rating, product_title, product_price FROM product_listings where location=\'%s\' and sector=\'%s\''
                             % (location, sector))
        result = cur.fetchall()
        cur.close()
        return result

    def get_url_product_description(self, sector):
        cur = self.connection.execute('SELECT distinct url, product_description, product_rating, product_title, product_price FROM product_listings where sector=\'%s\''
                             % (sector))
        result = cur.fetchall()
        cur.close()
        return result
    def close(self):
        if self.connection is not None:
            self.connection.close()

