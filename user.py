import sqlite3

class User:
    def __init__(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (username TEXT PRIMARY KEY, password TEXT, role TEXT)''')
        conn.close()
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS permissions
                     (FOREIGN KEY(role) REFERENCES users(role), admin INTEGER, storage_view INTEGER, storage_edit INTEGER, users_view INTEGER, users_edit INTEGER, permissions_edit INTEGER)''')
    def login(self, username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = c.fetchone()
        conn.close()
        return result
    
    def register(self, username, password, role):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        conn.close()
        return True
    
    def get_users(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        result = c.fetchall()
        conn.close()
        return result
    
    def get_user(self, username):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        return result
    
    
    def delete_user(self, username):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        return True
    
    def update_password(self, username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("UPDATE users SET password = ? WHERE username = ?", (password, username))
        conn.commit()
        conn.close()
        return True
    
    
    def get_permissions(self, username):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM permissions join users on permissions.role = users.role WHERE users.username = ?", (username,))
        result = c.fetchone()
        conn.close()
        return result
    
    def update_permissions(self, username, admin, storage_view, storage_edit, users_view, users_edit, permissions_edit):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("UPDATE permissions SET admin = ?, storage_view = ?, storage_edit = ?, users_view = ?, users_edit = ?, permissions_edit = ? WHERE role = (SELECT role FROM users WHERE username = ?)", (admin, storage_view, storage_edit, users_view, users_edit, permissions_edit, username))
        conn.commit()
        conn.close()
        return True
    
    def user_import_CSV(self, filename):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        with open(filename, 'r') as file:
            for line in file:
                username, password, role = line.split(',')
                c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        conn.close()
        return True
    
    def user_export_CSV(self, filename):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        with open(filename, 'w') as file:
            for row in c.fetchall():
                file.write(','.join(map(str, row)) + '\n')
        conn.close()
        return True
    
