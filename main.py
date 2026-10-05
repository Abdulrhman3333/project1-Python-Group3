import json
import os

# ==========================================
# OOP
# ==========================================

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

PARKING_PRICE = 20


class Event:

    def __init__(self, name, price, location, time, date, parking_capacity=50, tickets_available=100):
        self.name = name
        self.price = price
        self.location = location
        self.time = time
        self.date = date
        self.parking_capacity = parking_capacity
        self.parking_reserved = 0
        self.tickets_available = tickets_available

    def parking_available(self):
        return self.parking_capacity - self.parking_reserved

    def display_details(self):
        print(f"Title: {self.name}")
        print(f"Price: {self.price} SAR")
        print(f"Location: {self.location}")
        print(f"Time: {self.time}")
        print(f"Date: {self.date}")
        print(f"Tickets left: {self.tickets_available}")
        print(f"Parking spots left: {self.parking_available()} ({PARKING_PRICE} SAR per spot)")


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
    Event("Boulevard World", 250, "Riyadh", "8:00 PM", "2026-10-10", tickets_available=100),
    Event("Comedy Show", 100, "Riyadh", "9:00 PM", "2026-10-15", tickets_available=60),
    Event("Kingdom Arena Boxing Night", 80, "Riyadh", "7:30 PM", "2026-10-20", tickets_available=80),
    Event("Winter Wonderland", 200, "Riyadh", "6:00 PM", "2026-10-25", tickets_available=40)
]

cart = []                    # tickets waiting for checkout
parking_cart = []            # parking waiting for checkout
my_tickets = []              # tickets already bought
parking_reservations = []    # parking already reserved


# ==========================================
# Helpers
# ==========================================

# Asks until the user enters a number from low to high (0 = go back, returns None)

def get_number(prompt, low, high):

    while True:

        text = input(f"{prompt} (0 to go back): ").strip()

        if text.isdigit():

            number = int(text)

            if number == 0:
                return None

            if number >= low and number <= high:
                return number

        print(f"Please enter a number between {low} and {high}, or 0 to go back.")


# Shows the events and returns the one the user picked (or None)

def pick_event():

    show_events()

    choice = get_number("\nEnter event number", 1, len(events))

    if choice is None:
        return None

    return events[choice - 1]


# Adds tickets/spots to a list, merging with an existing item for the same event

def add_to_list(items, event, amount, is_parking):

    for item in items:

        if item.event == event:

            if is_parking:
                item.spots += amount
            else:
                item.tickets += amount

            return

    if is_parking:
        items.append(ParkingReservation(event, amount))
    else:
        items.append(CartItem(event, amount))


def cart_total():

    item_total = lambda item: item.total_price()

    return sum(map(item_total, cart)) + sum(map(item_total, parking_cart))


def save_data():

    data = {
        "tickets_available": {e.name: e.tickets_available for e in events},
        "parking_reserved": {e.name: e.parking_reserved for e in events},
        "my_tickets": {t.event.name: t.tickets for t in my_tickets},
        "parking_reservations": {p.event.name: p.spots for p in parking_reservations}
    }

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=2)


def load_data():

    if not os.path.exists(DATA_FILE):
        return

    try:
        with open(DATA_FILE) as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Saved data could not be read. Starting fresh.")
        return

    for event in events:

        event.tickets_available = data.get("tickets_available", {}).get(event.name, event.tickets_available)
        event.parking_reserved = data.get("parking_reserved", {}).get(event.name, 0)

        tickets = data.get("my_tickets", {}).get(event.name, 0)
        spots = data.get("parking_reservations", {}).get(event.name, 0)

        if tickets > 0:
            my_tickets.append(CartItem(event, tickets))

        if spots > 0:
            parking_reservations.append(ParkingReservation(event, spots))


# ==========================================
# 👤 PERSON 1
# Requirements 1, 2, 3
# ==========================================


# 1. Browse all available events

def show_events():

    print("\n===== Available Events =====")

    for i in range(len(events)):

        event = events[i]

        if event.tickets_available == 0:
            status = "SOLD OUT"
        else:
            status = f"{event.tickets_available} left"

        print(f"{i + 1}. {event.name} - {event.price} SAR ({status})")


# 2. View event details

def view_event_details():

    event = pick_event()

    if event is not None:
        print()
        event.display_details()


# 3. Search for an event by name

def search_event():

    name = input("\nEnter event name to search: ").strip()

    found = False

    for event in events:

        if name.lower() in event.name.lower():
            print()
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

    selected_event = pick_event()

    if selected_event is None:
        return

    in_cart = 0

    for item in cart:

        if item.event == selected_event:
            in_cart = item.tickets

    if in_cart + 1 > selected_event.tickets_available:
        print(f"Sorry, no more tickets available for {selected_event.name}.")
        return

    if in_cart > 0:
        add_to_list(cart, selected_event, 1, False)
        print("Ticket quantity increased.")

    else:
        add_to_list(cart, selected_event, 1, False)
        print(f"{selected_event.name} added to your cart.")


# 5. Remove an event ticket from cart

def remove_from_cart():

    if len(cart) == 0:
        print("\nYour cart has no tickets.")
        return

    show_cart()

    choice = get_number("\nEnter cart item number to remove", 1, len(cart))

    if choice is None:
        return

    removed_item = cart.pop(choice - 1)

    print(f"{removed_item.event.name} removed from your cart.")


# 6. List all events currently in cart

def show_cart():

    print("\n===== Your Cart =====")

    if len(cart) == 0 and len(parking_cart) == 0:
        print("Your cart is empty.")
        return

    if len(cart) > 0:

        print("Tickets:")

        for i in range(len(cart)):

            item = cart[i]

            print(f"{i + 1}. {item.event.name}")
            print(f"   Tickets: {item.tickets}")
            print(f"   Price per ticket: {item.event.price} SAR")
            print(f"   Total: {item.total_price()} SAR")

    if len(parking_cart) > 0:

        print("Parking:")

        for i in range(len(parking_cart)):

            item = parking_cart[i]

            print(f"{i + 1}. {item.event.name}")
            print(f"   Spots: {item.spots}")
            print(f"   Price per spot: {PARKING_PRICE} SAR")
            print(f"   Total: {item.total_price()} SAR")

    print("------------------------")
    print(f"Cart Total: {cart_total()} SAR")


# ==========================================
# 👥 ADDITIONAL REQUIREMENTS
# ==========================================


# 7. Modify the number of tickets

def modify_tickets():

    if len(cart) == 0:
        print("\nYour cart has no tickets.")
        return

    show_cart()

    choice = get_number("\nEnter cart item number", 1, len(cart))

    if choice is None:
        return

    item = cart[choice - 1]

    if item.event.tickets_available == 0:
        print("This event is sold out.")
        return

    number = get_number(f"Enter new number of tickets (max {item.event.tickets_available})",
                        1, item.event.tickets_available)

    if number is None:
        return

    item.tickets = number
    print("Ticket quantity updated.")


# 8. Checkout

def checkout():

    if len(cart) == 0 and len(parking_cart) == 0:
        print("\nYour cart is empty.")
        return

    print("\n===== Checkout =====")

    for item in cart:

        print(f"Event: {item.event.name}")
        print(f"Tickets: {item.tickets}")
        print(f"Total: {item.total_price()} SAR")
        print("------------------------")

    for item in parking_cart:

        print(f"Event: {item.event.name}")
        print(f"Parking spots: {item.spots}")
        print(f"Total: {item.total_price()} SAR")
        print("------------------------")

    total = cart_total()

    print(f"Grand Total: {total} SAR")

    confirm = input("Confirm reservation? (yes/no): ").strip().lower()

    if confirm == "yes" or confirm == "y":

        for item in cart:

            if item.tickets > item.event.tickets_available:
                print(f"Sorry, not enough tickets left for {item.event.name}. Please update your cart.")
                return

        for item in parking_cart:

            if item.spots > item.event.parking_available():
                print(f"Sorry, not enough parking left for {item.event.name}. Please update your cart.")
                return

        print("\n===== Reservation Confirmation =====")

        for item in cart:

            print(f"Event: {item.event.name}")
            print(f"Tickets: {item.tickets}")
            print(f"Total: {item.total_price()} SAR")

            item.event.tickets_available -= item.tickets
            add_to_list(my_tickets, item.event, item.tickets, False)

        for item in parking_cart:

            print(f"Event: {item.event.name}")
            print(f"Parking spots: {item.spots}")
            print(f"Total: {item.total_price()} SAR")

            item.event.parking_reserved += item.spots
            add_to_list(parking_reservations, item.event, item.spots, True)

        print(f"\nGrand Total: {total} SAR")
        print("Reservation confirmed successfully!")
        print("Thank you for your reservation.")

        cart.clear()
        parking_cart.clear()

        save_data()

    else:
        print("Reservation cancelled.")


# ==========================================
# 👥 NEW FEATURES
# ==========================================


# 9. Sell a purchased ticket

def sell_ticket():

    if len(my_tickets) == 0:
        print("\nYou have no tickets to sell. Tickets appear here after a confirmed checkout.")
        return

    print("\n===== My Tickets =====")

    for i in range(len(my_tickets)):
        ticket = my_tickets[i]
        print(f"{i + 1}. {ticket.event.name} - {ticket.tickets} ticket(s)")

    choice = get_number("\nEnter ticket number to sell", 1, len(my_tickets))

    if choice is None:
        return

    ticket = my_tickets[choice - 1]

    amount = get_number(f"Enter number of tickets to sell (max {ticket.tickets})", 1, ticket.tickets)

    if amount is None:
        return

    refund = amount * ticket.event.price

    ticket.tickets -= amount
    ticket.event.tickets_available += amount

    if ticket.tickets == 0:
        my_tickets.remove(ticket)

    save_data()

    print(f"You sold {amount} ticket(s) for {ticket.event.name}.")
    print(f"Refund amount: {refund} SAR")


# 10. Reserve parking for an event (added to the cart, paid at checkout)

def reserve_parking():

    selected_event = pick_event()

    if selected_event is None:
        return

    in_cart = 0

    for item in parking_cart:

        if item.event == selected_event:
            in_cart = item.spots

    available = selected_event.parking_available() - in_cart

    print(f"\nAvailable parking spots: {available}")
    print(f"Price per spot: {PARKING_PRICE} SAR")

    if available <= 0:
        print("No parking spots available for this event.")
        return

    spots = get_number("Enter number of parking spots to reserve", 1, available)

    if spots is None:
        return

    add_to_list(parking_cart, selected_event, spots, True)

    print(f"{spots} parking spot(s) for {selected_event.name} added to your cart.")


# 11. Remove parking from cart

def remove_parking_from_cart():

    if len(parking_cart) == 0:
        print("\nYour cart has no parking.")
        return

    show_cart()

    choice = get_number("\nEnter parking item number to remove", 1, len(parking_cart))

    if choice is None:
        return

    removed_item = parking_cart.pop(choice - 1)

    print(f"Parking for {removed_item.event.name} removed from your cart.")


# 12. Cancel a parking reservation

def cancel_parking():

    if len(parking_reservations) == 0:
        print("\nYou have no parking reservations. They appear here after a confirmed checkout.")
        return

    print("\n===== My Parking =====")

    for i in range(len(parking_reservations)):
        parking = parking_reservations[i]
        print(f"{i + 1}. {parking.event.name} - {parking.spots} spot(s)")

    choice = get_number("\nEnter parking number to cancel", 1, len(parking_reservations))

    if choice is None:
        return

    parking = parking_reservations[choice - 1]

    amount = get_number(f"Enter number of spots to cancel (max {parking.spots})", 1, parking.spots)

    if amount is None:
        return

    refund = amount * PARKING_PRICE

    parking.spots -= amount
    parking.event.parking_reserved -= amount

    if parking.spots == 0:
        parking_reservations.remove(parking)

    save_data()

    print(f"You cancelled {amount} parking spot(s) for {parking.event.name}.")
    print(f"Refund amount: {refund} SAR")


# 13. View my tickets and parking

def show_my_bookings():

    print("\n===== My Bookings =====")

    if len(my_tickets) == 0 and len(parking_reservations) == 0:
        print("You have no tickets or parking yet.")
        return

    print("Tickets:")

    if len(my_tickets) == 0:
        print("  (none)")

    for i in range(len(my_tickets)):
        ticket = my_tickets[i]
        print(f"  {i + 1}. {ticket.event.name} ({ticket.event.date}) - {ticket.tickets} ticket(s)")

    print("Parking:")

    if len(parking_reservations) == 0:
        print("  (none)")

    for i in range(len(parking_reservations)):
        parking = parking_reservations[i]
        print(f"  {i + 1}. {parking.event.name} ({parking.event.date}) - {parking.spots} spot(s)")


# ==========================================
# MAIN PROGRAM
# ==========================================

load_data()

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
    print("11. Remove parking from cart")
    print("12. Cancel parking")
    print("13. My tickets and parking")
    print("14. Exit")

    choice = input("\nEnter your choice: ").strip()

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
        remove_parking_from_cart()

    elif choice == "12":
        cancel_parking()

    elif choice == "13":
        show_my_bookings()

    elif choice == "14":
        save_data()
        print("Thank you for using the Entertainment Events platform!")
        break

    else:
        print("Invalid choice. Please try again.")
