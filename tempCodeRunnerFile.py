def my_sql_database():
    conn = sqlite3.connect("tunes2.db")

    cursor = conn.cursor()

    cursor.execute("DELETE FROM tunes2")
    conn.commit()
    conn.close()