import tkinter as tk
import tkinter.ttk as ttk
from time import sleep
from user import User
from storage import Storage

class LOG_IN(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Log In")
        self.geometry("300x200")
        self.resizable(False, False)
        self.create_widgets()
        self.mainloop()
        #self.iconify()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Username:")
        self.label.pack()
        self.entry_username = ttk.Entry(self)
        self.entry_username.pack()
        self.label = ttk.Label(self, text="Password:")
        self.label.pack()
        self.entry_password = ttk.Entry(self)
        self.entry_password.pack()
        self.button = ttk.Button(self, text="Log In", command=self.log_in)
        self.button.pack()
        self.label_empty = ttk.Label(self, text="")
        self.label_empty.pack()

    def log_in(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        user = User()
        result = user.login(username, password)
        if result:
            self.label_empty.config(text="Zalogowano pomyślnie")
            sleep(1)
            self.destroy()
            app = GUI()
            app.mainloop()
        else:
            self.label_empty.config(text="Niepoprawne dane logowania")
            self.entry_username.delete(0, 'end')
            self.entry_password.delete(0, 'end')
            self.entry_username.focus()
            self.update()

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Storage_Management_System")
        self.geometry("800x600")
        self.resizable(False, False)
        self.create_menu()
        self.labelframe = ttk.LabelFrame(self, text="")
        self.labelframe.pack(fill=tk.BOTH, expand=True)

    def create_menu(self):
        self.menu = tk.Menu(self,tearoff=False)
        self.config(menu=self.menu)
        self.menu_file = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.menu_file)
        self.menu_file.add_command(label="Log Out", command=self.log_out)
        self.menu_file.add_command(label="Exit", command=self.quit)
        self.menu_storage = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Storage", menu=self.menu_storage)
        self.menu_storage.add_command(label="View", command=self.view_storage)
        self.menu_storage.add_command(label="Add", command=self.add_storage)
        self.menu_storage.add_command(label="Edit", command=self.edit_storage)
        self.menu_storage.add_command(label="Delete", command=self.delete_storage)
        self.menu_orders = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Orders", menu=self.menu_orders)
        self.menu_orders.add_command(label="View", command=self.view_orders)
        self.menu_orders.add_command(label="Add", command=self.add_orders)
        self.menu_orders.add_command(label="Edit", command=self.edit_orders)
        self.menu_orders.add_command(label="Delete", command=self.delete_orders)
        self.menu_orders.add_command(label="Import CSV", command=self.import_csv)
        self.menu_orders.add_command(label="Export CSV", command=self.export_csv)
        self.menu_users = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Users", menu=self.menu_users)
        self.menu_users.add_command(label="View", command=self.view_users)
        self.menu_users.add_command(label="Add", command=self.add_users)
        self.menu_users.add_command(label="Edit", command=self.edit_users)
        self.menu_users.add_command(label="Delete", command=self.delete_users)
        self.menu_users.add_command(label="Change Password", command=self.change_password)
        self.menu_users.add_command(label="Permissions", command=self.permissions)

    def create_frame(self, title):
        for widget in self.labelframe.winfo_children():
            widget.destroy()
        self.labelframe.config(text=title)
        self.labelframe.update()

    def create_view_storage_control_frame(self):
        self.control_frame = ttk.Frame(self.labelframe)
        self.control_frame.pack(fill=tk.BOTH, expand=True)
        self.label = ttk.Label(self.control_frame, text="Filter by:")
        self.label.pack()
        self.combobox_filter = ttk.Combobox(self.control_frame, values=["ID", "Name", "Price", "Quantity"])
        self.combobox_filter.pack()
        self.label = ttk.Label(self.control_frame, text="Value:")
        self.label.pack()
        self.entry_value = ttk.Entry(self.control_frame)
        self.entry_value.pack()
        self.label = ttk.Label(self.control_frame, text="Order by:")
        self.label.pack()
        self.combobox_order_by = ttk.Combobox(self.control_frame, values=["ID", "Name", "Price", "Quantity"])
        self.combobox_order_by.pack()
        self.button = ttk.Button(self.control_frame, text="Search", command=self.search_storage)
        self.button.pack()

    def view_storage(self):
        self.create_frame("View Storage")
        self.create_view_storage_control_frame()
        self.treeview = ttk.Treeview(self.labelframe, columns=("ID", "Name", "Price", "Quantity"))
        self.treeview.heading("#0", text="ID")
        self.treeview.heading("#1", text="Name")
        self.treeview.heading("#2", text="Price")
        self.treeview.heading("#3", text="Quantity")
        self.treeview.pack(fill=tk.BOTH, expand=True)
        self.button = ttk.Button(self.labelframe, text="Refresh", command=self.refresh_storage)
        self.button.pack()
        self.refresh_storage()

    def refresh_storage(self):
        self.treeview.delete(*self.treeview.get_children())
        self.storage = Storage().get_items()
        for item in self.storage:
            self.treeview.insert("", "end", values=item)

    def search_storage(self):
        filter = self.combobox_filter.get()
        value = self.entry_value.get()
        order_by = self.combobox_order_by.get()
        self.treeview.delete(*self.treeview.get_children())
        self.storage = Storage().get_items(filter, value, order_by)
        for item in self.storage:
            self.treeview.insert("", "end", values=item)

    def add_storage(self):
        self.create_frame("Add Storage")
        self.label = ttk.Label(self.labelframe, text="Name:")
        self.label.pack()
        self.entry_name = ttk.Entry(self.labelframe)
        self.entry_name.pack()
        self.label = ttk.Label(self.labelframe, text="Price:")
        self.label.pack()
        self.entry_price = ttk.Entry(self.labelframe)
        self.entry_price.pack()
        self.label = ttk.Label(self.labelframe, text="Quantity:")
        self.label.pack()
        self.entry_quantity = ttk.Entry(self.labelframe)
        self.entry_quantity.pack()
        self.button = ttk.Button(self.labelframe, text="Add", command=self.add_storage_confirm)
        self.button.pack()

    def add_storage_confirm(self):
        name = self.entry_name.get()
        price = self.entry_price.get()
        quantity = self.entry_quantity.get()
        Storage().add_item(name, price, quantity)
        self.create_frame("Add Storage")
        self.label = ttk.Label(self.labelframe, text="Item added successfully")
        self.label.pack()

    def edit_storage(self):
        self.create_frame("Edit Storage")
        self.label = ttk.Label(self.labelframe, text="ID:")
        self.label.pack()
        self.entry_id = ttk.Entry(self.labelframe)
        self.entry_id.pack()
        self.button = ttk.Button(self.labelframe, text="Search", command=self.search_storage_edit)
        self.button.pack()

    def search_storage_edit(self):
        id = self.entry_id.get()
        item = Storage().get_item(id)
        if item:
            self.create_frame("Edit Storage")
            self.label = ttk.Label(self.labelframe, text="Name:")
            self.label.pack()
            self.entry_name = ttk.Entry(self.labelframe)
            self.entry_name.insert(0, item[1])
            self.entry_name.pack()
            self.label = ttk.Label(self.labelframe, text="Price:")
            self.label.pack()
            self.entry_price = ttk.Entry(self.labelframe)
            self.entry_price.insert(0, item[2])
            self.entry_price.pack()
            self.label = ttk.Label(self.labelframe, text="Quantity:")
            self.label.pack()
            self.entry_quantity = ttk.Entry(self.labelframe)
            self.entry_quantity.insert(0, item[3])
            self.entry_quantity.pack()
            self.button = ttk.Button(self.labelframe, text="Edit", command=self.edit_storage_confirm)
            self.button.pack()
        else:
            self.create_frame("Edit Storage")
            self.label = ttk.Label(self.labelframe, text="Item not found")
            self.label.pack()

    def edit_storage_confirm(self):
        id = self.entry_id.get()
        price = self.entry_price.get()
        quantity = self.entry_quantity.get()
        Storage().update_item(id, price, quantity)
        self.create_frame("Edit Storage")
        self.label = ttk.Label(self.labelframe, text="Edit successful")
        self.label.pack()
    
    def delete_storage(self):
        self.create_frame("Delete Storage")
        self.label = ttk.Label(self.labelframe, text="ID:")
        self.label.pack()
        self.entry_id = ttk.Entry(self.labelframe)
        self.entry_id.pack()
        self.button = ttk.Button(self.labelframe, text="Delete", command=self.delete_storage_confirm)
        self.button.pack()

    def delete_storage_confirm(self):
        id = self.entry_id.get()
        Storage().delete_item(id)
        self.create_frame("Delete Storage")
        self.label = ttk.Label(self.labelframe, text="Item deleted successfully")
        self.label.pack()

    def view_orders(self):
        self.create_frame("View Orders")
        self.treeview = ttk.Treeview(self.labelframe, columns=("Order ID", "Product ID", "Quantity", "Date"))
        self.treeview.heading("#0", text="Order ID")
        self.treeview.heading("#1", text="Product ID")
        self.treeview.heading("#2", text="Quantity")
        self.treeview.heading("#3", text="Date")
        self.treeview.pack(fill=tk.BOTH, expand=True)
        self.button = ttk.Button(self.labelframe, text="Refresh", command=self.refresh_orders)
        self.button.pack()
        self.refresh_orders()

    def refresh_orders(self):
        self.treeview.delete(*self.treeview.get_children())
        self.orders = Storage().get_orders()
        for order in self.orders:
            self.treeview.insert("", "end", values=order)

    def add_orders(self):
        self.create_frame("Add Orders")
        self.label = ttk.Label(self.labelframe, text="Product ID:")
        self.label.pack()
        self.entry_product_id = ttk.Entry(self.labelframe)
        self.entry_product_id.pack()
        self.label = ttk.Label(self.labelframe, text="Quantity:")
        self.label.pack()
        self.entry_quantity = ttk.Entry(self.labelframe)
        self.entry_quantity.pack()
        self.label = ttk.Label(self.labelframe, text="Date:")
        self.label.pack()
        self.entry_date = ttk.Entry(self.labelframe)
        self.entry_date.pack()
        self.button = ttk.Button(self.labelframe, text="Add", command=self.add_orders_confirm)
        self.button.pack()

    def add_orders_confirm(self):
        product_id = self.entry_product_id.get()
        quantity = self.entry_quantity.get()
        date = self.entry_date.get()
        Storage().add_order(product_id, quantity, date)
        self.create_frame("Add Orders")
        self.label = ttk.Label(self.labelframe, text="Order added successfully")
        self.label.pack()

    def edit_orders(self):
        self.create_frame("Edit Orders")
        self.label = ttk.Label(self.labelframe, text="Order ID:")
        self.label.pack()
        self.entry_order_id = ttk.Entry(self.labelframe)
        self.entry_order_id.pack()
        self.button = ttk.Button(self.labelframe, text="Search", command=self.search_orders_edit)
        self.button.pack()

    def search_orders_edit(self):
        order_id = self.entry_order_id.get()
        order = Storage().get_order(order_id)
        if order:
            self.create_frame("Edit Orders")
            self.label = ttk.Label(self.labelframe, text="Product ID:")
            self.label.pack()
            self.entry_product_id = ttk.Entry(self.labelframe)
            self.entry_product_id.insert(0, order[1])
            self.entry_product_id.pack()
            self.label = ttk.Label(self.labelframe, text="Quantity:")
            self.label.pack()
            self.entry_quantity = ttk.Entry(self.labelframe)
            self.entry_quantity.insert(0, order[2])
            self.entry_quantity.pack()
            self.label = ttk.Label(self.labelframe, text="Date:")
            self.label.pack()
            self.entry_date = ttk.Entry(self.labelframe)
            self.entry_date.insert(0, order[3])
            self.entry_date.pack()
            self.button = ttk.Button(self.labelframe, text="Edit", command=self.edit_orders_confirm)
            self.button.pack()
        else:
            self.create_frame("Edit Orders")
            self.label = ttk.Label(self.labelframe, text="Order not found")
            self.label.pack()

    def edit_orders_confirm(self):
        order_id = self.entry_order_id.get()
        product_id = self.entry_product_id.get()
        quantity = self.entry_quantity.get()
        date = self.entry_date.get()
        Storage().update_order(order_id, product_id, quantity, date)
        self.create_frame("Edit Orders")
        self.label = ttk.Label(self.labelframe, text="Edit successful")
        self.label.pack()

    def delete_orders(self):
        self.create_frame("Delete Orders")
        self.label = ttk.Label(self.labelframe, text="Order ID:")
        self.label.pack()
        self.entry_order_id = ttk.Entry(self.labelframe)
        self.entry_order_id.pack()
        self.button = ttk.Button(self.labelframe, text="Delete", command=self.delete_orders_confirm)
        self.button.pack()

    def delete_orders_confirm(self):
        order_id = self.entry_order_id.get()
        Storage().delete_order(order_id)
        self.create_frame("Delete Orders")
        self.label = ttk.Label(self.labelframe, text="Order deleted successfully")
        self.label.pack()

    def import_csv(self):
        self.create_frame("Import CSV")
        self.label = ttk.Label(self.labelframe, text="Filename:")
        self.label.pack()
        self.entry_filename = ttk.Entry(self.labelframe)
        self.entry_filename.pack()
        self.button = ttk.Button(self.labelframe, text="Import", command=self.import_csv_confirm)
        self.button.pack() 

    def import_csv_confirm(self):
        filename = self.entry_filename.get()
        Storage().order_import_CSV_update(filename)
        self.create_frame("Import CSV")
        self.label = ttk.Label(self.labelframe, text="CSV imported successfully")
        self.label.pack()

    def export_csv(self):
        self.create_frame("Export CSV")
        self.label = ttk.Label(self.labelframe, text="Filename:")
        self.label.pack()
        self.entry_filename = ttk.Entry(self.labelframe)
        self.entry_filename.pack()
        self.button = ttk.Button(self.labelframe, text="Export", command=self.export_csv_confirm)
        self.button.pack()

    def export_csv_confirm(self):
        filename = self.entry_filename.get()
        Storage().order_export_CSV(filename)
        self.create_frame("Export CSV")
        self.label = ttk.Label(self.labelframe, text="CSV exported successfully")
        self.label.pack()

    def view_users(self):
        self.create_frame("View Users")
        self.treeview = ttk.Treeview(self.labelframe, columns=("ID", "Username", "Role"))
        self.treeview.heading("#0", text="ID")
        self.treeview.heading("#1", text="Username")
        self.treeview.heading("#2", text="Role")
        self.treeview.pack(fill=tk.BOTH, expand=True)
        self.button = ttk.Button(self.labelframe, text="Refresh", command=self.refresh_users)
        self.button.pack()
        self.refresh_users()

    def refresh_users(self):
        self.treeview.delete(*self.treeview.get_children())
        self.users = User().get_users()
        for user in self.users:
            self.treeview.insert("", "end", values=user)

    def add_users(self):
        self.create_frame("Add Users")
        self.label = ttk.Label(self.labelframe, text="Username:")
        self.label.pack()
        self.entry_username = ttk.Entry(self.labelframe)
        self.entry_username.pack()
        self.label = ttk.Label(self.labelframe, text="Password:")
        self.label.pack()
        self.entry_password = ttk.Entry(self.labelframe)
        self.entry_password.pack()
        self.label = ttk.Label(self.labelframe, text="Role:")
        self.label.pack()
        self.entry_role = ttk.Entry(self.labelframe)
        self.entry_role.pack()
        self.button = ttk.Button(self.labelframe, text="Add", command=self.add_users_confirm)
        self.button.pack()

    def add_users_confirm(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        role = self.entry_role.get()
        User().register(username, password, role)
        self.create_frame("Add Users")
        self.label = ttk.Label(self.labelframe, text="User added successfully")
        self.label.pack()

    def edit_users(self):
        self.create_frame("Edit Users")
        self.label = ttk.Label(self.labelframe, text="Username:")
        self.label.pack()
        self.entry_username = ttk.Entry(self.labelframe)
        self.entry_username.pack()
        self.button = ttk.Button(self.labelframe, text="Search", command=self.search_users_edit)
        self.button.pack()

    def search_users_edit(self):
        username = self.entry_username.get()
        user = User().get_user(username)
        if user:
            self.create_frame("Edit Users")
            self.label = ttk.Label(self.labelframe, text="Password:")
            self.label.pack()
            self.entry_password = ttk.Entry(self.labelframe)
            self.entry_password.insert(0, user[2])
            self.entry_password.pack()
            self.label = ttk.Label(self.labelframe, text="Role:")
            self.label.pack()
            self.entry_role = ttk.Entry(self.labelframe)
            self.entry_role.insert(0, user[3])
            self.entry_role.pack()
            self.button = ttk.Button(self.labelframe, text="Edit", command=self.edit_users_confirm)
            self.button.pack()
        else:
            self.create_frame("Edit Users")
            self.label = ttk.Label(self.labelframe, text="User not found")
            self.label.pack()

    def edit_users_confirm(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        role = self.entry_role.get()
        User().update_password(username, password)
        User().update_role(username, role)
        self.create_frame("Edit Users")
        self.label = ttk.Label(self.labelframe, text="Edit successful")
        self.label.pack()

    def delete_users(self):
        self.create_frame("Delete Users")
        self.label = ttk.Label(self.labelframe, text="Username:")
        self.label.pack()
        self.entry_username = ttk.Entry(self.labelframe)
        self.entry_username.pack()
        self.button = ttk.Button(self.labelframe, text="Delete", command=self.delete_users_confirm)
        self.button.pack()

    def delete_users_confirm(self):
        username = self.entry_username.get()
        User().delete_user(username)
        self.create_frame("Delete Users")
        self.label = ttk.Label(self.labelframe, text="User deleted successfully")
        self.label.pack()

    def change_password(self):
        self.create_frame("Change Password")
        self.label = ttk.Label(self.labelframe, text="Username:")
        self.label.pack()
        self.entry_username = ttk.Entry(self.labelframe)
        self.entry_username.pack()
        self.label = ttk.Label(self.labelframe, text="Password:")
        self.label.pack()
        self.entry_password = ttk.Entry(self.labelframe)
        self.entry_password.pack()
        self.button = ttk.Button(self.labelframe, text="Change", command=self.change_password_confirm)
        self.button.pack()

    def change_password_confirm(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        User().update_password(username, password)
        self.create_frame("Change Password")
        self.label = ttk.Label(self.labelframe, text="Password changed successfully")
        self.label.pack()

    def permissions(self):
        self.create_frame("Permissions")
        self.label = ttk.Label(self.labelframe, text="Username:")
        self.label.pack()
        self.entry_username = ttk.Entry(self.labelframe)
        self.entry_username.pack()
        self.button = ttk.Button(self.labelframe, text="Search", command=self.search_permissions)
        self.button.pack()

    def search_permissions(self):
        username = self.entry_username.get()
        user = User().get_permissions(username)
        if user:
            self.create_frame("Permissions")
            self.label = ttk.Label(self.labelframe, text="Admin:")
            self.label.pack()
            self.entry_admin = ttk.Entry(self.labelframe)
            for n in user:
                print(n)
            self.entry_admin.insert(0, user[1])
            self.entry_admin.pack()
            self.label = ttk.Label(self.labelframe, text="Storage View:")
            self.label.pack()
            self.entry_storage_view = ttk.Entry(self.labelframe)
            self.entry_storage_view.insert(0, user[2])
            self.entry_storage_view.pack()
            self.label = ttk.Label(self.labelframe, text="Storage Edit:")
            self.label.pack()
            self.entry_storage_edit = ttk.Entry(self.labelframe)
            self.entry_storage_edit.insert(0, user[3])
            self.entry_storage_edit.pack()
            self.label = ttk.Label(self.labelframe, text="Users View:")
            self.label.pack()
            self.entry_users_view = ttk.Entry(self.labelframe)
            self.entry_users_view.insert(0, user[4])
            self.entry_users_view.pack()
            self.label = ttk.Label(self.labelframe, text="Users Edit:")
            self.label.pack()
            self.entry_users_edit = ttk.Entry(self.labelframe)
            self.entry_users_edit.insert(0, user[5])
            self.entry_users_edit.pack()
            self.label = ttk.Label(self.labelframe, text="Permissions Edit:")
            self.label.pack()
            self.entry_permissions_edit = ttk.Entry(self.labelframe)
            self.entry_permissions_edit.insert(0, user[6])
            self.entry_permissions_edit.pack()
            self.button = ttk.Button(self.labelframe, text="Edit", command=lambda:self.permissions_confirm(username))
            self.button.pack()
        else:
            self.create_frame("Permissions")
            self.label = ttk.Label(self.labelframe, text="User not found")
            self.label.pack()

    def permissions_confirm(self, username):
        
        admin = self.entry_admin.get()
        storage_view = self.entry_storage_view.get()
        storage_edit = self.entry_storage_edit.get()
        users_view = self.entry_users_view.get()
        users_edit = self.entry_users_edit.get()
        permissions_edit = self.entry_permissions_edit.get()
        User().update_permissions(username, admin, storage_view, storage_edit, users_view, users_edit, permissions_edit)
        self.create_frame("Permissions")
        self.label = ttk.Label(self.labelframe, text="Permissions edited successfully")
        self.label.pack()

    


    def log_out(self):
        self.destroy()
        app = LOG_IN()
        app.mainloop()

    def quit(self):
        self.destroy()
