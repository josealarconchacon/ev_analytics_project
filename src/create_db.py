import sqlite3

def create_db(df, db_path="db/ev_data.db"):
    conn = sqlite3.connect(db_path)
    df.to_sql("ev_population", conn, if_exists="replace", index=False)
    return conn
