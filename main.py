import os
import time
import csv

class File:
    def __init__(self, name, date, n_package, weight):
        self.name = name
        self.date = date
        self.n_package = n_package
        self.weight = weight

    def __str__(self):
        return f"{self.name},{self.date}, {self.n_package}, {self.weight}"

class Balance(File):
    def __init__(self, name, date, n_package, weight, price):
        super().__init__(name, date, n_package, weight)
        self.price = price

    def __str__(self):
        return f"{super().__str__()}, {self.price}"

class Inventory(File):
    def __init__(self, name, date, n_package, weight, price_per_unit):
        super().__init__(name, date, n_package, weight)
        self.price_per_unit = price_per_unit  # Guardamos el precio por unidad

    def __str__(self):
        return f"{super().__str__()}, {self.price_per_unit}"


# Directories and files
directory = os.getcwd()
balance_file = directory + '\Balance.txt'
inventory_file = directory + '\Inventory.txt'
history_file = directory + '\History.txt'

# Load data from file
def load_data_from_file(file_name):
    data = []
    if os.path.exists(file_name):
        try:
            with open(file_name, 'r', newline='') as f:
                reader = csv.reader(f)
                next(reader)  # skip header
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Error loading file {file_name}: {e}")
    return data

# Save data to file
def save_data_to_file(file_name, data, header):
    try:
        with open(file_name, 'w', newline='') as f:  # Cambiado 'a' por 'w' para sobrescribir el archivo
            writer = csv.writer(f)
            writer.writerow(header)
            for row in data:
                writer.writerow(row)
    except Exception as e:
        print(f"Error saving data in file {file_name}: {e}")

# Load existing data from files
balance_data = load_data_from_file(balance_file)
inventory_data = load_data_from_file(inventory_file)
history_data = load_data_from_file(history_file)


# Initialize lists from loaded data
balance_lst = [Balance(data[0], data[1], int(data[2]), float(data[3]), float(data[4])) for data in balance_data]
inventory_lst = [Inventory(data[0], data[1], int(data[2]), float(data[3]), float(data[4])) for data in inventory_data]

# Records on historical
def add_to_history(operation, date):
    history_data.append([date, operation])
    save_data_to_file(history_file, history_data, ["Date", "Operation"])

# Show balance
def show_balance():
    try:
        total_balance = sum([float(item.price) for item in balance_lst])
        print(f"Total balance: {total_balance}€")
    except ValueError:
        print("Error calculating balance.")

# Purchase function
def purchase_item():
    print("\n--- Purchasing item ---")
    try:
        # Solicitar datos de la compra
        item_name = str(input("Add item name: "))

        # Validar cantidad como entero positivo
        while True:
            try:
                quantity = abs(int(input("How many units/kg?: ")))
                if quantity > 0:
                    break
                else:
                    print("Quantity must be greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a valid number for quantity.")

        # Validar precio por unidad como flotante positivo
        while True:
            try:
                price_per_unit = abs(float(input("Add price per unit/kg (€): ")))
                if price_per_unit > 0:
                    break
                else:
                    print("Price per unit must be greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a valid number for price.")

        # Calcular el costo total
        total_cost = price_per_unit * quantity

        # Registrar la compra
        curr_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
        item_id = len(balance_lst) + 1

        # Registrar en el balance como gasto negativo
        balance_entry = Balance(item_name, curr_time, item_id, quantity, -total_cost)
        balance_lst.append(balance_entry)

        # Registrar en el inventario (guardando el precio por unidad correctamente)
        inventory_entry = Inventory(item_name, curr_time, item_id, quantity, price_per_unit)
        inventory_lst.append(inventory_entry)

        # Guardar cambios en los archivos
        save_data_to_file(balance_file, [(entry.name, entry.date, entry.n_package, entry.weight, entry.price) for entry in balance_lst],
                          ["Name", "Date", "Package Number", "Quantity", "Total Cost"])
        save_data_to_file(inventory_file, [(entry.name, entry.date, entry.n_package, entry.weight, entry.price_per_unit) for entry in inventory_lst],
                          ["Name", "Date", "Package Number", "Quantity", "Price per Unit"])

        # Registrar la operación en el historial
        add_to_history(f"Purchase: {item_name} (Quantity: {quantity}, Total Cost: {total_cost}€)", curr_time)

        # Confirmación al usuario
        print(f"Purchase completed: {item_name}, Quantity: {quantity}, Price per Unit: {price_per_unit}€, Total Cost: {total_cost}€")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Sale function
def sale_item():
    print("\n--- Making sale ---")
    try:
        while True:  # Bucle para seguir pidiendo el nombre del ítem hasta que se encuentre o se ingrese 'end'
            item_name = str(input("Enter the name of the item (or type 'back' to return to main menu): "))

            if item_name.lower() == 'back':
                return  # Si el usuario escribe 'back', vuelve al menú principal

            # Buscar el ítem en el inventario
            item = next((i for i in inventory_lst if i.name == item_name), None)

            if item is None:
                print(f"No items found in inventory with the name '{item_name}'. Please try again.")
                continue  # Si el ítem no se encuentra, sigue pidiendo el nombre
            else:
                break  # Si el ítem se encuentra, sale del bucle

        # Mostrar detalles del ítem
        available_quantity = sum(i.weight for i in inventory_lst if i.name == item_name)  # Sumar las cantidades del inventario
        price_per_unit = item.price_per_unit  # Precio por unidad del primer item encontrado
        print(f"Item found: {item_name}, Available: {available_quantity} units/kg, Price per unit: {price_per_unit}€")

        # Solicitar cantidad a vender
        while True:
            try:
                quantity_to_sell = abs(float(input(f"Enter quantity to sell (max {available_quantity}): ")))
                if quantity_to_sell > 0 and quantity_to_sell <= available_quantity:
                    break
                else:
                    print(f"Please enter a valid quantity (1 to {available_quantity}).")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        # Calcular el total de la venta
        total_sale = price_per_unit * quantity_to_sell

        # Registrar la venta como una nueva entrada en el inventario
        curr_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
        item_id = len(inventory_lst) + 1  # Nuevo ID de paquete
        inventory_entry = Inventory(item_name, curr_time, item_id, quantity_to_sell, price_per_unit)
        inventory_lst.append(inventory_entry)  # Añadir la venta al inventario

        # Registrar la venta en el balance como un ingreso (positivo)
        balance_entry = Balance(item_name, curr_time, item_id, quantity_to_sell, total_sale)  # Balance positivo
        balance_lst.append(balance_entry)

        # Guardar cambios en los archivos
        save_data_to_file(balance_file,
                          [(entry.name, entry.date, entry.n_package, entry.weight, entry.price) for entry in balance_lst],
                          ["Name", "Date", "Package Number", "Quantity", "Total Cost"])
        save_data_to_file(inventory_file,
                          [(entry.name, entry.date, entry.n_package, entry.weight, entry.price_per_unit) for entry in inventory_lst],
                          ["Name", "Date", "Package Number", "Quantity", "Price per Unit"])

        # Registrar la operación en el historial
        add_to_history(f"Sale: {item_name} (Quantity: {quantity_to_sell}, Total Sale: {total_sale}€)", curr_time)

        # Confirmación al usuario
        print(f"Sale completed: {item_name}, Quantity: {quantity_to_sell}, Total Sale: {total_sale}€")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Display inventory
def show_inventory():
    print("\n--- Current Inventory ---")
    # Encabezados actualizados
    print(
        f"{'Name':<20} {'Date':<20} {'Package Number':<15} {'Kg/Units':<12} {'Price per Unit (€)':<20} {'Balance (€)':<15}")
    print("-" * 100)

    # Imprimir los elementos del inventario
    for item in inventory_lst:
        try:
            # Convertir valores a flotantes para cálculos
            item_weight = float(item.weight)
            item_price_per_unit = float(item.price_per_unit)  # Usar price_per_unit directamente

            # Buscar si este item tiene una compra o venta en el balance
            matching_balance_entry = next((entry for entry in balance_lst if entry.name == item.name and entry.n_package == item.n_package), None)

            if matching_balance_entry:
                # Si la entrada del balance tiene un precio negativo (compra), el balance será negativo
                # Si la entrada del balance tiene un precio positivo (venta), el balance será positivo
                if matching_balance_entry.price < 0:
                    total_balance = matching_balance_entry.price  # Compra, balance negativo
                else:
                    total_balance = matching_balance_entry.price  # Venta, balance positivo
            else:
                total_balance = 0  # Si no hay entrada de balance asociada, el balance es 0

            # Imprimir datos del inventario
            print(
                f"{item.name:<20} {item.date:<20} {item.n_package:<15} {item_weight:<12.2f} {item_price_per_unit:<20.2f} {total_balance:<15.2f}")
        except ValueError:
            print(f"Error processing item: {item.name}. Please check data format.")


# User options menu
def main_menu():
    while True:
        print("\n--- Operations Menu ---\n" +
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
                                  [(item.name, item.date, item.n_package, item.weight, item.price) for item in balance_lst],
                                  ["Name", "Date", "Package Number", "Weight", "Price"])
                save_data_to_file(history_file, history_data, ["Date", "Operation"])
                exit()
            else:
                print("Invalid option. Try again.")
        except ValueError:
            print("Please enter a valid number.")

# Start the program
if __name__ == "__main__":
    print("------------ Welcome to warehouse accounting system -------------------------")
    main_menu()
