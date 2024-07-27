
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Database connection
def get_db():
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    return conn, cursor

# Create table if it doesn't exist
conn, cursor = get_db()
cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')
conn.commit()
conn.close()

class Item(BaseModel):
    name: str

@app.post("/items/")
async def create_item(item: Item):
    conn, cursor = get_db()
    cursor.execute("INSERT INTO items (name) VALUES (?)", (item.name,))
    conn.commit()
    conn.close()
    return {"name": item.name}

@app.get("/items/")
async def read_items():
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return [{"id": item[0], "name": item[1]} for item in items]
