from flask import Flask, render_template, request, redirect
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
DATA_FILE = "expenses.csv"

@app.route('/')
def index():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["date", "category", "amount"])

    total = df["amount"].sum() if not df.empty else 0
    return render_template("index.html", expenses=df.to_dict(orient='records'), total=total)

@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    category = request.form['category']
    amount = float(request.form['amount'])

    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["date", "category", "amount"])

    new_data = {"date": date, "category": category, "amount": amount}
    df = pd.concat([df, pd.DataFrame([new_data])])
    df.to_csv(DATA_FILE, index=False)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
