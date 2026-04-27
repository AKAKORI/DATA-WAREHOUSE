from flask import Flask, render_template, request, redirect # Fixed Imports
import sqlite3

app = Flask(__name__)

def get_data_from_db():
    conn = sqlite3.connect('finance_dw.db')
    cursor = conn.cursor()
    # ELT Transformation happens here in SQL
    cursor.execute("SELECT vendor, amount, amount * 0.12 AS tax, amount + (amount * 0.12) AS total FROM staging_transactions")
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    data = get_data_from_db()
    return render_template('index.html', transactions=data)

@app.route('/add', methods=['POST'])
def add_transaction():
    # 1. Get the data from the HTML form
    vendor = request.form.get('vendor')
    amount = request.form.get('amount')

    # 2. Connect to database and insert it
    conn = sqlite3.connect('finance_dw.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO staging_transactions (vendor, amount) VALUES (?, ?)", (vendor, amount))
    conn.commit()
    conn.close()

    # 3. Go back to the home page to see the new item
    return redirect('/')

@app.route('/delete/<name>')
def delete_transaction(name):
    # 1. Connect to the warehouse
    conn = sqlite3.connect('finance_dw.db')
    cursor = conn.cursor()
    
    # 2. Tell SQL to remove the item with that specific name
    cursor.execute("DELETE FROM staging_transactions WHERE vendor = ?", (name,))
    
    # 3. Save the changes and close
    conn.commit()
    conn.close()
    
    # 4. Refresh the page so the item disappears
    return redirect('/')
# This block MUST be at the very end of your file
if __name__ == '__main__':
    print("Website starting at http://127.0.0.1:5000")
    app.run(debug=True)