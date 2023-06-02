"""Online store tests."""

from vabaoop import Item, Basket, Client, Store
from datetime import date

apelsin = Item("apelsin", 4)
banaan = Item("banaan", 3)
arbuus = Item("arbuus", 5)

def test_item_name_is_not_valid():
    """Item should only accept string as name."""
    try:
        Item(12345, 7)
        assert False
    except ValueError:
        assert True

def test_item_name_valid():
    """Test if item name is added to item parameters correctly."""
    melon = Item("melon", 7)
    assert melon.name == "melon"

def test_item_price_negative():
    """Items should only have a positive price."""
    try:
        Item("melon", -10)
        assert False
    except ValueError:
        assert True

def test_item_price_positive():
    """Test if item price is added to item parameters."""
    melon = Item("melon", 7)
    ananass = Item("ananass", 2.4)
    assert melon.price == 7
    assert ananass.price == 2.4

def test_basket_add_one():
    """Test if basket storage works correctly when adding one item."""
    basket = Basket()
    basket.add(apelsin, 1)
    assert basket.storage == [apelsin]
    assert basket.storage[0].amount == 1
    assert basket.storage[0].name == "apelsin"
    assert basket.storage[0].price == 4

def test_basket_add_multiple():
    """Test if items are added correctly when basket already has items in storage."""
    basket = Basket()
    basket.add(apelsin, 1)
    basket.add(banaan, 2)
    assert basket.storage == [apelsin, banaan]
    assert basket.storage[1].amount == 2

def test_basket_add_invalid_item():
    """Only items of Item class can be added."""
    basket = Basket()
    mango = "mango"
    try:
        basket.add(mango, 3)
        assert False
    except ValueError:
        assert True

def test_basket_add_negative_amount():
    """Amount added to basket has to be a positive integer."""
    basket = Basket()
    try:
        basket.add(apelsin, -3)
        assert False
    except ValueError:
        assert True

def test_basket_add_float_amount():
    """Amount added to basket has to be a positive integer."""
    basket = Basket()
    try:
        basket.add(apelsin, 1.3)
        assert False
    except ValueError:
        assert True

def test_basket_add_zero():
    """Amount added to basket has to be a positive integer."""
    basket = Basket()
    try:
        basket.add(apelsin, 0)
        assert False
    except ValueError:
        assert True

def test_basket_increase_amount_of_existing_item():
    """Test if item amount in basket increases correctly."""
    basket = Basket()
    basket.add(apelsin, 1)
    basket.add(banaan, 2)
    basket.add(banaan, 4)
    assert basket.storage[1].amount == 6
    assert banaan.amount == 6

def test_basket_remove_one_empty():
    """Test if one item is removed from basket correctly when result is empty storage."""
    basket = Basket()
    basket.add(apelsin, 1)
    basket.remove(apelsin, 1)
    assert basket.storage == []

def test_basket_remove_items_after():
    """Test if one item is removed correctly when there are still items in basket afterwards."""
    basket = Basket()
    basket.add(apelsin, 1)
    basket.add(banaan, 1)
    basket.add(arbuus, 1)
    basket.remove(banaan, 1)
    assert basket.storage == [apelsin, arbuus]

def test_basket_remove_multiple_items():
    """Test if multiple items are removed correctly from basket."""
    basket = Basket()
    basket.add(apelsin, 1)
    basket.add(banaan, 1)
    basket.add(arbuus, 1)
    basket.remove(banaan, 1)
    basket.remove(apelsin, 1)
    assert basket.storage == [arbuus]

def test_basket_remove_reduce_amount():
    """Test if amount of item is reduced correctly."""
    basket = Basket()
    basket.add(apelsin, 1)
    basket.add(banaan, 5)
    basket.add(arbuus, 1)
    basket.remove(banaan, 2)
    assert basket.storage == [apelsin, banaan, arbuus]
    assert basket.storage[1].amount == 3
    assert banaan.amount == 3
    
def test_basket_remove_negative_amount():
    """Amount being removed has to be positive."""
    basket = Basket()
    basket.add(apelsin, 2)
    try:
        basket.remove(apelsin, -1)
        assert False
    except ValueError:
        assert True

def test_basket_remove_float_amount():
    """Amount being removed has to be an integer."""
    basket = Basket()
    basket.add(apelsin, 2)
    try:
        basket.remove(apelsin, 1.1)
        assert False
    except ValueError:
        assert True

def test_basket_remove_too_much():
    """More cannot be removed than what is in the basket."""
    basket = Basket()
    basket.add(apelsin, 1)
    try:
        basket.remove(apelsin, 2)
        assert False
    except ValueError:
        assert True

def test_basket_remove_item_not_in_basket():
    """Item cannot be removed if it is not in the basket."""
    basket = Basket()
    basket.add(apelsin, 1)
    try:
        basket.remove(banaan, 1)
        assert False
    except ValueError:
        assert True

def test_basket_remove_invalid_item():
    """Removable item has to be of Item class."""
    basket = Basket()
    basket.add(apelsin, 1)
    mango = "mango"
    try:
        basket.remove(mango, 1)
        assert False
    except ValueError:
        assert True

def test_client_invalid_type():
    """Client type can only be "gold" or "regular"."""
    try:
        client = Client(123, "silver", 1000)
        assert False
    except ValueError:
        assert True

def test_client_invalid_balance():
    """Client cannot have negative balance."""
    try:
        client = Client(123, "regular", -1000)
        assert False
    except ValueError:
        assert True

def test_client_valid():
    """Test if clients and their properties are created correctly."""
    client1 = Client(123, "regular", 1000)
    client2 = Client(223, "gold", 200.5)
    client3 = Client(323, "regular", 0)
    assert (client1.id, client2.id, client3.id) == (123, 223, 323)
    assert (client1.type, client2.type, client3.type) == ("regular", "gold", "regular")
    assert client1.balance == 1000
    assert client2.balance == 200.5
    assert client3.balance == 0
    assert client2.history == []
    assert client2.get_history() == []
    assert isinstance(client2.basket, Basket)

def test_store_add_clients():
    """Test if clients are added to the store correctly."""
    store = Store()
    client1 = Client(123, "regular", 1000)
    client2 = Client(223, "gold", 200.5)
    client3 = Client(323, "regular", 0)
    store.add_client(client1)
    store.add_client(client2)
    store.add_client(client3)
    assert store.get_clients() == [client1, client2, client3]

def test_store_add_invalid_client():
    """Client added to the store must be of Client class."""
    store = Store()
    client = "client"
    try:
        store.add_client(client)
        assert False
    except ValueError:
        assert True

def test_store_add_items():
    """Test if items are added to the store correctly."""
    store = Store()
    store.add_item(apelsin, 1)
    store.add_item(banaan, 2)
    assert store.get_storage() == {"apelsin": 1, "banaan": 2} 

def test_store_increase_item_amount():
    """Test if item amount in store increases correctly."""
    store = Store()
    store.add_item(apelsin, 1)
    store.add_item(banaan, 2)
    store.add_item(banaan, 3)
    store.add_item(apelsin, 1)
    assert store.get_storage() == {"apelsin": 2, "banaan": 5} 

def test_store_negative_item_amount():
    """Amount of item being added to store must be positive."""
    store = Store()
    try:
        store.add_item(apelsin, -1)
        assert False
    except ValueError:
        assert True

def test_store_zero_item_amount():
    """Amount of item being added to store must be positive."""
    store = Store()
    try:
        store.add_item(apelsin, 0)
        assert False
    except ValueError:
        assert True

def test_store_float_item_amount():
    """Amount of item being added to store must be an integer."""
    store = Store()
    try:
        store.add_item(apelsin, 1.0)
        assert False
    except ValueError:
        assert True

def test_store_invalid_item():
    """Item being added to store must be of Item class."""
    store = Store()
    mango = "mango"
    try:
        store.add_item(mango, 1)
        assert False
    except ValueError:
        assert True

def test_store_purchase_regular():
    """Test if purchase of a regular client is made correctly."""
    client = Client(123, "regular", 1000)
    store = Store()
    store.add_client(client)
    store.add_item(apelsin, 6)
    store.add_item(banaan, 7)
    client.basket.add(apelsin, 1)
    client.basket.add(banaan, 4)
    store.purchase(client, "01.06.2023")
    client.basket.add(apelsin, 3)
    store.purchase(client)
    assert store.get_storage() == {"apelsin": 2, "banaan": 3}
    assert store.get_clients() == [client]
    assert store.get_purchases() == [[123, "01.06.2023", "apelsin x1", "banaan x4"], [123, date.today().strftime("%d.%m.%Y"), "apelsin x3"]]
    assert client.basket.storage == []
    assert client.get_history() == [[date.today().strftime("%d.%m.%Y"), "apelsin x3"], ["01.06.2023", "apelsin x1", "banaan x4"]]
    assert client.balance == 972

def test_store_purchase_gold():
    """Test if gold client balance is reduced correctly."""
    client = Client(223, "gold", 1000)
    store = Store()
    store.add_client(client)
    store.add_item(apelsin, 5)
    store.add_item(banaan, 2)
    client.basket.add(apelsin, 3)
    client.basket.add(banaan, 2)
    store.purchase(client)
    assert store.get_storage() == {"apelsin": 2}
    assert client.balance == 983.8

def test_store_purchase_not_enough_balance():
    """Clients can't purchase if they don't have enough balance."""
    client = Client(123, "regular", 17)
    store = Store()
    store.add_client(client)
    store.add_item(apelsin, 5)
    store.add_item(banaan, 2)
    client.basket.add(apelsin, 3)
    client.basket.add(banaan, 2)
    try:
        store.purchase(client)
        assert False
    except ValueError:
        assert True

def test_store_purchase_wouldnt_have_enough_balance_if_wasnt_gold():
    """Client would not have enough balance otherwise but since they're a gold client they can buy."""
    client = Client(223, "gold", 17)
    store = Store()
    store.add_client(client)
    store.add_item(apelsin, 5)
    store.add_item(banaan, 2)
    client.basket.add(apelsin, 3)
    client.basket.add(banaan, 2)
    store.purchase(client)
    assert client.balance == 0.8

def test_store_purchase_unregistered_client():
    """Client has to be registered to store to be able to purchase."""
    client = Client(223, "gold", 17)
    store = Store()
    store.add_item(apelsin, 5)
    client.basket.add(apelsin, 3)
    try:
        store.purchase(client)
        assert False
    except ValueError:
        assert True

def test_store_purchase_not_enough_item():
    """Item cannot be purchased if there isn't enough in store."""
    client = Client(223, "gold", 17)
    store = Store()
    store.add_client(client)
    store.add_item(apelsin, 3)
    client.basket.add(apelsin, 5)
    try:
        store.purchase(client)
        assert False
    except ValueError:
        assert True

def test_store_purchase_item_missing():
    """Item cannot be purchased if it isn't in store."""
    client = Client(223, "gold", 17)
    store = Store()
    store.add_client(client)
    store.add_item(apelsin, 3)
    client.basket.add(apelsin, 5)
    client.basket.add(banaan, 2)
    try:
        store.purchase(client)
        assert False
    except ValueError:
        assert True


if __name__ == "__main__":
    test_item_name_is_not_valid()
    test_item_name_valid()
    test_item_price_negative()
    test_item_price_positive()
    test_basket_add_one()
    test_basket_add_multiple()
    test_basket_add_invalid_item()
    test_basket_add_negative_amount()
    test_basket_add_float_amount()
    test_basket_add_zero()
    test_basket_increase_amount_of_existing_item()
    test_basket_remove_one_empty()
    test_basket_remove_items_after()
    test_basket_remove_multiple_items()
    test_basket_remove_reduce_amount()
    test_basket_remove_negative_amount()
    test_basket_remove_float_amount()
    test_basket_remove_too_much()
    test_basket_remove_item_not_in_basket()
    test_basket_remove_invalid_item()
    test_client_invalid_type()
    test_client_invalid_balance()
    test_client_valid()
    test_store_add_clients()
    test_store_add_invalid_client()
    test_store_add_items()
    test_store_increase_item_amount()
    test_store_negative_item_amount()
    test_store_zero_item_amount()
    test_store_float_item_amount()
    test_store_invalid_item()
    test_store_purchase_regular()
    test_store_purchase_gold()
    test_store_purchase_not_enough_balance()
    test_store_purchase_wouldnt_have_enough_balance_if_wasnt_gold()
    test_store_purchase_unregistered_client()
    test_store_purchase_not_enough_item()
    test_store_purchase_item_missing()