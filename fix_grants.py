import oracledb

try:
    conn = oracledb.connect(user='system', password='12345678', dsn='localhost/xe')
    cursor = conn.cursor()
    
    # Run the grant for categoria
    cursor.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON categoria TO rol_fintech_operador")
    print("Grant for categoria successful")
    
    # Recreate all synonyms pointing to SYSTEM instead of ADMIN
    tables = ['usuario', 'cuenta_bancaria', 'categoria', 'transaccion', 'meta_ahorro', 'estado_cuenta']
    for table in tables:
        cursor.execute(f"CREATE OR REPLACE SYNONYM fintech_app.{table} FOR system.{table}")
        print(f"Created synonym for {table}")
        
    cursor.execute("CREATE OR REPLACE SYNONYM fintech_app.sp_registrar_transaccion FOR system.sp_registrar_transaccion")
    print("Created synonym for sp_registrar_transaccion")
    
    conn.commit()
    print("All fixes applied successfully!")
except Exception as e:
    print("Error applying fixes:", e)
