import sqlite3,os

conn = sqlite3.connect(os.path.abspath('../test.db'))
cursor = conn.cursor()
cursor.execute('select * from question')
values = cursor.fetchall()
cursor.close()
conn.close()
print(values)