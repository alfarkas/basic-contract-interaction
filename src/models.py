class Product:
    def __init__(self, name, status, owner, new_owner):
        self.name = name
        self.status = status
        self.owner = owner
        self.new_owner = new_owner
        
class WatchList:
    _subscribers = []

    def get_subscribers(self):
        return self._subscribers.copy()

    def subscribe(self, address):
        """Add an address to the subscriber list

        :param address: wallet address to add
        :type address: str
        """
        self._subscribers.append(address)

    def unsubscribe(self, address):
        """Removes an address to the subscriber list.

        :param address: wallet address to remove from the subscribers
        :type address: str
        """
        self._subscribers.remove(address)

    def is_subscribed(self, address):
        """Returns a boolean indicating if the given address is in the subscription list or not.

        :param address: address to check
        :type address: str
        """
        return address in self._subscribers