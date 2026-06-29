import oracledb
conn = oracledb.connect(user='system', password='12345678', dsn='localhost/xe')
print(conn.cursor().execute("SELECT owner, table_name FROM all_tables WHERE table_name = 'CATEGORIA'").fetchall())
