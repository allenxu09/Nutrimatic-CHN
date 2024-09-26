import sqlite3
import re
from fastapi import FastAPI, HTTPException
import time
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

        # Combine the characters into a single string
        filtered_items = [''.join(chars) for chars in filtered_items]
        return filtered_items
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

def match(expr: str):
    # Convert the input expression to a regex
    # "*" is replaced with a match for a pinyin word of 2 to 6 characters (syllables)
    result = expr
    result = result.replace('"', '\\b')  # Replace " with word boundaries
    result = result.replace('*', '\\S{1,6}')  # Replace * with a non-whitespace syllable of length 2 to 6
    #result = result.replace(' ', '\\s+')  # Ensure spaces between syllables are handled correctly
    result = result.replace('?', '\\S')
    return result

@app.get("/")
async def getRoot():
    #return time now
    return {"result": time.time()}

@app.get("/get/{expr}")
async def getResults(expr: str):
    # Pass the expression through the match function
    regex_pattern = match(expr)
    results = search_items(regex_pattern)
    return {"results": results}
