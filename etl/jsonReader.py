import json
import psycopg2

try:
    connect_str = "dbname='jobsdb' user='master' host='jobsdb3342904.c7qtisnmt03r.us-east-2.rds.amazonaws.com' password='dancingSpongeyGophers'"
    conn = psycopg2.connect(connect_str)
    print("Connection Success!")
except Exception as e:
    print("DB Error: ")
    print(e)

#cursor for sending things to our DB
queryCursor = conn.cursor()

jsonData = '{"URL": 1, "b": 2, "c": 3, "d": 4, "e": 5}'

with open('../craigslist/spiders/results.json', 'r') as cl_file:
    print(cl_file.name)
    jobs_dict = json.load(cl_file)

for job in jobs_dict:
    title = job['Title']
    title = title.replace("'", "''")
    url = job['URL']
    url = url.replace("'", "''")
    address = job['Address']
    address = address.replace("'", "''")
    compensation = job['Compensation']
    compensation = compensation.replace("'", "''")
    employmentType = job['EmploymentType']
    employmentType = employmentType.replace("'", "''")
    description = job['Description']
    description = description.replace("'", "''")
    insertString = "INSERT INTO job_listings VALUES('" + title + "', '" + url + "', '" + address + "', '" + compensation + "', '" + employmentType + "', '" + "TEMP DESCRIPTION" + "');"

    try: 
        print("inserting: " + insertString)
        queryCursor.execute(insertString) 
    except Exception as e:
        print("DB Error: ")
        print(e)
conn.commit()
queryCursor.close()
conn.close()

