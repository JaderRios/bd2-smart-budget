from conexion import cursor_oracle

cursor_oracle.execute("SELECT DBMS_METADATA.GET_DDL('TABLE', 'USUARIO') FROM DUAL")
print(cursor_oracle.fetchone()[0].read())

cursor_oracle.execute("SELECT DBMS_METADATA.GET_DDL('TABLE', 'CUENTA_BANCARIA') FROM DUAL")
print(cursor_oracle.fetchone()[0].read())
