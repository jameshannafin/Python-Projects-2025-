import sqlite3

def clear_database():
    conn = sqlite3.connect('freight.db')
    cursor = conn.cursor()
    
    # Delete all rows from each table
    cursor.execute('DELETE FROM shipments')
    cursor.execute('DELETE FROM clients')
    cursor.execute('DELETE FROM ports')
    cursor.execute('DELETE FROM delivery_locations')
    cursor.execute('DELETE FROM arrival')
    cursor.execute('DELETE FROM delivery')
    
    conn.commit()
    conn.close()

# Call this function to clear the database
clear_database()
