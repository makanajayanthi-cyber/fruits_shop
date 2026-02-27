# ============ DATA ============

fruits = [
    [1, "Apple", 50, 120, 80],    # ID, Name, Quantity, Selling Price, Cost Price
    [2, "Banana", 100, 40, 20],
    [3, "Mango", 60, 150, 100]
]

cart = []

# ============ MAIN LOOP ============

while True:
    print("\n====== FRUIT SHOP ======")
    print("1. Customer")
    print("2. Owner")
    print("3. Exit")
#=========== CUSTOMER SECTION ========
    
    role = input("Select role: ")
    if role == '1':
        while True:
            print("\n--- CUSTOMER MENU ---")
            print("1. View Fruits")
            print("2. Add Fruit")
            print("3. Remove Fruit")
            print("4. Total Cost")
            print("5. Bill")
            print("6. Back")

            ch = input("Choose: ")

            # VIEW FRUITS
            if ch == '1':
                print("\nID | Name | Qty | Price")
                for f in fruits:
                    print(f[0], f[1], f[2], f[3])

            # ADD TO CART
            elif ch == '2':
                fid = int(input("Enter Fruit ID: "))
                qty = int(input("Quantity: "))

                for f in fruits:
                    if f[0] == fid:
                        if qty <= f[2]:
                            cost = qty * f[3]
                            cart.append([f[0], f[1], qty, cost])
                            f[2] -= qty
                            print("Added to cart!")
                        else:
                            print("Not enough stock!")
                        break
                else:
                    print("Invalid ID!")

            # REMOVE FROM CART
            elif ch == '3':
                name = input("Enter fruit name to remove: ")
                for item in cart:
                    if item[1].lower() == name.lower():
                        # return stock back
                        for f in fruits:
                            if f[0] == item[0]:
                                f[2] += item[2]
                        cart.remove(item)
                        print("Removed from cart!")
                        break
                else:
                    print("Item not in cart!")

            # TOTAL COST
            elif ch == '4':
                total = sum(item[3] for item in cart)
                print("Total Cost = ₹", total)

            # BILL
            elif ch == '5':
                print("\n🧾 FINAL BILL")
                total = 0
                for item in cart:
                    print(item[1], "x", item[2], "= ₹", item[3])
                    total += item[3]
                print("Grand Total = ₹", total)

            elif ch == '6':
                break
            else:
                print("Invalid choice!")

#============== OWNER SECTION ========


    elif role == '2':
        while True:
            print("\n--- OWNER MENU ---")
            print("1. View Fruits")
            print("2. Add Fruit")
            print("3. Delete Fruit")
            print("4. Modify Fruit")
            print("5. Item Profit")
            print("6. Total Profit")
            print("7. Back")

            ch = input("Choose: ")

            # VIEW
            if ch == '1':
                for f in fruits:
                    print(f)

            # ADD
            elif ch == '2':
                new_id = fruits[-1][0] + 1
                name = input("Fruit name: ")
                qty = int(input("Quantity: "))
                sp = int(input("Selling price: "))
                cp = int(input("Cost price: "))
                fruits.append([new_id, name, qty, sp, cp])
                print("Fruit added!")

            # DELETE
            elif ch == '3':
                fid = int(input("Fruit ID: "))
                for f in fruits:
                    if f[0] == fid:
                        fruits.remove(f)
                        print("Fruit deleted!")
                        break
                else:
                    print("Fruit not found!")

            # MODIFY
            elif ch == '4':
                fid = int(input("Fruit ID: "))
                for f in fruits:
                    if f[0] == fid:
                        f[2] = int(input("New Quantity: "))
                        f[3] = int(input("New Selling Price: "))
                        f[4] = int(input("New Cost Price: "))
                        print("Fruit updated!")
                        break
                else:
                    print("Fruit not found!")

            # ITEM PROFIT
            elif ch == '5':
                print("\nItem Profit:")
                for f in fruits:
                    print(f[1], "Profit per item =", f[3] - f[4])

            # TOTAL PROFIT
            elif ch == '6':
                profit = 0
                for f in fruits:
                    profit += (f[3] - f[4]) * f[2]
                print("Total Profit:", profit)

            elif ch == '7':
                break
            else:
                print("Invalid choice!")

    elif role == '3':
        print("Thank you! Visit again 🍉")
        break
    else:
        print("Invalid choice!")



                
