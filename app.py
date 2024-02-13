from flask import Flask, g, render_template, request

import os
import sqlite3
import pandas as pd

### stuff from last class
app = Flask(__name__)

def get_message_db():
  try:
      return g.message_db
  except:
    g.message_db = sqlite3.connect("messages_db.sqlite")
    cmd = 'CREATE TABLE IF NOT EXISTS messages (handle text(255), message text(255))' # replace this with your SQL query
    cursor = g.message_db.cursor()
    cursor.execute(cmd)
    return g.message_db

def insert_message(handle, message):
        db = get_message_db()
        cursor = db.cursor()
        cmd = \
        f"""
        INSERT INTO messages (handle, message)
        VALUES ("{handle}", "{message}");
        """
        cursor.execute(cmd)
        db.commit()

def random_messages(n):
        cmd = \
        f"""
        SELECT * FROM messages ORDER BY RANDOM() LIMIT {n};
        """
        with get_message_db() as conn:
            messages = pd.read_sql_query(cmd, conn)
        return messages

@app.route('/')
def main():
    return render_template('hello.html')

@app.route('/hello/')
def hello():
    return render_template('hello.html')


@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try:
            insert_message(request.form["handle"], request.form["message"])
            return render_template('submit.html', thanks=True)
        except:
            return render_template('submit.html', error=True)

@app.route('/view/')
def view():
    n_messages = 5
    df = random_messages(n_messages)
    messages = list(df.itertuples(index=False, name=None))
    return render_template('view.html', messages=messages)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

