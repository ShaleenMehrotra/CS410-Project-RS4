# Currently support sqllite3 rdbms can be extended to any database

import sqlite3
import os

#db_file_path = '../datasource/offline/jobrecommendersystem.db'
db_file_path_new = '../datasource/offline/productrecommendersystem.db'

def __connect_db__():
    """Connect to the specific database."""
    package_dir = os.path.abspath(os.path.dirname(__file__))
    #final_path = os.path.join(package_dir, db_file_path)
    final_path = os.path.join(package_dir, db_file_path_new)
    connection = sqlite3.connect(final_path)
    connection.row_factory = sqlite3.Row
    return connection


def get_db():
    """
    Open a new database connection.

    If there is none yet for the
    current application context.
    """
    return __connect_db__()
