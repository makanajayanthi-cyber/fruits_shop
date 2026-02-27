import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql@123",
    database="fruit_shop"
)
cursor = db.cursor()


# ---------------- VIEW FRUITS ----------------
def view_fruits():
    print("\n--- AVAILABLE FRUITS ---")
    print("ID | Name       | Price/kg | Stock(kg)")
    print("--------------------------------------")

    cursor.execute("SELECT fruit_id, fruit_name, price_per_kg, stock_kg FROM fruits")
    for fid, name, price, stock in cursor.fetchall():
        print(f"{fid:<3}| {name:<10}| {price:<9}| {stock}")


# ---------------- CUSTOMER MENU ----------------
def customer_menu():
    while True:
        print("\n--- CUSTOMER MENU ---")
        print("1. Add Fruit to Cart")
        print("2. Remove Fruit from Cart")
        print("3. Update Quantity")
        print("4. View Total Cost")
        print("5. Generate Bill")
        print("6. Back")

        choice = input("Enter choice: ")

        # ADD
        if choice == '1':
            view_fruits()
            fid = int(input("Enter Fruit ID: "))
            qty = int(input("Enter Quantity: "))

            cursor.execute(
                "SELECT fruit_name, price_per_kg, stock_kg FROM fruits WHERE fruit_id=%s",
                (fid,)
            )
            data = cursor.fetchone()

            if data and data[2] >= qty:
                name, price, stock = data
                total = price * qty

                cursor.execute(
                    "INSERT INTO cart (fruit_id, fruit_name, quantity, total_price) VALUES (%s,%s,%s,%s)",
                    (fid, name, qty, total)
                )

                cursor.execute(
                    "UPDATE fruits SET stock_kg = stock_kg - %s WHERE fruit_id=%s",
                    (qty, fid)
                )

                db.commit()
                print("Added to cart!")
            else:
                print("Not enough stock!")

        # REMOVE
        elif choice == '2':
            cursor.execute("SELECT cart_id, fruit_id, fruit_name, quantity FROM cart")
            items = cursor.fetchall()

            if not items:
                print("Cart is empty!")
                continue

            print("\n--- YOUR CART ---")
            for i, item in enumerate(items, start=1):
                print(f"{i}. {item[2]} | Qty:{item[3]}kg")

            try:
                idx = int(input("Enter item number to remove: "))
                cid = items[idx-1][0]
                fid = items[idx-1][1]
                qty = items[idx-1][3]
            except (ValueError, IndexError):
                print("Invalid choice!")
                continue

            cursor.execute(
                "UPDATE fruits SET stock_kg = stock_kg + %s WHERE fruit_id=%s",
                (qty, fid)
            )

            cursor.execute(
                "DELETE FROM cart WHERE cart_id=%s",
                (cid,)
            )

            db.commit()
            print("Item removed!")

        # UPDATE
        elif choice == '3':
           cursor.execute("SELECT cart_id, fruit_id, fruit_name, quantity FROM cart")
           items = cursor.fetchall()

           if not items:
             print("Cart is empty!")
             continue

           print("\n--- YOUR CART ---")
           for i, item in enumerate(items, start=1):
             print(f"{i}. {item[2]} | Qty:{item[3]}kg")

           try:
             idx = int(input("Enter item number: "))
             new_qty = int(input("New Quantity: "))
             cid = items[idx-1][0]
             fid = items[idx-1][1]
             old_qty = items[idx-1][3]
           except (ValueError, IndexError):
             print("Invalid input!")
             continue

           diff = new_qty - old_qty

    # get stock + price
           cursor.execute(
        "SELECT stock_kg, price_per_kg FROM fruits WHERE fruit_id=%s",
        (fid,)
    )
           stock, price = cursor.fetchone()

           if diff > 0 and stock < diff:
             print("Not enough stock!")
             continue

    # update fruit stock
           cursor.execute(
        "UPDATE fruits SET stock_kg = stock_kg - %s WHERE fruit_id=%s",
        (diff, fid)
    )

    # update cart quantity + total_price
           new_total = price * new_qty

           cursor.execute(
        "UPDATE cart SET quantity=%s, total_price=%s WHERE cart_id=%s",
        (new_qty, new_total, cid)
    )

           db.commit()
           print("Quantity updated successfully!")

        # TOTAL
        elif choice == '4':
            cursor.execute("SELECT SUM(total_price) FROM cart")
            total = cursor.fetchone()[0]
            print("Total Cost:", total if total else 0)

        # BILL
        elif choice == '5':
            cursor.execute("SELECT fruit_id, fruit_name, quantity FROM cart")
            items = cursor.fetchall()

            if not items:
                print("Cart is empty!")
                continue

            total_bill = 0
            print("\n--- FINAL BILL ---")

            for fid, name, qty in items:
                cursor.execute(
                    "SELECT price_per_kg, cost_price FROM fruits WHERE fruit_id=%s",
                    (fid,)
                )
                price, cost_price = cursor.fetchone()

                item_total = price * qty
                total_bill += item_total

                print(f"{name} = {price} * {qty}kg = {item_total}")

                profit = item_total - (cost_price * qty)

                cursor.execute(
                    """INSERT INTO daily_sale
                       (fruit_id, fruit_name, quantity, total_price, profit)
                       VALUES (%s,%s,%s,%s,%s)""",
                    (fid, name, qty, item_total, profit)
                )

            print("TOTAL BILL:", total_bill)

            cursor.execute("DELETE FROM cart")
            db.commit()

            print("Bill generated!")

        elif choice == '6':
            break


# ---------------- OWNER MENU ----------------
def owner_menu():
    while True:
        print("\n--- OWNER MENU ---")
        print("1. View Fruits")
        print("2. Add Fruit")
        print("3. Delete Fruit")
        print("4. Modify Fruit")
        print("5. Item Profit")
        print("6. Total Profit")
        print("7. Back")

        ch = input("Enter choice: ")

        if ch == '1':
            view_fruits()

        elif ch == '2':
            name = input("Fruit Name: ")
            price = int(input("Price/kg: "))
            stock = int(input("Stock: "))
            cost = int(input("Cost Price: "))

            cursor.execute(
                "INSERT INTO fruits (fruit_name, price_per_kg, stock_kg, cost_price) VALUES (%s,%s,%s,%s)",
                (name, price, stock, cost)
            )
            db.commit()

        elif ch == '3':
            fid = int(input("Fruit ID: "))
            cursor.execute("DELETE FROM fruits WHERE fruit_id=%s", (fid,))
            db.commit()

        elif ch == '4':
            fid = int(input("Fruit ID: "))
            price = int(input("New Price: "))
            stock = int(input("New Stock: "))

            cursor.execute(
                "UPDATE fruits SET price_per_kg=%s, stock_kg=%s WHERE fruit_id=%s",
                (price, stock, fid)
            )
            db.commit()

        elif ch == '5':
            cursor.execute(
                "SELECT fruit_name, SUM(profit) FROM daily_sale GROUP BY fruit_name"
            )
            for name, profit in cursor.fetchall():
                print(name, ":", profit)

        elif ch == '6':
            cursor.execute("SELECT SUM(profit) FROM daily_sale")
            p = cursor.fetchone()[0]
            print("Total Profit:", p if p else 0)

        elif ch == '7':
            break


# ---------------- MAIN ----------------
while True:
    print("\n=== FRUIT SHOP SYSTEM ===")
    print("1. Customer")
    print("2. Owner")
    print("3. Exit")

    opt = input("Choose option: ")

    if opt == '1':
        customer_menu()

    elif opt == '2':
        user = input("Username: ")
        pwd = input("Password: ")

        if user == "admin" and pwd == "admin123":
            owner_menu()
        else:
            print("Invalid login")

    elif opt == '3':
        print("Thank you for using Fruit Shop")
        break
