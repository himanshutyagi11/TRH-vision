import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT student_id, Intren FROM vision_profile WHERE student_id IS NOT NULL AND student_id != '' LIMIT 20;")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
