def get_db_connection():
    # Define the connection string for SQL Server Express
    # Replace 'YOUR_SERVER_NAME', 'YOUR_DATABASE_NAME', 'YOUR_USERNAME', 'YOUR_PASSWORD' as needed
    # For SQL Express, the server name is typically 'localhost\\SQLEXPRESS' or '.\\SQLEXPRESS'
    conn_string = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost\\SQLEXPRESS;"  # Example for local SQL Express
        "Database=YourDatabaseName;"
        "UID=YourUsername;"
        "PWD=YourPassword;"
        "TrustServerCertificate=yes;" # May be needed for local development
        
        Data Source=localhost\SQLEXPRESS01;Integrated Security=True;Persist Security Info=False;Pooling=False;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=True;Application Name="SQL Server Management Studio";Command Timeout=0
    )
    conn = pyodbc.connect(conn_string)
    return conn