# ==========================================
# OOP
# ==========================================

class Event:

    def __init__(self, name, price, location, time, date):
        self.name = name
        self.price = price
        self.location = location
        self.time = time
        self.date = date

    def display_details(self):
        print(f"Title: {self.name}")
        print(f"Price: {self.price} SAR")
        print(f"Location: {self.location}")
        print(f"Time: {self.time}")
        print(f"Date: {self.date}")


class CartItem:

    def __init__(self, event, tickets=1):
        self.event = event
        self.tickets = tickets

    def total_price(self):
        return self.event.price * self.tickets


# ==========================================
# Data
# ==========================================

events = [
    Event("Boulevard World", 350, "Riyadh", "8:00 PM", "2026-10-10"),
    Event("Comedy Show", 100, "Riyadh", "9:00 PM", "2026-10-15"),
    Event("Kingdom Arena Boxing Night", 80, "Riyadh", "7:30 PM", "2026-10-20"),
    Event("Winter Wonderland", 200, "Riyadh", "6:00 PM", "2026-10-25")
]

cart = []


# ==========================================
# 👤 PERSON 1
# Requirements 1, 2, 3
# ==========================================


# 1. Browse all available events

def show_events():

    print("\n===== Available Events =====")

    for i in range(len(events)):
        print(f"{i + 1}. {events[i].name} - {events[i].price} SAR")


# 2. View event details

def view_event_details():

    show_events()

    choice = int(input("\nEnter event number: "))

    if choice >= 1 and choice <= len(events):
        events[choice - 1].display_details()

    else:
        print("Invalid event number.")


# 3. Search for an event by name

def search_event():

    name = input("\nEnter event name to search: ")

    found = False

    for event in events:

        if name.lower() in event.name.lower():
            event.display_details()
            found = True

    if found == False:
        print("Event not found.")


# ==========================================
# 👤 PERSON 2
# Requirements 4, 5, 6
# ==========================================


# 4. Add an event ticket to cart

def add_to_cart():

    show_events()

    choice = int(input("\nEnter event number: "))

    if choice >= 1 and choice <= len(events):

        selected_event = events[choice - 1]

        found = False

        for item in cart:

            if item.event == selected_event:
                item.tickets += 1
                found = True
                print("Ticket quantity increased.")

        if found == False:
            cart.append(CartItem(selected_event))
            print(f"{selected_event.name} added to your cart.")

    else:
        print("Invalid event number.")


# 5. Remove an event ticket from cart

def remove_from_cart():

    if len(cart) == 0:
        print("\nYour cart is empty.")
        return

    show_cart()

    choice = int(input("\nEnter cart item number to remove: "))

    if choice >= 1 and choice <= len(cart):

        removed_item = cart.pop(choice - 1)

        print(f"{removed_item.event.name} removed from your cart.")

    else:
        print("Invalid cart item number.")


# 6. List all events currently in cart

def show_cart():

    print("\n===== Your Cart =====")

    if len(cart) == 0:
        print("Your cart is empty.")
        return

    total = 0

    for i in range(len(cart)):

        item = cart[i]

        print(f"{i + 1}. {item.event.name}")
        print(f"   Tickets: {item.tickets}")
        print(f"   Price per ticket: {item.event.price} SAR")
        print(f"   Total: {item.total_price()} SAR")

        total += item.total_price()

    print("------------------------")
    print(f"Cart Total: {total} SAR")


# ==========================================
# 👥 ADDITIONAL REQUIREMENTS
# ==========================================


# 7. Modify the number of tickets

def modify_tickets():

    if len(cart) == 0:
        print("\nYour cart is empty.")
        return

    show_cart()

    choice = int(input("\nEnter cart item number: "))

    if choice >= 1 and choice <= len(cart):

        number = int(input("Enter new number of tickets: "))

        if number > 0:
            cart[choice - 1].tickets = number
            print("Ticket quantity updated.")

        else:
            print("Number of tickets must be greater than 0.")

    else:
        print("Invalid cart item number.")


# 8. Checkout

def checkout():

    if len(cart) == 0:
        print("\nYour cart is empty.")
        return

    print("\n===== Checkout =====")

    total = 0

    for item in cart:

        print(f"Event: {item.event.name}")
        print(f"Tickets: {item.tickets}")
        print(f"Total: {item.total_price()} SAR")
        print("------------------------")

        total += item.total_price()

    print(f"Grand Total: {total} SAR")

    confirm = input("Confirm reservation? (yes/no): ")

    if confirm.lower() == "yes":

        print("\n===== Reservation Confirmation =====")

        for item in cart:

            print(f"Event: {item.event.name}")
            print(f"Tickets: {item.tickets}")
            print(f"Total: {item.total_price()} SAR")

        print(f"\nGrand Total: {total} SAR")
        print("Reservation confirmed successfully!")
        print("Thank you for your reservation.")

        cart.clear()

    else:
        print("Reservation cancelled.")


# ==========================================
# MAIN PROGRAM
# ==========================================

while True:

    print("\n================================")
    print("    Entertainment Events")
    print("================================")

    print("1. Browse all events")
    print("2. View event details")
    print("3. Search for an event")
    print("4. Add an event ticket to cart")
    print("5. Remove an event ticket from cart")
    print("6. List all events in cart")
    print("7. Modify number of tickets")
    print("8. Checkout")
    print("9. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        show_events()

    elif choice == "2":
        view_event_details()

    elif choice == "3":
        search_event()

    elif choice == "4":
        add_to_cart()

    elif choice == "5":
        remove_from_cart()

    elif choice == "6":
        show_cart()

    elif choice == "7":
        modify_tickets()

    elif choice == "8":
        checkout()

    elif choice == "9":
        print("Thank you for using the Entertainment Events platform!")
        break

    else:
        print("Invalid choice. Please try again.")