class ChocAnClient:
    """Simple base class for ChocAn Clients."""
    def __init__(self, name, number, street, city, state, zip, email, standing):
        """Stores information."""
        self.name     = name
        self.number   = number
        self.street   = street
        self.city     = city
        self.state    = state
        self.zip      = zip
        self.email    = email
        self.standing = standing

        # For Member:   Services recieved
        # For Provider: Services provided
        self.services = []

    def getTotal(self):
        """Gets the total fee."""
        total = 0
        for service in self.services:
            total += service.fee
        return total

class ChocAnMember(ChocAnClient):
    pass
    # def __init__(self, name, number, street, city, state, zip, email):
    #    super().__init__(name, number, street, city, state, zip, email)
    
class ChocAnProvider(ChocAnClient):
    pass
    # def __init__(self, name, number, street, city, state, zip, email):
    #    super().__init__(name, None, street, city, state, zip, email)



