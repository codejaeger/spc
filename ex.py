import sqlite3
conn =sqlite3.connect('db.sqlite3')
curs=conn.cursor()
curs.execute("SELECT * FROM usrs_bookindex")
rows = curs.fetchall()
for row in rows:
	print(row)
conn.close()