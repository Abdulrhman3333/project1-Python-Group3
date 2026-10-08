
import json
import os

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
        self.tickets_total = tickets_available  # new: lets the UI draw a "sold" progress bar

    def parking_available(self):
        return self.parking_capacity - self.parking_reserved


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


def _find(items, event):
    return next((i for i in items if i.event is event), None)


def _merge(items, event, amount, kind):
    item = _find(items, event)
    if item is None:
        items.append(CartItem(event, amount) if kind == "ticket" else ParkingReservation(event, amount))
    elif kind == "ticket":
        item.tickets += amount
    else:
        item.spots += amount


class Store:
    

    def __init__(self):
        self.events = [
            Event("Boulevard World", 250, "Riyadh", "8:00 PM", "2026-10-10", tickets_available=100),
            Event("Comedy Show", 100, "Riyadh", "9:00 PM", "2026-10-15", tickets_available=60),
            Event("Kingdom Arena Boxing Night", 80, "Riyadh", "7:30 PM", "2026-10-20", tickets_available=80),
            Event("Winter Wonderland", 200, "Riyadh", "6:00 PM", "2026-10-25", tickets_available=40),
        ]
        self.cart = []
        self.parking_cart = []
        self.my_tickets = []
        self.parking_reservations = []
        self.load()

    def cart_total(self):
        return sum(i.total_price() for i in self.cart + self.parking_cart)

    
    def add_ticket(self, event):
        item = _find(self.cart, event)
        in_cart = item.tickets if item else 0
        if in_cart + 1 > event.tickets_available:
            return False, f"No more tickets left for {event.name}."
        _merge(self.cart, event, 1, "ticket")
        return True, f"{event.name} added to your cart."

    def change_tickets(self, event, delta):
        item = _find(self.cart, event)
        if item is None:
            return False, "That ticket is not in your cart."
        new = item.tickets + delta
        if new <= 0:
            self.cart.remove(item)
            return True, f"{event.name} removed from your cart."
        if new > event.tickets_available:
            return False, f"Only {event.tickets_available} tickets left for {event.name}."
        item.tickets = new
        return True, "Quantity updated."

    def remove_ticket(self, event):
        item = _find(self.cart, event)
        if item:
            self.cart.remove(item)
        return True, f"{event.name} removed from your cart."

   
    def add_parking(self, event, spots):
        item = _find(self.parking_cart, event)
        in_cart = item.spots if item else 0
        if spots < 1 or in_cart + spots > event.parking_available():
            return False, f"Not enough parking left for {event.name}."
        _merge(self.parking_cart, event, spots, "parking")
        return True, f"{spots} parking spot(s) for {event.name} added to your cart."

    def remove_parking(self, event):
        item = _find(self.parking_cart, event)
        if item:
            self.parking_cart.remove(item)
        return True, f"Parking for {event.name} removed from your cart."

   
    def checkout(self):
        if not self.cart and not self.parking_cart:
            return False, "Your cart is empty."
        for i in self.cart:
            if i.tickets > i.event.tickets_available:
                return False, f"Not enough tickets left for {i.event.name}. Update your cart."
        for i in self.parking_cart:
            if i.spots > i.event.parking_available():
                return False, f"Not enough parking left for {i.event.name}. Update your cart."

        total = self.cart_total()
        for i in self.cart:
            i.event.tickets_available -= i.tickets
            _merge(self.my_tickets, i.event, i.tickets, "ticket")
        for i in self.parking_cart:
            i.event.parking_reserved += i.spots
            _merge(self.parking_reservations, i.event, i.spots, "parking")
        self.cart.clear()
        self.parking_cart.clear()
        self.save()
        return True, f"Booking confirmed. You paid {total} SAR."

    
    def sell_ticket(self, event, amount=1):
        item = _find(self.my_tickets, event)
        if item is None or amount > item.tickets:
            return False, "You do not have that many tickets."
        item.tickets -= amount
        event.tickets_available += amount
        if item.tickets == 0:
            self.my_tickets.remove(item)
        self.save()
        return True, f"Sold {amount} ticket(s). Refund: {amount * event.price} SAR."

    def cancel_parking(self, event, amount=1):
        item = _find(self.parking_reservations, event)
        if item is None or amount > item.spots:
            return False, "You do not have that many parking spots."
        item.spots -= amount
        event.parking_reserved -= amount
        if item.spots == 0:
            self.parking_reservations.remove(item)
        self.save()
        return True, f"Cancelled {amount} spot(s). Refund: {amount * PARKING_PRICE} SAR."

    
    def save(self):
        data = {
            "tickets_available": {e.name: e.tickets_available for e in self.events},
            "parking_reserved": {e.name: e.parking_reserved for e in self.events},
            "my_tickets": {t.event.name: t.tickets for t in self.my_tickets},
            "parking_reservations": {p.event.name: p.spots for p in self.parking_reservations},
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE) as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return
        for e in self.events:
            e.tickets_available = data.get("tickets_available", {}).get(e.name, e.tickets_available)
            e.parking_reserved = data.get("parking_reserved", {}).get(e.name, 0)
            tickets = data.get("my_tickets", {}).get(e.name, 0)
            spots = data.get("parking_reservations", {}).get(e.name, 0)
            if tickets > 0:
                self.my_tickets.append(CartItem(e, tickets))
            if spots > 0:
                self.parking_reservations.append(ParkingReservation(e, spots))
