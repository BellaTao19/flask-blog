import sqlite3

with sqlite3.connect("blog.db") as connection:
	c = connection.cursor()
	c.execute("CREATE TABLE entry(entry_id INT, entry_title TEXT, entry_body TEXT, entry_date Timestamp)")
	c.execute('INSERT INTO entry VALUES(1,"Good","This is my first blog", CURRENT_TIMESTAMP)')
	c.execute('INSERT INTO entry VALUES(2,"Hello","This is my second blog", CURRENT_TIMESTAMP)')
	c.execute('INSERT INTO entry VALUES(3,"Bella","This is my third blog", CURRENT_TIMESTAMP)')