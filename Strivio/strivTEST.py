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
                        client_id INTEGER,
                        origin_port_id INTEGER,
                        destination_port_id INTEGER,
                        status TEXT,
                        FOREIGN KEY(client_id) REFERENCES clients(id),
                        FOREIGN KEY(origin_port_id) REFERENCES ports(id),
                        FOREIGN KEY(destination_port_id) REFERENCES ports(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY,
                        client_name TEXT,
                        contact_info TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS ports (
                        id INTEGER PRIMARY KEY,
                        port_name TEXT,
                        location TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS delivery_locations (
                        id INTEGER PRIMARY KEY,
                        client_id INTEGER,
                        location_name TEXT,
                        address TEXT,
                        FOREIGN KEY(client_id) REFERENCES clients(id))''')
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
        # Notebook for Tabs
        self.tabControl = ttk.Notebook(self.root)
        self.shipment_tab = ttk.Frame(self.tabControl)
        self.client_tab = ttk.Frame(self.tabControl)
        self.port_tab = ttk.Frame(self.tabControl)
        self.delivery_location_tab = ttk.Frame(self.tabControl)

        # Adding tabs to the notebook
        self.tabControl.add(self.shipment_tab, text='Shipments')
        self.tabControl.add(self.client_tab, text='Clients')
        self.tabControl.add(self.port_tab, text='Ports')
        self.tabControl.add(self.delivery_location_tab, text='Delivery Locations')
        self.tabControl.pack(expand=1, fill="both")

        # Initialize individual tab contents
        self.initialize_shipment_tab()
        self.initialize_client_tab()
        self.initialize_port_tab()
        self.initialize_delivery_location_tab()

    ########### SHIPMENT TAB ###########
    def initialize_shipment_tab(self):
        # Treeview for Shipments List
        self.shipment_tree = ttk.Treeview(self.shipment_tab, columns=("ID", "Shipment Number", "Client", "Origin", "Destination", "Status"), show="headings")
        self.shipment_tree.heading("ID", text="ID")
        self.shipment_tree.heading("Shipment Number", text="Shipment Number")
        self.shipment_tree.heading("Client", text="Client")
        self.shipment_tree.heading("Origin", text="Origin")
        self.shipment_tree.heading("Destination", text="Destination")
        self.shipment_tree.heading("Status", text="Status")
        self.shipment_tree.pack(fill=tk.BOTH, expand=True)

        # Add and Load Buttons
        add_button = tk.Button(self.shipment_tab, text="Add Shipment", command=self.add_shipment)
        add_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Load shipments data from database
        self.load_shipments()

        # Bind the treeview click event to open shipment details
        self.shipment_tree.bind("<Double-1>", self.open_shipment_details)

    def load_shipments(self):
        self.shipment_tree.delete(*self.shipment_tree.get_children())  # Clear existing rows
        conn = sqlite3.connect('freight.db')
        cursor = conn.cursor()
        
        # Check if the shipments table has the client_id column
        cursor.execute("PRAGMA table_info(shipments)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'client_id' not in columns:
            raise ValueError("Column 'client_id' does not exist in the 'shipments' table.")
        
        cursor.execute('''SELECT shipments.id, shipments.shipment_number, clients.client_name, 
                                ports1.port_name AS origin_port, ports2.port_name AS destination_port, 
                                shipments.status
                        FROM shipments
                        LEFT JOIN clients ON shipments.client_id = clients.id
                        LEFT JOIN ports AS ports1 ON shipments.origin_port_id = ports1.id
                        LEFT JOIN ports AS ports2 ON shipments.destination_port_id = ports2.id''')
        
        for row in cursor.fetchall():
            self.shipment_tree.insert('', tk.END, values=row)
        
        conn.close()

    def add_shipment(self):
        AddShipmentWindow(self)

    def open_shipment_details(self, event):
        item = self.shipment_tree.selection()[0]
        shipment_id = self.shipment_tree.item(item, "values")[0]
        ShipmentDetailWindow(self.root, shipment_id, self.load_shipments)

    ########### CLIENT TAB ###########
    def initialize_client_tab(self):
        # Treeview for Clients List
        self.client_tree = ttk.Treeview(self.client_tab, columns=("ID", "Client Name", "Contact Info"), show="headings")
        self.client_tree.heading("ID", text="ID")
        self.client_tree.heading("Client Name", text="Client Name")
        self.client_tree.heading("Contact Info", text="Contact Info")
        self.client_tree.pack(fill=tk.BOTH, expand=True)

        # Add and Load Buttons
        add_button = tk.Button(self.client_tab, text="Add Client", command=self.add_client)
        add_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Load clients data from database
        self.load_clients()

    def load_clients(self):
        self.client_tree.delete(*self.client_tree.get_children())  # Clear existing rows
        conn = sqlite3.connect('freight.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        for row in cursor.fetchall():
            self.client_tree.insert('', tk.END, values=row)
        conn.close()

    def add_client(self):
        # Add client logic goes here
        pass

    ########### PORT TAB ###########
    def initialize_port_tab(self):
        # Treeview for Ports List
        self.port_tree = ttk.Treeview(self.port_tab, columns=("ID", "Port Name", "Location"), show="headings")
        self.port_tree.heading("ID", text="ID")
        self.port_tree.heading("Port Name", text="Port Name")
        self.port_tree.heading("Location", text="Location")
        self.port_tree.pack(fill=tk.BOTH, expand=True)

        # Add and Load Buttons
        add_button = tk.Button(self.port_tab, text="Add Port", command=self.add_port)
        add_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Load ports data from database
        self.load_ports()

    def load_ports(self):
        self.port_tree.delete(*self.port_tree.get_children())  # Clear existing rows
        conn = sqlite3.connect('freight.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ports")
        for row in cursor.fetchall():
            self.port_tree.insert('', tk.END, values=row)
        conn.close()

    def add_port(self):
        # Add port logic goes here
        pass

    ########### DELIVERY LOCATION TAB ###########
    def initialize_delivery_location_tab(self):
        # Treeview for Delivery Locations List
        self.delivery_location_tree = ttk.Treeview(self.delivery_location_tab, columns=("ID", "Client", "Location Name", "Address"), show="headings")
        self.delivery_location_tree.heading("ID", text="ID")
        self.delivery_location_tree.heading("Client", text="Client")
        self.delivery_location_tree.heading("Location Name", text="Location Name")
        self.delivery_location_tree.heading("Address", text="Address")
        self.delivery_location_tree.pack(fill=tk.BOTH, expand=True)

        # Add and Load Buttons
        add_button = tk.Button(self.delivery_location_tab, text="Add Delivery Location", command=self.add_delivery_location)
        add_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Load delivery locations data from database
        self.load_delivery_locations()

    def load_delivery_locations(self):
        self.delivery_location_tree.delete(*self.delivery_location_tree.get_children())  # Clear existing rows
        conn = sqlite3.connect('freight.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT delivery_locations.id, clients.client_name, delivery_locations.location_name, delivery_locations.address
                          FROM delivery_locations
                          LEFT JOIN clients ON delivery_locations.client_id = clients.id''')
        for row in cursor.fetchall():
            self.delivery_location_tree.insert('', tk.END, values=row)
        conn.close()

    def add_delivery_location(self):
        # Add delivery location logic goes here
        pass

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

        tk.Label(self.window, text="Client:").pack()
        self.client_dropdown = ttk.Combobox(self.window, values=self.get_clients())
        self.client_dropdown.pack()

        tk.Label(self.window, text="Origin Port:").pack()
        self.origin_dropdown = ttk.Combobox(self.window, values=self.get_ports())
        self.origin_dropdown.pack()

        tk.Label(self.window, text="Destination Port:").pack()
        self.destination_dropdown = ttk.Combobox(self.window, values=self.get_ports())
        self.destination_dropdown.pack()

        tk.Label(self.window, text="Status:").pack()
        self.status = tk.Entry(self.window)
        self.status.pack()

        # Save Button
        save_button = tk.Button(self.window, text="Save", command=self.save_shipment)
        save_button.pack()

    def get_clients(self):
        conn = sqlite3.connect('freight.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, client_name FROM clients")
        clients = [f"{row[0]}: {row[1]}" for row in cursor.fetchall()]
        conn.close()
        return clients

    def get_ports(self):
        conn = sqlite3.connect('freight.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, port_name FROM ports")
        ports = [f"{row[0]}: {row[1]}" for row in cursor.fetchall()]
        conn.close()
        return ports

    def save_shipment(self):
        client_id = self.client_dropdown.get().split(":")[0]
        origin_port_id = self.origin_dropdown.get().split(":")[0]
        destination_port_id = self.destination_dropdown.get().split(":")[0]

        conn = sqlite3.connect('freight.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO shipments (shipment_number, client_id, origin_port_id, destination_port_id, status) VALUES (?, ?, ?, ?, ?)', 
                       (self.shipment_number.get(), client_id, origin_port_id, destination_port_id, self.status.get()))
        conn.commit()
        conn.close()
        self.parent_app.load_shipments()  # Refresh the list of shipments
        self.window.destroy()

# Shipment Detail Window
class ShipmentDetailWindow:
    def __init__(self, parent, shipment_id, refresh_callback):
        self.refresh_callback = refresh_callback
        self.shipment_id = shipment_id
        self.window = tk.Toplevel(parent)
        self.window.title(f"Shipment {shipment_id} Details")

        self.window.geometry("800x600+100+100")  # Adjust the size of the window

        # Create Tabs
        self.tabControl = ttk.Notebook(self.window)
        self.info_tab = ttk.Frame(self.tabControl)
        self.arrival_tab = ttk.Frame(self.tabControl)
        self.delivery_tab = ttk.Frame(self.tabControl)
        self.overview_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.info_tab, text='Info')
        self.tabControl.add(self.arrival_tab, text='Arrival')
        self.tabControl.add(self.delivery_tab, text='Delivery')
        self.tabControl.add(self.overview_tab, text='Overview')
        self.tabControl.pack(expand=1, fill="both")

        # Load Data into Tabs
        self.load_info_tab()
        self.load_arrival_tab()
        self.load_delivery_tab()
        self.load_overview_tab()

        # Delete Button
        delete_button = tk.Button(self.window, text="Delete Shipment", command=self.delete_shipment)
        delete_button.pack(side=tk.BOTTOM, pady=10)

    def load_overview_tab(self):
        # Load and display consolidated information
        tk.Label(self.overview_tab, text="Overview of Shipment Details", font=("Arial", 12)).pack()
        # Fetch data from the database and display in read-only format
        pass

    def load_info_tab(self):
        # Load shipment info and display in the Info tab
        conn = sqlite3.connect('freight.db')
        cursor = conn.cursor()
        cursor.execute("SELECT shipment_number, origin_port_id, destination_port_id, status FROM shipments WHERE id=?", (self.shipment_id,))
        shipment = cursor.fetchone()
        conn.close()

        tk.Label(self.info_tab, text="Shipment Number:").pack()
        self.shipment_number_entry = tk.Entry(self.info_tab)
        self.shipment_number_entry.insert(0, shipment[0])
        self.shipment_number_entry.pack()

        # Additional fields for origin and destination dropdowns can be added in a similar manner.
        # Example:
        # tk.Label(self.info_tab, text="Origin Port:").pack()
        # self.origin_port_entry = tk.Entry(self.info_tab)
        # self.origin_port_entry.insert(0, shipment[1])
        # self.origin_port_entry.pack()

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
        cursor.execute("UPDATE shipments SET shipment_number=?, origin_port_id=?, destination_port_id=?, status=? WHERE id=?",
                       (self.shipment_number_entry.get(), self.origin_port_entry.get(), self.destination_port_entry.get(), 
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
