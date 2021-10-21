import libs.DatabaseProvider as db

class JobListingsDao:
    connection = None

    def __init__(self):
        if self.connection is None:
            self.connection = db.get_db()
        return

    def get_url_job_description_sector(self, location, sector):
        cur = self.connection.execute('SELECT distinct url, job_description, company_name, location, job_title, salary FROM job_listings where location=\'%s\' and sector=\'%s\''
                             % (location, sector))
        result = cur.fetchall()
        cur.close()
        return result

    def get_url_job_description(self, sector):
        cur = self.connection.execute('SELECT distinct url, job_description, company_name, location, job_title, salary FROM job_listings where sector=\'%s\''
                             % (sector))
        result = cur.fetchall()
        cur.close()
        return result
    def close(self):
        if self.connection is not None:
            self.connection.close()

