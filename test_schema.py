from conexion import cursor_oracle

cursor_oracle.execute("SELECT table_name, column_name, identity_column FROM user_tab_columns WHERE table_name = 'USUARIO' OR table_name = 'CUENTA_BANCARIA'")
for row in cursor_oracle.fetchall():
    print(row)
