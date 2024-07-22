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

directory = os.getcwd()
balance_file =  directory + '\Balance.txt'
inventory_file = directory + '\Inventory.txt'
history_file = directory + '\History.txt'


global balance_lst
global inventory_lst
global history_lst

packages = []
item_index = 0
packages_index = 0
package_weight = 0
inventory_lst = []



if os.path.exists(balance_file) or os.path.exists(inventory_file) or os.path.exists(history_file):
    print('The file exists!')
else:
    # Create CSV files with headers
    with open(balance_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Package Number", "Weight", "Amount"])
    with open(inventory_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Package Number", "Weight", "Amount"])
    with open(history_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Operation"])

print("------------ Welcome to package system -------------------------")

n_items = None
packages = []

while n_items is None:
    try:
        n_items = abs(int(input("Add number of items to be sent: ")))
    except ValueError:
        print("Wrong item weight. Please add numeric value.")

    if n_items == "Exit":
        print("Thanks for using us!")
        exit()

    else:

        while item_index < n_items:

            try:

                item_weight = abs(round(float(input("Please add item weight: ")), 2))

                if item_weight == 0:
                    print("Not more items to send\n")
                    item_index = n_items

                elif 1 <= item_weight <= 10:

                    if package_weight + item_weight <= 20:

                        print("Item number " + str(item_index + 1) + " added to current package")
                        package_weight = package_weight + item_weight
                        packages.append(package_weight)
                        curr_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
                        print(curr_time)
                        item = Balance(curr_time, item_index, packages_index, item_weight)
                        inventory_lst.append(item)


                        # Save data to CSV file
                        with open(balance_file, 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow([curr_time, item_index, packages_index, item_weight])

                        item = Balance(curr_time, item_index, packages_index, item_weight)
                        inventory_lst.append(item)

                    else:

                        print("\n"
                                  "-------------------------------------------------------------------------------------\n"
                                  "Previous package has been sent\n"
                                  "-------------------------------------------------------------------------------------\n"
                                  "Initializing new package")
                        packages.append(0)
                        packages_index += 1
                        package_weight = item_weight
                        packages[packages_index] = package_weight
                else:
                    print("Your item weight is larger than 10kg.\n"
                              "It can't be sent")

                item_index += 1

            except ValueError:
                print("Wrong item weight. Please add numeric value.")



print("\n--------------------------------------------------- Generating inventory information ---------------------------------------------------------------------------------------------\n")

curr_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())

total_weight = sum(packages)
max_weight = len(packages) * 20
unused_capacity = max_weight - total_weight

lighter_package_weight = min(packages)
lighter_package_index = packages.index(lighter_package_weight)


print('Number of packages sent: {0}. \n'
        'Total weight of packages sent: {1}kg \n'
        'Total unused capacity: {2}kg \n'
        'The lighter package number: {3} \n'
        'Unused capacity from lighter package: {4}kg'.format(len(packages), total_weight, unused_capacity,
                                                             lighter_package_index + 1, 20 - lighter_package_weight))