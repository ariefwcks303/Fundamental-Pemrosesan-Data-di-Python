from sqlalchemy import create_engine, text

default_db_url = 'postgresql+psycopg2://postgres:000000@localhost:5432/postgres'

# --- PASTIKAN BARIS INI ADA ---
engine = create_engine(default_db_url, isolation_level="AUTOCOMMIT") 
# ------------------------------

create_db_query = text("CREATE DATABASE companydb OWNER postgres ENCODING 'UTF8';")

try:
    with engine.connect() as connection:
        connection.execute(create_db_query)
        print("Database 'companydb' berhasil dibuat!")

except Exception as e:
    # ... (penanganan error sudah ada)
    pass