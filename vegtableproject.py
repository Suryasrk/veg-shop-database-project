import pymysql as vegs
import random
from datetime import date

con = vegs.connect(
    host="localhost",
    user="root",
    password="Sathvik@121",
    database="veg"
)
cur = con.cursor()


def print_line():
    print("-" * 80)



def shopkeeper():
    while True:
        print("\n1. View Vegetables")
        print("2. Add Vegetable")
        print("3. Delete Vegetable")
        print("4. Modify Quantity")
        print("5. Itemized Profit")
        print("6. Total Profit (Particular Day)")
        print("7. Total Profit (All Days)")
        print("8. View Sales History")
        print("9. Exit\n")

        ch = input("Enter option: ")


        if ch == '1':
            cur.execute("SELECT veg_name, quantity, sell_price, cost_price FROM vegetables")
            rows = cur.fetchall()

            print_line()
            print(f"{'VEGETABLE':<20}{'QTY':<10}{'SELL':<10}{'COST':<10}")
            print_line()

            for r in rows:
                print(f"{r[0]:<20}{r[1]:<10}{r[2]:<10}{r[3]:<10}")

            print_line()


        elif ch == '2':
            name = input("Vegetable name: ")
            qty = int(input("Quantity: "))
            sp = int(input("Selling price: "))
            cp = int(input("Cost price: "))

            cur.execute(
                "INSERT INTO vegetables (veg_name, quantity, sell_price, cost_price) VALUES (%s,%s,%s,%s)",
                (name, qty, sp, cp)
            )
            con.commit()
            print("Vegetable added!")


        elif ch == '3':
            name = input("Vegetable name: ")
            cur.execute("DELETE FROM vegetables WHERE veg_name=%s", (name,))
            con.commit()
            print("Deleted!")


        elif ch == '4':
            name = input("Vegetable name: ")
            qty = int(input("Quantity to add: "))

            cur.execute(
                "UPDATE vegetables SET quantity = quantity + %s WHERE veg_name=%s",
                (qty, name)
            )
            con.commit()
            print("Updated!")

        elif ch == '5':
            cur.execute("""
                SELECT veg_name,
                SUM((sell_price - cost_price) * quantity)
                AS profit FROM sales_history GROUP BY veg_name
            """)
            rows = cur.fetchall()

            print_line()
            print(f"{'VEGETABLE':<20}{'PROFIT':<10}")
            print_line()

            for r in rows:
                print(f"{r[0]:<20}{r[1]:<10}")

            print_line()


        elif ch == '6':
            d = input("Enter date (YYYY-MM-DD): ")

            cur.execute(
                "SELECT SUM((sell_price - cost_price) * quantity) \
                 FROM sales_history \
                 WHERE DATE(sale_date) = %s",
                (d,)
            )
            total = cur.fetchone()[0]

            print("Profit on", d, "=", total if total else 0)


        elif ch == '7':
            cur.execute("""SELECT SUM((sell_price - cost_price) * quantity)FROM sales_history """)

            total = cur.fetchone()[0]

            print("Total Profit =", total if total else 0)


        elif ch == '8':
            cur.execute("""
                SELECT name, mobile, veg_name, quantity, total_price, sale_date
                FROM sales_history
            """)

            rows = cur.fetchall()

            print_line()
            print(f"{'NAME':<12}{'MOBILE':<15}{'VEGETABLE':<15}{'QTY':<8}{'PRICE':<10}{'DATE'}")
            print_line()

            for r in rows:
                print(f"{r[0]:<12}{r[1]:<15}{r[2]:<15}{r[3]:<8}{r[4]:<10}{r[5]}")

            print_line()



        elif ch == '9':
            break



def customer(user_id, name, mobile):

    while True:
        print("\n1. View Vegetables")
        print("2. Add to Cart")
        print("3. View Cart")
        print("4. Modify Cart Quantity")
        print("5. Delete Item from Cart")
        print("6. Bill")
        print("7. Exit")

        ch = input("Enter option: ")


        if ch == '1':
            cur.execute("SELECT veg_name, quantity, sell_price FROM vegetables")
            rows = cur.fetchall()

            print_line()
            print(f"{'VEGETABLE':<20}{'QTY':<10}{'SELL':<10}")
            print_line()

            for r in rows:
                print(f"{r[0]:<20}{r[1]:<10}{r[2]:<10}")
            print_line()


        elif ch == '2':
            veg = input("Vegetable name: ")
            qty = int(input("Quantity: "))

            cur.execute("SELECT sell_price, quantity FROM vegetables WHERE veg_name=%s", (veg,))
            data = cur.fetchone()

            if data and qty <= data[1]:

                price = qty * data[0]

                cur.execute(
                    "SELECT quantity, price FROM cart WHERE user_id=%s AND veg_name=%s",
                    (user_id, veg)
                )
                exist = cur.fetchone()

                if exist:
                    cur.execute("""
                        UPDATE cart
                        SET quantity=quantity+%s, price=price+%s
                        WHERE user_id=%s AND veg_name=%s
                    """, (qty, price, user_id, veg))
                else:
                    cur.execute(
                        "INSERT INTO cart (user_id, veg_name, quantity, price) VALUES (%s,%s,%s,%s)",
                        (user_id, veg, qty, price)
                    )

                cur.execute(
                    "UPDATE vegetables SET quantity=quantity-%s WHERE veg_name=%s",
                    (qty, veg)
                )

                con.commit()
                print("Added!")

        elif ch == '3':

            cur.execute(
                "SELECT veg_name, quantity, price FROM cart WHERE user_id=%s",
                (user_id,)
            )
            rows = cur.fetchall()

            if not rows:
                print("Cart is empty!")
                continue

            print_line()
            print(f"{'VEGETABLE':<20}{'QTY':<10}{'PRICE':<10}")
            print_line()

            total = 0
            for veg_name, qty, price in rows:
                print(f"{veg_name:<20}{qty:<10}{price:<10}")
                total += price

            print_line()
            print("TOTAL =", total)


        elif ch == '4':

            veg = input("Vegetable name: ")


            cur.execute(
                "SELECT quantity FROM cart WHERE user_id=%s AND veg_name=%s",
                (user_id, veg)
            )
            row = cur.fetchone()

            if not row:
                print("Item not in cart!")
                continue

            current_qty = row[0]

            print("\n1. Increase quantity")
            print("2. Decrease quantity")
            choice = input("Choose option: ")

            change = int(input("Enter quantity: "))


            cur.execute(
                "SELECT sell_price, quantity FROM vegetables WHERE veg_name=%s",
                (veg,)
            )
            sp, stock = cur.fetchone()


            if choice == '1':

                if change > stock:
                    print("Not enough stock!")
                    continue

                new_qty = current_qty + change
                new_price = new_qty * sp


                cur.execute(
                    "UPDATE cart SET quantity=%s, price=%s WHERE user_id=%s AND veg_name=%s",
                    (new_qty, new_price, user_id, veg)
                )


                cur.execute(
                    "UPDATE vegetables SET quantity = quantity - %s WHERE veg_name=%s",
                    (change, veg)
                )

                print("Quantity increased!")


            elif choice == '2':

                if change > current_qty:
                    print("Cannot decrease more than cart quantity!")
                    continue

                new_qty = current_qty - change


                cur.execute(
                    "UPDATE vegetables SET quantity = quantity + %s WHERE veg_name=%s",
                    (change, veg)
                )

                if new_qty == 0:

                    cur.execute(
                        "DELETE FROM cart WHERE user_id=%s AND veg_name=%s",
                        (user_id, veg)
                    )
                    print("Item removed from cart!")
                else:
                    new_price = new_qty * sp

                    cur.execute(
                        "UPDATE cart SET quantity=%s, price=%s WHERE user_id=%s AND veg_name=%s",
                        (new_qty, new_price, user_id, veg)
                    )

                    print("Quantity decreased!")

            else:
                print("Invalid choice!")
                continue

            con.commit()


        elif ch == '5':

            veg = input("Vegetable name: ")

            cur.execute(
                "SELECT quantity FROM cart WHERE user_id=%s AND veg_name=%s",
                (user_id, veg)
            )
            row = cur.fetchone()

            if not row:
                print("Item not found!")
                continue

            qty = row[0]


            cur.execute(
                "UPDATE vegetables SET quantity = quantity + %s WHERE veg_name=%s",
                (qty, veg)
            )


            cur.execute(
                "DELETE FROM cart WHERE user_id=%s AND veg_name=%s",
                (user_id, veg)
            )

            con.commit()
            print("Item removed!")




        elif ch == '6':

            cur.execute(
                "SELECT veg_name, quantity, price FROM cart WHERE user_id=%s",
                (user_id,)
            )
            items = cur.fetchall()

            if not items:
                print("Cart is empty!")
                continue

            total_bill = 0

            print_line()
            print("BILL")
            print_line()

            for veg_name, qty, total_price in items:

                cur.execute(
                    "SELECT sell_price, cost_price FROM vegetables WHERE veg_name=%s",
                    (veg_name,)
                )
                sp, cp = cur.fetchone()

                print(f"{veg_name:<15} {qty} x {sp} = {total_price}")

                cur.execute("""
                    INSERT INTO sales_history
                    (user_id, name, mobile, veg_name, quantity, sell_price, cost_price, total_price)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (user_id, name, mobile, veg_name, qty, sp, cp, total_price))

                total_bill += total_price


            cur.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))

            con.commit()

            print_line()
            print("TOTAL BILL =", total_bill)
            print_line()


        elif ch == '7':
            break



print("\n******** VEGETABLE STORE MANAGEMENT SYSTEM ********")

while True:
    print("\n1. Shopkeeper")
    print("2. Customer")
    print("3. Exit\n")

    choice = input("Enter choice: ")


    if choice == '1':
        u = input("Username: ")
        p = input("Password: ")

        cap = random.randint(1000, 9999)
        print("Captcha:", cap)

        if input("Enter captcha: ") != str(cap):
            print("Wrong captcha!")
            continue

        if u == "Surya" and p == "Sathvik@121":
            shopkeeper()
        else:
            print("Invalid credentials!")


    elif choice == '2':

        while True:
            print("\n1. Login")
            print("2. Signup")
            print("3. Back\n")

            opt = input("Choose option: ")

            if opt == '1':

                mobile = input("Mobile: ")
                password = input("Password: ")

                cap = random.randint(1000, 9999)
                print("Captcha:", cap)

                if input("Enter captcha: ") != str(cap):
                    print("Wrong captcha!")
                    continue

                cur.execute(
                    "SELECT user_id,name,mobile FROM users WHERE mobile=%s AND password=%s",
                    (mobile, password)
                )
                user = cur.fetchone()

                if user:
                    customer(user[0], user[1], user[2])
                    break

            elif opt == '2':
                name = input("Name: ")
                mobile = input("Mobile: ")
                password = input("Password: ")

                cur.execute(
                    "INSERT INTO users VALUES (NULL,%s,%s,%s)",
                    (name, mobile, password)
                )
                con.commit()
                print("Signup successful! Please login.")

            elif opt == '3':
                break

    elif choice == '3':
        print('Thank You , Bye')
        break

con.close()
