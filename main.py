import tkinter as tk
import sqlite3

con = sqlite3.connect("database.db")
cursor = con.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        code STRING PRIMARY KEY,
        description STRING,
        price STRING,
        quantity STRING
    )
""")
con.close()


program = tk.Tk()
program.title("Stock Management Tool")


# Function to add a new product
def add_product():
    def submit_product():
        code = productCodeEntry.get()
        desc = productDescriptionEntry.get("1.0", "end-1c")
        price = productPriceEntry.get()
        quantity = productQuantityEntry.get()

        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO products (code, description, price, quantity) VALUES (?,?,?,?)
        """, (code, desc, price, quantity))
        con.commit()
        con.close()

    window = tk.Tk()

    productCodeLbl = tk.Label(window, text="Product code:")
    productCodeLbl.pack()
    productCodeEntry = tk.Entry(window)
    productCodeEntry.pack()

    productDescriptionLbl = tk.Label(window, text="Product Description:")
    productDescriptionLbl.pack()
    productDescriptionEntry = tk.Text(window, height=10, padx=10)
    productDescriptionEntry.pack()

    productPriceLbl = tk.Label(window, text="Product Price:")
    productPriceLbl.pack()
    productPriceEntry = tk.Entry(window)
    productPriceEntry.pack()

    productQuantityLbl = tk.Label(window, text="Product Quantity:")
    productQuantityLbl.pack()
    productQuantityEntry = tk.Entry(window)
    productQuantityEntry.pack()

    submitBtn = tk.Button(window, text="Submit", command=submit_product)
    submitBtn.pack()

    window.mainloop()


# Function to handle editing/deleting a product
def edit_product(code):
    def update_product():
        desc = productDescriptionEntry.get("1.0", "end-1c")
        price = productPriceEntry.get()
        quantity = productQuantityEntry.get()

        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("""
            UPDATE products SET description=?, price=?, quantity=? WHERE code=?
        """, (desc, price, quantity, code))
        con.commit()
        con.close()
        edit_window.destroy()
        refresh_product_list()  # Refresh the main window after update

    def delete_product():
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("DELETE FROM products WHERE code=?", (code,))
        con.commit()
        con.close()
        edit_window.destroy()
        refresh_product_list()  # Refresh the main window after deletion

    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM products WHERE code=?", (code,))
    product_data = cursor.fetchone()
    con.close()

    edit_window = tk.Tk()
    edit_window.title(f"Edit Product {code}")

    # Product Description
    productDescriptionLbl = tk.Label(edit_window, text="Product Description:")
    productDescriptionLbl.pack()
    productDescriptionEntry = tk.Text(edit_window, height=10, padx=10)
    productDescriptionEntry.insert(tk.END, product_data[1])
    productDescriptionEntry.pack()

    # Product Price
    productPriceLbl = tk.Label(edit_window, text="Product Price:")
    productPriceLbl.pack()
    productPriceEntry = tk.Entry(edit_window)
    productPriceEntry.insert(tk.END, product_data[2])
    productPriceEntry.pack()

    # Product Quantity
    productQuantityLbl = tk.Label(edit_window, text="Product Quantity:")
    productQuantityLbl.pack()
    productQuantityEntry = tk.Entry(edit_window)
    productQuantityEntry.insert(tk.END, product_data[3])
    productQuantityEntry.pack()

    # Update and Delete Buttons
    updateBtn = tk.Button(edit_window, text="Update", command=update_product)
    updateBtn.pack()

    deleteBtn = tk.Button(edit_window, text="Delete", command=delete_product)
    deleteBtn.pack()

    edit_window.mainloop()


# Function to refresh the list of products in the main window
def refresh_product_list():
    # Clear the current frame
    for widget in frame.winfo_children():
        widget.destroy()

    headers = ["Code", "Description", "Price", "Quantity"]
    for col, header in enumerate(headers):
        tk.Label(frame, text=header, font=('Arial', 12, 'bold'), borderwidth=2, relief='ridge', width=15).grid(row=0, column=col)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    # Add each product as a clickable row
    for row_index, product in enumerate(products, start=1):
        for col_index, value in enumerate(product):
            label = tk.Label(frame, text=value)
            label.grid(row=row_index, column=col_index)
            label.bind("<Button-1>", lambda e, code=product[0]: edit_product(code))  # Binding click event

# Add product button
addProductBtn = tk.Button(program, text="Add a new product", command=add_product)
addProductBtn.pack()

# Display current stock
currentStockLabel = tk.Label(program, text="Current items in stock:", font=("Ariel", 15))
currentStockLabel.pack()

# Frame for the product list
frame = tk.Frame(program)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# Load and display the products
refresh_product_list()

program.mainloop()

