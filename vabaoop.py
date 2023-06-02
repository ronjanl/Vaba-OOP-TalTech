"""Online store."""

from datetime import date, datetime


class Item:
    """Item class."""

    def __init__(self, name: str, price: int):
        """
        Create an item.
        :param name: name of item
        :param price: price of item
        """
        if not isinstance(name, str):
            raise ValueError("Item name has to be a string.")
        else:
            self.name = name
        if price < 0:
            raise ValueError("Price can't be negative.")
        else:
            self.price = price
            
        
class Basket:
    """Basket class."""

    def __init__(self):
        """
        Create a basket.
        :param storage: items in basket
        """
        self.storage = []

    def add(self, item: Item, amount: int):
        """
        Add item to basket. The amount has to be positive and item has to be of Item class.
        :param item: item that is being added
        :param amount: amount that is being added
        """
        if amount <= 0 or not isinstance(amount, int):
            raise ValueError("This is not a valid amount.")
        if isinstance(item, Item):
            if item in self.storage:
                item.amount += amount
            else:
                self.storage.append(item)
                item.amount = amount
        else:
            raise ValueError("This is not a valid item.")

    def remove(self, item: Item, amount: int):
        """
        Remove item from basket. Item has to be in basket, of Item class, and more cannot be removed than is in the basket.
        :param item: item that is being removed
        :param amount: amount that is being removed
        """
        if amount < 0 or not isinstance(amount, int):
            raise ValueError("This is not a valid amount.") 
        if isinstance(item, Item):
            if item in self.storage:
                if item.amount - amount >= 0:
                    item.amount -= amount
                else:
                    raise ValueError("Cannot remove more than is in the basket.")
                if item.amount == 0:
                    self.storage.remove(item)
            else:
                raise ValueError("Item not in basket.")
        else:
            raise ValueError("This is not a valid item.")

        
class Client:
    """Client class."""

    def __init__(self, id: int, type: str, balance: int):
        """
        Create a client.
        :param id: client id
        :param type: client type (gold or regular)
        :param balance: how much money client has on their account
        """
        self.id = id
        if type not in ["gold", "regular"]:
            raise ValueError("This is not a valid type of client.")
        else:
            self.type = type
        if balance < 0:
            raise ValueError("Balance can't be negative.")
        else:
            self.balance = balance
        self.history = []
        self.basket = Basket()

    def get_history(self):
        """Return the purchase history."""
        return self.history


class Store:
    """Online store class."""

    def __init__(self):
        """
        Create an online store.
        :param storage: items and their amounts in store
        :param clients: registered clients
        :param purchases: purchases made from store
        """
        self.storage = {}
        self.clients = []
        self.purchases = []

    def purchase(self, client: Client, datetoday=date.today().strftime("%d.%m.%Y")):
        """
        Purchase items from store. Items cannot be bought if they're not in the store, if they're isn't a sufficient amount or if the client doesn't have enough money or hasn't been registered.
        :param client: client that is purchasing
        :param datetoday: current date
        """
        if client not in self.clients:
            raise ValueError("This client has not been registered.")
        cost = 0
        current = [datetoday]
        for item in client.basket.storage:
            if item.amount <= self.storage[item.name]:
                current.append(f"{item.name} x{item.amount}")
                cost += item.price * item.amount
                self.storage[item.name] = self.storage[item.name] - item.amount
                if self.storage[item.name] == 0:
                    del self.storage[item.name]
            else:
                raise ValueError("There is not enough of item in store.")
            
        if client.type == "gold":
            cost = 0.9 * cost

        if cost > client.balance:
            raise ValueError("Account doesn't have enough money to complete the purchase.")
        else:
            client.balance = round(client.balance - cost, 2)
      
        client.history.append(current.copy())
        current.insert(0, client.id)
        self.purchases.append(current)

        client.history.sort(key=lambda x: datetime.strptime(x[0], "%d.%m.%Y"), reverse=True)
        client.basket.storage.clear()

    def add_item(self, item: Item, amount):
        """
        Add item to store.
        :param item: item being added to store
        :param amount: amount of item being added
        """
        if amount <= 0 or not isinstance(amount, int):
            raise ValueError("This is not a valid amount.")
        if isinstance(item, Item):
            if item.name in self.storage:
                self.storage[item.name] += amount
            else:
                self.storage[item.name] = amount
        else:
            raise ValueError("This is not a valid item.")

    def add_client(self, client: Client):
        """
        Add client to store.
        :param client: client that is being added
        """
        if isinstance(client, Client):
            self.clients.append(client)
        else:
            raise ValueError("This is not a valid client.")
        
    def get_clients(self):
        """Get clients registered to store."""
        return self.clients
    
    def get_purchases(self):
        """Get purchases made in store."""
        return self.purchases
    
    def get_storage(self):
        """Get items and their amounts in store."""
        return self.storage