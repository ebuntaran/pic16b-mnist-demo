from flask import Flask, g, render_template, request

import os
import sqlite3
import pandas as pd

app = Flask(__name__)

def get_message_db():
#check if there is a message database. if not...
  try:
      return g.message_db
  except:
    #create a new database
    g.message_db = sqlite3.connect("messages_db.sqlite")
    #add a table with columns for handles and messages
    cmd = 'CREATE TABLE IF NOT EXISTS messages (handle text(255), message text(255))'
    cursor = g.message_db.cursor()
    cursor.execute(cmd)
    return g.message_db

def insert_message(handle, message):
        #get database
        db = get_message_db()
        cursor = db.cursor()
        #add a new row to the database with the given info with a sql command
        cmd = \
        f"""
        INSERT INTO messages (handle, message)
        VALUES ("{handle}", "{message}");
        """
        cursor.execute(cmd)
        db.commit()

def random_messages(n):
        #select n random messages from the database with a sql command
        cmd = \
        f"""
        SELECT * FROM messages ORDER BY RANDOM() LIMIT {n};
        """
        with get_message_db() as conn:
            messages = pd.read_sql_query(cmd, conn)
        #return as a dataframe
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
            #call the insert message function with the parameters given by the form
            insert_message(request.form["handle"], request.form["message"])
            #show a message if the request goes through
            return render_template('submit.html', thanks=True)
        except:
            #show a message if there is an error
            return render_template('submit.html', error=True)

@app.route('/view/')
def view():
    n_messages = 5
    #get n messages as a dataframe
    df = random_messages(n_messages)
    #convert dataframe to list of tuples for jinja
    messages = list(df.itertuples(index=False, name=None))
    #return as an argument
    return render_template('view.html', messages=messages)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

