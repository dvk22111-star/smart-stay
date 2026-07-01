from database.connection import engine


try:
    print("Checking SQL Server connection...")

    with engine.connect() as conn:
        print("SUCCESS - Connected to SQL Server")

except Exception as e:
    print("FAILED")
    print(e)