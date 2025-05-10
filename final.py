import pymysql
import regex as re
import subprocess
import os
from datetime import datetime
def get_connection_as_user(user, password):
    return pymysql.connect(
        host="localhost",
        user=user,
        password=password,
        database="Delivery_System"
    )

## Dialing code for Asean and South Asia countries
# +673: Brunei, +855: Cambodia, +86: China, +62: Indonesia, +81: Japan, +82: South Korea, +856: Laos
# +60: Malaysia, +976: Mongolia, +95: Myanmar, +63: Philippines, +65: Singapore, +66: Thailand, +886: Taiwan, +84: Vietnam
dialing_code = {"673": 7, "855": [8,9], "86": 11, "62": [10,12], "81": [10,11], "82": [10,11], "856": [8,10],
                "60": [9-10], "976": 8, "95": [9,11], "63": 10, "65": 8, "66": 9, "886": 9, "84": 9}
def validate_phone_number(phone_number):
    cleaned = re.sub(r'[^\d]', '', phone_number)

    for code, length in dialing_code.items():
        if cleaned.startswith(code):
            local_number = cleaned[len(code):]

            if (isinstance(length, list) and len(local_number) in length) or len(local_number) == length:
                return f"0{local_number}"
            
    return False
    
def add_customer(connection):
    customer_name = input("Enter customer name: ")
    cursor = connection.cursor()
    while True:
        phone_number = input("Enter phone number: +")
        validated = validate_phone_number(phone_number)
        if validated is False:
            print("Invalid phone number format. Please try again.")
        else:
            phone_number = validate_phone_number(phone_number)
            break
    while True:
        country = input("Enter country: ")
        country = (re.sub(r'[^a-zA-Z0-9 ]', '', country)).strip().title()
        cursor.execute(
            "SELECT CountryCode FROM Countries WHERE CountryName = %s",
            (country,)
        )
        country_code = cursor.fetchone()
        if country_code is None:
            print("Country not found. Please enter a country in SouthEast and South Asia.")
        else:
            country = country_code[0]
            break
    
    while True:
        city = input("Enter city: ")
        city = (re.sub(r'[^a-zA-Z0-9 ]', '', city)).strip().title()
        cursor.execute(
            "SELECT CityCode FROM Cities WHERE CityName = %s AND CountryCode = %s",
            (city, country)
        )
        city_code = cursor.fetchone()
        if city_code is None:
            cursor.execute(
                "INSERT INTO Cities (CityName, CountryCode) VALUES (%s, %s)",
                (city, country)
            )
            city_code = cursor.lastrowid
            break
        else:
            city_code = city_code[0]
        break

    address = input("Enter address: ")

    cursor.execute(
        "INSERT INTO Customers (CustomerName, PhoneNumber, Address, City) VALUES (%s, %s, %s, %s)",
        (customer_name, phone_number, address, city_code)
    )
    connection.commit()
    print("Customer added successfully.")
    cursor.close()
def create_order(connection):
    while True:
        try:
            customer_id = int(input("Enter customer ID: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid customer ID.")
    
    try:
        order_date = input("Enter order date (YYYY-MM-DD): ")
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Orders (CustomerID, OrderDate) VALUES (%s, %s)",
                (customer_id, order_date)
            )
            connection.commit()
            print("Order created successfully.")
    except pymysql.Error as e:
        print(f"Error: {e}")
        return

def update_order_status(connection):
    while True:
        try:
            order_id = int(input("Enter order ID: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid order ID.")
    while True:
        new_status = input("Enter new status: (ordered / in transit / successful / failed)").lower()
        if new_status not in ['ordered','in transit' 'successful', 'failed']:
            print("Invalid status. Please enter a valid status.")
        else: break

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE Orders SET Status = %s WHERE OrderID = %s",
                (new_status, order_id)
            )
            connection.commit()
            print("Order status updated successfully.")
    except pymysql.Error as e:
        print(f"Error: {e}")
        return

def update_delivery_status(connection):
    cursor = connection.cursor()
   
    while True:
        delivery_id = input("Enter delivery ID: ")
        if not delivery_id.isdigit():
            print("Delivery ID must be a number. Please try again.")
            continue


        cursor.execute("SELECT 1 FROM Deliveries WHERE DeliveryID = %s", (delivery_id,))
        if cursor.fetchone():
            break
        else:
            print("Delivery ID does not exist. Please try again.")
   
    valid_statuses = ['transit warehouse', 'transit customer', 'successful', 'failed']
    while True:
        new_status = input(f"Enter new status {valid_statuses}: ").lower()
        if new_status in valid_statuses:
            break
        else:
            print("Invalid status. Please enter a valid status.")

    delivery_end_date = None
    if new_status in ['successful', 'failed']:
        while True:
            delivery_end_date = input("Enter delivery end date (YYYY-MM-DD): ")
            try:
                # Kiểm tra định dạng ngày tháng
                datetime.strptime(delivery_end_date, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
    try:
        if delivery_end_date:
            cursor.execute(
                "UPDATE Deliveries SET Status = %s, DeliveryEndDate = %s WHERE DeliveryID = %s",
                (new_status, delivery_end_date, delivery_id)
            )
        else:
            cursor.execute(
                "UPDATE Deliveries SET Status = %s WHERE DeliveryID = %s",
                (new_status, delivery_id)
            )
        connection.commit()
        print("Delivery status updated successfully.")
    except Exception as e:
        print("Error updating delivery:", e)
    finally:
        cursor.close()

def add_expense(connection):
    cursor = connection.cursor()

    # Lặp đến khi delivery_id hợp lệ
    while True:
        try:
            delivery_id = int(input("Enter Delivery ID: "))
            cursor.execute("SELECT 1 FROM Deliveries WHERE DeliveryID = %s", (delivery_id,))
            if cursor.fetchone():
                break
            else:
                print("Invalid Delivery ID. Please try again.")
        except ValueError:
            print("Please enter a valid integer for Delivery ID.")

    # Lấy thông tin chi phí
    valid_types = ['toll', 'fee', 'fuel', 'handling', 'other']
    while True:
        expense_type = input(f"Enter expense type ({', '.join(valid_types)}): ").lower()
        if expense_type in valid_types:
            break
        else:
            print("Invalid expense type. Please try again.")

    while True:
        try:
            amount = float(input("Enter amount (e.g., 123.45): "))
            break
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")

    # Thêm chi phí
    try:
        cursor.execute(
            "INSERT INTO Expenses (DeliveryID, ExpenseType, Amount) VALUES (%s, %s, %s)",
            (delivery_id, expense_type, amount)
        )
        connection.commit()
        print("Expense added successfully.")
    except Exception as e:
        print("Failed to add expense:", e)
        connection.rollback()
    finally:
        cursor.close()

def add_city(connection):
    cursor = connection.cursor()
    while True:
        city_name = input("Enter city name: ")
        if city_name.isdigit():
            print("City name cannot be a number. Please try again.")
        else:
            break
    while True:
        country = input("Enter country: ")
        country = (re.sub(r'[^a-zA-Z0-9 ]', '', country)).strip().title()
        cursor.execute(
            "SELECT CountryCode FROM Countries WHERE CountryName = %s",
            (country,)
        )
        country_code = cursor.fetchone()
        if country_code is None:
            print("Country not found. Please enter a country in SouthEast and South Asia.")
        else:
            country = country_code[0]
            break
    cursor.execute(
        "INSERT INTO Cities (CityName, CountryCode) VALUES (%s, %s)",
        (city_name, country)
    )
    connection.commit()
    print("City added successfully.")
    cursor.close()
    return cursor.lastrowid
def update_cus_info(connection):
    while True:
        try:
            customer_id = int(input("Enter customer ID: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid customer ID.")

    new_address = input("Enter new address: (Leave blank if not updating) ").strip()
    
    new_phone = input("Enter new phone number: (Leave blank if not updating) +")
    if new_phone:    
        while True:
            validated = validate_phone_number(new_phone)
            if validated:
                new_phone = validated
                break
            else:
                print("Invalid phone number format. Please try again.")
                new_phone = input("Enter new phone number: (Leave blank if not updating) +").strip()

    new_city = input("Enter new city: (Leave blank if not updating) ")
    if new_city:    
        while True:
            new_city = (re.sub(r'[^a-zA-Z0-9 ]', '', new_city)).strip().title()
            cursor.execute(
                "SELECT CityCode FROM Cities WHERE CityName = %s",
                (new_city,)
            )
            city_code = cursor.fetchone()
            if city_code is None:
                m = input("City not found. Please create a new city by typing 'create' or quit by typing 'quit'.")
                if m == 'quit':
                    return
                elif m == 'create':
                    city_code = add_city(connection)
                    break
            else:
                city_code = city_code[0]
                break
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE Customers SET Address = %s WHERE CustomerID = %s",
                (new_address, customer_id)
            ) if new_address else None
            cursor.execute(
                "UPDATE Customers SET PhoneNumber = %s WHERE CustomerID = %s",
                (new_phone, customer_id)
            ) if new_phone else None
            cursor.execute(
                "UPDATE Customers SET City = %s WHERE CustomerID = %s",
                (city_code, customer_id)
            ) if new_city else None
            connection.commit()
            print("Customer updated successfully.")
    except pymysql.Error as e:
        print(f"Error: {e}")
        return

def view_cus_orders(connection):
    ''''Return all orders of customer with given ID'''
    while True:
        try:
            customer_id = int(input("Enter customer ID: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid customer ID.")

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM Customers WHERE CustomerID = %s",
                (customer_id)
            )
            customer = cursor.fetchone()
            if not customer:
                print("Customer not found.")
                return
            print(f"Customer: {customer[1]}, Phone: {customer[2]}, Address: {customer[3]}")
            cursor.execute(
                "SELECT * FROM Orders WHERE CustomerID = %s",
                (customer_id)
            )
            connection.commit()
            for order in cursor.fetchall():
                print(f"Order ID: {order[0]}, Order Date: {order[2]}, Delivery Fail Count: {order[3]}, Status: {order[4]}")
    except pymysql.Error as e:
        print(f"Error: {e}")
        return
def view_orders(connection):
    '''Return all orders'''
    try:    
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT o.OrderID, c.CustomerName  , o.OrderDate, o.Status
                FROM Orders o
                JOIN Customers c USING(CustomerID)             
            ''')
            
            for order in cursor.fetchall():
                print(order)
    except pymysql.Error as e:
        print(f"Error: {e}")
        return

def outstanding_orders(connection):
    try:    
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM OutstandingOrders"
            )
            connection.commit()
            for order in cursor.fetchall():
                print(order)
    except:
        print("No outstanding orders")
        return

def view_delivery_details(connection):
    '''Return delivery details'''
    while True:    
        try:    
            delivery_id = int(input("Enter delivery ID: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid delivery ID.")
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Status
                FROM Deliveries 
                WHERE DeliveryID = %s
            """, (delivery_id,))
            result = cursor.fetchone()
            if not result:
                print("Delivery not found.")
                return
            
            status = result[0]
            print(status)
            if status == 'transit customer':
                cursor.execute(
                    "SELECT * FROM ShipperCustomerView WHERE DeliveryID = %s",
                    (delivery_id)
                )
            elif status == 'transit warehouse':
                cursor.execute(
                    "SELECT * FROM WarehouseWarehouseView WHERE DeliveryID = %s",
                    (delivery_id)
                )
            else:
                print("Status not in transit.")
                return
           
            row = cursor.fetchone()
            if row:
                print("\nDelivery Details:")
                for col, val in zip([desc[0] for desc in cursor.description], row):
                    print(f"{col}: {val}")
            else:
                print("No details found for this delivery.")

    except pymysql.Error as e:
        print(f"Error: {e}")
        return

def view_available_vehicles(connection):
    '''Return all available vehicles'''
    try:   
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT VehicleID, VehicleType, LicensePlate
                FROM Vehicles
                WHERE Status = 'available'
            ''')

            for vehicle in cursor.fetchall():
                print(vehicle)
    except:
        print("No available vehicles")
        return

def assign_delivery(connection):
    while True:
        try:
            order_id = int(input("Enter order ID: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid order ID.")
    while True:
        try:
            vehicle_id = int(input("Enter vehicle ID: "))
        except ValueError:
            print("Invalid input. Please enter a valid vehicle ID.")
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT Status FROM Vehicles WHERE VehicleID = %s",
                    (vehicle_id,)
                )
                result = cursor.fetchone()
                if not result:
                    command = input("Invalid vehicle ID. Please try again or enter 'exit' to quit.")
                    if command.lower() == 'exit':
                        break
                    continue

                vehicle_status = result[0]
                if vehicle_status != 'available':
                    command = input("Vehicle is not available. Please choose another vehicle or enter 'exit' to quit.")
                    if command.lower() == 'exit':
                        break
                    continue

                cursor.execute("CALL AssignDelivery(%s, %s)", (order_id, vehicle_id))
                connection.commit()
                print("Delivery assigned successfully.")
                break
        except pymysql.Error as e:
            print(f"Error assigning delivery: {e}")
            connection.rollback()
            break

def avg_cost_per_vehicle_type(connection):
    try:    
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT v.VehicleType, AVG(t.TotalCost) AS AvgCost
                FROM Vehicles v
                JOIN (
                    SELECT d.VehicleID, SUM(e.Amount) AS TotalCost
                    FROM Deliveries d
                    JOIN Expenses e ON d.DeliveryID = e.DeliveryID
                    GROUP BY d.DeliveryID
                ) t ON v.VehicleID = t.VehicleID
                GROUP BY v.VehicleType;
            ''')
            
            results = cursor.fetchall()
            for vehicle, avg_cost in results:
                print(f"Vehicle Type: {vehicle}, Average Cost: {avg_cost:.2f}")
    except pymysql.Error as e:
        print(f"Error: {e}")
        return


def calculate_delivery_success_rate(connection):
    """Calculate and display the delivery success rate with formatted output"""
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    SUM(Status = 'successful') AS SuccessfulCount,
                    SUM(Status = 'failed') AS FailedCount
                FROM Deliveries;
            """)
            result = cursor.fetchone()
            successful = result[0] or 0
            failed = result[1] or 0

            total = successful + failed
            print("\n=== Delivery Success Rate Report ===")
            if total == 0:
                print("No completed deliveries yet.")
            else:
                success_rate = (successful / total) * 100
                print(f"{'Successful Deliveries':<25}: {successful}")
                print(f"{'Failed Deliveries':<25}: {failed}")
                print(f"{'Total Deliveries':<25}: {total}")
                print(f"{'Success Rate':<25}: {success_rate:.2f}%")
            print("=" * 38)

def calculate_order_success_rate(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    SUM(Status = 'successful') AS SuccessfulCount,
                    SUM(Status = 'failed') AS FailedCount
                FROM Orders;
            """)
            result = cursor.fetchone()
            successful = result[0] or 0
            failed = result[1] or 0

            total = successful + failed
            print("\n=== Order Success Rate Report ===")
            if total == 0:
                print("No completed or failed orders yet.")
            else:
                success_rate = (successful / total) * 100
                print(f"{'Successful Orders':<25}: {successful}")
                print(f"{'Failed Orders':<25}: {failed}")
                print(f"{'Total Orders':<25}: {total}")
                print(f"{'Success Rate':<25}: {success_rate:.2f}%")
            print("=" * 36)

def generate_invoice(connection):
    while True:    
        try:    
            delivery_id = int(input("Enter delivery ID: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid delivery ID.")
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DeliveryID
                FROM Deliveries 
                WHERE DeliveryID = %s AND d.Status = 'successful'
                """, (delivery_id,))
            delivery = cursor.fetchone()
            if not delivery:
                return f"Delivery with ID {delivery_id} not found or not successful."
            cursor.execute("""
                    SELECT ExpenseType, Amount
                    FROM Expenses
                    WHERE DeliveryID = %s
                """, (delivery_id,))
            expenses = cursor.fetchall()
            total = sum(expense[1] for expense in expenses)
           
            print("="*60)
            print(f"{'INVOICE':>30}")
            print()
            print(f"Delivery ID #: {delivery_id:<20} DATE: {delivery[3]}")
            print()
            print(f"BILL TO: HQ")
            print()
            print("-"*60)
            print(f"{'DESCRIPTION':<40}{'AMOUNT':>20}")
            print("-"*60)
            for desc, amt in expenses:
                print(f"{desc:<40}{amt:>20}")
            print("-"*60)
            print(f"{'TOTAL':<40}{total:>20}")
            print("="*60)
            print("Thank you for your business!")
    except pymysql.Error as e:
        print(f"Error: {e}")
        return

def order_cost_breakdown(connection):
    '''Return report of expenses by each delivery for an order given OrderID'''
    while True:
        try:
            order_id = int(input("Enter order ID: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid order ID.")
    try:
        with connection.cursor() as cursor:
            # Lấy danh sách deliveries theo order
            cursor.execute("""
                SELECT d.DeliveryID, d.DeliveryEndDate, d.Status
                FROM Deliveries d
                WHERE d.OrderID = %s
                ORDER BY d.DeliveryID
            """, (order_id,))
            deliveries = cursor.fetchall()

            if not deliveries:
                print(f"No deliveries found for Order ID: {order_id}")
                return

            for leg_num, delivery in enumerate(deliveries, start=1):
                delivery_id = delivery[0]
                delivery_date = delivery[1]
                print("=" * 65)
                print(f"{f'Cost Breakdown for Delivery (Leg {leg_num})':^65}")
                print()
                print(f"Delivery ID #: {delivery_id} \t\tDATE: {delivery_date}")
                print("-" * 65)
                print(f"{'DESCRIPTION':<40}{'AMOUNT':>20}")
                print("-" * 65)

                # Lấy các chi phí của delivery này
                cursor.execute("""
                    SELECT ExpenseType, SUM(Amount) AS TotalAmount
                    FROM Expenses
                    WHERE DeliveryID = %s
                    GROUP BY ExpenseType
                """, (delivery_id))
                expenses = cursor.fetchall()

                total_amount = 0
                if not expenses:
                    print(f"{'No recorded expenses.':<40}")
                else:
                    for exp_type, amount in expenses:
                        print(f"{exp_type:<40}{float(amount):>20.2f}")
                        total_amount += float(amount)

                print("-" * 65)
                print(f"{'TOTAL':<40}{total_amount:>20.2f}")
                print("=" * 65)
                print("Thank you for your business!\n")
    except pymysql.Error as e:
        print(f"Error: {e}")
        return


def period_cost_breakdown(conn):
    """Fetch cost breakdown for a given date range and display it."""
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    date_re = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    year_re = re.compile(r'^\d{4}$')
    # User input for period type and date range
    period_type = input("Please enter period type (monthly/quarterly/custom_period): ").lower().replace(' ', '')
    if period_type not in ['monthly', 'quarterly', 'custom_period']:
        print("Invalid input. Please enter 'monthly', 'quarterly', or 'custom_period'. Exiting.")
        return

    if period_type == 'custom_period':
        start_date = input("Enter start date (YYYY-MM-DD): ").replace(' ', '')
        end_date = input("Enter end date (YYYY-MM-DD): ").replace(' ', '')

        if not date_re.match(start_date) or not date_re.match(end_date):
            print("Invalid date format. Please use YYYY-MM-DD. Exiting.")
            return

        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            if start_dt > end_dt:
                print("Start date must be before or equal to end date. Exiting.")
                return
        except ValueError:
            print("Invalid calendar date. Please enter real dates. Exiting.")
            return
    else:
        year_input = input("Please enter year (YYYY): ").strip()
        if not year_re.match(year_input):
            print("Invalid year format. Use a 4-digit year like 2025. Exiting.")
            return
        start_date = f"{year_input}-01-01"
        end_date = f"{year_input}-12-31"

    # SQL query to fetch cost breakdown
    query = """
        SELECT
            DATE_FORMAT(d.DeliveryEndDate, '%%Y-%%m') AS AccountingPeriod,
            e.ExpenseType,
            SUM(e.Amount) AS Total_Cost
        FROM Expenses e
        JOIN Deliveries d ON d.DeliveryID = e.DeliveryID
        WHERE d.DeliveryEndDate BETWEEN %s AND %s
        GROUP BY AccountingPeriod, e.ExpenseType;
    """
    cursor.execute(query, (start_date, end_date))  # Execute query with parameters
    results = cursor.fetchall()
    cursor.close()

    # Handle case where no data is found
    if not results:
        print("No cost data found for the selected period.")
        return

    # Define headers for monthly or quarterly report
    headers = ["Period", "Fuel ($)", "Fee ($)", "Handling ($)", "Toll ($)", "Other ($)", "Total ($)"]
    # Initialize a dictionary to store costs by period and type
    cost_data = {
        'fuel': 0.00,
        'fee': 0.00,
        'handling': 0.00,
        'toll': 0.00,
        'other': 0.00
    }
    # Organize data based on period type
    periods = {}
    # Fill in the cost data from the query results
    for row in results:
        period = row["AccountingPeriod"]
        if period not in periods:
            periods[period] = {key: 0.00 for key in cost_data}

        # Assign costs for each expense type to the correct period
        if row["ExpenseType"] in cost_data:
            periods[period][row["ExpenseType"]] = row["Total_Cost"]

    # Function to print the monthly report
    def print_monthly_report():
        print("\nMonthly Cost Breakdown Report:")
        headers = ["Period", "Fuel", "Fee", "Handling", "Toll", "Other", "Total"]
        widths = [10, 10, 10, 10, 10, 10, 10]

        # Print headers
        print("-" * 80)
        header_row = "".join(f"{name:<{w}}" for name, w in zip(headers, widths))
        print(header_row)
        print("-" * 80)

        # Print data rows
        for period, data in periods.items():
            total_cost = sum(float(v) for v in data.values())
            row = [
                period,
                f"{float(data['fuel']):.2f}",
                f"{float(data['fee']):.2f}",
                f"{float(data['handling']):.2f}",
                f"{float(data['toll']):.2f}",
                f"{float(data['other']):.2f}",
                f"{total_cost:.2f}"
            ]
            print("".join(f"{val:<{w}}" for val, w in zip(row, widths)))
        print("-" * 80)

    # Function to print the quarterly report
    def print_quarterly_report():
        print("\nQuarterly Cost Breakdown Report:")
        print("-" * 80)
        # Adjusted headers for the quarterly report
        headers = ["Quarter", "Fuel ($)", "Fee ($)", "Handling ($)", "Toll ($)", "Other ($)", "Total ($)"]       
        # Column widths (adjusted to fit larger values)
        widths = [12, 12, 12, 12, 12, 12, 14]  # Adjust widths for bigger values

        # Print header
        print("{:<{w[0]}} {:>{w[1]}} {:>{w[2]}} {:>{w[3]}} {:>{w[4]}} {:>{w[5]}} {:>{w[6]}}".format(*headers, w=widths))
        print("-" * 80)

        # Grouping the months into quarters
        quarters = {
            "Q1": ['01', '02', '03'],
            "Q2": ['04', '05', '06'],
            "Q3": ['07', '08', '09'],
            "Q4": ['10', '11', '12'],
        }
        for quarter, months in quarters.items():
            quarter_data = {key: 0.00 for key in cost_data}
            # Summing up data for each quarter
            for period, data in periods.items():
                month = period.split('-')[1]
                if month in months:
                    for key in cost_data:
                        quarter_data[key] += float(data[key])
            total_cost = sum(float(v) for v in quarter_data.values())

            # Print values for the quarter (ensuring we only print the values if they're non-zero)
            print("{:<{w[0]}} {:>{w[1]}.2f} {:>{w[2]}.2f} {:>{w[3]}.2f} {:>{w[4]}.2f} {:>{w[5]}.2f} {:>{w[6]}.2f}".format(
                quarter,
                float(quarter_data["fuel"]),
                float(quarter_data["fee"]),
                float(quarter_data["handling"]),
                float(quarter_data["toll"]),
                float(quarter_data["other"]),
                total_cost,
                w=widths
            ))
        print("-" * 80)
    # Call the appropriate report format based on user input
    if period_type == 'monthly':
        print_monthly_report()
    elif period_type == 'quarterly':
        print_quarterly_report()
    elif period_type == 'custom_period':
        print_monthly_report()
    else:
        print("Invalid period type! Please choose 'monthly' or 'quarterly'.")

    # Function to print the monthly report
    def print_monthly_report():
        print("\nMonthly Cost Breakdown Report:")
        headers = ["Period", "Fuel", "Fee", "Handling", "Toll", "Other", "Total"]
        widths = [10, 10, 10, 10, 10, 10, 10]

        # Print headers
        print("-" * 80)
        header_row = "".join(f"{name:<{w}}" for name, w in zip(headers, widths))
        print(header_row)
        print("-" * 80)

        # Print data rows
        for period, data in periods.items():
            total_cost = sum(float(v) for v in data.values())
            row = [
                period,
                f"{float(data['fuel']):.2f}",
                f"{float(data['fee']):.2f}",
                f"{float(data['handling']):.2f}",
                f"{float(data['toll']):.2f}",
                f"{float(data['other']):.2f}",
                f"{total_cost:.2f}"
            ]
            print("".join(f"{val:<{w}}" for val, w in zip(row, widths)))
        print("-" * 80)

    # Function to print the quarterly report
    def print_quarterly_report():
        print("\nQuarterly Cost Breakdown Report:")
        print("-" * 80)
        # Adjusted headers for the quarterly report
        headers = ["Quarter", "Fuel ($)", "Fee ($)", "Handling ($)", "Toll ($)", "Other ($)", "Total ($)"]       
        # Column widths (adjusted to fit larger values)
        widths = [12, 12, 12, 12, 12, 12, 14]  # Adjust widths for bigger values

        # Print header
        print("{:<{w[0]}} {:>{w[1]}} {:>{w[2]}} {:>{w[3]}} {:>{w[4]}} {:>{w[5]}} {:>{w[6]}}".format(*headers, w=widths))
        print("-" * 80)

        # Grouping the months into quarters
        quarters = {
            "Q1": ['01', '02', '03'],
            "Q2": ['04', '05', '06'],
            "Q3": ['07', '08', '09'],
            "Q4": ['10', '11', '12'],
        }
        for quarter, months in quarters.items():
            quarter_data = {key: 0.00 for key in cost_data}
            # Summing up data for each quarter
            for period, data in periods.items():
                month = period.split('-')[1]
                if month in months:
                    for key in cost_data:
                        quarter_data[key] += float(data[key])
            total_cost = sum(float(v) for v in quarter_data.values())

            # Print values for the quarter (ensuring we only print the values if they're non-zero)
            print("{:<{w[0]}} {:>{w[1]}.2f} {:>{w[2]}.2f} {:>{w[3]}.2f} {:>{w[4]}.2f} {:>{w[5]}.2f} {:>{w[6]}.2f}".format(
                quarter,
                float(quarter_data["fuel"]),
                float(quarter_data["fee"]),
                float(quarter_data["handling"]),
                float(quarter_data["toll"]),
                float(quarter_data["other"]),
                total_cost,
                w=widths
            ))
        print("-" * 80)
    # Call the appropriate report format based on user input
    if period_type == 'monthly':
        print_monthly_report()
    elif period_type == 'quarterly':
        print_quarterly_report()
    elif period_type == 'custom_period':
        print_monthly_report()
    else:
        print("Invalid period type! Please choose 'monthly' or 'quarterly'.")

def back_up():
    # Get MySQL credentials and backup directory from the user
    user = input("Enter your MySQL username: ")
    password = input("Enter your MySQL password: ")
    db_name = 'Delivery_System'
    backup_dir = input("Enter the directory where backups should be stored (e.g., D:\\Backups): ")

    # Check if directory exists, if not, create it
    if not os.path.exists(backup_dir):
        print(f"Directory '{backup_dir}' does not exist. Creating it now...")
        os.makedirs(backup_dir)

    # Get current date and time in formatted string
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"delivery_backup_{current_time}.sql"

    # Generate filename for backup based on current date and time
    backup_file_path = os.path.join(backup_dir, filename)

    # Define the mysqldump command
    mysql_dump_path = input("Enter mysqldump.exe location:")
    command = f'"{mysql_dump_path}" -u {user} -p{password} {db_name} > "{backup_file_path}"'

    # === RUN MYSQLDUMP BACKUP ===
    try:
        print(f"Creating backup of database '{db_name}'...")
        subprocess.run(command, shell=True, check=True)

        # Inform user about the success
        print(f"Backup created successfully!\nFile saved at: {backup_file_path}")
    except subprocess.CalledProcessError as e:
        # Handle errors
        print(f"Backup failed: {e}")

def recovery():
    # Get MySQL credentials and backup file details from the user
    user = input("Enter your MySQL username: ")
    password = input("Enter your MySQL password: ")
    db_name = input("Enter the name of the database to restore: ")
    backup_file = input("Enter the full path of the backup file to restore from: ")

    # Check if the backup file exists
    if not os.path.exists(backup_file):
        print(f"The file '{backup_file}' does not exist. Please check the path and try again.")
        return None, None, None, None

    # Define the path to the MySQL command
    mysql_path = input("Enter mysqldump.exe location:")

    # Define the restore command
    command = f'"{mysql_path}" -u {user} -p{password} {db_name} < "{backup_file}"'

    try:
        print(f"🔄 Restoring database '{db_name}' from backup...")
        subprocess.run(command, shell=True, check=True)

        # Inform user about success
        print(f"Database '{db_name}' restored successfully from: {backup_file}")
    except subprocess.CalledProcessError as e:
        # Handle errors
        print(f"Database restore failed: {e}")

def custom_query(connection):
    try:    
        with connection.cursor() as cursor:
            while True:
                sql_query = input("Query: (type 'exit' to quit): ")
                if sql_query.lower() == 'exit':
                    break
                try:
                    cursor.execute(sql_query)
                    if sql_query.strip().lower().startswith("select"):
                        results = cursor.fetchall()
                        if not results:
                            print("No results found.")
                        else:
                            for row in results:
                                print(row)
                    else:
                        connection.commit()
                        print("Query executed successfully.")
                except Exception as e:
                    print(f"Query error: {e}")
    except pymysql.Error as e:
        print(f"Connection error: {e}")


def menu(user, connection):
    if user == "manager":
        while True:
            print("0: Logout")
            print("1. Add customer")
            print("2. Create order")
            print("3. Update order status")
            print("4. Update customer information")
            print("5. View a customer's orders")
            print("6. View all orders")
            print("7. View outstanding orders")
            print("8. Generate invoice.")
            print("9. View cost breakdown by period")
            print("10. View cost breakdown by order")
            print("11. Backup database")
            print("12. Restore database")
            print("13. View delivery success rate")
            print("14. View order success rate")
            print("15. Custom query")
            choice = input("Choose an option: ")
            if choice == "0": break
            elif choice == "1": add_customer(connection)
            elif choice == "2": create_order(connection)
            elif choice == "3": update_order_status(connection)
            elif choice == "4": update_cus_info(connection)
            elif choice == "5": view_cus_orders(connection)
            elif choice == "6": view_orders(connection)
            elif choice == "7": outstanding_orders(connection)
            elif choice == "8": generate_invoice(connection)
            elif choice == "9": period_cost_breakdown(connection)
            elif choice == "10": order_cost_breakdown(connection)
            elif choice == "11": back_up()
            elif choice == "12": recovery()
            elif choice == "13": calculate_delivery_success_rate(connection)
            elif choice == "14": calculate_order_success_rate(connection)
            elif choice == "15": custom_query(connection)
            else: print("Invalid choice. Please try again.")
    elif user == "dispatcher":
        while True:
            print("0: Logout")
            print("1. Assign delivery")
            print("2. View all orders")
            print("3. View outstanding orders")
            print("4. View available vehicles")
            print("5. Custom query")
            choice = input("Choose an option: ")
            if choice == "0": break
            elif choice == "1": assign_delivery(connection)
            elif choice == "2": view_orders(connection)
            elif choice == "3": outstanding_orders(connection)
            elif choice == "4": view_available_vehicles(connection)
            elif choice == "5": custom_query(connection)
            else: print("Invalid choice. Please try again.")
    elif user == "accountant":
        while True:
            print("0: Logout")
            print("1. View average cost per vehicle type")
            print("2. Generate invoice")
            print("3. View cost breakdown by order")
            print("4. View cost breakdown by period")
            print("5. Custom query")
            choice = input("Choose an option: ")
            if choice == "0": break
            elif choice == "1": avg_cost_per_vehicle_type(connection)
            elif choice == "2": generate_invoice(connection)
            elif choice == "3": order_cost_breakdown(connection)
            elif choice == "4": period_cost_breakdown(connection)
            elif choice == "5": custom_query(connection)
            else: print("Invalid choice. Please try again.")
    elif user == "shipper":
        while True:
            print("0: Logout")
            print("1. View delivery")
            print("2. Update delivery status")
            print("3. Add expense")
            choice = input("Choose an option: ")
            if choice == "0": break
            elif choice == "1": view_delivery_details(connection)
            elif choice == "2": update_delivery_status(connection)
            elif choice == "3": add_expense(connection)
            else: print("Invalid choice. Please try again.")
    else:
        print("Invalid user type. Please try again.")

def login():
    print("----Login----")
    user = input("Username (manager / dispatcher / accountant / shipper): ")
    password = input("Enter password: ")
    try:
        connection = get_connection_as_user(user, password)
        print(f"Login successful as {user}.")
        menu(user, connection)
        connection.close()
    except pymysql.MySQLError as err:
        print(f"Login failed: {err}")

if __name__ == "__main__":
    while True:
        login()
        cont = input("Do you want to continue? (y/n): ")
        if cont.lower() != "y":
            break