import psycopg2

try:
    connect_str = "dbname='jobsdb' user='master' host='jobsdb3342904.c7qtisnmt03r.us-east-2.rds.amazonaws.com' password='dancingSpongeyGophers'"
    conn = psycopg2.connect(connect_str)
    queryCursor = conn.cursor()
    queryCursor.execute("""SELECT * FROM job_listings;""")
    rows = queryCursor.fetchall()
    print(rows)
except Exception as e:
    print("DB Error: ")
    print(e)

#psql --host=jobsdb3342904.c7qtisnmt03r.us-east-2.rds.amazonaws.com --port=5432 --username=master --no-password --dbname=jobsdb
