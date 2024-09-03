import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Setup Database
def setup_database():
    conn = sqlite3.connect('freight.db')
    cursor = conn.cursor()
    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS shipments (
                        id INTEGER PRIMARY KEY,
                        shipment_number TEXT,
                        origin TEXT,
                        destination TEXT,
                        status TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS arrival (
                        shipment_id INTEGER,
                        arrival_time TEXT,
                        arrival_location TEXT,
                        FOREIGN KEY(shipment_id) REFERENCES shipments(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS delivery (
                        shipment_id INTEGER,
                        delivery_time TEXT,
                        delivery_status TEXT,
                        FOREIGN KEY(shipment_id) REFERENCES shipments(id))''')
    conn.commit()
    conn.close()

# Main Application
class FreightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Freight Management")
        self.create_home_page()

    def create_home_page(self):
        # Treeview for Shipments List
        self.tree = ttk.Treeview(self.root, columns=("ID", "Shipment Number", "Origin", "Destination", "Status"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Shipment Number", text="Shipment Number")
        self.tree.heading("Origin", text="Origin")
        self.tree.heading("Destination", text="Destination")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Add and Load Buttons
        add_button = tk.Button(self.root, text="Add Shipment", command=self.add_shipment)
        add_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Load shipments data from database
        self.load_shipments()

        # Bind the treeview click event to open shipment details
        self.tree.bind("<Double-1>", self.open_shipment_details)

    def load_shipments(self):
        self.tree.delete(*self.tree.get_children())  # Clear existing rows
        conn = sqlite3.connect('freight.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM shipments")
        for row in cursor.fetchall():
            self.tree.insert('', tk.END, values=row)
        conn.close()

    def add_shipment(self):
        AddShipmentWindow(self)

    def open_shipment_details(self, event):
        item = self.tree.selection()[0]
        shipment_id = self.tree.item(item, "values")[0]
        ShipmentDetailWindow(self.root, shipment_id, self.load_shipments)

# Add Shipment Window
class AddShipmentWindow:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.window = tk.Toplevel(parent_app.root)
        self.window.title("Add New Shipment")

        # Input fields for the new shipment
        tk.Label(self.window, text="Shipment Number:").pack()
        self.shipment_number = tk.Entry(self.window)
        self.shipment_number.pack()

        tk.Label(self.window, text="Origin:").pack()
        self.origin = tk.Entry(self.window)
        self.origin.pack()

        tk.Label(self.window, text="Destination:").pack()
        self.destination = tk.Entry(self.window)
        self.destination.pack()

        tk.Label(self.window, text="Status:").pack()
        self.status = tk.Entry(self.window)
        self.status.pack()

        # Save Button
        save_button = tk.Button(self.window, text="Save", command=self.save_shipment)
        save_button.pack()

    def save_shipment(self):
        conn = sqlite3.connect('freight.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO shipments (shipment_number, origin, destination, status) VALUES (?, ?, ?, ?)', 
                       (self.shipment_number.get(), self.origin.get(), self.destination.get(), self.status.get()))
        conn.commit()
        conn.close()
        self.parent_app.load_shipments()  # Refresh the list of shipments
        self.window.destroy()

# Shipment Details Window
class ShipmentDetailWindow:
    def __init__(self, parent, shipment_id, refresh_callback):
        self.refresh_callback = refresh_callback
        self.shipment_id = shipment_id
        self.window = tk.Toplevel(parent)
        self.window.title(f"Shipment {shipment_id} Details")

        # Create Tabs
        self.tabControl = ttk.Notebook(self.window)
        self.info_tab = ttk.Frame(self.tabControl)
        self.arrival_tab = ttk.Frame(self.tabControl)
        self.delivery_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.info_tab, text='Info')
        self.tabControl.add(self.arrival_tab, text='Arrival')
        self.tabControl.add(self.delivery_tab, text='Delivery')
        self.tabControl.pack(expand=1, fill="both")

        # Load Data into Tabs
        self.load_info_tab()
        self.load_arrival_tab()
        self.load_delivery_tab()

        # Delete Button
        delete_button = tk.Button(self.window, text="Delete Shipment", command=self.delete_shipment)
        delete_button.pack(side=tk.BOTTOM, pady=10)

    def load_info_tab(self):
        # Load shipment info and display in the Info tab
        conn = sqlite3.connect('freight.db')
        cursor = conn.cursor()
        cursor.execute("SELECT shipment_number, origin, destination, status FROM shipments WHERE id=?", (self.shipment_id,))
        shipment = cursor.fetchone()
        conn.close()

        tk.Label(self.info_tab, text="Shipment Number:").pack()
        self.shipment_number_entry = tk.Entry(self.info_tab)
        self.shipment_number_entry.insert(0, shipment[0])
        self.shipment_number_entry.pack()

        tk.Label(self.info_tab, text="Origin:").pack()
        self.origin_entry = tk.Entry(self.info_tab)
        self.origin_entry.insert(0, shipment[1])
        self.origin_entry.pack()

        tk.Label(self.info_tab, text="Destination:").pack()
        self.destination_entry = tk.Entry(self.info_tab)
        self.destination_entry.insert(0, shipment[2])
        self.destination_entry.pack()

        tk.Label(self.info_tab, text="Status:").pack()
        self.status_entry = tk.Entry(self.info_tab)
        self.status_entry.insert(0, shipment[3])
        self.status_entry.pack()

        save_button = tk.Button(self.info_tab, text="Save Changes", command=self.save_info)
        save_button.pack()

    def load_arrival_tab(self):
        # Load arrival info and display in the Arrival tab
        pass

    def load_delivery_tab(self):
        # Load delivery info and display in the Delivery tab
        pass

    def save_info(self):
        # Update shipment information in the database
        conn = sqlite3.connect('freight.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE shipments SET shipment_number=?, origin=?, destination=?, status=? WHERE id=?",
                       (self.shipment_number_entry.get(), self.origin_entry.get(), self.destination_entry.get(), 
                        self.status_entry.get(), self.shipment_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Shipment details updated successfully!")

    def delete_shipment(self):
        # Confirm and delete the shipment
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this shipment?"):
            conn = sqlite3.connect('freight.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM shipments WHERE id=?", (self.shipment_id,))
            cursor.execute("DELETE FROM arrival WHERE shipment_id=?", (self.shipment_id,))
            cursor.execute("DELETE FROM delivery WHERE shipment_id=?", (self.shipment_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Shipment deleted successfully!")
            self.refresh_callback()  # Refresh the main list of shipments
            self.window.destroy()

if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    app = FreightApp(root)
    root.mainloop()
