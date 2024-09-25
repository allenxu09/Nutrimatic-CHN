import sqlite3
import re
from fastapi import FastAPI, HTTPException

app = FastAPI()

def search_items(expr: str):
    try:
        # Connect to the database
        conn = sqlite3.connect('res/main.db')
        cursor = conn.cursor()

        # Prepare the SQL query
        query = "SELECT py1, py2, py3, py4, char1, char2, char3, char4 FROM idiom"
        cursor.execute(query)

        # Fetch all items
        items = cursor.fetchall()

        # Concatenate py1, py2, py3, py4 into a single string with spaces
        concatenated_items = [(' '.join(item[:4]), item[4:]) for item in items]

        # Filter items using the regular expression
        pattern = re.compile(expr)
        filtered_items = [chars for py, chars in concatenated_items if pattern.search(py)]

        return filtered_items
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

def match(expr: str):
    result=expr
    result=result.replace('\"','\\b')
    result=result.replace('?', '\S')
    #print(result)
    return result


@app.get("/get/{expr}")
async def getResults(expr: str):
    results = search_items(match(expr))
    return {"results": results}