from conexion import cursor_oracle

cursor_oracle.execute("SELECT trigger_name, table_name FROM user_triggers WHERE table_name IN ('USUARIO', 'CUENTA_BANCARIA')")
print("TRIGGERS:")
for row in cursor_oracle.fetchall():
    print(row)

cursor_oracle.execute("SELECT sequence_name FROM user_sequences")
print("SEQUENCES:")
for row in cursor_oracle.fetchall():
    print(row)
