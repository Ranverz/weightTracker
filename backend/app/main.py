from flask import Flask
import psycopg2
import os

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "ok"}

@app.route("/db")
def db_test():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = conn.cursor()
    cur.execute("SELECT 1")
    return {"db": cur.fetchone()[0]}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
