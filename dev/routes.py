from database import connect_db

def load_routes(db_path):
    conn = connect_db(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ROUTES")
    routes = cursor.fetchall()
    conn.close()
    return [{"origin": row["ORIGIN"], "destination": row["DESTINATION"], "travel_time": row["TRAVEL_TIME"]} for row in routes]
