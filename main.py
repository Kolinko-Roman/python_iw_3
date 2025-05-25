import json
import threading
from uuid import uuid4

# --- МОДЕЛІ ---

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

class Train:
    def __init__(self, train_id, destination, seats):
        self.train_id = train_id
        self.destination = destination
        self.seats = seats
        self.lock = threading.Lock()

class Ticket:
    def __init__(self, ticket_id, user_id, train_id):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.train_id = train_id

# --- СИСТЕМА БРОНЮВАННЯ ---

class BookingSystem:
    def __init__(self):
        self.users = {}
        self.trains = {}
        self.tickets = []

    def add_user(self, name):
        user_id = str(uuid4())
        user = User(user_id, name)
        self.users[user_id] = user
        return user

    def add_train(self, destination, seats):
        train_id = str(uuid4())
        train = Train(train_id, destination, seats)
        self.trains[train_id] = train
        return train

    def book_ticket(self, user_id, train_id):
        train = self.trains[train_id]
        with train.lock:
            if train.seats > 0:
                train.seats -= 1
                ticket_id = str(uuid4())
                ticket = Ticket(ticket_id, user_id, train_id)
                self.tickets.append(ticket)
                self.save_bookings()
                return ticket
            else:
                print("Немає вільних місць")
                return None

    def save_bookings(self):
        data = [{"ticket_id": t.ticket_id, "user_id": t.user_id, "train_id": t.train_id} for t in self.tickets]
        with open('bookings.json', 'w') as f:
            json.dump(data, f, indent=4)

# --- ПРИКЛАД ВИКОРИСТАННЯ З БАГАТОПОТОЧНІСТЮ ---

system = BookingSystem()
user = system.add_user("Олена")
train = system.add_train("Львів", 2)

threads = []
for _ in range(4):
    t = threading.Thread(target=system.book_ticket, args=(user.user_id, train.train_id))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
