import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
import databaseHandler
from tkcalendar import DateEntry

current_user = None

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title('COP 3703 Database Implementation')
        self.root.geometry('450x200')
        self.root.iconbitmap('logo.ico')

        self.root.resizable(width=False, height=False)

        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.pack(expand=True)
        
        ttk.Label(self.frame, text="Username:").grid(row=0, column=0, pady=5)
        self.username = ttk.Entry(self.frame)
        self.username.grid(row=0, column=1, pady=5)
        
        ttk.Label(self.frame, text="Password:").grid(row=1, column=0, pady=5)
        self.password = ttk.Entry(self.frame, show="*")
        self.password.grid(row=1, column=1, pady=5)
        
        ttk.Button(self.frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.frame, text="Create Account", command=self.show_create_account).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(self.frame, text="Forgot Password", command=self.show_forgot_password).grid(row=4, column=0, columnspan=2, pady=5)

    def login(self):
        username = self.username.get()
        password = self.password.get()

        try:
            userInfo = databaseHandler.executeSQL(f"SELECT * FROM Account WHERE Username = '{username}'")
            if userInfo == []:
                messagebox.showerror("Error", f"Account '{username}' does not exist!")
                return
            
            if userInfo[0][6] == 0:
                messagebox.showerror("Error", f"Account '{username}' has been deleted. You can still request your data.")
                return
            
            if userInfo[0][4] != password:
                messagebox.showerror("Error", "Invalid Password!")
                return
        except:
            messagebox.showerror("Error", "Login error")
            return

        global current_user
        current_user = userInfo[0]
        self.root.destroy()
        MainApplication(current_user[7])

    def show_create_account(self):
        CreateAccountWindow(self.root)

    def show_forgot_password(self):
        ForgotPasswordWindow(self.root)

class ForgotPasswordWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)

        self.window.title("Forgot Password")
        self.window.geometry("400x200")
        self.window.iconbitmap('logo.ico')

        self.window.resizable(width=False, height=False)
        
        frame = ttk.Frame(self.window, padding="20")
        frame.pack(expand=True)
        
        ttk.Label(
            frame,
            text="Enter your email and new password:",
            wraplength=300
        ).grid(row=0, column=0, columnspan=3, pady=(0, 20))

        ttk.Label(frame, text="Email:").grid(row=1, column=0, pady=5, sticky="e")
        self.email_entry = ttk.Entry(frame, width=30)
        self.email_entry.grid(row=1, column=1, pady=5, padx=(10, 0), sticky="ew")

        ttk.Label(frame, text="New Password:").grid(row=2, column=0, pady=5, sticky="e")
        self.password_entry = ttk.Entry(frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5, padx=(10, 0), sticky="ew")

        self.show_password = tk.BooleanVar()
        self.show_password_btn = ttk.Checkbutton(
            frame,
            text="Show Password",
            variable=self.show_password,
            command=self.toggle_password_visibility
        )
        self.show_password_btn.grid(row=2, column=2, padx=(10, 0))
        
        ttk.Button(
            frame,
            text="Reset Password",
            command=self.reset_password
        ).grid(row=4, column=0, columnspan=3, pady=20)
        
        frame.columnconfigure(1, weight=1)

    def toggle_password_visibility(self):
        show_char = "" if self.show_password.get() else "*"
        self.password_entry["show"] = show_char

    def reset_password(self):
        email = self.email_entry.get().strip()
        new_password = self.password_entry.get()
        
        if not email:
            messagebox.showerror("Error", "Please enter your email address!", parent=self.window)
            return
            
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address!", parent=self.window)
            return

        if not new_password:
            messagebox.showerror("Error", "Please enter a new password!", parent=self.window)
            return

        if len(new_password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long!", parent=self.window)
            return

        if databaseHandler.executeSQL(f"SELECT * FROM Account WHERE Email = '{email}'") == []:
            messagebox.showerror("Error", f"Email '{email}' does not exist.", parent=self.window)
            return
        
        try:
            databaseHandler.executeSQL(f"UPDATE Account SET Password = '{new_password}' WHERE Email = '{email}'")
            messagebox.showinfo("Success", "Password has been reset successfully!", parent=self.window)
            self.window.destroy()
        except:
            messagebox.showerror("Error", "Failed to reset password. Please try again.", parent=self.window)

class CreateAccountWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)

        self.window.title("Create Account")
        self.window.geometry("400x275")
        self.window.iconbitmap('logo.ico')

        self.window.resizable(width=False, height=False)
        
        frame = ttk.Frame(self.window, padding="20")
        frame.pack(expand=True)
        
        ttk.Label(
            frame, 
            text="Create User Account", 
            font=('Helvetica', 12, 'bold')
        ).grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        fields = ["Username", "Email", "First Name", "Last Name", "Password"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            ttk.Label(frame, text=field + ":").grid(row=i+1, column=0, pady=5, sticky="e")
            if field == "Password":
                self.entries[field] = ttk.Entry(frame, show="*")
            else:
                self.entries[field] = ttk.Entry(frame)
            self.entries[field].grid(row=i+1, column=1, pady=5, padx=(10,0), sticky="ew")
        
        self.show_password = tk.BooleanVar()
        self.show_password_btn = ttk.Checkbutton(
            frame, 
            text="Show Password",
            variable=self.show_password,
            command=self.toggle_password_visibility
        )
        self.show_password_btn.grid(row=5, column=2, padx=(10,0))
        
        ttk.Button(
            frame, 
            text="Create Account", 
            command=self.create_account
        ).grid(row=6, column=0, columnspan=3, pady=20)

        frame.columnconfigure(1, weight=1)

    def toggle_password_visibility(self):
        if self.show_password.get():
            self.entries["Password"]["show"] = ""
        else:
            self.entries["Password"]["show"] = "*"

    def create_account(self):
        for field, entry in self.entries.items():
            if not entry.get().strip():
                messagebox.showerror("Error", f"{field} cannot be empty!", parent=self.window)
                return

        email = self.entries["Email"].get()
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address!")
            return

        password = self.entries["Password"].get()
        username = self.entries["Username"].get()
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long!")
            return

        if databaseHandler.executeSQL(f"SELECT * FROM Account WHERE Email = '{email}'") != []:
            messagebox.showerror("Error", f"Email '{email}' is already associated with an account.", parent=self.window)
            return
        
        if databaseHandler.executeSQL(f"SELECT * FROM Account WHERE Username = '{username}'") != []:
            messagebox.showerror("Error", f"Username '{username}' is already associated with an account.", parent=self.window)
            return

        map = {
            "First Name": "FirstName",
            "Last Name": "LastName"
        }

        user_data = {}
        for field, entry in self.entries.items():
            db_field = map.get(field, field)
            user_data[db_field] = entry.get()

        try:
            databaseHandler.executeSQL(f"INSERT INTO Account (FirstName, LastName, Email, Password, Username, Is_Active, isEmployee) values ('{user_data["FirstName"]}', '{user_data["LastName"]}', '{user_data["Email"]}', '{user_data["Password"]}', '{user_data["Username"]}', true, true);")
        except:
            messagebox.showerror("Error", "Account creation failed!", parent=self.window)
            return

        messagebox.showinfo("Success", "Account created successfully!")
        self.window.destroy()

class MainApplication:
    def __init__(self, isEmployee):
        self.root = tk.Tk()

        self.root.title("COP 3703 POS System")
        self.root.iconbitmap('logo.ico')
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        
        self.tab_sizes = {
            "User Account Management": "500x430",
            "Product Management": "950x500",
            "New Transaction": "1050x600",
            "Transaction History": "875x500"
        }

        self.root.resizable(width=False, height=False)
        
        self.create_user_management_tab()
        self.create_transaction_tab()
        self.create_transaction_history_tab()

        if isEmployee == 1:
            self.create_product_management_tab()
            
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.on_tab_change(None)

    def on_tab_change(self, event):
        current_tab = self.notebook.select()
        if current_tab:
            tab_text = self.notebook.tab(current_tab, "text")
            if tab_text in self.tab_sizes:
                self.root.geometry(self.tab_sizes[tab_text])

    def create_user_management_tab(self):
        user_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(user_frame, text="User Account Management")
        
        ttk.Label(user_frame, text="User Profile", font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        self.profile_entries = {}
        fields = ["Username", "Email", "First Name", "Last Name", "Password"]
        
        for field in fields:
            ttk.Label(user_frame, text=field + ":").pack(pady=2)
            entry = ttk.Entry(user_frame)
            entry.pack(pady=2)
            self.profile_entries[field] = entry
        
        ttk.Button(
            user_frame, 
            text="Update Profile",
            command=lambda: self.update_profile(fields)
        ).pack(pady=10)
        
        ttk.Button(
            user_frame, 
            text="Delete Account",
            command=lambda: self.delete_account()
        ).pack(pady=5)

    def create_product_management_tab(self):
        product_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(product_frame, text="Product Management")
        
        list_frame = ttk.Frame(product_frame)
        list_frame.pack(fill='both', expand=True)
        
        columns = ("Movie_ID", "Title", "Genre", "Category", "Rating", "Price", "Stock_Amount")
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Movie_ID":
                self.tree.column(col, width=35)
            elif col == "Title":
                self.tree.column(col, width=200)
            else:
                self.tree.column(col, width=100)
        self.tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        movies = databaseHandler.executeSQL("SELECT Movie_ID, Title, Genre, Category, Rating, Price, Stock_Amount FROM `Movies`")

        for item in self.tree.get_children():
            self.tree.delete(item)

        for movie in movies:
            self.tree.insert('', 'end', values=movie)
        
        button_frame = ttk.Frame(product_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Product", command=self.add_product_window).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Edit Product", command=self.edit_product_window).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Delete Product", command=self.delete_product).pack(side='left', padx=5)
        ttk.Button(button_frame, text="View Product", command=self.view_product_window).pack(side='left', padx=5)

    def delete_product(self):
        if not self.tree.selection():
            messagebox.showerror("Error", "Please select a movie to delete")
            return
            
        selected_item = self.tree.selection()[0]
        movie_id = self.tree.item(selected_item)['values'][0]
        movie_title = self.tree.item(selected_item)['values'][1]
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{movie_title}'? This action cannot be undone.")
        
        if confirm:
            try:
                databaseHandler.executeSQL(f"DELETE FROM Movies WHERE Movie_ID = {movie_id}")
                messagebox.showinfo("Success", "Movie deleted successfully!")
                self.refresh_movie_list()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def edit_product_window(self):
        if not self.tree.selection():
            messagebox.showerror("Error", "Please select a movie to edit")
            return
            
        selected_item = self.tree.selection()[0]
        movie_id = self.tree.item(selected_item)['values'][0]
        
        movie_data = databaseHandler.executeSQL(f"SELECT Movie_ID, Title, Genre, Category, Rating, Price, Stock_Amount FROM Movies WHERE Movie_ID = {movie_id}")
        if not movie_data:
            return
            
        movie = movie_data[0]
        
        popup = tk.Toplevel(self.root)
        popup.title("Edit Movie")
        popup.iconbitmap('logo.ico')

        frame = ttk.Frame(popup, padding="20")
        frame.grid(row=0, column=0, sticky="nw")

        ttk.Label(
            frame, 
            text="Edit Movie", 
            font=('Helvetica', 12, 'bold')
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        self.product_entries = {}
        
        fields = ["Title", "Genre", "Category", "Rating", "Price", "Stock_Amount"]
        
        for i, field in enumerate(fields):
            ttk.Label(frame, text=field + ":").grid(row=i+1, column=0, pady=5, padx=(0,10), sticky="w")
            entry = ttk.Entry(frame, width=30)
            entry.insert(0, movie[i+1])
            entry.grid(row=i+1, column=1, pady=5, sticky="w")
            self.product_entries[field] = entry

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20, sticky="w")
        
        ttk.Button(
            button_frame, 
            text="Save Changes",
            command=lambda: self.save_edited_product(movie_id)
        ).pack(side='left', padx=(0,5))
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=popup.destroy
        ).pack(side='left')

        frame.grid_columnconfigure(1, weight=1)
        
        popup.update_idletasks()
        popup.geometry('')

        self.refresh_movie_list()

    def view_product_window(self):
        if not self.tree.selection():
            messagebox.showerror("Error", "Please select a movie to view")
            return
            
        selected_item = self.tree.selection()[0]
        movie_id = self.tree.item(selected_item)['values'][0]
        
        movie_data = databaseHandler.executeSQL(f"SELECT Movie_ID, Title, Genre, Category, Rating, Price, Stock_Amount FROM Movies WHERE Movie_ID = {movie_id}")
        if not movie_data:
            return
            
        movie = movie_data[0]
        
        popup = tk.Toplevel(self.root)
        popup.title("View Movie")
        popup.iconbitmap('logo.ico')

        frame = ttk.Frame(popup, padding="20")
        frame.grid(row=0, column=0, sticky="nw")

        ttk.Label(
            frame, 
            text="Movie Details", 
            font=('Helvetica', 12, 'bold')
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        fields = ["Title", "Genre", "Category", "Rating", "Price", "Stock_Amount"]
        
        for i, field in enumerate(fields):
            ttk.Label(frame, text=field + ":", font=('Helvetica', 10, 'bold')).grid(row=i+1, column=0, pady=5, padx=(0,10), sticky="w")
            ttk.Label(frame, text=str(movie[i+1])).grid(row=i+1, column=1, pady=5, sticky="w")

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20, sticky="w")
        
        ttk.Button(
            button_frame, 
            text="Close",
            command=popup.destroy
        ).pack(side='left')

        frame.grid_columnconfigure(1, weight=1)
        
        popup.update_idletasks()
        popup.geometry('')

    def save_edited_product(self, movie_id):
        values = {field: entry.get().strip() for field, entry in self.product_entries.items()}
        
        if not all(values.values()):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            price = float(values["Price"])
            stock = int(values["Stock_Amount"])
            
            databaseHandler.executeSQL(
                f"""UPDATE Movies 
                    SET Title = '{values["Title"]}',
                        Genre = '{values["Genre"]}',
                        Category = '{values["Category"]}',
                        Rating = '{values["Rating"]}',
                        Price = {price},
                        Stock_Amount = {stock}
                    WHERE Movie_ID = {movie_id}"""
            )
            
            messagebox.showinfo("Success", "Movie updated successfully!")
            self.refresh_movie_list()
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    widget.destroy()
                
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_product_window(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add New Movie")
        popup.iconbitmap('logo.ico')

        frame = ttk.Frame(popup, padding="20")
        frame.grid(row=0, column=0, sticky="nw")

        ttk.Label(
            frame, 
            text="Add New Movie", 
            font=('Helvetica', 12, 'bold')
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        self.product_entries = {}
        
        fields = ["Title", "Genre", "Category", "Rating", "Price", "Stock_Amount"]
        
        for i, field in enumerate(fields):
            ttk.Label(frame, text=field + ":").grid(row=i+1, column=0, pady=5, padx=(0,10), sticky="w")
            entry = ttk.Entry(frame, width=30)
            entry.grid(row=i+1, column=1, pady=5, sticky="w")
            self.product_entries[field] = entry

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20, sticky="w")
        
        ttk.Button(
            button_frame, 
            text="Add Movie",
            command=self.save_new_product
        ).pack(side='left', padx=(0,5))
        
        ttk.Button(
            button_frame, 
            text="Cancel",
            command=popup.destroy
        ).pack(side='left')

        frame.grid_columnconfigure(1, weight=1)
        
        popup.update_idletasks()
        popup.geometry('')

    def save_new_product(self):
        values = {field: entry.get().strip() for field, entry in self.product_entries.items()}
        
        if not all(values.values()):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            price = float(values["Price"])
            stock = int(values["Stock_Amount"])
            
            databaseHandler.executeSQL(
                f"""INSERT INTO Movies (Title, Genre, Category, Rating, Price, Stock_Amount) 
                    VALUES ('{values["Title"]}', '{values["Genre"]}', '{values["Category"]}',
                    '{values["Rating"]}', {price}, {stock})"""
            )
            
            messagebox.showinfo("Success", "Movie added successfully!")
            self.refresh_movie_list()

            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    widget.destroy()
                    
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for Price and Stock Amount!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add movie! {e}")

    def create_transaction_tab(self):
        trans_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(trans_frame, text="New Transaction")
        
        left_panel = ttk.Frame(trans_frame)
        left_panel.pack(side='left', fill='both', expand=True)
        
        right_panel = ttk.Frame(trans_frame)
        right_panel.pack(side='right', fill='both', expand=True)

        ttk.Label(left_panel, text="Available Movies", font=('Helvetica', 12, 'bold')).pack(pady=10)
        self.product_tree = ttk.Treeview(left_panel, columns=("Movie_ID", "Title", "Price", "Stock_Amount"), show='headings')
        for col in ("Movie_ID", "Title", "Price", "Stock_Amount"):
            if col == "Movie_ID" or col == "Price" or col == "Stock_Amount":
                self.product_tree.column(col, width=60)
            elif col == "Title":
                self.product_tree.column(col, width=200)
            else:
                self.product_tree.column(col, width=100)

            if col == "Stock_Amount":
                self.product_tree.heading(col, text="Stock")
            else:
                self.product_tree.heading(col, text=col)
        self.product_tree.pack(fill='both', expand=True)

        movies = databaseHandler.executeSQL("SELECT Movie_ID, Title, Price, Stock_Amount FROM `Movies` WHERE `Stock_Amount` > 0;")

        for item in self.product_tree.get_children():
            self.product_tree.delete(item)

        for movie in movies:
            formatted_movie = list(movie)
            formatted_movie[2] = f"${formatted_movie[2]}"
            self.product_tree.insert('', 'end', values=formatted_movie)

        self.product_tree.bind('<Double-1>', self.add_to_cart)

        ttk.Label(right_panel, text="Shopping Cart", font=('Helvetica', 12, 'bold')).pack(pady=10)
        self.cart_tree = ttk.Treeview(right_panel, columns=("Movie Title", "Quantity", "Price"), show='headings')
        for col in ("Movie Title", "Quantity", "Price"):
            self.cart_tree.heading(col, text=col)
        self.cart_tree.pack(fill='both', expand=True)
        
        controls_frame = ttk.Frame(right_panel)
        controls_frame.pack(fill='x', pady=10)
        self.total_label = ttk.Label(controls_frame, text="Total: $0.00", font=('Helvetica', 12, 'bold'))
        self.total_label.pack(side='left')
        ttk.Button(controls_frame, text="Complete Transaction", command=self.complete_transaction).pack(side='right', padx=5)
        ttk.Button(controls_frame, text="Clear Cart", command=self.clear_cart).pack(side='right', padx=5)
        ttk.Button(controls_frame, text="Remove Item", command=self.remove_from_cart).pack(side='right', padx=5)

    def complete_transaction(self):
        if not self.cart_tree.get_children():
            messagebox.showwarning("Empty Cart", "Please add items to cart before completing transaction")
            return

        transaction_items = []
        total_amount = 0

        movies = databaseHandler.executeSQL("SELECT Movie_ID, Title, Stock_Amount FROM Movies")
        movie_info = {movie[1]: {"id": movie[0], "stock": movie[2]} for movie in movies}

        if self.update_total() >= 250:
            messagebox.showwarning("Cart", "Please update total under $250.00!")
            return
        
        transaction_id = databaseHandler.executeSQL(f"INSERT INTO Transactions (Account_ID, TransactionDate, TotalAmount, PaymentMethod) VALUES ({current_user[0]}, '{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', {self.update_total()}, 'Online/Application');")["last_insert_id"]

        for i, item in enumerate(self.cart_tree.get_children()):
            cart_item = self.cart_tree.item(item)['values']
            movie_name = cart_item[0]
            quantity = cart_item[1]
            total = float(cart_item[3].replace('$', ''))
            
            movie_id = movie_info[movie_name]["id"]
            current_stock = movie_info[movie_name]["stock"]
            
            if quantity > current_stock:
                messagebox.showerror("Stock Error", f"Not enough stock for {movie_name}")
                return
                
            transaction_items.append((movie_id, quantity))
            total_amount += total

            databaseHandler.executeSQL(f"UPDATE Movies SET Stock_Amount = {current_stock - quantity} WHERE Movie_ID = {movie_id}")
            databaseHandler.executeSQL(f"INSERT INTO TransactionItems (Transaction_ID, Movie_ID, Quantity, Subtotal) VALUES ({transaction_id}, {movie_id}, {quantity}, {total})")


        messagebox.showinfo("Success", "Transaction completed successfully!")
        self.clear_cart()
        self.refresh_movie_list()

    def refresh_movie_list(self):
        movies = databaseHandler.executeSQL("SELECT Movie_ID, Title, Price, Stock_Amount FROM `Movies` WHERE `Stock_Amount` > 0;")
        movies_manage = databaseHandler.executeSQL("SELECT * FROM `Movies`;")

        for item in self.tree.get_children():
            self.tree.delete(item)

        for movie in movies_manage:
            formatted_movie = list(movie)
            formatted_movie[5] = f"${formatted_movie[5]}"
            self.tree.insert('', 'end', values=formatted_movie)

        for item in self.product_tree.get_children():
            self.product_tree.delete(item)

        for movie in movies:
            formatted_movie = list(movie)
            formatted_movie[2] = f"${formatted_movie[2]}"
            self.product_tree.insert('', 'end', values=formatted_movie)

    def create_transaction_history_tab(self):
        history_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(history_frame, text="Transaction History")

        filter_frame = ttk.Frame(history_frame)
        filter_frame.pack(fill='x', pady=10)
        ttk.Label(filter_frame, text="Date Range:").pack(side='left')
        self.cal = DateEntry(filter_frame, width=12, year=2019, month=6, day=22, background='darkblue', foreground='white', borderwidth=2).pack(side='left', padx='5')
        ttk.Button(filter_frame, text="Search").pack(side='left', padx='5')
        
        columns = ("Transaction_ID", "Date", "Subtotal", "Payment Method")
        self.transaction_tree = ttk.Treeview(history_frame, columns=columns, show='headings')
        for col in columns:
            self.transaction_tree.heading(col, text=col)
        self.transaction_tree.pack(fill='both', expand=True)

        transactions = databaseHandler.executeSQL(f"SELECT Transaction_ID, TransactionDate, TotalAmount, PaymentMethod FROM `Transactions` WHERE `Account_ID` = {current_user[0]};")

        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)

        for transaction in transactions:
            formatted_transaction = list(transaction)
            formatted_transaction[2] = f"${formatted_transaction[2]}"
            self.transaction_tree.insert('', 'end', values=formatted_transaction)

    def add_to_cart(self, event):
        selected_item = self.product_tree.selection()[0]
        item_details = self.product_tree.item(selected_item)['values']
        current_stock = item_details[3]
        
        if current_stock <= 0:
            messagebox.showerror("Out of Stock", "This item is out of stock!")
            return
            
        existing_items = self.cart_tree.get_children()
        for cart_item in existing_items:
            cart_values = self.cart_tree.item(cart_item)['values']
            if cart_values[0] == item_details[1]:
                new_quantity = cart_values[1] + 1
                if new_quantity > current_stock:
                    messagebox.showerror("Insufficient Stock", f"Only {current_stock} items available!")
                    return
                    
                price = float(item_details[2].replace('$', ''))
                new_total = new_quantity * price
                self.cart_tree.item(cart_item, values=(
                    cart_values[0],
                    new_quantity,
                    item_details[2],
                    f"${new_total:.2f}"
                ))
                break
        else:
            price = float(item_details[2].replace('$', ''))
            self.cart_tree.insert('', 'end', values=(
                item_details[1],
                1,
                item_details[2],
                f"${price:.2f}"
            ))
        
        self.update_total()

    def remove_from_cart(self):
        selected_item = self.cart_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to remove")
            return
            
        selected_item = selected_item[0]
        item_values = self.cart_tree.item(selected_item)['values']
        
        current_quantity = int(item_values[1])
        price_per_item = float(item_values[2].replace('$', ''))
        
        if current_quantity > 1:
            new_quantity = current_quantity - 1
            new_total = price_per_item * new_quantity
            self.cart_tree.item(selected_item, values=(item_values[0], new_quantity, f"${price_per_item:.2f}", f"${new_total:.2f}"))
        else:
            self.cart_tree.delete(selected_item)
        
        self.update_total()
        
    def update_total(self):
        total = 0
        for item in self.cart_tree.get_children():
            values = self.cart_tree.item(item)['values']
            quantity = int(values[1])
            price_per_item = float(values[2].replace('$', ''))
            total += price_per_item * quantity
        
        self.total_label.config(text=f"Total: ${total:.2f}")
        return int(float(total))

    def clear_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        self.update_total()

    def delete_account(self):
        global current_user

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete your account? This action cannot be undone. Your data will be deleted in 30 days")
        # arbitary number of 30 days

        if confirm:
            try:
                databaseHandler.executeSQL(f"UPDATE Account SET Is_Active = false WHERE Account_ID = '{current_user[0]}'")
                messagebox.showinfo("Success", "Account deleted successfully!")
                self.root.destroy()
                LoginWindow()
            except:
                messagebox.showerror("Error", "Failed to delete account")

    def update_profile(self, fields):
        global current_user

        for field in fields:
            curr_value = self.profile_entries[field].get()
            if curr_value.strip() != "":
                try:
                    if field == "First Name":
                        databaseHandler.executeSQL(f"UPDATE Account SET FirstName = '{curr_value}' WHERE Account_ID = '{current_user[0]}';")
                    elif field == "Last Name":
                        databaseHandler.executeSQL(f"UPDATE Account SET LastName = '{curr_value}' WHERE Account_ID = '{current_user[0]}';")
                    elif field == "Email":
                        databaseHandler.executeSQL(f"UPDATE Account SET Email = '{curr_value}' WHERE Account_ID = '{current_user[0]}';")
                    elif field == "Username":
                        databaseHandler.executeSQL(f"UPDATE Account SET Username = '{curr_value}' WHERE Account_ID = '{current_user[0]}';")
                    elif field == "Password":
                        databaseHandler.executeSQL(f"UPDATE Account SET Password = '{curr_value}' WHERE Account_ID = '{current_user[0]}';")
                except:
                    messagebox.showerror("Error", f"Failed to update {field}")
                    return
            self.profile_entries[field].delete(0, tk.END)
        messagebox.showinfo("Success", "Profile updated successfully!")
                

def main():
    app = LoginWindow()
    app.root.mainloop()

if __name__ == "__main__":
    main()