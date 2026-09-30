# ==========================================
# OOP
# ==========================================

class Event:

    def __init__(self, name, price, location, time, date, parking_capacity=50):
        self.name = name
        self.price = price
        self.location = location
        self.time = time
        self.date = date
        self.parking_capacity = parking_capacity
        self.parking_reserved = 0

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


class ParkingReservation:

    def __init__(self, event, spots):
        self.event = event
        self.spots = spots

    def total_price(self):
        return self.spots * PARKING_PRICE


# ==========================================
# Data
# ==========================================

events = [
    Event("Boulevard World", 250, "Riyadh", "8:00 PM", "2026-10-10"),
    Event("Comedy Show", 100, "Riyadh", "9:00 PM", "2026-10-15"),
    Event("Kingdom Arena Boxing Night", 80, "Riyadh", "7:30 PM", "2026-10-20"),
    Event("Winter Wonderland", 200, "Riyadh", "6:00 PM", "2026-10-25")
]

cart = []
my_tickets = []
parking_reservations = []

PARKING_PRICE = 20


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

        for item in cart:
            my_tickets.append(CartItem(item.event, item.tickets))

        cart.clear()

    else:
        print("Reservation cancelled.")


# ==========================================
# 👥 NEW FEATURES
# ==========================================


# 9. Sell a purchased ticket

def sell_ticket():

    if len(my_tickets) == 0:
        print("\nYou have no tickets to sell.")
        return

    print("\n===== My Tickets =====")

    for i in range(len(my_tickets)):
        ticket = my_tickets[i]
        print(f"{i + 1}. {ticket.event.name} - {ticket.tickets} ticket(s)")

    choice = int(input("\nEnter ticket number to sell: "))

    if choice >= 1 and choice <= len(my_tickets):

        ticket = my_tickets[choice - 1]

        amount = int(input(f"Enter number of tickets to sell (max {ticket.tickets}): "))

        if amount >= 1 and amount <= ticket.tickets:

            refund = amount * ticket.event.price

            ticket.tickets -= amount

            if ticket.tickets == 0:
                my_tickets.pop(choice - 1)

            print(f"You sold {amount} ticket(s) for {ticket.event.name}.")
            print(f"Refund amount: {refund} SAR")

        else:
            print("Invalid number of tickets.")

    else:
        print("Invalid ticket number.")


# 10. Reserve parking for an event

def reserve_parking():

    show_events()

    choice = int(input("\nEnter event number: "))

    if choice >= 1 and choice <= len(events):

        selected_event = events[choice - 1]

        available = selected_event.parking_capacity - selected_event.parking_reserved

        print(f"\nAvailable parking spots: {available}")
        print(f"Price per spot: {PARKING_PRICE} SAR")

        if available == 0:
            print("No parking spots available for this event.")
            return

        spots = int(input("Enter number of parking spots to reserve: "))

        if spots >= 1 and spots <= available:

            selected_event.parking_reserved += spots

            parking_reservations.append(ParkingReservation(selected_event, spots))

            total = spots * PARKING_PRICE

            print(f"\nParking reserved for {selected_event.name}.")
            print(f"Spots reserved: {spots}")
            print(f"Total: {total} SAR")

        else:
            print("Invalid number of parking spots.")

    else:
        print("Invalid event number.")


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
    print("9. Sell a ticket")
    print("10. Reserve parking")
    print("11. Exit")

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
        sell_ticket()

    elif choice == "10":
        reserve_parking()

    elif choice == "11":
        print("Thank you for using the Entertainment Events platform!")
        break

    else:
        print("Invalid choice. Please try again.")