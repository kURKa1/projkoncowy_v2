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
        c.execute('''CREATE TABLE IF NOT EXISTS orders(order_id INTEGER PRIMARY KEY, product_id INTEGER, quantity INTEGER, date TEXT)''')
        conn.close()


    def add_item(self, name, price, quantity):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("INSERT INTO main (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
        conn.commit()
        conn.close()
        return True
    
    def get_items(self, filter = None, value = None, order_by = None):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        if filter == None and value == None and order_by == None:
            c.execute("SELECT * FROM main")
        elif filter != None and value != None and order_by == None:
            c.execute("SELECT * FROM main WHERE ? = ?", (filter, value))
        elif filter == None and value == None and order_by != None:
            c.execute("SELECT * FROM main ORDER BY ?", (order_by,))
        elif filter != None and value != None and order_by != None:
            c.execute("SELECT * FROM main WHERE ? = ? ORDER BY ?", (filter, value, order_by))
        result = c.fetchall()
        conn.close()
        return result
    
    def get_item(self, id):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("SELECT * FROM main WHERE id = ?", (id,))
        result = c.fetchone()
        conn.close()
        return result
    
    def delete_item(self, id):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("DELETE FROM main WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True
    
    def update_item(self, id, price, quantity):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("UPDATE main SET price = ?, quantity = ? WHERE id = ?", (price, quantity, id))
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
        c.execute("INSERT INTO orders (product_id, quantity, date) VALUES (?, ?, ?)", (id, quantity, datetime.datetime.now().strftime("%Y-%m-%d")))
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
    
    def get_col_name(self):
        conn = sqlite3.connect('Storage.db')
        c = conn.cursor()
        c.execute("SELECT * FROM main limit 1")
        col_name = [i[0] for i in c.description]
        conn.close()
        return col_name