import sqlite3 as sql

def createDB(DBName):
    con=sql.connect(f'{DBName}')
    cur=con.cursor()
    cur.execute("CREATE TABLE main(ID INTEGER PRIMARY KEY AUTOINCREMENT, service VARCHAR(255),loginID VARCHAR(255),loginPass VARCHAR(255))")
    con.commit()
    return 0

def accessDB(DBName):
    try:
        con=sql.connect(f'{DBName}')
        return con
    except:
        return f"Database {DBName} not found."

def createGroup(groupName,connection):
    cursor=connection.cursor()
    cursor.execute(f"CREATE TABLE {groupName}(ID INTEGER PRIMARY KEY AUTOINCREMENT, service VARCHAR(255), loginID VARCHAR(255), loginPass VARCHAR(255))")
    connection.commit()
    return 0

def viewGroup(groupName, connection):
    cursor=connection.cursor()
    res=cursor.execute(f"SELECT * FROM {groupName}")
    return res.fetchall()

def deleteGroup(groupName, connection):
    cursor=connection.cursor()
    try:
        cursor.execute(f"DROP TABLE {groupName}")
        connection.commit()
        return 0
    except:
        return f"Table {groupName} not found."

def createEntry(groupName, service, loginID, loginPass, connection):
    cursor=connection.cursor()
    cursor.execute(f"INSERT INTO {groupName} (service, loginID, loginPass) VALUES (?, ?, ?)",(service,loginID,loginPass))
    connection.commit()
    return 0

def viewEntry(groupName, service, connection):
    cursor=connection.cursor()
    res=cursor.execute(f"SELECT * FROM {groupName} WHERE service=?",(service,))
    return res.fetchone()

def updateEntry(groupName, service, loginID, loginPass,ID, connection):
    cursor=connection.cursor()
    cursor.execute(f"UPDATE {groupName} SET service=?, loginID=?, loginPass=? WHERE ID=?",(service, loginID, loginPass,ID))
    connection.commit()
    return 0

def deleteEntry(ID,groupName, connection):
    cursor=connection.cursor()
    cursor.execute(f"DELETE FROM {groupName} WHERE ID=?",(ID,))
    connection.commit()
    return 0

# --- TUI (TEXT-BASED USER INTERFACE) ---

def print_menu(db_name):
    """Prints the main menu options."""
    print("\n--- 🔐 DB Test TUI (Working Code) ---")
    if db_name:
        print(f"Connected to: {db_name}.db")
    else:
        print("Not connected to any database.")
    print("---------------------------------")
    print("1. Create Database (Initial Setup)")
    print("2. Access Database")
    print("--- (Must be connected) ---")
    print("3. Create Group (Table)")
    print("4. View Group (Table)")
    print("5. Delete Group (Table)")
    print("6. Create Entry")
    print("7. View Entry")
    print("8. Update Entry")
    print("9. Delete Entry")
    print("10. Exit")
    print("---------------------------------")

def main():
    """Main application loop."""
    con = None
    db_name = ""

    while True:
        print_menu(db_name)
        choice = input("Enter your choice (1-10): ")

        # --- Connection and Exit ---
        if choice == '1':
            try:
                db_name_input = input("Enter new database name: ")
                createDB(f'{db_name_input}.db')
                print(f"Ran createDB for '{db_name_input}.db'.")
                print("Note: You must now use Option 2 to connect.")
            except Exception as e:
                print(f"\n---!!! ERROR !!!---")
                print(f"Error details: {e}")
                print("-------------------")

        elif choice == '2':
            try:
                db_name_input = input("Enter database name to access: ")
                con = accessDB(f'{db_name_input}.db')
                if isinstance(con, str):
                    print(con) # Print "Database not found"
                    con = None
                else:
                    db_name = db_name_input
                    print(f"Successfully connected to {db_name}.db.")
            except Exception as e:
                print(f"\n---!!! ERROR !!!---")
                print(f"Error details: {e}")
                con = None
                
        elif choice == '10':
            if con:
                con.close()
                print("Connection closed.")
            print("Exiting.")
            sys.exit()

        # --- Operations requiring a connection ---
        elif not con:
            print("\n*** Please create (1) or access (2) a database first. ***")
            continue

        # --- Other operations (wrapped in try/except) ---
        try:
            if choice == '3':
                group = input("Enter new group name: ")
                createGroup(group, con)
                print(f"Group '{group}' created.")

            elif choice == '4':
                group = input("Enter group name to view: ")
                entries = viewGroup(group, con)
                if not entries:
                    print(f"Group '{group}' is empty or doesn't exist.")
                else:
                    print(f"\n--- Entries in {group} ---")
                    print("(ID, Service, Login, Password)")
                    for entry in entries:
                        print(entry)
            
            elif choice == '5':
                group = input("Enter group name to delete: ")
                result = deleteGroup(group, con)
                if result == 0:
                    print(f"Group '{group}' deleted.")
                else:
                    print(result) # Print error message

            elif choice == '6':
                group = input("Enter group name: ")
                service = input("Enter service name: ")
                login = input("Enter login ID: ")
                passwd = input("Enter password: ")
                createEntry(group, service, login, passwd, con)
                print("Entry created successfully!")

            elif choice == '7':
                group = input("Enter group name: ")
                service = input("Enter service name to view: ")
                entry = viewEntry(group, service, con)
                print(entry if entry else "Entry not found.")

            elif choice == '8':
                group = input("Enter group name: ")
                try:
                    entry_id = int(input("Enter ID of entry to update: "))
                except ValueError:
                    print("Invalid ID. Must be a number.")
                    continue
                service = input("Enter NEW service name: ")
                login = input("Enter NEW login ID: ")
                passwd = input("Enter NEW password: ")
                updateEntry(group, service, login, passwd, entry_id, con)
                print(f"Entry {entry_id} updated.")

            elif choice == '9':
                group = input("Enter group name: ")
                try:
                    entry_id = int(input("Enter ID of entry to delete: "))
                except ValueError:
                    print("Invalid ID. Must be a number.")
                    continue
                deleteEntry(entry_id, group, con)
                print(f"Entry {entry_id} deleted.")
                
            elif choice not in ('1', '2', '10'):
                print("Invalid choice. Please enter a number from 1 to 10.")

        except Exception as e:
            print(f"\n---!!! AN ERROR OCCURRED !!!---")
            print(f"Error details: {e}")
            print("(e.g., table not found, etc.)")
            print("---------------------------------")


if __name__ == "__main__":
    main()
