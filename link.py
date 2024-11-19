import psycopg2

connection = psycopg2.connect(
   user='project_10',
   password='bmibxk',
   host='140.117.68.66',
   port='5432',
   dbname='project_10'  # PostgreSQL 的資料庫名稱
#  user='postgres',
#  password='postgres',
#  host='localhost',
#  port='5432',
#  dbname='project_10'  # PostgreSQL 的資料庫名稱
)
cursor = connection.cursor()

