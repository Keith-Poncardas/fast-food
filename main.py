# Program Title: Untitled
# Author / Programmer: Mariel B. Perin
# Language Used: Python, Structured Query Language lite
# Date Launched: September 24, 2024

# Mas compact ang SQLITE compared sa SQL, kasi serverless sya saka bagay sya for embbedded systems and local storage use kagaya nitong project mo
# though they are highly related, kaibahan lang serverless sya, same syntax lng silang dalawa.
# Built in narin ung SQLite sa python library, u don't need to install separate modules for that.

# Instruction kung papano iinstall ung pretty table:
# Copy mo to maayeys  (pip install prettytable) remove the parentheses then ipaste mo sa CMD mo o ung terminal then reload mo ung code editor mo done!

import sqlite3
from prettytable import PrettyTable

# Dito yung mismong connection ng database mo mayeys (gagawa sya ng panibagong database kapag hindi ito nag exist)
def connect_db():
    # Kapag hindi itong file na ito hindi sya nag exist, gagawa sya ng panibagong database file.
    return sqlite3.connect('fast_food_db.sqlite')


# Gagawa sya ng table sa database kapag hindi nag exist ung pinaka file mo.
def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS fastfoodchains (
                      ChainID INTEGER PRIMARY KEY AUTOINCREMENT,
                      ChainName TEXT,
                      Owner TEXT,
                      SignatureFood TEXT)''')
    conn.commit()
    conn.close()


# Ito ung function na mag aadd ka ng fastfood chain, kung ano man un HAHA
def create_fastfood(chain_name, owner, signature_food):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO fastfoodchains (ChainName, Owner, SignatureFood) VALUES (?, ?, ?)"
    cursor.execute(query, (chain_name, owner, signature_food))
    conn.commit()
    cursor.close()
    conn.close()
    print("Fast food chain added successfully.")


# Ito naman ung ididisplay nya ung lahat ng mga fast food chains na nilagay mo.
def display_fastfoods():
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM fastfoodchains"
    cursor.execute(query)
    results = cursor.fetchall()

    # Dito na ma gegenerate ung pretty table mo na module, pansin mo walang hard code na loops.
    if results:
        table = PrettyTable(["Chain ID", "Chain Name", "Owner", "Signature Food"])
        for row in results:
            table.add_row(row)
        print(table)
    else:
        print("No fast food chains available.")

    cursor.close()
    conn.close()

# Ito ung function na pwede mo iupdate ung fastfood base sa ID na need sa parameter (chain_id).
def update_fastfood(chain_id):
    conn = connect_db()
    cursor = conn.cursor()

    while True:
        print("\nWhich field do you want to edit?")
        print("1. Chain Name")
        print("2. Owner")
        print("3. Signature Food")
        print("4. Back to Menu")

        try:
            option = int(input("Choose an option (1-4): "))
            if option < 1 or option > 4:
                print("Invalid option. Please try again.")
                continue

            if option == 1:
                chain_name = input("Enter new fast food chain name: ")
                query = "UPDATE fastfoodchains SET ChainName = ? WHERE ChainID = ?"
                cursor.execute(query, (chain_name, chain_id))
                conn.commit()
                print("Chain name updated successfully.")

            elif option == 2:
                owner = input("Enter new owner name: ")
                query = "UPDATE fastfoodchains SET Owner = ? WHERE ChainID = ?"
                cursor.execute(query, (owner, chain_id))
                conn.commit()
                print("Owner updated successfully.")

            elif option == 3:
                signature_food = input("Enter new signature food: ")
                query = "UPDATE fastfoodchains SET SignatureFood = ? WHERE ChainID = ?"
                cursor.execute(query, (signature_food, chain_id))
                conn.commit()
                print("Signature food updated successfully.")

            elif option == 4:
                print("Done editing.")
                break

        except ValueError:
            print("Invalid input. Please try again.")
            continue

    cursor.close()
    conn.close()


# Kapag naman mag dedelete ka sa fast food layunin un ng function na ito.
def delete_fastfood(chain_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = "DELETE FROM fastfoodchains WHERE ChainID = ?"
    cursor.execute(query, (chain_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print("Fast food chain deleted successfully")

# Ito ung bibilangin nya kung ilan ung rows ng table mo (makikita mo un kapag mag display entry ka)
def countRows():
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM fastfoodchains"
    cursor.execute(query)
    result = cursor.fetchone()
    row_count = result[0]
    cursor.close()
    conn.close()
    return row_count


# Syempreee bannerrr 🤩
def banner(text, width=60, char='*'):
    print(f"\n{char * width}")
    print(text.center(width))
    print(f"{char * width}")


# Ito ung main menu mayeys, pinaka puso ito ng program mo, dapat laging naka initialized ito sa pinaka end.
def menu():
    initialize_db()  # Ensure the table exists
    while True:
        banner("FAST FOOD CHAINS", 60)

        print(f"{' ' * 18}1. ADD ENTRY")
        print(f"{' ' * 18}2. DELETE ENTRY")
        print(f"{' ' * 18}3. EDIT ENTRY")
        print(f"{' ' * 18}4. DISPLAY ENTRY")
        print(f"{' ' * 18}5. EXIT")

        try:
            option = int(input("\nChoose an option (1-5): "))
            if option < 1 or option > 5:
                print("Invalid option. Please try again.")
                continue

            if option == 1:
                banner("ADD AN ENTRY", 60)
                chain_name = input("Enter fast food chain name: ")
                owner = input("Enter owner name: ")
                signature_food = input("Enter signature food: ")
                create_fastfood(chain_name, owner, signature_food)

            elif option == 2:
                banner("DELETE AN ENTRY", 60)
                if countRows() == 0:
                    print("No fast food chain to delete.")
                else:
                    display_fastfoods()
                    chain_id = int(input("Enter fast food chain ID to delete: "))
                    delete_fastfood(chain_id)

            elif option == 3:
                banner("EDIT AN ENTRY", 60)
                if countRows() == 0:
                    print("No fast food chain to update.")
                else:
                    display_fastfoods()
                    chain_id = int(input("Enter fast food chain ID to update: "))
                    update_fastfood(chain_id)

            elif option == 4:
                banner("DISPLAY AN ENTRY", 60)
                if countRows() == 0:
                    print("No fast food chains to display.")
                else:
                    display_fastfoods()

            elif option == 5:
                print("Exiting program.")
                break

        except ValueError:
            print("Invalid input. Please try again.")
            continue


# wag kalimutang i-initialize (menu) kasi ndi sya mag ru-run.
menu()
