import sqlite3

class User:
    def __init__(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (username TEXT PRIMARY KEY NOT NULL UNIQUE, password TEXT NOT NULL, role TEXT)''')
        conn.close()
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS permissions
                     (permission_username TEXT, admin INTEGER, storage_view INTEGER, storage_edit INTEGER, users_view INTEGER, users_edit INTEGER, permissions_edit INTEGER)''')
        conn.close()
        # Add default admin user
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = 'admin'")
        result = c.fetchone()
        if result == None:
            c.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin', 'admin')")
            c.execute("INSERT INTO permissions (permission_username, admin, storage_view, storage_edit, users_view, users_edit, permissions_edit) VALUES ('admin', 1, 1, 1, 1, 1, 1)")
            conn.commit()
        conn.close()

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
    
    def add_user(self, username, password, role, storage_view, storage_edit, users_view, users_edit, permissions_edit):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        c.execute("INSERT INTO permissions (permission_username, admin, storage_view, storage_edit, users_view, users_edit, permissions_edit) VALUES (?, 0, ?, ?, ?, ?, ?)", (username, storage_view, storage_edit, users_view, users_edit, permissions_edit))
        conn.commit()
        conn.close()
        return True
    
    def get_users(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT username, role FROM users")
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
    
    def update_role(self, username, role):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("UPDATE users SET role = ? WHERE username = ?", (role, username))
        conn.commit()
        conn.close()
        return True
    
    def get_permissions(self, username):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT permission_username , admin, storage_view, storage_edit, users_view, users_edit, permissions_edit FROM permissions join users on permissions.permission_username = users.username WHERE users.username = ?", (username,))
        result = c.fetchone()
        conn.close()
        return result
    
    def update_permissions(self, username, admin, storage_view, storage_edit, users_view, users_edit, permissions_edit):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("UPDATE permissions SET admin = ?, storage_view = ?, storage_edit = ?, users_view = ?, users_edit = ?, permissions_edit = ? WHERE permission_username = ?", (admin, storage_view, storage_edit, users_view, users_edit, permissions_edit, username))
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
    
