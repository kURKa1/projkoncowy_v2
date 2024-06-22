import sqlite3
import datetime

class Storage:
    def __init__(self):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS main
                     (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, quantity INTEGER)''')
        conn.close()
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS orders(FOREIGN KEY(id) REFERENCES main(id), quantity INTEGER, date TEXT)''')
        conn.close()


    def add_item(self, name, price, quantity):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("INSERT INTO main (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
        conn.commit()
        conn.close()
        return True
    
    def get_items(self):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("SELECT * FROM main")
        result = c.fetchall()
        conn.close()
        return result
    
    def get_item(self, name):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("SELECT * FROM main WHERE name = ?", (name,))
        result = c.fetchone()
        conn.close()
        return result
    
    def delete_item(self, name):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("DELETE FROM main WHERE name = ?", (name,))
        conn.commit()
        conn.close()
        return True
    
    def update_item(self, name, price, quantity):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("UPDATE main SET price = ?, quantity = ? WHERE name = ?", (price, quantity, name))
        conn.commit()
        conn.close()
        return True
    
    def storage_import_CSV(self, filename):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        with open(filename, 'r') as file:
            for line in file:
                name, price, quantity = line.split(',')
                c.execute("INSERT INTO main (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
        conn.commit()
        conn.close()
        return True
    
    def storage_export_CSV(self, filename):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("SELECT * FROM main")
        with open(filename, 'w') as file:
            for row in c.fetchall():
                file.write(','.join(map(str, row)) + '\n')
        conn.close()
        return True
    
    def add_order(self, id, quantity):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("INSERT INTO orders (id, quantity, date) VALUES (?, ?, ?)", (id, quantity, datetime.datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()
        return True
    
    def get_orders(self):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("SELECT * FROM orders")
        result = c.fetchall()
        conn.close()
        return result
    
    def get_order(self, id):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("SELECT * FROM orders WHERE id = ?", (id,))
        result = c.fetchone()
        conn.close()
        return result
    
    def delete_order(self, id):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("DELETE FROM orders WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True
    
    def update_order(self, id, quantity):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("UPDATE orders SET quantity = ? WHERE id = ?", (quantity, id))
        conn.commit()
        conn.close()
        return True
    
    def order_import_CSV_update(self, filename):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        with open(filename, 'r') as file:
            for line in file:
                id, quantity = line.split(',')
                c.execute("UPDATE orders SET quantity = ? WHERE id = ?", (quantity, id))
        conn.commit()
        conn.close()
        return True
    
    def order_export_CSV(self, filename):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("SELECT * FROM orders")
        with open(filename, 'w') as file:
            for row in c.fetchall():
                file.write(','.join(map(str, row)) + '\n')
        conn.close()
        return True