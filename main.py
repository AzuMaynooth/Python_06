'''
WAREHOUSE WITH A TXT DB

In this exercise, you'll extend the functionality of the company account and warehouse operations program from the previous lesson.
You'll implement saving and loading of account balance, warehouse inventory, and operation history to/from a text file.

1. You can store balance, inventory and history in separate files or in one file.

2. At the start of the program, if the file(s) exists, load the data from the file and use it to initialize the program state.
  - If the file does not exist or if there are any errors during file reading (e.g., the file is corrupted or not readable), handle these cases gracefully.
  - Make sure to save all the data to correct files when the program is being shutdown.

Hints:

- Use built-in Python functions for file I/O and converting data to Python objects (i.e. literal_eval).
- Remember to handle any file I/O errors that may occur.
- Think about the format in which you'll save the data to the file. The format should be easy to read back into the program.
- Always close the files after you're done with them to free up system resources.

'''


import os
import time
import csv

class File:
    def __init__(self, date, n_package, weight):
        self.date = date
        self.n_package = n_package
        self.weight = weight

    def __str__(self):
        return f"{self.date}, {self.n_package}, {self.weight}"

class Balance(File):
    def __init__(self, date, n_package, weight, amount):
        super().__init__(date, n_package, weight)
        self.amount = amount

    def __str__(self):
        return f"{super().__str__()}, {self.amount}"

class Inventory(File):
    def __init__(self, date, n_package, weight, amount):
        super().__init__(date, n_package, weight)
        self.amount = amount

    def __str__(self):
        return f"{super().__str__()}, {self.amount}"

# Directories nad files
directory = os.getcwd()
balance_file =  directory + '\Balance.txt'
inventory_file = directory + '\Inventory.txt'
history_file = directory + '\History.txt'


# Load date from file
def load_data_from_file(file_name):
    data = []
    if os.path.exists(file_name):
        try:
            with open(file_name, 'r', newline='') as f:
                reader = csv.reader(f)
                next(reader)  # jump header
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Error loading file {file_name}: {e}")
    return data



# Save data in file
def save_data_to_file(file_name, data, header):
    try:
        with open(file_name, 'a', newline='') as f:
            writer = csv.writer(f)
            if not os.path.exists(file_name) or os.path.getsize(file_name) == 0:
                writer.writerow(header)
            for row in data:
                writer.writerow(row)
    except Exception as e:
        print(f"Error saving data in file {file_name}: {e}")



# Load existing data from files
balance_data = load_data_from_file(balance_file)
inventory_data = load_data_from_file(inventory_file)
history_data = load_data_from_file(history_file)

# Initilice lists from loaded data
balance_lst = [Balance(*data) for data in balance_data]
inventory_lst = [Inventory(*data) for data in inventory_data]

# Records on historical
def add_to_history(operation, date):
    history_data.append([date, operation])
    save_data_to_file(history_file, history_data, ["Date", "Operation"])


# Show balance
def show_balance():
    try:
        total_balance = sum([float(item.amount) for item in balance_lst])
        print(f"Total balance: {total_balance}€")
    except ValueError:
        print("Error calculating balance.")


# Purchase function
def purchase_item():
    print("\n--- Purchasing item ---")
    try:
        item_weight = abs(round(float(input("Add weight (kg): ")), 2))
        item_amount = abs(round(float(input("Add amount (€): ")), 2))
        curr_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())

        item = Balance(curr_time, len(balance_lst) + 1, item_weight, item_amount)  # Add new balance
        balance_lst.append(item)
        inventory_lst.append(item)

        # Save data in file
        save_data_to_file(balance_file, [(item.date, item.n_package, item.weight, item.amount)],
                          ["Date", "Package Number", "Weight", "Amount"])
        save_data_to_file(inventory_file, [(item.date, item.n_package, item.weight, item.amount)],
                          ["Date", "Package Number", "Weight", "Amount"])

        # Record the operation in history
        add_to_history("Purchase made ", curr_time)
        print(f"Purchase made: {item.amount}€ by {item.weight}kg")
    except ValueError:
        print("Incorrect value.")


# Sale function
def sale_item():
    print("\n--- Making sale ---")
    try:
        item_weight = abs(round(float(input("Add weight (kg): ")), 2))
        item_amount = abs(round(float(input("Add amount (€): ")), 2))
        curr_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())

        item = Balance(curr_time, len(balance_lst) + 1, item_weight, -item_amount)  # sale (negative amount)
        balance_lst.append(item)
        inventory_lst.append(item)

        # Save data in file
        save_data_to_file(balance_file, [(item.date, item.n_package, item.weight, item.amount)],
                          ["Date", "Package Number", "Weight", "Amount"])
        save_data_to_file(inventory_file, [(item.date, item.n_package, item.weight, item.amount)],
                          ["Date", "Package Number", "Weight", "Amount"])

        # Record the operation in history
        add_to_history("Venta realizada", curr_time)
        print(f"Sale made: {item.amount}€ by {item.weight}kg")
    except ValueError:
        print("Incorrect value. You must enter valid numbers.")


# display inventory
def show_inventory():
    print("\n--- Current inventory ---")
    for item in inventory_lst:
        print(item)


# User options menu
def main_menu():
    print("\n--- Menú de operaciones ---\n" +
          "1. Make purchase\n" +
          "2. Make sale\n" +
          "3. See balance\n" +
          "4. View inventory\n" +
          "5. Exit\n")



    while True:
        print("\n--- Menú de operaciones ---\n" +
              "1. Make purchase\n" +
              "2. Make sale\n" +
              "3. See balance\n" +
              "4. View inventory\n" +
              "5. Exit\n")
        try:
            option = int(input("\nChoose one option: "))

            if option == 1:
                purchase_item()
            elif option == 2:
                sale_item()
            elif option == 3:
                show_balance()
            elif option == 4:
                show_inventory()
            elif option == 5:
                print("Thank you for using the system.")
                # Save all data before exit
                save_data_to_file(balance_file,
                                  [(item.date, item.n_package, item.weight, item.amount) for item in balance_lst],
                                  ["Date", "Package Number", "Weight", "Amount"])
                save_data_to_file(inventory_file,
                                  [(item.date, item.n_package, item.weight, item.amount) for item in inventory_lst],
                                  ["Date", "Package Number", "Weight", "Amount"])
                save_data_to_file(history_file, history_data, ["Date", "Operation"])
                exit()
            else:
                print("Invalid option. Try again.")
        except ValueError:
            print("Please enter a valid number.")


# Iniciar el programa
if __name__ == "__main__":
    print("------------ Welcome to warehouse accounting system -------------------------")
    main_menu()