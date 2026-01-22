"""
Load follows data from CSV file into the database
"""

import os
import csv
from dbutils import DBUtils

MYSQL_USER = "root"
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
MYSQL_DATABASE = "twitter_db"
CSV_FILE = "follows_sample.csv"

def load_follows(csv_file, user, password, database, host="localhost"):
    """
    Load follows data from CSV file into the follows table
    """
    
    # connect to the database
    dbu = DBUtils(user, password, database, host)

    # clear existing data from follows table
    dbu.execute("DELETE FROM follows")
    
    # read CSV
    follows_data = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            follower_id = int(row['USER_ID'])
            followee_id = int(row['FOLLOWS_ID'])
            follows_data.append((follower_id, followee_id))
    
    # insert data
    sql = "INSERT INTO follows (follower_id, followee_id) VALUES (%s, %s)"
    dbu.insert_many(sql, follows_data)
    
    # verify the number of follows
    result = dbu.execute("SELECT COUNT(*) as count FROM follows")
    print(f"total follows in database: {result['count'][0]}")
    
    dbu.close()

if __name__ == '__main__':
    load_follows(CSV_FILE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
